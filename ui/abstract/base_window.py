# ui/abstract/base_window.py

from abc import ABC, abstractmethod

class AbstractWindow(ABC):
    """
    Abstract base class for the main application window.
    Defines the essential methods any UI framework implementation must provide.
    """

    @abstractmethod
    def __init__(self, title="GCS Application", *args, **kwargs):
        """
        Initialize the main window.
        Implementations should set up the basic window frame, title, etc.
        """
        pass

    @abstractmethod
    def setup_ui(self):
        """
        Create and arrange the main UI elements (panels, menus, etc.)
        within the window. This is called after __init__.
        """
        pass

    @abstractmethod
    def run(self):
        """
        Start the UI event loop. This method should block until the
        window is closed.
        """
        pass

    @abstractmethod
    def close(self):
        """
        Programmatically close and destroy the window.
        Should trigger necessary cleanup.
        """
        pass

    # Potential future additions:
    # @abstractmethod
    # def add_panel(self, panel_instance, location):
    #     """Adds a major UI panel to the window."""
    #     pass
    #
    # @abstractmethod
    # def show_status_message(self, message, duration=0):
    #     """Displays a message in a status bar."""
    #     pass