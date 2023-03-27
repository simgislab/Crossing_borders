# -*- coding: utf-8 -*-
import os

from avral.operation import AvralOperation
from avral.io.types import FileType

from .utils import write_to_csv
from .crossing_borders_osgeo import crossing_borders


class CrossingBorders(AvralOperation):
    def __init__(self):
        super(CrossingBorders, self).__init__(
            name="CrossingBorders",
            inputs={
                u"borders": FileType(),
                u"objects": FileType(),
            },
            outputs={
                u'output': FileType(),
            },
        )
        self.answer_filename = 'answer.csv'

    def main(self):
        borders_path = self.getInput(u"borders").strip()
        objects_path = self.getInput(u"objects").strip()
        data = crossing_borders(borders_path, objects_path, logger=self.logger)

        answer_path = os.path.join(os.getcwd(), self.answer_filename)

        write_to_csv(data, answer_path)
        self.setOutput(u'output', answer_path)

    def _do_work(self):
        self.logger.info(".START processing in cwd: %s" % os.getcwd())
        self.main()
        self.logger.info(".END processing in cwd: %s" % os.getcwd())
