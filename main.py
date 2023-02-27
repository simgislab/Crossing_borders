import argparse
import os
from shapely import from_geojson, intersects
from shapely.geometry import shape
import json
import fiona
import csv


def get_options():
    parser = argparse.ArgumentParser(description='My script')
    parser.add_argument('bor_dir', type=str, help='Path to borders')
    parser.add_argument('obj_dir', type=str, help='Path to objects')
    args = parser.parse_args()
    return args


def write_to_csv(mass_data):
    create_file = open('crossing_borders.csv', 'w')
    file_writer = csv.writer(create_file, delimiter=",", lineterminator="\r")
    for row in mass_data:
        file_writer.writerow([row[0], row[1], row[2], row[3]])
    create_file.close()


def crossing_borders(fields_path, objects_path):
    count = 0
    field_files = os.listdir(fields_path)
    object_files = os.listdir(objects_path)
    flag = True
    points = []
    polygons = []
    answer = [["", 'points', 'polygons', 'total']]
    for object_file in object_files:
        if '.shp' != object_file[-4:]:
            continue
        with fiona.open(os.path.join(objects_path, object_file)) as shapefile:
            for record in shapefile:
                shaped = shape(record['geometry'])
                if shaped.geom_type == 'Point':
                    points.append(shaped)
                elif shaped.geom_type == "Polygon" or shaped.geom_type == 'MultiPolygon':
                    polygons.append(shaped)

    for field_file in field_files:
        try:
            path = os.path.join(fields_path, field_file)
            f = open(path, 'r')
            data_fields = json.load(f)
            border_polygon = from_geojson(json.dumps(data_fields))
            f.close()
            count_points = 0
            count_polygons = 0
            for point in points:
                if intersects(border_polygon, point):
                    count_points += 1
            for polygon in polygons:
                if intersects(border_polygon, polygon):
                    count_polygons += 1
        except Exception:
            count_points = -1
            count_polygons = -1

        answer.append([field_file.split(".")[0], count_points, count_polygons, max(count_points + count_polygons, -1)])
    return answer


if __name__ == "__main__":
    args = get_options()
    data = crossing_borders(args.bor_dir, args.obj_dir)
    write_to_csv(data)
    print("Complete")
