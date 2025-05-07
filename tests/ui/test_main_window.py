import pytest
from PySide6.QtWidgets import QApplication
from PySide6.QtTest import QTest
from PySide6.QtCore import Qt
from ui.main_window import MainWindow
from core.signal_manager import SignalManager

@pytest.fixture
def app():
    return QApplication([])

@pytest.fixture
def signal_manager():
    return SignalManager()

@pytest.fixture
def main_window(app, signal_manager):
    window = MainWindow(signal_manager)
    window.show()
    return window

class TestMainWindow:
    def test_main_window_initialization(self, main_window, signal_manager):
        """Test that the main window initializes correctly."""
        assert main_window.signal_manager == signal_manager
        assert main_window.windowTitle() == "ArduPilot GCS Basic"
        assert main_window.isVisible()

    def test_connection_controls(self, main_window):
        """Test the connection control widgets."""
        # Test connection string input
        main_window.connection_input.setText("udpin:localhost:14550")
        assert main_window.connection_input.text() == "udpin:localhost:14550"

        # Test baud rate selection
        main_window.baud_rate_combo.setCurrentText("115200")
        assert main_window.baud_rate_combo.currentText() == "115200"

    def test_telemetry_display(self, main_window):
        """Test updating telemetry display."""
        test_data = {
            'altitude': 100.5,
            'heading': 45,
            'latitude': 37.123,
            'longitude': -122.456,
            'battery_remaining': 75,
            'ground_speed': 5.5
        }
        
        main_window.signal_manager.telemetry_update.emit(test_data)
        QTest.qWait(100)  # Wait for signal processing
        
        # Verify the display was updated
        assert "100.5" in main_window.altitude_label.text()
        assert "45" in main_window.heading_label.text()
        assert "75" in main_window.battery_label.text()

    def test_status_message_display(self, main_window):
        """Test status message display."""
        test_message = "Test status message"
        main_window.signal_manager.status_message.emit(test_message)
        QTest.qWait(100)  # Wait for signal processing
        
        assert test_message in main_window.status_label.text()

    def test_connection_status_display(self, main_window):
        """Test connection status display."""
        # Test connected state
        main_window.signal_manager.connection_status_changed.emit({'connected': True})
        QTest.qWait(100)  # Wait for signal processing
        assert "Connected" in main_window.connection_status_label.text()
        
        # Test disconnected state
        main_window.signal_manager.connection_status_changed.emit({'connected': False})
        QTest.qWait(100)  # Wait for signal processing
        assert "Disconnected" in main_window.connection_status_label.text() 