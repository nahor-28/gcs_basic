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
        self.attitude = {}
        self.position = {}
        self.gps_info = {}
        self.system_status = {} # e.g., arming state, mode
        # self.connect_signals() # Remove direct connection to raw telemetry_update

    # Remove connect_signals as the model no longer directly listens to raw telemetry_update
    # def connect_signals(self):
    #     """Connect signal handlers."""
    #     if self.signal_manager:
    #         self.signal_manager.telemetry_update.connect(
    #             lambda data: self.update_from_raw_telemetry(data, from_signal=True)
    #         )

    def update_attitude(self, data):
        """Update attitude data and emit a signal."""
        self.attitude.update(data)
        if self.signal_manager:
            self.signal_manager.vehicle_attitude_updated.emit(self.attitude.copy())

    def update_position(self, data):
        """Update position data and emit a signal."""
        self.position.update(data)
        if self.signal_manager:
            self.signal_manager.vehicle_position_updated.emit(self.position.copy())
            
    def update_gps_info(self, data):
        """Update GPS info data and emit a signal."""
        self.gps_info.update(data)
        if self.signal_manager:
            self.signal_manager.vehicle_gps_updated.emit(self.gps_info.copy())

    def update_system_status(self, data):
        """Update system status (e.g., arming, mode) and emit a signal."""
        self.system_status.update(data)
        if self.signal_manager:
            self.signal_manager.vehicle_status_updated.emit(self.system_status.copy())

    # The controller will now call these specific update methods
    # instead of a generic `update` method.
    # def update(self, data, from_signal=False):
    #     """
    #     Update the model with new telemetry data.
    #     This method is now replaced by more specific update methods
    #     called by the VehicleController.
    #     """
    #     pass # Keep for compatibility or remove if not needed

    def get_attitude_data(self):
        return self.attitude.copy()

    def get_position_data(self):
        return self.position.copy()
        
    def get_gps_data(self):
        return self.gps_info.copy()

    def get_system_status_data(self):
        return self.system_status.copy()

    def get_all_data(self):
        """
        Get all current vehicle data.
        
        Returns:
            dict: A dictionary containing all vehicle data.
        """
        return {
            "attitude": self.attitude.copy(),
            "position": self.position.copy(),
            "gps": self.gps_info.copy(),
            "status": self.system_status.copy(),
        }

    # get_data can be an alias for get_all_data or be removed if specific getters are preferred.
    def get_data(self):
        return self.get_all_data()
