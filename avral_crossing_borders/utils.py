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
