class BaseController:
    """Base class for all controllers in the application."""
    
    def __init__(self, model=None, view=None, signal_manager=None):
        """
        Initialize the base controller.
        
        Args:
            model: The model this controller will use
            view: The view this controller will update
            signal_manager: The application's signal manager for communication
        """
        self.model = model
        self.view = view
        self.signal_manager = signal_manager
        self.connect_signals()
        
    def connect_signals(self):
        """Connect signal handlers."""
        pass
        
    def update_view(self):
        """Update the view with current model data."""
        if self.model and self.view:
            self.view.update_view(self.model.get_data())
