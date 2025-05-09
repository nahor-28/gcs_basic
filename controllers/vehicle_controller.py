from PySide6.QtCore import QObject

class VehicleController(QObject):
    """Controller for vehicle-related operations."""
    
    def __init__(self, vehicle_model, telemetry_view, signal_manager):
        super().__init__()
        self.vehicle_model = vehicle_model
        self.telemetry_view = telemetry_view
        self.signal_manager = signal_manager
        
        # Connect view signals
        # if telemetry_view:
        #     telemetry_view.mode_changed.connect(self.set_mode)
        #     telemetry_view.arm_requested.connect(self.arm)
        #     telemetry_view.disarm_requested.connect(self.disarm)
            
    # def set_mode(self, mode):
    #     """Set vehicle flight mode."""
    #     if self.signal_manager:
    #         self.signal_manager.set_mode.emit(mode)
            
    # def arm(self):
    #     """Arm the vehicle."""
    #     if self.signal_manager:
    #         self.signal_manager.arm_request.emit()
            
    # def disarm(self):
    #     """Disarm the vehicle."""
    #     if self.signal_manager:
    #         self.signal_manager.disarm_request.emit()
            
    def update_view(self):
        """Update the telemetry view with current vehicle data."""
        if self.telemetry_view:
            self.telemetry_view.update_view(self.vehicle_model.data) 