from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QDialogButtonBox,
    QWidget
)


class ListSelectionDialog(QDialog):
    """
    A custom dialog that mimics QInputDialog.getItem but uses a QListWidget
    instead of a QComboBox for better readability of long strings (like paths).
    """

    def __init__(
        self,
        parent: QWidget | None,
        title: str,
        label: str,
        items: list[str],
        current: int = 0,
    ):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(500, 300)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(label))

        self.list_widget = QListWidget()
        self.list_widget.addItems(items)

        # Set the default selected row if within bounds
        if 0 <= current < len(items):
            self.list_widget.setCurrentRow(current)

        # Allow double-clicking an item to act as clicking "OK"
        self.list_widget.itemDoubleClicked.connect(self.accept)
        layout.addWidget(self.list_widget)

        # Standard OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    @staticmethod
    def get_item(
        parent: QWidget | None,
        title: str,
        label: str,
        items: list[str],
        current: int = 0,
        **kwargs
    ) -> tuple[str, bool]:
        """
        Static method that exactly mirrors QInputDialog.getItem signature.

        Returns
        -------
        tuple[str, bool]
            The selected string and a boolean indicating if OK was pressed.
        """
        dialog = ListSelectionDialog(
            parent=parent,
            title=title,
            label=label,
            items=items,
            current=current
        )

        # Execute the dialog blockingly
        result = dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            if dialog.list_widget.currentItem():
                return dialog.list_widget.currentItem().text(), True

        return "", False
