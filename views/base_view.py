from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QObject

class BaseView(QWidget):
    """Base class for all views in the MVC architecture."""
    
    def __init__(self, signal_manager=None):
        super().__init__()
        self.signal_manager = signal_manager
        self.setup_ui()
        self.connect_signals()
        
    def setup_ui(self):
        """Setup the UI components. To be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement setup_ui()")
        
    def connect_signals(self):
        """Connect signals to slots. To be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement connect_signals()")
        
    def update_view(self, data):
        """Update the view with new data. To be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement update_view()") 