from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QScrollArea, QFrame, QGridLayout,
    QLineEdit, QMessageBox
)
from PySide6.QtCore import Qt, Signal

class ConfigPanel(QWidget):
    """A panel for displaying and editing drone parameters."""
    parameter_changed = Signal(str, float)  # parameter name, new value
    
    def __init__(self, signal_manager, parent=None):
        super().__init__(parent)
        self.signal_manager = signal_manager
        self.setup_ui()
        self.connect_signals()
        
    def setup_ui(self):
        """Creates and arranges the configuration panel."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header = QFrame()
        header.setStyleSheet("background-color: #f8f9fa; border-bottom: 1px solid #dee2e6;")
        header_layout = QHBoxLayout(header)
        
        title = QLabel("Drone Parameters")
        title.setStyleSheet("font-weight: bold;")
        header_layout.addWidget(title)
        
        # Refresh button
        refresh_button = QPushButton("↻")
        refresh_button.setFixedSize(24, 24)
        refresh_button.setStyleSheet("""
            QPushButton {
                border: none;
                padding: 0;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
                border-radius: 3px;
            }
        """)
        refresh_button.clicked.connect(self.request_parameters)
        header_layout.addWidget(refresh_button)
        
        close_button = QPushButton("×")
        close_button.setFixedSize(24, 24)
        close_button.setStyleSheet("""
            QPushButton {
                border: none;
                padding: 0;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
                border-radius: 3px;
            }
        """)
        close_button.clicked.connect(self.hide)
        header_layout.addWidget(close_button)
        
        layout.addWidget(header)
        
        # Scroll area for parameters
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Container for parameters
        self.param_container = QWidget()
        self.param_layout = QGridLayout(self.param_container)
        self.param_layout.setSpacing(5)
        
        scroll.setWidget(self.param_container)
        layout.addWidget(scroll)
        
        self.setLayout(layout)
        
        # Set initial size and style
        self.setFixedWidth(300)
        self.setStyleSheet("""
            QWidget {
                background-color: white;
            }
            QLabel {
                padding: 2px;
            }
            QPushButton {
                padding: 2px 8px;
                border: 1px solid #dee2e6;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
            QLineEdit {
                padding: 2px 5px;
                border: 1px solid #dee2e6;
                border-radius: 3px;
            }
        """)
        
    def connect_signals(self):
        """Connect to signal manager signals."""
        self.signal_manager.parameter_update.connect(self.update_parameters)
        
    def request_parameters(self):
        """Request parameter update from the drone."""
        self.signal_manager.parameter_request.emit()
        
    def update_parameters(self, parameters):
        """Update the parameter display with new values."""
        # Clear existing parameters
        while self.param_layout.count():
            item = self.param_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        # Add new parameters
        row = 0
        for name, value in parameters.items():
            # Parameter name
            name_label = QLabel(name)
            self.param_layout.addWidget(name_label, row, 0)
            
            # Parameter value with edit button
            value_widget = QWidget()
            value_layout = QHBoxLayout(value_widget)
            value_layout.setContentsMargins(0, 0, 0, 0)
            value_layout.setSpacing(2)
            
            value_edit = QLineEdit(str(value))
            value_edit.setAlignment(Qt.AlignRight)
            value_edit.setFixedWidth(80)
            value_edit.returnPressed.connect(
                lambda n=name, e=value_edit: self.on_parameter_edit(n, e)
            )
            value_layout.addWidget(value_edit)
            
            self.param_layout.addWidget(value_widget, row, 1)
            row += 1
            
    def on_parameter_edit(self, name, edit):
        """Handle parameter value edit."""
        try:
            new_value = float(edit.text())
            self.signal_manager.parameter_set.emit(name, new_value)
        except ValueError:
            QMessageBox.warning(
                self,
                "Invalid Value",
                f"Please enter a valid number for parameter {name}"
            )
            
    def showEvent(self, event):
        """Handle show event."""
        super().showEvent(event)
        # Request parameter update when shown
        self.request_parameters() 