from PySide6.QtCore import QObject, Signal

class BaseModel(QObject):
    """Base class for all models in the MVC architecture."""
    
    # Common signals that all models might need
    data_changed = Signal(dict)  # Emitted when model data changes
    error_occurred = Signal(str)  # Emitted when an error occurs
    
    def __init__(self, signal_manager=None):
        super().__init__()
        self.signal_manager = signal_manager
        self._data = {}
        
    @property
    def data(self):
        """Get the current model data."""
        return self._data.copy()
        
    def update(self, new_data):
        """Update the model data and emit appropriate signals."""
        self._data.update(new_data)
        self.data_changed.emit(self._data)
        
    def clear(self):
        """Clear the model data."""
        self._data.clear()
        self.data_changed.emit(self._data) 