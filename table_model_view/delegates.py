#!/usr/bin/env python3
#
#   delegates.py
#   Holds delegates to use in place of raw table data to display in table view
#   Using Python 3.6 and PySide2 v.5.12
#
#   Copyright (C) 2019 Robert Parker
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see <https://www.gnu.org/licenses/>.


from PySide2.QtWidgets import QStyledItemDelegate
from PySide2.QtCore import QRect


class FillColorDelegate(QStyledItemDelegate):
    def __init__(self, model, color):
        """
        This delegate replaces a cell's display with a solid fill color surrounded by a thin white border

        :param model: underlying ProxyModel object
        :param color: QColor object
        """

        super().__init__()
        self.color = color
        self.model = model

    def createEditor(self, parent, option, index):
        return None

    def paint(self, painter, option, index):
        source_index = self.model.mapToSource(index)
        row = source_index.row()
        column = source_index.column()
        value = self.model.sourceModel().dataset[row][column]

        rect = QRect(option.rect.x()+1, option.rect.y()+1, option.rect.width()-2, option.rect.height()-2)

        if value:
            painter.save()
            painter.setBrush(self.color)
            painter.fillRect(rect, painter.brush())
