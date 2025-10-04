#
# Copyright (c) 2019-2025
# Pertti Palo, Scott Moisik, Matthew Faytak, and Motoki Saito.
#
# This file is part of the Phonetic Analysis ToolKIT
# (see https://github.com/giuthas/patkit/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# The example data packaged with this program is licensed under the
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0
# International (CC BY-NC-SA 4.0) License. You should have received a
# copy of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0
# International (CC BY-NC-SA 4.0) License along with the data. If not,
# see <https://creativecommons.org/licenses/by-nc-sa/4.0/> for details.
#
# When using the toolkit for scientific publications, please cite the
# articles listed in README.md. They can also be found in
# citations.bib in BibTeX format.
#
"""Dialog for asking if we should overwrite an existing file or files."""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QDialogButtonBox)
from PyQt6.QtCore import Qt

from patkit.data_structures import Answer


class OpenAnswerDialog(QDialog):

    def __init__(
        self,
        name: str,
        answers: list[Answer] | None,
        icon: QIcon | None = None,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)

        self.chosen_answer_name = None
        if name == "":
            self.name = "Please select the answer you want to open."
        else:
            self.name = name

        # The checklist
        self.list_view = QListView()
        self.list_view.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.model = QStandardItemModel()
        for answer in answers:
            item = QStandardItem(answer.name)
            # TODO NEXT: this needs to be a radiobutton or single selection not
            # checkable.
            item.setCheckable(True)
            check = (QtCore.Qt.CheckState.Checked
                     if checked else QtCore.Qt.CheckState.Unchecked)
            item.setCheckState(check)
            self.model.appendRow(item)
        self.list_view.setModel(self.model)

        # TODO: this doesn't quite work, but rather sets the width too large
        self.list_view.setMinimumWidth(
            self.list_view.contentsRect().width())

        # The cancel, ok buttons
        dialog_buttons = (
            QDialogButtonBox.StandardButton.Open |
            QDialogButtonBox.StandardButton.Cancel
        )
        self.open_cancel_buttons = QDialogButtonBox(dialog_buttons)
        self.open_cancel_buttons.accepted.connect(self._handle_open)
        self.open_cancel_buttons.button(
            QDialogButtonBox.StandardButton.Open).clicked.connect(
            self._handle_open)
        self.ok_cancel_buttons.rejected.connect(self._handle_cancel)

        # Assemble the window contents
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.list_view)
        vbox.addStretch(1)
        vbox.addWidget(self.ok_cancel_buttons)

        self.answer = None

        self.setWindowTitle(self.name)
        if icon:
            self.setWindowIcon(icon)

        self.adjustSize()

    def _handle_open(self):
        self.answer = 'open'

    def _handle_cancel(self):
        self.answer = None


    @staticmethod
    def confirm_overwrite(
        answers: list[str] | None,
        parent=None
    ) -> str | None:
        dialog = OpenAnswerDialog(answers, parent)
        dialog.exec()
        pressed_button = dialog.pressed_button
        return pressed_button

    @staticmethod
    def get_selection(
            name: str,
            answers: list[Answer] | None,
            icon: QIcon | None = None,
            parent: QWidget | None = None,
    ) -> tuple[bool | None, str | None]:
        dialog = OpenAnswerDialog(
            name=name,
            answers=answers,
            icon=icon,
            parent=parent,
        )
        if dialog.exec() == QDialog.DialogCode.Rejected:
            return None, None
        return dialog.create_new, dialog.chosen_answer_name
