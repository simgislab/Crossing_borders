# -*- coding: utf-8 -*-
import os

from avral.operation import AvralOperation
from avral.io.types import StringType, FileType
import datetime

from .crossing_borders import crossing_borders, write_to_csv
from .crossing_borders_osgeo import crossing_borders_osgeo


class CrossingBorders(AvralOperation):
    def __init__(self):
        super(CrossingBorders, self).__init__(
            name="CrossingBorders",
            inputs={
                u"objects_path": StringType(),
            },
            outputs={
                u'csv': FileType(),
            },
        )
        self.borders_path = '/opt/avral_crossing_borders/points_for_scripts.zip'
        self.answer_path = '/opt/avral_crossing_borders/answer/answer.csv'
        self.answer_osgeo_path = '/opt/avral_crossing_borders/answer/answer_osgeo.csv'

    def main(self):
        objects_path = self.getInput(u"objects_path").strip()
        func_start = datetime.datetime.now()
        print("First function started")
        data_1 = crossing_borders(self.borders_path, objects_path)
        func_end = datetime.datetime.now()
        print(f"The function was performed for {(func_end - func_start).total_seconds()} seconds")
        func_start = datetime.datetime.now()
        print("Second function started")
        data_2 = crossing_borders_osgeo(self.borders_path, objects_path)
        func_end = datetime.datetime.now()
        print(f"The function was performed for {(func_end - func_start).total_seconds()} seconds")
        write_to_csv(data_1, self.answer_path)
        write_to_csv(data_2, self.answer_osgeo_path)
        self.setOutput(u'csv', self.answer_path)

    def _do_work(self):
        self.logger.info(".START processing in cwd: %s" % os.getcwd())
        self.main()
        self.logger.info(".END processing in cwd: %s" % os.getcwd())
