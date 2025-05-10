from PySide6.QtCore import QObject, Signal, QTimer
from models.base_model import BaseModel

class ConnectionModel(QObject):
    """Model for connection state and management."""
    
    # Connection state signals
    status_changed = Signal(str, str)  # status, message
    connection_established = Signal()
    connection_lost = Signal()
    data_changed = Signal(dict)  # Emits the entire data dictionary
    error_occurred = Signal(str)  # Emits error message
    
    def __init__(self, signal_manager):
        super().__init__()
        self.signal_manager = signal_manager
        self.data = {
            'status': 'DISCONNECTED',
            'message': '',
            'connection_string': '',
            'baud_rate': 115200
        }
        
        # Connect to signal manager
        if signal_manager:
            signal_manager.connection_status_changed.connect(self.handle_connection_status)
            
        self.reconnect_timer = None
        self.reconnect_attempts = 0
        self.MAX_RECONNECT_ATTEMPTS = 5
        self.RECONNECT_BACKOFF_BASE = 1.0  # seconds
        
    def handle_connection_status(self, status, message):
        """Handle connection status changes."""
        self.data['status'] = status
        self.data['message'] = message
        
    def connect(self, connection_string, baud_rate):
        """Request connection to vehicle."""
        self.data['connection_string'] = connection_string
        self.data['baud_rate'] = baud_rate
        if self.signal_manager:
            self.signal_manager.connection_request.emit(connection_string, baud_rate)
            
    def disconnect(self):
        """Request disconnection from vehicle."""
        if self.signal_manager:
            self.signal_manager.disconnect_request.emit()
            
    def reconnect(self):
        """Request reconnection to vehicle."""
        if self.signal_manager:
            self.signal_manager.reconnect_request.emit()
        
    def handle_heartbeat(self):
        """Handle heartbeat received."""
        self.data['last_heartbeat'] = self.data.get('timestamp')
        
        # If we were reconnecting, update status to connected
        if self.data['status'] == 'RECONNECTING':
            self._update_status('CONNECTED', "Reconnected via Heartbeat")
            self.reconnect_attempts = 0
            if self.reconnect_timer:
                self.reconnect_timer.stop()
                
    def _handle_connected(self):
        """Handle successful connection."""
        self.data['is_connecting'] = False
        self._update_status('CONNECTED', "Connected successfully")
        self.connection_established.emit()
        
    def _handle_disconnected(self, message=""):
        """Handle disconnection."""
        self.data['is_connecting'] = False
        self._update_status('DISCONNECTED', message or "Disconnected")
        self.connection_lost.emit()
        
    def _handle_error(self, message):
        """Handle connection error."""
        self.data['is_connecting'] = False
        self._update_status('ERROR', message)
        self.error_occurred.emit(message)
        
    def _handle_reconnecting(self, message):
        """Handle reconnection attempt."""
        self._update_status('RECONNECTING', message)
        self._attempt_reconnect()
        
    def _attempt_reconnect(self):
        """Attempt to reconnect to the vehicle."""
        if self.reconnect_attempts >= self.MAX_RECONNECT_ATTEMPTS:
            self._update_status('ERROR', "Maximum reconnection attempts reached")
            return
            
        # Calculate backoff time
        backoff_time = self.RECONNECT_BACKOFF_BASE * (2 ** self.reconnect_attempts)
        self.reconnect_attempts += 1
        
        # Schedule reconnect attempt
        if not self.reconnect_timer:
            self.reconnect_timer = QTimer()
            self.reconnect_timer.timeout.connect(self._perform_reconnect)
            
        self.reconnect_timer.start(int(backoff_time * 1000))
        
    def _perform_reconnect(self):
        """Perform the actual reconnection attempt."""
        if self.signal_manager and self.data['connection_string']:
            self.signal_manager.reconnect_request.emit()
            
    def _update_status(self, status, message=""):
        """Update connection status."""
        self.data['status'] = status
        self.status_changed.emit(status, message)
        self.data_changed.emit(self.data) 