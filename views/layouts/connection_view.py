from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton, 
    QLabel, QLineEdit, QComboBox, QFormLayout
)
from PySide6.QtCore import Qt, Signal
from views.base_view import BaseView
from core.utils import get_connection_strings

class ConnectionView(BaseView):
    """Connection view component for managing vehicle connections."""
    
    connect_clicked = Signal(str, int)  # connection_string, baud_rate
    disconnect_clicked = Signal()
    
    def __init__(self, signal_manager=None, parent=None):
        super().__init__(signal_manager)
    
    def setup_ui(self):
        """Setup the connection UI components."""
        # Create layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(5)  # Reduce spacing
        
        # Connection string input as a combo box - make it fixed width
        self.conn_string_combo = QComboBox()
        self.conn_string_combo.setEditable(True)
        self.conn_string_combo.setFixedWidth(180)
        
        # Populate the combo box with available connection strings
        for conn_string in get_connection_strings():
            self.conn_string_combo.addItem(conn_string)
        
        # Baud rate selection (for serial connections) - make it compact
        self.baud_combo = QComboBox()
        for baud in ["57600", "115200"]:
            self.baud_combo.addItem(baud)
        self.baud_combo.setCurrentText("115200")
        self.baud_combo.setFixedWidth(80)  # Set fixed width
        
        # Create form layout for inputs
        form_layout = QFormLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)  # Reduce margins
        form_layout.setSpacing(2)  # Reduce spacing
        form_layout.addRow("Connection:", self.conn_string_combo)
        form_layout.addRow("Baud Rate:", self.baud_combo)
        
        # Create separate connect and disconnect buttons
        self.connect_button = QPushButton("Connect")
        self.disconnect_button = QPushButton("Disconnect")
        self.disconnect_button.setEnabled(False)  # Initially disabled
        
        # Set fixed width for buttons
        self.connect_button.setFixedWidth(90)
        self.disconnect_button.setFixedWidth(90)
        
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(5)
        button_layout.addWidget(self.connect_button)
        button_layout.addWidget(self.disconnect_button)
        
        # Create wrapper layout
        wrapper_layout = QVBoxLayout()
        wrapper_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        wrapper_layout.setSpacing(2)  # Reduce spacing
        wrapper_layout.addLayout(form_layout)
        wrapper_layout.addLayout(button_layout)
        
        # Add to main layout
        main_layout.addLayout(wrapper_layout)
        
        # Set main layout
        self.setLayout(main_layout)
        
        # Store current connection status, primarily for button logic
        self._current_status = "DISCONNECTED" 
    
    def connect_signals(self):
        """Connect signals to slots."""
        self.connect_button.clicked.connect(self._on_connect_clicked)
        self.disconnect_button.clicked.connect(self._on_disconnect_clicked)
        
        if self.signal_manager:
            # Listen to the model changed signal
            self.signal_manager.connection_model_changed.connect(self._handle_connection_model_changed)
    
    def _on_connect_clicked(self):
        """Handle connect button click."""
        conn_string = self.conn_string_combo.currentText()
        baud_rate = int(self.baud_combo.currentText())
        self.connect_clicked.emit(conn_string, baud_rate)
    
    def _on_disconnect_clicked(self):
        """Handle disconnect button click."""
        self.disconnect_clicked.emit()
    
    def _handle_connection_model_changed(self, model_data: dict):
        """
        Handle connection model changes.
        Updates UI elements based on the new model state.
        
        Args:
            model_data: Dictionary containing the full connection model state.
        """
        status = model_data.get('status', 'DISCONNECTED')
        self._current_status = status # Update internal status tracker

        connection_string = model_data.get('connection_string', "")
        baud_rate = model_data.get('baud_rate', 115200)

        # Update input fields with model data
        if connection_string:
            idx = self.conn_string_combo.findText(connection_string)
            if idx == -1:
                self.conn_string_combo.addItem(connection_string)
                self.conn_string_combo.setCurrentText(connection_string)
            else:
                self.conn_string_combo.setCurrentIndex(idx)
        
        self.baud_combo.setCurrentText(str(baud_rate))

        # Update UI state based on connection status
        if status == "CONNECTED":
            self.connect_button.setEnabled(False)
            self.disconnect_button.setEnabled(True)
            self.conn_string_combo.setEnabled(False)
            self.baud_combo.setEnabled(False)
        elif status in ["CONNECTING", "RECONNECTING"]:
            self.connect_button.setEnabled(False)
            self.disconnect_button.setEnabled(True)
            self.conn_string_combo.setEnabled(False)
            self.baud_combo.setEnabled(False)
        else: # DISCONNECTED, ERROR, or other
            self.connect_button.setEnabled(True)
            self.disconnect_button.setEnabled(False)
            self.conn_string_combo.setEnabled(True)
            self.baud_combo.setEnabled(True)

    # The update_view method is no longer needed as updates are event-driven by _handle_connection_model_changed
    # def update_view(self, data):
    #     ...
