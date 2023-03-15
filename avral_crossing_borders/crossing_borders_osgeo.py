import os
from crossing_borders import unzip
from osgeo import ogr, osr, gdal


def crossing_borders_osgeo(fields_path, objects_path):
    path_to_borders, temp_borders = unzip(fields_path)
    path_to_objects, temp_objects = unzip(objects_path)
    field_files = os.listdir(path_to_borders)
    object_files = os.listdir(path_to_objects)
    geoms = []
    answer = [[""]]
    driver = ogr.GetDriverByName("ESRI Shapefile")
    for object_file in object_files:
        if '.shp' != object_file[-4:]:
            continue
        shapefile = os.path.join(os.getcwd(), path_to_objects, object_file)
        dataSource = driver.Open(shapefile, 0)
        layer = dataSource.GetLayer()
        mass = []
        for feature in layer:
            geom = feature.GetGeometryRef()
            mass.append(geom)
    if mass:
        print('-------------------------------------')
        print(type(mass[0]))
        print('-------------------------------------')
        print('-------------------------------------')
        print(dir(mass[0]))
        print('-------------------------------------')
        print('-------------------------------------')
        print(mass[0].GetGeometryType())
        print('-------------------------------------')
        print('-------------------------------------')
        print(len(mass))
        print('-------------------------------------')
    return layer
    

if __name__ == "__main__":
    meh = crossing_borders_osgeo(r'/opt/avral_crossing_borders/points_for_scripts.zip',
     r'/opt/avral_crossing_borders/oopt.zip')