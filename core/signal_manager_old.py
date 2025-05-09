from PySide6.QtCore import QObject, Signal

class SignalManager(QObject):
    """
    Centralized signal manager for the GCS application.
    Replaces the event bus with Qt's signal/slot mechanism.
    """
    # Telemetry signals
    telemetry_update = Signal(dict)  # Data: dict (parsed message data)

    # Connection signals
    connection_request = Signal(str, int)  # Data: conn_string, baud
    disconnect_request = Signal()  # No data
    reconnect_request = Signal()  # No data

        # Status signals
    connection_status_changed = Signal(str, str)  # Data: status, message
    status_text_received = Signal(str, int)  # Data: text, severity
    
    # Command signals (for future use)
    
    def __init__(self):
        super().__init__()
        print("SignalManager initialized.") 