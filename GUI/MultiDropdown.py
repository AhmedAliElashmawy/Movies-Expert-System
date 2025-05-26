from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QListWidget, QListWidgetItem, QCheckBox, QApplication
)
from PyQt5.QtCore import Qt, QPoint, QEvent
from PyQt5.QtGui import QCursor


class MultiSelectDropdown(QWidget):
    def __init__(self, items=None, placeholder="Select items...", parent=None):
        super().__init__(parent)
        self.items = items or []

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.line_edit = QLineEdit()
        self.line_edit.setReadOnly(True)
        self.line_edit.setPlaceholderText(placeholder)

        self.list_widget = QListWidget()
        self.list_widget.setWindowFlags(Qt.Popup)
        self.list_widget.setFocusPolicy(Qt.NoFocus)
        self.list_widget.hide()

        # Styling
        self.set_style()

        for item_text in self.items:
            item = QListWidgetItem(self.list_widget)
            checkbox = QCheckBox(item_text)
            self.list_widget.setItemWidget(item, checkbox)
            checkbox.stateChanged.connect(self.update_selection)

        self.line_edit.mousePressEvent = self.show_list

        self.line_edit.installEventFilter(self)
        self.list_widget.installEventFilter(self)

        self.layout.addWidget(self.line_edit)

        # Install event filter on app to detect clicks outside dropdown
        QApplication.instance().installEventFilter(self)

    def set_style(self):
        style = """
        QLineEdit {
            background-color: rgba(255, 255, 255, 0.85);
            border: 1px solid #2E1A47;
            border-radius: 6px;
            padding: 6px;
            font-size: 14px;
            color: #1A1A40;
            min-width: 200px;
        }

        QLineEdit:hover {
            border: 1px solid #9D7AF0;
        }

        QLineEdit::placeholder {
            color: #7D7D7D;
        }

        QListWidget {
            background-color: rgba(255, 255, 255, 0.95);
            border: 1px solid #2E1A47;
            border-radius: 6px;
            padding: 4px;
            font-size: 14px;
            color: #1A1A40;
            min-width: 200px;
        }

        QListWidget::item {
            border: none;
            padding: 4px;
        }

        QListWidget::item:hover {
            background-color: #D8C3F3;
            border-radius: 4px;
        }

        QCheckBox {
            padding-left: 4px;
        }

        QCheckBox::indicator {
            width: 16px;
            height: 16px;
            border-radius: 3px;
        }

        QCheckBox::indicator:checked {
            background-color: #9D7AF0;
            border: 1px solid #2E1A47;
        }

        QCheckBox::indicator:unchecked {
            border: 1px solid #2E1A47;
        }
        """
        self.line_edit.setStyleSheet(style)
        self.list_widget.setStyleSheet(style)

    def show_list(self, event):
        if self.list_widget.isVisible():
            self.list_widget.hide()
            return

        pos = self.line_edit.mapToGlobal(QPoint(0, self.line_edit.height()))
        self.list_widget.move(pos)
        self.list_widget.setMinimumWidth(self.line_edit.width())
        self.list_widget.show()
        self.list_widget.setFocus()

    def update_selection(self):
        selected = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            checkbox = self.list_widget.itemWidget(item)
            if checkbox.isChecked():
                selected.append(checkbox.text())
        self.line_edit.setText(", ".join(selected))

    def get_selected_items(self):
        selected = []
        for i in range(self.list_widget.count()):
            checkbox = self.list_widget.itemWidget(self.list_widget.item(i))
            if checkbox.isChecked():
                selected.append(checkbox.text())
        return selected

    def clear_selection(self):
        """Clear all selected items in the dropdown."""
        # Uncheck all checkboxes in the list widget
        for i in range(self.list_widget.count()):
            checkbox = self.list_widget.itemWidget(self.list_widget.item(i))
            if checkbox.isChecked():
                checkbox.setChecked(False)
        
        # Clear the text in the line edit
        self.line_edit.setText("")
        
        # If you have a separate list of selected items
        if hasattr(self, 'selected_items'):
            self.selected_items = []

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Leave:
            pos = QApplication.instance().widgetAt(QCursor.pos())
            if pos not in (self.line_edit, self.list_widget) and not self.list_widget.isHidden():
                if pos is None or (pos != self.line_edit and not self.list_widget.isAncestorOf(pos)):
                    self.list_widget.hide()

        if event.type() == QEvent.MouseButtonPress:
            if self.list_widget.isVisible():
                clicked_widget = QApplication.instance().widgetAt(event.globalPos())
                if clicked_widget not in (self.line_edit, self.list_widget) and \
                   not self.list_widget.isAncestorOf(clicked_widget):
                    self.list_widget.hide()

        return super().eventFilter(obj, event)
