import pytest
from unittest.mock import Mock, patch
from core.telemetry_manager import TelemetryManager
from core.signal_manager import SignalManager

class TestTelemetryManager:
    @pytest.fixture
    def signal_manager(self):
        return SignalManager()

    @pytest.fixture
    def telemetry_manager(self, signal_manager):
        return TelemetryManager(signal_manager)

    def test_telemetry_manager_initialization(self, telemetry_manager, signal_manager):
        """Test that the telemetry manager initializes correctly."""
        assert telemetry_manager.signal_manager == signal_manager
        assert telemetry_manager.connection_string == ""
        assert telemetry_manager.baud_rate == 57600
        assert telemetry_manager.vehicle is None
        assert telemetry_manager.connection_thread is None
        assert not telemetry_manager.is_connected

    @patch('pymavlink.mavutil.mavlink_connection')
    def test_connect_success(self, mock_mavlink_connection, telemetry_manager):
        """Test successful connection to a vehicle."""
        mock_vehicle = Mock()
        mock_mavlink_connection.return_value = mock_vehicle
        
        telemetry_manager.connection_string = "udpin:localhost:14550"
        telemetry_manager.connect()
        
        mock_mavlink_connection.assert_called_once_with(
            "udpin:localhost:14550",
            baud=57600
        )
        assert telemetry_manager.vehicle == mock_vehicle
        assert telemetry_manager.connection_thread is not None
        assert telemetry_manager.is_connected

    def test_connect_invalid_connection_string(self, telemetry_manager):
        """Test connection with invalid connection string."""
        telemetry_manager.connection_string = ""
        telemetry_manager.connect()
        
        assert telemetry_manager.vehicle is None
        assert telemetry_manager.connection_thread is None
        assert not telemetry_manager.is_connected

    def test_disconnect(self, telemetry_manager):
        """Test disconnecting from a vehicle."""
        # Setup a mock vehicle
        mock_vehicle = Mock()
        telemetry_manager.vehicle = mock_vehicle
        telemetry_manager.is_connected = True
        
        telemetry_manager.disconnect()
        
        assert telemetry_manager.vehicle is None
        assert not telemetry_manager.is_connected
        mock_vehicle.close.assert_called_once()

    @patch('pymavlink.mavutil.mavlink_connection')
    def test_telemetry_processing(self, mock_mavlink_connection, telemetry_manager):
        """Test processing of telemetry data."""
        # Setup mock vehicle and message
        mock_vehicle = Mock()
        mock_message = Mock()
        mock_message.get_type.return_value = 'GLOBAL_POSITION_INT'
        mock_message.relative_alt = 1000
        mock_message.hdg = 45
        
        mock_vehicle.recv_match.return_value = mock_message
        mock_mavlink_connection.return_value = mock_vehicle
        
        # Connect to vehicle
        telemetry_manager.connection_string = "udpin:localhost:14550"
        telemetry_manager.connect()
        
        # Process a message
        telemetry_manager._process_message(mock_message)
        
        # Verify the message was processed correctly
        mock_message.get_type.assert_called_once() 