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


def unzip(dir_path):
    if zipfile.is_zipfile(dir_path):
        with zipfile.ZipFile(dir_path, 'r') as myzip:
            name = os.path.join(os.path.dirname(dir_path), '')
            temp_dir = tempfile.TemporaryDirectory(dir=name)
            myzip.extractall(temp_dir.name)
            if os.listdir(temp_dir.name) and os.path.isdir(os.path.join(temp_dir.name, os.listdir(temp_dir.name)[0])):
                first_file = os.path.join(temp_dir.name, os.listdir(temp_dir.name)[0])
                while os.listdir(first_file) and os.path.isfile(first_file):
                    first_file = os.path.join(first_file, os.listdir(first_file)[0])
                return first_file, temp_dir
        return temp_dir.name, temp_dir
    return dir_path, None


def temp_files(func):
    def inner(fields_path, objects_path, logger):
        path_to_borders, temp_borders = unzip(fields_path)
        path_to_objects, temp_objects = unzip(objects_path)
        result = func(path_to_borders, path_to_objects, logger)
        if temp_borders:
            temp_borders.cleanup()
        if temp_objects:
            temp_objects.cleanup()
        return result

    return inner
