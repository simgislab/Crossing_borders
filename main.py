import argparse
import os
from shapely import from_geojson, contains, disjoint
from shapely.geometry import shape
import json
import fiona


def main():
    parser = argparse.ArgumentParser(description='My script')
    parser.add_argument('bor_dir', type=str, help='Path to borders')
    parser.add_argument('obj_dir', type=str, help='Path to objects')
    args = parser.parse_args()

    fields_path = args.bor_dir
    objects_path = args.obj_dir

    count = 0
    field_files = os.listdir(fields_path)
    object_files = os.listdir(objects_path)
    flag = True

    for field_file in field_files:
        try:
            f = open("".join([fields_path, r"\\", field_file]))
            data_fields = json.load(f)
            form1 = from_geojson(json.dumps(data_fields))
            f.close()
            for object_file in object_files:
                if '.shp' != object_file[-4:]:
                    continue
                with fiona.open("".join([objects_path + r"\\", object_file])) as shapefile:
                    # Iterate over the records
                    for record in shapefile:
                        # Get the geometry from the record
                        geometry = shape(record['geometry'])
                        if not disjoint(form1, geometry) and not contains(form1, geometry):
                            count += 1
        except:
            if flag:
                print("Unread files")
                flag = False
            print(field_file)

    if not flag:
        print('---------------------------------------------------------------')
    print("Number of border crossings: ", count)


if __name__ == "__main__":
    main()
