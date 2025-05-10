from PySide6.QtCore import QObject

class BaseModel(QObject):
    """Base class for all models in the application."""
    
    def __init__(self, signal_manager=None):
        """
        Initialize the base model.
        
        Args:
            signal_manager: The application's signal manager for communication
        """
        super().__init__()
        self.signal_manager = signal_manager
        
    def update(self, data):
        """
        Update the model with new data.
        
        Args:
            data: The data to update the model with
        """
        pass
