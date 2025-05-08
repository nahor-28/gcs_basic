from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QPushButton,
    QFrame, QSizePolicy, QMenu
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from ui.layouts.connection_layout import ConnectionLayout

class HeaderLayout(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Creates and arranges the header elements."""
        layout = QHBoxLayout()
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(5)
        
        # Left section
        left_section = QHBoxLayout()
        left_section.setSpacing(10)
        
        # Connection status
        self.connection_status = QLabel("Disconnected")
        self.connection_status.setStyleSheet("color: red;")
        left_section.addWidget(self.connection_status)
        
        # Add connection layout
        self.connection_layout = ConnectionLayout()
        self.connection_layout.setMaximumHeight(40)  # Make it fit in header
        self.connection_layout.setStyleSheet("""
            QGroupBox {
                border: none;
                margin-top: 0px;
            }
            QGroupBox::title {
                display: none;
            }
        """)
        left_section.addWidget(self.connection_layout)
        
        # Mode display
        self.mode_label = QLabel("Mode: ---")
        left_section.addWidget(self.mode_label)
        
        # Arm/Disarm button
        self.arm_button = QPushButton("ARM")
        self.arm_button.setEnabled(False)
        self.arm_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        left_section.addWidget(self.arm_button)
        
        # GPS status
        self.gps_status = QLabel("GPS: No Fix")
        left_section.addWidget(self.gps_status)
        
        # Battery status
        self.battery_status = QLabel("Battery: ---")
        left_section.addWidget(self.battery_status)
        
        # Add left section to main layout
        layout.addLayout(left_section)
        
        # Add stretch to push right section to the end
        layout.addStretch()
        
        # Right section
        right_section = QHBoxLayout()
        right_section.setSpacing(10)
        
        # System/Drone ID
        self.system_id = QLabel("System ID: ---")
        right_section.addWidget(self.system_id)
        
        # Menu button with hamburger icon (≡)
        self.menu_button = QPushButton("≡")
        self.menu_button.setStyleSheet("""
            QPushButton {
                border: none;
                padding: 5px 10px;
                font-size: 20px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
                border-radius: 3px;
            }
        """)
        self.menu_button.clicked.connect(self.show_menu)
        right_section.addWidget(self.menu_button)
        
        # Add right section to main layout
        layout.addLayout(right_section)
        
        # Set the main layout
        self.setLayout(layout)
        
        # Set fixed height and style
        self.setFixedHeight(40)
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border-bottom: 1px solid #dee2e6;
            }
        """)
        
    def show_menu(self):
        """Show the menu with parameter panel option."""
        menu = QMenu(self)
        param_action = menu.addAction("Parameters")
        param_action.triggered.connect(self.show_parameters)
        menu.exec(self.menu_button.mapToGlobal(self.menu_button.rect().bottomLeft()))
        
    def show_parameters(self):
        """Show the parameters panel."""
        # This will be implemented later
        pass
        
    def update_connection_status(self, status, message=""):
        """Update connection status display."""
        if status == "CONNECTED":
            self.connection_status.setText("Connected")
            self.connection_status.setStyleSheet("color: green;")
            self.arm_button.setEnabled(True)
            self.connection_layout.set_connected(True)
        else:
            self.connection_status.setText("Disconnected")
            self.connection_status.setStyleSheet("color: red;")
            self.arm_button.setEnabled(False)
            self.connection_layout.set_connected(False)
            
    def update_mode(self, mode):
        """Update flight mode display."""
        self.mode_label.setText(f"Mode: {mode}")
        
    def update_gps_status(self, fix_type, satellites):
        """Update GPS status display."""
        fix_map = {0: "No Fix", 1: "No Fix", 2: "2D Fix", 3: "3D Fix", 
                  4: "DGPS", 5: "RTK Float", 6: "RTK Fixed"}
        fix_str = fix_map.get(fix_type, f"Unknown ({fix_type})")
        self.gps_status.setText(f"GPS: {fix_str} ({satellites} sats)")
        
    def update_battery(self, voltage, percentage):
        """Update battery status display."""
        self.battery_status.setText(f"Battery: {voltage:.1f}V ({percentage:.0f}%)")
        
    def update_system_id(self, system_id):
        """Update system ID display."""
        self.system_id.setText(f"System ID: {system_id}")