from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QPushButton,
    QFrame, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

class HeaderLayout(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Creates and arranges the header elements."""
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        
        # Left section
        left_section = QHBoxLayout()
        left_section.setSpacing(10)
        
        # Connection status
        self.connection_status = QLabel("Disconnected")
        self.connection_status.setStyleSheet("color: red;")
        left_section.addWidget(self.connection_status)
        
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
        
        # Hamburger menu button
        self.menu_button = QPushButton()
        self.menu_button.setIcon(QIcon(":/icons/menu.png"))  # You'll need to add this icon
        self.menu_button.setStyleSheet("""
            QPushButton {
                border: none;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
                border-radius: 3px;
            }
        """)
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
        
    def update_connection_status(self, status, message=""):
        """Update connection status display."""
        if status == "CONNECTED":
            self.connection_status.setText("Connected")
            self.connection_status.setStyleSheet("color: green;")
            self.arm_button.setEnabled(True)
        else:
            self.connection_status.setText("Disconnected")
            self.connection_status.setStyleSheet("color: red;")
            self.arm_button.setEnabled(False)
            
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