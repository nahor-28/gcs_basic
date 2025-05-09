from PySide6.QtCore import QObject

class BaseController(QObject):
    """Base class for all controllers in the MVC architecture."""
    
    def __init__(self, model, view, signal_manager=None):
        super().__init__()
        self.model = model
        self.view = view
        self.signal_manager = signal_manager
        self._connect_signals()
        
    def _connect_signals(self):
        """Connect model and view signals. Override in subclasses."""
        pass
        
    def update_view(self):
        """Update the view with current model data. Override in subclasses."""
        pass
        
    def handle_error(self, error_message):
        """Handle errors from the model. Override in subclasses."""
        if self.signal_manager:
            self.signal_manager.status_message.emit(error_message, 3)  # ERROR severity 