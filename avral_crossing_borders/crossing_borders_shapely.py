import os
import json
import fiona
from shapely import from_geojson, intersects
from shapely.geometry import shape

from .utils import temp_files


@temp_files
def crossing_borders(fields_path, objects_path, logger):
    field_files = os.listdir(fields_path)
    object_files = os.listdir(objects_path)
    geoms = []
    answer = [[""]]

    logger.info('Geometry processing started')
    for object_file in object_files:
        if '.shp' != object_file[-4:]:
            continue
        path_object = os.path.join(os.getcwd(), objects_path, object_file)
        with fiona.open(path_object) as shapefile:
            for record in shapefile:
                shaped = shape(record['geometry'])
                flag = False
                for geom in geoms:
                    if geom[0] == shaped.geom_type:
                        geom.append(shaped)
                        flag = True
                if not flag:
                    geoms.append([f'{shaped.geom_type}', shaped])
                    answer[0].append(f'{shaped.geom_type}')
    answer[0].append('Total')
    logger.info('Geometry processing is finished')

    percent = 0
    logger.info("Counting of intersections has started")
    for field_file in field_files:
        try:
            path = os.path.join(fields_path, field_file)
            f = open(path, 'r')
            data_fields = json.load(f)
            border_polygon = from_geojson(json.dumps(data_fields))
            f.close()
            new_row = [0 for _ in range(len(geoms) + 1)]
            new_row[0] = field_file.split(".")[0]
            for type_geom in range(0, len(geoms)):
                for geom in geoms[type_geom][1:]:
                    if intersects(border_polygon, geom):
                        new_row[type_geom + 1] += 1
            new_row.append(max(sum(new_row[1:]), -1))
        except Exception:
            # If the file is not read, the value is -1
            new_row = [-1 for _ in range(len(geoms) + 2)]
            new_row[0] = field_file.split(".")[0]
        answer.append(new_row)
        percent += 1
        print(f"Counting is completed by {('{0:.2f}'.format(percent / len(field_files) * 100))}%", end='\r')
    logger.info("Counting of intersections is finished")
    return answer

