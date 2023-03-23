#!/usr/bin/env python
import argparse

from .utils import write_to_csv
from .crossing_borders_shapely import crossing_borders


def get_options():
    parser = argparse.ArgumentParser(description='My script')
    parser.add_argument('-b', '--bor_dir', type=str, help='Path to borders')
    parser.add_argument('-i', '--obj_dir', type=str, help='Path to objects')
    parser.add_argument('-o', '--path_to_csv', type=str, help='Path to output csv file')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    opt = get_options()
    data = crossing_borders(opt.bor_dir, opt.obj_dir)
    write_to_csv(data, opt.path_to_csv)
    print("Complete")
