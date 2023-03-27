import os
import csv
import zipfile
import tempfile


def write_to_csv(mass_data, path_to_csv):
    if os.path.isfile(path_to_csv):
        os.remove(path_to_csv)
    create_file = open(path_to_csv, "w")
    file_writer = csv.writer(create_file, delimiter=",", lineterminator="\r")
    for row in mass_data:
        file_writer.writerow(row)
    create_file.close()


def unzip(path):
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path, 'r') as myzip:
            name = '\\'.join(path.split('\\')[0:-1])
            temp_dir = tempfile.TemporaryDirectory(dir=name)
            myzip.extractall(temp_dir.name)
        return temp_dir.name, temp_dir
    return path, None


def temp_files(func):
    def inner(fields_path, objects_path, logger):
        path_to_borders, temp_borders = unzip(fields_path)
        path_to_objects, temp_objects = unzip(objects_path)
        path_to_borders = os.path.join(path_to_borders, os.path.basename(fields_path).split('.')[0])
        path_to_objects = os.path.join(path_to_objects, os.path.basename(objects_path).split('.')[0])
        result = func(path_to_borders, path_to_objects, logger)
        if temp_borders:
            temp_borders.cleanup()
        if temp_objects:
            temp_objects.cleanup()
        return result
    return inner