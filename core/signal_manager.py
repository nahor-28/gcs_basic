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

    # Status signals
    connection_status_changed = Signal(str, str, str)  # Data: status, message, actual_conn_string
    status_text_received = Signal(str, int)  # Data: text, severity
    
    # Model-specific update signals
    vehicle_attitude_updated = Signal(dict)
    vehicle_position_updated = Signal(dict)
    vehicle_gps_updated = Signal(dict)
    vehicle_status_updated = Signal(dict) # For general vehicle status like arming, mode
    connection_model_changed = Signal(dict)
    status_model_new_message = Signal(dict)

    # Vehicle command signals
    arm_takeoff_request = Signal(float)  # Data: target_altitude
    command_response = Signal(str, bool, str)  # Data: command_type, success, message
    
    def __init__(self):
        super().__init__()
        print("SignalManager initialized.") 