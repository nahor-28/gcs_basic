from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QObject

class BaseView(QWidget):
    """Base class for all views in the application."""
    
    def __init__(self, signal_manager=None):
        """
        Initialize the base view.
        
        Args:
            signal_manager: The application's signal manager for communication
        """
        super().__init__()
        self.signal_manager = signal_manager
        self.setup_ui()
        self.connect_signals()
        
    def setup_ui(self):
        """Set up the UI components for this view."""
        pass
        
    def connect_signals(self):
        """Connect signal handlers."""
        pass
        
    def update_view(self, data):
        """
        Update the view with new data.
        
        Args:
            data: The data to update the view with
        """
        pass
