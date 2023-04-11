import os
import sys
import json
from osgeo import ogr, gdal

from avral_crossing_borders.utils import temp_files


def read_border(path):
    exp = path.split('.')[-1]
    mass = []
    if exp == 'geojson':
        f = open(path, 'r')
        data_fields = json.dumps(json.load(f)['features'][0]['geometry'])
        border_polygon = ogr.CreateGeometryFromJson(data_fields)
        f.close()
        mass.append(border_polygon)
    
    return mass


def read_objects(path):
    exp = path.split('.')[-1]
    mass = []
    if exp == 'geojson':
        f = open(path, 'r')
        data_fields = json.dumps(json.load(f)['features'][0]['geometry'])
        border_polygon = ogr.CreateGeometryFromJson(data_fields)
        f.close()
        mass.append(border_polygon)
    
    return mass


@temp_files
def crossing_borders(fields_path, objects_path, logger):
    field_files = sorted(os.listdir(fields_path))
    object_files = sorted(os.listdir(objects_path))
    geoms = []
    answer = [["Region"]]
    driver = ogr.GetDriverByName("ESRI Shapefile")
    

    logger.info('Geometry processing started')
    for object_file in object_files:
        if '.shp' == object_file[-4:]:
            shapefile = os.path.join(os.getcwd(), objects_path, object_file)
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
        if object_file.split('.')[-1] == 'gpkg':
            driver_gpkg = ogr.GetDriverByName("GPKG")
            dataSource = ogr.Open(os.path.join(objects_path, object_file))
            ogrData = ogr.Open(os.path.join(objects_path, object_file))
            num = ogrData.GetLayerCount()
            for count in range(num):
                layer = ogrData.GetLayer(count)
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
    logger.info('Geometry processing is finished')

    percent = 0
    gdal.UseExceptions()
    logger.info("Counting of intersections has started")
    for field_file in field_files:
        try:
            borderfile = os.path.join(fields_path, field_file)
            border_polygons = read_border(borderfile)
            new_row = [0 for _ in range(len(geoms) + 1)]
            new_row[0] = field_file.split(".")[0]
            for border_polygon in border_polygons:
                for type_geom in range(0, len(geoms)):
                    for geom in geoms[type_geom][1:]:
                        if border_polygon.Intersect(geom):
                            new_row[type_geom + 1] += 1
                new_row.append(max(sum(new_row[1:]), -1))
        except Exception as e:
            print('-----------------------------------------')
            print(e)
            print('-----------------------------------------')
            # If the file is not read, the value is -1
            new_row = [-1 for _ in range(len(geoms) + 2)]
            new_row[0] = field_file.split(".")[0]
        answer.append(new_row)
        percent += 1
        print(f"Counting is completed by {('{0:.2f}'.format(percent / len(field_files) * 100))}%", end='\r')
        
    logger.info("Counting of intersections is finished")
    return answer


# TODO: move to tests
if __name__ == "__main__":
    meh = crossing_borders(r'/opt/avral_crossing_borders/points_for_scripts.zip',
                                 r'/opt/avral_crossing_borders/oopt.zip')
