import argparse
import os

from shapely import from_geojson, intersects
from shapely.geometry import shape
import json
import fiona
import csv
import zipfile
import shutil


def get_options():
    parser = argparse.ArgumentParser(description='My script')
    parser.add_argument('bor_dir', type=str, help='Path to borders')
    parser.add_argument('obj_dir', type=str, help='Path to objects')
    parser.add_argument('path_to_csv', type=str, help='Path to output csv file')
    args = parser.parse_args()
    return args


def write_to_csv(mass_data, path_to_csv):
    create_file = open(path_to_csv, 'w')
    file_writer = csv.writer(create_file, delimiter=",", lineterminator="\r")
    for row in mass_data:
        file_writer.writerow(row)
    create_file.close()


def unzip(path):
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path, 'r') as myzip:
            name = path.split('.')[0]
            os.mkdir(name)
            myzip.extractall(f'{name}')
        new_path = name
        print(new_path)
        return new_path
    return path


def crossing_borders(fields_path, objects_path):
    new_fields_path = unzip(fields_path)
    new_objects_path = unzip(objects_path)
    field_files = os.listdir(new_fields_path)
    object_files = os.listdir(new_objects_path)
    geoms = []
    answer = [[""]]
    for object_file in object_files:
        if '.shp' != object_file[-4:]:
            continue
        path_object = os.path.join(os.getcwd(), new_objects_path, object_file)
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

    for field_file in field_files:
        try:
            path = os.path.join(new_fields_path, field_file)
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
    if zipfile.is_zipfile(fields_path):
        shutil.rmtree(new_fields_path)
    if zipfile.is_zipfile(objects_path):
        shutil.rmtree(new_objects_path)
    return answer


if __name__ == "__main__":
    opt = get_options()
    data = crossing_borders(opt.bor_dir, opt.obj_dir)
    write_to_csv(data, opt.path_to_csv)
    print("Complete")
