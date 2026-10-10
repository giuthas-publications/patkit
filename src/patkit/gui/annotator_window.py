#
# Copyright (c) 2019-2026
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
"""
This is the main window of the PATKIT annotator.
"""

from typing import Any

from PyQt6 import QtCore, QtGui, QtWidgets

from patkit.constants import AnnotatorMode, ExerciseMode
from patkit.data_structures import Session

from .player_controls import PlayerControls


class UiMainWindow(object):
    """
    User interface definition for the PATKIT Annotator main window.

    This class constructs and configures the layout, widgets, menu items,
    and localization properties for the main application interface.
    """

    # Menu declarations, actions, and texts
    #
    # TODO 0.24: Move this to a separate file and translate it to yaml, after
    # reading in from a package resource, validate with pydantic. Eventually
    # grow this into the save format for editable shortcuts. The edited version
    # should live in .patkit in the user's home dir and any parts of it present
    # should precede the resource file.
    MENU_SPECS: tuple[dict[str, Any], ...] = (
        {
            "attr": "menu_file",
            "title": "File",
            "items": [
                {
                    "attr": "action_open",
                    "text": "Open...",
                    "shortcut": "Ctrl+Shift+O",
                },
                {
                    "attr": "action_save_current_textgrid",
                    "text": "Save current TextGrid",
                },
                {
                    "attr": "action_save_all_textgrids",
                    "text": "Save all TextGrids",
                },
                {
                    "attr": "action_save_all",
                    "text": "Save all",
                    "shortcut": "Ctrl+Shift+S",
                },
                None,  # Separator
                {
                    "attr": "action_quit",
                    "text": "Quit",
                    "shortcut": "Ctrl+Q",
                },
            ],
            "standalone_actions": [
                {"attr": "actionNew", "text": "New"},
                {"attr": "actionSave_as", "text": "Save as"},
            ],
        },
        {
            "attr": "menu_edit",
            "title": "Edit",
            "enabled": False,
            "items": [
                {
                    "attr": "action_undo",
                    "text": "Undo",
                    "shortcut": "Ctrl+Z",
                },
                {
                    "attr": "action_redo",
                    "text": "Redo",
                    "shortcut": "Ctrl+Shift+Z",
                },
            ],
        },
        {
            "attr": "menu_exercise",
            "title": "Exercise",
            "items": [
                {
                    "attr": "action_new_exercise",
                    "text": "New exercise...",
                    "shortcut": "Ctrl+Shift+N",
                },
                {"attr": "action_save_exercise", "text": "Save exercise"},
                {
                    "attr": "action_package_exercise",
                    "text": "Package exercise...",
                },
                {
                    "attr": "action_unpackage_exercise",
                    "text": "Unpackage exercise...",
                },
                None,  # Separator
                {
                    "attr": "action_new_answer",
                    "text": "New answer...",
                    "shortcut": "Ctrl+N",
                },
                {
                    "attr": "action_save_answer",
                    "text": "Save answer",
                    "shortcut": "Ctrl+S",
                },
                {
                    "attr": "action_open_answer",
                    "text": "Open answer...",
                    "shortcut": "Ctrl+O",
                },
                None,  # Separator
                {
                    "attr": "action_compare_to_example",
                    "text": "Compare to example",
                    "enabled": False,  # TODO 0.24: Implement this?
                },
                {
                    "attr": "action_show_example",
                    "text": "Show example",
                    "shortcut": "Alt+E",
                    "checkable": True,
                    "checked": False,
                },
            ],
        },
        {
            "attr": "menu_export",
            "title": "Export",
            "items": [
                {
                    "attr": "action_export_aggregate_images",
                    "text": "Export aggregate images...",
                },
                {
                    "attr": "action_export_annotations_and_metadata",
                    "text": "Export annotations and metadata...",
                },
                {
                    "attr": "action_export_distance_matrices",
                    "text": "Export distance matrices...",
                },
                {
                    "attr": "action_export_main_figure",
                    "text": "Export main figure...",
                    "shortcut": "Ctrl+E",
                },
                {
                    "attr": "action_export_ultrasound_frame",
                    "text": "Export ultrasound figure...",
                },
            ],
            "standalone_actions": [
                {
                    "attr": "action_export_analysis",
                    "text": "Export analysis...",
                    "enabled": False,
                },
            ],
        },
        {
            "attr": "menu_image",
            "title": "Image",
            "submenus": [
                {
                    "attr": "menu_select_image",
                    "title": "Select image",
                    "items": [
                        {
                            "attr": "action_mean_image",
                            "text": "Mean image",
                            "checkable": True,
                            "checked": False,
                        },
                        {
                            "attr": "action_frame",
                            "text": "Frame at cursor",
                            "checkable": True,
                            "checked": True,
                        },
                        {
                            "attr": "action_raw_frame",
                            "text": "Raw frame at cursor",
                            "checkable": True,
                            "checked": False,
                        },
                    ],
                    "action_group": "menu_select_small_action_group",
                },
            ],
        },
        {
            "attr": "menu_kymography",
            "title": "Kymography",
            "items": [
                {
                    "attr": "action_display_kymography_line",
                    "text": "Display kymography sampling line",
                    "checkable": True,
                    "checked": True,
                },
                {
                    "attr": "action_display_small_kymogram",
                    "text": "Display small kymogram",
                    "checkable": True,
                    "checked": True,
                },
                {
                    "attr": "action_display_main_kymogram",
                    "text": "Display main kymogram",
                    "enabled": False,
                },
            ],
        },
        {
            "attr": "menu_navigation",
            "title": "Navigation",
            "items": [
                {
                    "attr": "action_next",
                    "text": "Next Recording",
                    "shortcut": "Down",
                },
                {
                    "attr": "action_previous",
                    "text": "Previous Recording",
                    "shortcut": "Up",
                },
                None,  # Separator
                {
                    "attr": "action_next_frame",
                    "text": "Next Frame",
                    "shortcut": "Right",
                },
                {
                    "attr": "action_previous_frame",
                    "text": "Previous Frame",
                    "shortcut": "Left",
                },
            ],
        },
        {
            "attr": "menu_script",
            "title": "Script",
            "enabled": False,
            "standalone_actions": [
                {
                    "attr": "actionShow_interpreter",
                    "text": "Show interpreter",
                },
                {
                    "attr": "actionRun_file",
                    "text": "Run file..."
                },
            ],
        },
    )

    def setupUi(self, main_window: QtWidgets.QMainWindow) -> None:
        """
        Set up the user interface components for the main window.

        Parameters
        ----------
        main_window : QtWidgets.QMainWindow
            The parent QMainWindow instance to populate with UI widgets.
        """
        # Main elements and sizing
        main_window.setObjectName("MainWindow")
        # main_window.resize(1087, 795)
        main_window.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setObjectName("central_widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.central_widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mplwindow = QtWidgets.QWidget(self.central_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.mplwindow.sizePolicy().hasHeightForWidth()
        )
        self.mplwindow.setSizePolicy(sizePolicy)
        self.mplwindow.setObjectName("mplwindow")
        self.mplWindowVerticalLayout = QtWidgets.QVBoxLayout(self.mplwindow)
        self.mplWindowVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.mplWindowVerticalLayout.setObjectName("mplWindowVerticalLayout")

        # Side panel
        self.side_panel = QtWidgets.QFrame(self.central_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.side_panel.sizePolicy().hasHeightForWidth()
        )
        self.side_panel.setSizePolicy(sizePolicy)
        self.side_panel.setMinimumSize(QtCore.QSize(150, 0))
        # self.side_panel.setMaximumSize(QtCore.QSize(300, 16777215))
        self.side_panel.setObjectName("side_panel")
        self.side_panel_layout = QtWidgets.QVBoxLayout(self.side_panel)
        self.side_panel_layout.setContentsMargins(0, 0, 0, 0)
        self.side_panel_layout.setObjectName("side_panel_layout")

        # Vertical splitter for side panel (to resize/collapse ultrasound)
        self.side_panel_splitter = QtWidgets.QSplitter(
            QtCore.Qt.Orientation.Vertical
        )
        self.side_panel_layout.addWidget(self.side_panel_splitter)

        # Top container for side panel
        self.side_panel_top_widget = QtWidgets.QWidget()
        self.side_panel_top_layout = QtWidgets.QVBoxLayout(
            self.side_panel_top_widget
        )
        self.side_panel_top_layout.setContentsMargins(0, 0, 0, 0)
        self.side_panel_splitter.addWidget(self.side_panel_top_widget)

        # Mode selection
        self.mode_controls = QtWidgets.QGroupBox(self.side_panel_top_widget)
        self.mode_controls.setMaximumSize(QtCore.QSize(16777215, 80))
        self.mode_controls.setObjectName("mode_box")
        self.mode_layout = QtWidgets.QHBoxLayout(self.mode_controls)
        self.mode_layout.setContentsMargins(0, 0, 0, 0)
        self.mode_layout.setObjectName("mode_layout")

        self.mode_drop_down = QtWidgets.QComboBox(self.mode_controls)
        self.mode_drop_down.addItems(list(AnnotatorMode.values()))
        self.mode_layout.addWidget(self.mode_drop_down)
        self.exercise_drop_down = QtWidgets.QComboBox(self.mode_controls)
        self.exercise_drop_down.addItems(list(ExerciseMode.values()))
        self.mode_layout.addWidget(self.exercise_drop_down)
        self.side_panel_top_layout.addWidget(self.mode_controls)

        # Navigation buttons and widgets
        self.go_to_group = QtWidgets.QGroupBox(self.side_panel_top_widget)
        self.go_to_group.setMaximumSize(QtCore.QSize(16777215, 80))
        self.go_to_group.setObjectName("groupBox")
        self.go_to_layout = QtWidgets.QHBoxLayout(self.go_to_group)
        self.go_to_layout.setContentsMargins(0, 0, 0, 0)
        self.go_to_layout.setObjectName("go_to_layout")

        self.go_to_line_edit = QtWidgets.QLineEdit(self.go_to_group)
        self.go_to_line_edit.setMaximumSize(QtCore.QSize(80, 16777215))
        self.go_to_line_edit.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.go_to_line_edit.setObjectName("go_to_line_edit")
        self.go_to_layout.addWidget(self.go_to_line_edit)
        self.goButton = QtWidgets.QPushButton(self.go_to_group)
        self.goButton.setMaximumSize(QtCore.QSize(80, 16777215))
        self.goButton.setObjectName("goButton")
        self.go_to_layout.addWidget(self.goButton)

        self.previous_button = QtWidgets.QPushButton(self.go_to_group)
        self.previous_button.setMaximumSize(QtCore.QSize(80, 16777215))
        self.previous_button.setObjectName("previous_button")
        self.go_to_layout.addWidget(self.previous_button)
        self.next_button = QtWidgets.QPushButton(self.go_to_group)
        self.next_button.setMaximumSize(QtCore.QSize(80, 16777215))
        self.next_button.setObjectName("next_button")
        self.go_to_layout.addWidget(self.next_button)
        self.side_panel_top_layout.addWidget(self.go_to_group)

        # List view
        self.database_view = QtWidgets.QListView(self.side_panel_top_widget)
        self.database_model = QtGui.QStandardItemModel()
        self.database_view.setModel(self.database_model)
        self.database_view.setObjectName("databaseView")
        self.side_panel_top_layout.addWidget(self.database_view)
        self.database_view.clicked[QtCore.QModelIndex].connect(
            main_window.on_database_view_clicked
        )

        self.play_controls = PlayerControls(self.side_panel_top_widget)
        self.side_panel_top_layout.addWidget(self.play_controls)

        # Ultrasound frame display
        self.ultrasoundFrame = QtWidgets.QWidget(self.side_panel_top_widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.Preferred,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.ultrasoundFrame.sizePolicy().hasHeightForWidth()
        )
        self.ultrasoundFrame.setSizePolicy(sizePolicy)
        self.ultrasoundFrame.setMinimumSize(QtCore.QSize(150, 100))
        self.ultrasoundFrame.setObjectName("ultrasoundFrame")

        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.ultrasoundFrame)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")

        # Vertical splitter between kymogram_canvas and ultra_canvas
        self.kymogram_ultra_splitter = QtWidgets.QSplitter(
            QtCore.Qt.Orientation.Vertical
        )
        self.verticalLayout_6.addWidget(self.kymogram_ultra_splitter)
        self.side_panel_splitter.addWidget(self.ultrasoundFrame)

        # TODO 1.1: Consider bringing these back as a e.g. a mode option like
        # exercises. Or build a customisation example from them. They are
        # connected with a section in translation code further below and in
        # two places in qt_annotator.
        #
        # Annotation radio buttons
        # self.positionRB = QtWidgets.QGroupBox(self.side_panel)
        # self.positionRB.setObjectName("positionRB")
        # self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.positionRB)
        # self.verticalLayout_5.setObjectName("verticalLayout_5")
        # self.positionRB_1 = QtWidgets.QRadioButton(self.positionRB)
        # self.positionRB_1.setAutoFillBackground(False)
        # self.positionRB_1.setObjectName("positionRB_1")
        # self.tonguePositionRBs = QtWidgets.QButtonGroup(main_window)
        # self.tonguePositionRBs.setObjectName("tonguePositionRBs")
        # self.tonguePositionRBs.addButton(self.positionRB_1)
        # self.verticalLayout_5.addWidget(self.positionRB_1)
        # self.positionRB_2 = QtWidgets.QRadioButton(self.positionRB)
        # self.positionRB_2.setAutoFillBackground(False)
        # self.positionRB_2.setObjectName("positionRB_2")
        # self.tonguePositionRBs.addButton(self.positionRB_2)
        # self.verticalLayout_5.addWidget(self.positionRB_2)
        # self.positionRB_3 = QtWidgets.QRadioButton(self.positionRB)
        # self.positionRB_3.setAutoFillBackground(False)
        # self.positionRB_3.setObjectName("positionRB_3")
        # self.tonguePositionRBs.addButton(self.positionRB_3)
        # self.verticalLayout_5.addWidget(self.positionRB_3)
        # self.side_panel_layout.addWidget(self.positionRB)

        # Main horizontal splitter for resizable side panel vs plots
        self.main_splitter = QtWidgets.QSplitter(
            QtCore.Qt.Orientation.Horizontal
        )
        self.main_splitter.addWidget(self.side_panel)
        self.main_splitter.addWidget(self.mplwindow)
        # Give the plot window stretching priority when
        # resizing the whole application
        self.main_splitter.setStretchFactor(1, 1)
        self.horizontalLayout.addWidget(self.main_splitter)

        main_window.setCentralWidget(self.central_widget)

        # Menu bar and menus
        self._setup_menubar(main_window)

        # Statusbar
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def _setup_menubar(self, main_window: QtWidgets.QMainWindow) -> None:
        """
        Construct the menu bar, menus, and actions dynamically from MENU_SPECS.

        Parameters
        ----------
        main_window : QtWidgets.QMainWindow
            The main application window hosting the menu bar.
        """
        # Menu bar
        # self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar = main_window.menuBar()
        self.menubar.setNativeMenuBar(False)
        self.menubar.setObjectName("menubar")

        for menu_spec in self.MENU_SPECS:
            menu = QtWidgets.QMenu(self.menubar)
            menu.setObjectName(menu_spec["attr"])
            if not menu_spec.get("enabled", True):
                menu.setEnabled(False)
            setattr(self, menu_spec["attr"], menu)

            # Submenus
            for sub_spec in menu_spec.get("submenus", []):
                submenu = menu.addMenu("")
                submenu.setObjectName(sub_spec["attr"])
                setattr(self, sub_spec["attr"], submenu)

                if "action_group" in sub_spec:
                    group = QtGui.QActionGroup(submenu)
                    setattr(self, sub_spec["action_group"], group)

                for item in sub_spec.get("items", []):
                    action = self._build_action(main_window, item)
                    submenu.addAction(action)
                    if "action_group" in sub_spec:
                        group.addAction(action)

            # Menu items
            for item in menu_spec.get("items", []):
                if item is None:
                    menu.addSeparator()
                else:
                    action = self._build_action(main_window, item)
                    menu.addAction(action)

            # Standalone actions
            for item in menu_spec.get("standalone_actions", []):
                self._build_action(main_window, item)

            self.menubar.addAction(menu.menuAction())

        # main_window.setMenuBar(self.menubar)

    def _build_action(
        self, main_window: QtWidgets.QMainWindow, item_spec: dict[str, Any]
    ) -> QtGui.QAction:
        """
        Instantiate a QAction from a spec item dictionary and register it.

        Parameters
        ----------
        main_window : QtWidgets.QMainWindow
            Parent window for the action.
        item_spec : dict[str, Any]
            Configuration dictionary containing object attribute name and
            states.

        Returns
        -------
        QtGui.QAction
            The constructed QAction instance.
        """
        action = QtGui.QAction(main_window)
        action.setObjectName(item_spec["attr"])
        if item_spec.get("checkable", False):
            action.setCheckable(True)
            action.setChecked(item_spec.get("checked", False))
        if not item_spec.get("enabled", True):
            action.setEnabled(False)
        setattr(self, item_spec["attr"], action)
        return action

    def retranslateUi(self, main_window: QtWidgets.QMainWindow) -> None:
        """
        Translate user interface text for localization using MENU_SPECS schema.

        Parameters
        ----------
        main_window : QtWidgets.QMainWindow
            The parent QMainWindow instance containing localized components.
        """
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(
            _translate("MainWindow", "PATKIT Annotator")
        )
        self.mode_controls.setTitle(
            _translate("MainWindow", "Annotator Mode")
        )
        self.go_to_group.setTitle(
            _translate("MainWindow", "Go to Recording")
        )
        self.goButton.setText(_translate("MainWindow", "Go"))
        self.previous_button.setText(
            _translate("MainWindow", "Previous")
        )
        self.next_button.setText(_translate("MainWindow", "Next"))

        # Annotation radio buttons
        # self.positionRB.setTitle(
        #     _translate("MainWindow", "Customised Metadata: TonguePosition")
        # )
        # self.positionRB_1.setText(_translate("MainWindow", "High"))
        # self.positionRB_2.setText(_translate("MainWindow", "Low"))
        # self.positionRB_3.setText(
        #     _translate("MainWindow", "Other / Not visible"))

        # Mode menu actions
        # self.action_exercise_mode.setText(
        #   _translate("MainWindow", "Exercise"))
        # self.action_annotator_mode.setText(
        #     _translate("MainWindow", "Annotator"))

        # Translate menu titles, submenus, and action labels from MENU_SPECS
        for menu_spec in self.MENU_SPECS:
            menu = getattr(self, menu_spec["attr"])
            menu.setTitle(_translate("MainWindow", menu_spec["title"]))

            for sub_spec in menu_spec.get("submenus", []):
                submenu = getattr(self, sub_spec["attr"])
                submenu.setTitle(_translate("MainWindow", sub_spec["title"]))

            actions_to_translate: list[dict[str, Any]] = []
            for item in menu_spec.get("items", []):
                if isinstance(item, dict):
                    actions_to_translate.append(item)
            for sub_spec in menu_spec.get("submenus", []):
                for item in sub_spec.get("items", []):
                    if isinstance(item, dict):
                        actions_to_translate.append(item)
            for item in menu_spec.get("standalone_actions", []):
                actions_to_translate.append(item)

            for act_spec in actions_to_translate:
                action = getattr(self, act_spec["attr"])
                action.setText(_translate("MainWindow", act_spec["text"]))
                if "shortcut" in act_spec:
                    action.setShortcut(
                        _translate("MainWindow", act_spec["shortcut"])
                    )

    def add_items_to_database_view(self, session: Session) -> None:
        """
        Add items/recordings to the list view.

        Parameters
        ----------
        session : Session
            Use the recordings in the given session to populate the list view.
        """
        for recording in session:
            display_text = (
                f"{recording.basename}: "
                f"{recording.metadata.prompt.strip()}"
            )
            self.database_model.appendRow(
                QtGui.QStandardItem(display_text)
            )

    def replace_items_in_database_view(self, session: Session) -> None:
        """
        Replace the items/recordings in the list view.

        Parameters
        ----------
        session : Session
            Use the recordings in the given Session to replace the old ones.
        """
        self.database_model.clear()
        self.add_items_to_database_view(session)
