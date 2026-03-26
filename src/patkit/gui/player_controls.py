# Original version: Copyright (C) 2025 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

from PyQt6.QtMultimedia import QMediaPlayer, QtAudio
from PyQt6.QtWidgets import (
    QComboBox, QHBoxLayout, QSizePolicy, QSlider, QStyle,
    QToolButton, QWidget
)
from PyQt6.QtGui import QPalette
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot


class PlayerControls(QWidget):

    play = pyqtSignal()
    pause = pyqtSignal()
    stop = pyqtSignal()
    rewind = pyqtSignal()
    change_volume = pyqtSignal(float)
    change_muting = pyqtSignal(bool)
    change_rate = pyqtSignal(float)

    def __init__(self, parent=None):
        super().__init__(parent)

        style = self.style()
        self.player_state = QMediaPlayer.PlaybackState.StoppedState
        self.player_muted = False

        self.play_button = QToolButton(self)
        self.play_button.setIcon(style.standardIcon(
            QStyle.StandardPixmap.SP_MediaPlay))
        self.play_button.setToolTip("Play")
        self.play_button.clicked.connect(self.play_clicked)

        self.pause_button = QToolButton(self)
        self.pause_button.setIcon(style.standardIcon(
            QStyle.StandardPixmap.SP_MediaPause))
        self.pause_button.setToolTip("Pause")
        self.pause_button.clicked.connect(self.pause_clicked)

        self.stop_button = QToolButton(self)
        self.stop_button.setIcon(style.standardIcon(
            QStyle.StandardPixmap.SP_MediaStop))
        self.stop_button.setToolTip("Stop")
        self.stop_button.clicked.connect(self.stop)

        self.rewind_button = QToolButton(self)
        self.rewind_button.setIcon(
            style.standardIcon(QStyle.StandardPixmap.SP_MediaSkipBackward)
        )  # noqa: E501
        self.rewind_button.setToolTip("Rewind")
        self.rewind_button.clicked.connect(self.rewind)

        self.mute_button = QToolButton(self)
        self.mute_button.setIcon(style.standardIcon(
            QStyle.StandardPixmap.SP_MediaVolume))
        self.mute_button.setToolTip("Mute - not implemented yet")
        # self.mute_button.clicked.connect(self.mute_clicked)

        self.volume_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.volume_slider.setRange(0, 100)
        sp = self.volume_slider.sizePolicy()
        sp.setHorizontalPolicy(QSizePolicy.Policy.MinimumExpanding)
        self.volume_slider.setSizePolicy(sp)
        self.volume_slider.setToolTip("Volume - not implemented yet")
        # self.volume_slider.valueChanged.connect(
        #     self.on_volume_slider_value_changed)

        self.rate_box = QComboBox(self)
        self.rate_box.setToolTip("Playback rate - not implemented yet")
        self.rate_box.addItem("0.5x", 0.5)
        self.rate_box.addItem("1.0x", 1.0)
        self.rate_box.addItem("2.0x", 2.0)
        self.rate_box.setCurrentIndex(1)
        # self.rate_box.activated.connect(self.update_rate)

        self._doSetState(QMediaPlayer.PlaybackState.StoppedState, True)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.rewind_button)
        layout.addWidget(self.play_button)
        layout.addWidget(self.pause_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.mute_button)
        layout.addWidget(self.volume_slider)
        layout.addWidget(self.rate_box)

        self.mute_button.setEnabled(False)
        self.volume_slider.setEnabled(False)
        self.rate_box.setEnabled(False)

    def state(self):
        return self.player_state

    @pyqtSlot(QMediaPlayer.PlaybackState)
    def setState(self, state):
        self._doSetState(state, False)

    def _doSetState(self, state, force):
        if state != self.player_state or force:
            self.player_state = state

            baseColor = self.palette().color(QPalette.ColorRole.Base)
            inactiveStyleSheet = f"background-color: {baseColor.name()}"
            defaultStyleSheet = ""

            if state == QMediaPlayer.PlaybackState.StoppedState:
                self.stop_button.setStyleSheet(inactiveStyleSheet)
                self.play_button.setStyleSheet(defaultStyleSheet)
                self.pause_button.setStyleSheet(defaultStyleSheet)
            elif state == QMediaPlayer.PlaybackState.PlayingState:
                self.stop_button.setStyleSheet(defaultStyleSheet)
                self.play_button.setStyleSheet(inactiveStyleSheet)
                self.pause_button.setStyleSheet(defaultStyleSheet)
            elif state == QMediaPlayer.PlaybackState.PausedState:
                self.stop_button.setStyleSheet(defaultStyleSheet)
                self.play_button.setStyleSheet(defaultStyleSheet)
                self.pause_button.setStyleSheet(inactiveStyleSheet)

    def volume(self):
        linearVolume = QtAudio.convertVolume(
            self.volume_slider.value() / 100.0,
            QtAudio.VolumeScale.LogarithmicVolumeScale,
            QtAudio.VolumeScale.LinearVolumeScale
        )
        return linearVolume

    @pyqtSlot("float")
    def set_volume(self, volume):
        logarithmicVolume = QtAudio.convertVolume(
            volume,
            QtAudio.VolumeScale.LinearVolumeScale,
            QtAudio.VolumeScale.LogarithmicVolumeScale)
        self.volume_slider.setValue(round(logarithmicVolume * 100.0))

    # def isMuted(self):
    #     return self.player_muted

    # @pyqtSlot(bool)
    # def set_muted(self, muted):
    #     if muted != self.player_muted:
    #         self.player_muted = muted
    #         sp = (QStyle.StandardPixmap.SP_MediaVolumeMuted
    #               if muted else QStyle.StandardPixmap.SP_MediaVolume)
    #         self.mute_button.setIcon(self.style().standardIcon(sp))

    @pyqtSlot()
    def play_clicked(self):
        self.play.emit()

    @pyqtSlot()
    def pause_clicked(self):
        self.pause.emit()

    # @pyqtSlot()
    # def mute_clicked(self):
    #     self.change_muting.emit(not self.player_muted)

    # def playback_rate(self):
    #     return self.rate_box.itemData(self.rate_box.currentIndex())

    # def set_playback_rate(self, rate):
    #     for i in range(0, self.rate_box.count()):
    #         if qFuzzyCompare(rate, self.rate_box.itemData(i)):
    #             self.rate_box.setCurrentIndex(i)
    #             return

    #     self.rate_box.addItem(f"{rate}x", rate)
    #     self.rate_box.setCurrentIndex(self.rate_box.count() - 1)

    # @pyqtSlot()
    # def update_rate(self):
    #     self.change_rate.emit(self.playback_rate())

    @pyqtSlot()
    def on_volume_slider_value_changed(self):
        self.change_volume.emit(self.volume())
