from controllers.base_controller import BaseController

class VehicleController(BaseController):
    """Controller for vehicle-related operations."""
    
    def __init__(self, vehicle_model, telemetry_view, signal_manager):
        """
        Initialize the vehicle controller.
        
        Args:
            vehicle_model: The vehicle model
            telemetry_view: The telemetry view
            signal_manager: The application's signal manager
        """
        super().__init__(vehicle_model, telemetry_view, signal_manager)
    
    def connect_signals(self):
        """Connect signal handlers."""
        if self.signal_manager:
            # Connect to telemetry signals with flag parameter to prevent recursion
            self.signal_manager.telemetry_update.connect(
                lambda data: self.handle_telemetry_update(data, from_signal=True)
            )
    
    def handle_telemetry_update(self, data, from_signal=False):
        """
        Handle telemetry update.
        
        Args:
            data: Dictionary with telemetry data
            from_signal: Flag indicating if this was called from a signal
        """
        # Update the model - pass the from_signal flag to avoid recursion
        if self.model:
            self.model.update(data, from_signal=from_signal)
        
        # Update the view (if applicable)
        if self.view:
            self.view.update_view(data)
    
    def set_mode(self, mode):
        """
        Set the vehicle flight mode.
        
        Args:
            mode: Flight mode string
        """
        # In a real application, this would send the mode change command
        # to the vehicle and handle the response
        if self.signal_manager:
            # Example of how a command signal might be used
            # This signal would be defined in signal_manager
            # self.signal_manager.set_mode.emit(mode)
            pass
    
    def arm(self):
        """Arm the vehicle."""
        # In a real application, this would send the arm command
        # to the vehicle and handle the response
        if self.signal_manager:
            # Example of how a command signal might be used
            # self.signal_manager.arm_request.emit()
            pass
    
    def disarm(self):
        """Disarm the vehicle."""
        # In a real application, this would send the disarm command
        # to the vehicle and handle the response
        if self.signal_manager:
            # Example of how a command signal might be used
            # self.signal_manager.disarm_request.emit()
            pass
    
    def update_view(self):
        """Update the view with current model data."""
        if self.model and self.view:
            self.view.update_view(self.model.get_data())
