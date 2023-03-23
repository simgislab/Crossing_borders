# -*- coding: utf-8 -*-
import os

from avral.operation import AvralOperation
from avral.io.types import StringType, FileType

from .utils import write_to_csv
from .crossing_borders_osgeo import crossing_borders


class CrossingBorders(AvralOperation):
    def __init__(self):
        super(CrossingBorders, self).__init__(
            name="CrossingBorders",
            inputs={
                u"borders_path": StringType(),
                u"objects_path": StringType(),
            },
            outputs={
                u'csv': FileType(),
            },
        )
        self.answer_path = '/opt/avral_crossing_borders/answer.csv'

    def main(self):
        borders_path = self.getInput(u"borders_path").strip()
        objects_path = self.getInput(u"objects_path").strip()
        data = crossing_borders(borders_path, objects_path)
        write_to_csv(data, self.answer_path)
        self.setOutput(u'csv', self.answer_path)

    def _do_work(self):
        self.logger.info(".START processing in cwd: %s" % os.getcwd())
        self.main()
        self.logger.info(".END processing in cwd: %s" % os.getcwd())
