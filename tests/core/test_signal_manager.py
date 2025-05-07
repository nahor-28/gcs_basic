import pytest
from PySide6.QtCore import QObject
from core.signal_manager import SignalManager

class TestSignalManager:
    @pytest.fixture
    def signal_manager(self):
        return SignalManager()

    def test_signal_manager_initialization(self, signal_manager):
        """Test that the signal manager initializes correctly."""
        assert isinstance(signal_manager, QObject)
        assert hasattr(signal_manager, 'telemetry_update')
        assert hasattr(signal_manager, 'connection_status_changed')
        assert hasattr(signal_manager, 'status_message')

    def test_telemetry_update_signal(self, signal_manager):
        """Test that the telemetry update signal can be emitted and received."""
        received_data = None
        
        def on_telemetry_update(data):
            nonlocal received_data
            received_data = data
        
        signal_manager.telemetry_update.connect(on_telemetry_update)
        test_data = {'altitude': 100, 'heading': 45}
        signal_manager.telemetry_update.emit(test_data)
        
        assert received_data == test_data

    def test_connection_status_signal(self, signal_manager):
        """Test that the connection status signal can be emitted and received."""
        received_status = None
        
        def on_connection_status(status):
            nonlocal received_status
            received_status = status
        
        signal_manager.connection_status_changed.connect(on_connection_status)
        test_status = {'connected': True, 'port': 'COM1'}
        signal_manager.connection_status_changed.emit(test_status)
        
        assert received_status == test_status

    def test_status_message_signal(self, signal_manager):
        """Test that the status message signal can be emitted and received."""
        received_message = None
        
        def on_status_message(message):
            nonlocal received_message
            received_message = message
        
        signal_manager.status_message.connect(on_status_message)
        test_message = "Test status message"
        signal_manager.status_message.emit(test_message)
        
        assert received_message == test_message 