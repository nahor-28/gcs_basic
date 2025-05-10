from models.base_model import BaseModel

class VehicleModel(BaseModel):
    """Model for vehicle-related data."""
    
    def __init__(self, signal_manager=None):
        """
        Initialize the vehicle model.
        
        Args:
            signal_manager: The application's signal manager for communication
        """
        super().__init__(signal_manager)
        self.telemetry_data = {}
        self.connect_signals()
        
    def connect_signals(self):
        """Connect signal handlers."""
        if self.signal_manager:
            # Connect to telemetry signals - use lambda to pass from_signal=True
            self.signal_manager.telemetry_update.connect(
                lambda data: self.update(data, from_signal=True)
            )
    
    def update(self, data, from_signal=False):
        """
        Update the model with new telemetry data.
        
        Args:
            data: Dictionary containing telemetry data
            from_signal: Flag to prevent recursive signal emission
        """
        if isinstance(data, dict):
            self.telemetry_data.update(data)
            
            # Only emit signal if not already called from the telemetry_update signal
            # This prevents infinite recursion
            if self.signal_manager and not from_signal:
                self.signal_manager.telemetry_update.emit(self.telemetry_data)
    
    def get_data(self):
        """
        Get the current telemetry data.
        
        Returns:
            dict: The current telemetry data
        """
        return self.telemetry_data
