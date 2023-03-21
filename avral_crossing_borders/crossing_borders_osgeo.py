import sys
import json
import os
from .crossing_borders import unzip
from osgeo import ogr, osr, gdal


def crossing_borders_osgeo(fields_path, objects_path):
    path_to_borders, temp_borders = unzip(fields_path)
    path_to_objects, temp_objects = unzip(objects_path)
    field_files = os.listdir(path_to_borders)
    object_files = os.listdir(path_to_objects)
    geoms = []
    answer = [[""]]
    driver = ogr.GetDriverByName("ESRI Shapefile")
    geom_mass = []

    for object_file in object_files:
        if '.shp' != object_file[-4:]:
            continue
        shapefile = os.path.join(os.getcwd(), path_to_objects, object_file)
        dataSource = driver.Open(shapefile, 0)
        layer = dataSource.GetLayer()
        if layer is None:
            sys.exit(1)
        for feature in layer:
            flag = False
            geom_ref = feature.GetGeometryRef()
            geom = ogr.CreateGeometryFromWkt(str(geom_ref))
            geom_name = geom.GetGeometryName()
            for mass_geom in geoms:
                if mass_geom[0] == geom_name:
                    mass_geom.append(geom)
                    flag = True
            if not flag:
                geoms.append([f'{geom_name}', geom])
                answer[0].append(f'{geom_name}')
    answer[0].append('Total')

    percent = 0
    gdal.UseExceptions()
    for field_file in field_files:
        try:
            borderfile = os.path.join(path_to_borders, field_file)
            f = open(borderfile, 'r')
            data_fields = json.dumps(json.load(f)['features'][0]['geometry'])
            border_polygon = ogr.CreateGeometryFromJson(data_fields)
            f.close()
            new_row = [0 for _ in range(len(geoms) + 1)]
            new_row[0] = field_file.split(".")[0]
            for type_geom in range(0, len(geoms)):
                for geom in geoms[type_geom][1:]:
                    if border_polygon.Intersect(geom):
                        new_row[type_geom + 1] += 1
                        geoms[type_geom].remove(geom)
            new_row.append(max(sum(new_row[1:]), -1))
        except Exception:
            # If the file is not read, the value is -1
            new_row = [-1 for _ in range(len(geoms) + 2)]
            new_row[0] = field_file.split(".")[0]
        answer.append(new_row)
        percent += 1
        print(f"Counting is completed by {round((percent / len(field_files) * 100), 2)}%", end='\r')
    if temp_borders:
        temp_borders.cleanup()
    if temp_objects:
        temp_objects.cleanup()
    return answer
    


if __name__ == "__main__":
    meh = crossing_borders_osgeo(r'/opt/avral_crossing_borders/points_for_scripts.zip',
                                 r'/opt/avral_crossing_borders/oopt.zip')
