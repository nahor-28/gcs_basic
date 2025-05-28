from controllers.base_controller import BaseController
import logging

logger = logging.getLogger(__name__)

class ConnectionController(BaseController):
    """Controller for connection-related operations."""
    
    def __init__(self, connection_model, view=None, signal_manager=None):
        super().__init__(connection_model, view, signal_manager)
        self.connect_signals()
        logger.info("ConnectionController initialized")
    
    def connect_signals(self):
        """Connect signal handlers."""
        if self.signal_manager:
            # Connect to connection request signals
            self.signal_manager.connection_request.connect(self._handle_connection_request)
            self.signal_manager.disconnect_request.connect(self._handle_disconnect_request)
            logger.debug("ConnectionController: Connected to signals")
    
    def _handle_connection_request(self, conn_string, baud_rate):
        """
        Handle connection request.
        
        Args:
            conn_string: Connection string (e.g., 'udp:localhost:14550')
            baud_rate: Baud rate for serial connections
        """
        logger.info(f"ConnectionController: Received connection request for {conn_string} at {baud_rate} baud")
        
        # Only update model if we're not already connected
        if not (self.model and self.model.connection_status == "CONNECTED"):
            self.model.handle_connection_request(conn_string, baud_rate)
        
        # We don't need to directly emit the signal here as the HeaderView that receives
        # the UI button click already emits connection_request
    
    def _handle_disconnect_request(self):
        """
        Handle disconnect request.
        """
        logger.info("ConnectionController: Received disconnect request")
        
        # Update the model's state
        if self.model:
            self.model.handle_disconnect_request()
        
        # Same as above, we don't need to emit a signal here as the HeaderView
        # already emits disconnect_request when the UI button is clicked

    # Remove the update_view method as it's no longer used for polling
    # def update_view(self):
    #     ...
