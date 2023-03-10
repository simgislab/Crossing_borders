# -*- coding: utf-8 -*-
import os

from avral.operation import AvralOperation
from avral.io.types import StringType, FileType

from .crossing_borders import crossing_borders, write_to_csv



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
        self.borders_path = '/opt/avral_crossing_borders/borders'
        self.answer_path = '/opt/avral_crossing_borders/answer/answer.csv'

    def main(self):
        objects_path = self.getInput(u"objects_path").strip()

        data = crossing_borders(self.borders_path, objects_path)
        write_to_csv(data, self.answer_path)
        self.setOutput(u'csv', self.answer_path)

    def zip_to_directory(self, )


    def _do_work(self):
        self.logger.info(".START processing in cwd: %s" % os.getcwd())
        self.main()
        self.logger.info(".END processing in cwd: %s" % os.getcwd())
