from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QDoubleSpinBox, 
    QPushButton, QFrame, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QPixmap
import logging

logger = logging.getLogger(__name__)

class ArmTakeoffDialog(QDialog):
    """Dialog for confirming arm & takeoff operation with safety checks."""
    
    # Signal emitted when user confirms the operation
    arm_takeoff_confirmed = Signal(float)  # altitude
    
    def __init__(self, parent=None, current_mode="UNKNOWN", armed_status=False):
        super().__init__(parent)
        self.current_mode = current_mode
        self.armed_status = armed_status
        self.setWindowTitle("Arm & Takeoff Confirmation")
        self.setModal(True)
        self.setFixedSize(350, 200)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the dialog UI."""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("⚠️ ARM & TAKEOFF CONFIRMATION")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #d32f2f; margin-bottom: 10px;")
        layout.addWidget(title_label)
        
        # Altitude selection
        altitude_layout = QHBoxLayout()
        altitude_label = QLabel("Target Altitude:")
        altitude_label.setFont(QFont("Arial", 10, QFont.Bold))
        
        self.altitude_spinbox = QDoubleSpinBox()
        self.altitude_spinbox.setRange(1.0, 100.0)
        self.altitude_spinbox.setValue(10.0)
        self.altitude_spinbox.setSuffix(" meters")
        self.altitude_spinbox.setDecimals(1)
        
        altitude_layout.addWidget(altitude_label)
        altitude_layout.addWidget(self.altitude_spinbox)
        altitude_layout.addStretch()
        
        layout.addLayout(altitude_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setStyleSheet("QPushButton { background-color: #f44336; color: white; padding: 8px 16px; border: none; border-radius: 4px; font-weight: bold; }")
        self.cancel_button.clicked.connect(self.reject)
        
        self.confirm_button = QPushButton("CONFIRM ARM & TAKEOFF")
        self.confirm_button.setStyleSheet("QPushButton { background-color: #ff9800; color: white; padding: 8px 16px; border: none; border-radius: 4px; font-weight: bold; }")
        self.confirm_button.clicked.connect(self.confirm_action)
        
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.confirm_button)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        self.setLayout(layout)
        
    def confirm_action(self):
        """Handle confirmation button click."""
        altitude = self.altitude_spinbox.value()
        
        # Final confirmation
        reply = QMessageBox.question(
            self,
            "Final Confirmation",
            f"Are you absolutely sure you want to ARM and TAKEOFF to {altitude}m?\n\n"
            "This will start the motors and the vehicle will leave the ground.\n\n"
            "Click YES only if you are ready and the area is safe.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            logger.info(f"ArmTakeoffDialog: User confirmed arm & takeoff to {altitude}m")
            self.arm_takeoff_confirmed.emit(altitude)
            self.accept()
        else:
            logger.info("ArmTakeoffDialog: User cancelled final confirmation")
            
    def closeEvent(self, event):
        """Handle dialog close event."""
        logger.info("ArmTakeoffDialog: Dialog closed")
        event.accept() 