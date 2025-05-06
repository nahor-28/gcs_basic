# ui/abstract/base_widget.py

from abc import ABC, abstractmethod

class AbstractWidget(ABC):
    """
    Abstract base class for UI widgets.
    Ensures widgets have a standard way to be updated.
    """

    @abstractmethod
    def __init__(self, parent, event_bus, *args, **kwargs):
        """
        Initialize the widget.

        Args:
            parent: The container widget (Tkinter frame, QWidget, etc.).
            event_bus: Reference to the application's event bus for
                       potential event publishing or subscribing within the widget.
        """
        self.parent = parent
        self.event_bus = event_bus
        # Concrete implementations will create the actual UI element (Label, Button, Canvas)
        self._ui_element = None # Placeholder for the actual tk/qt widget

    @abstractmethod
    def update_data(self, data):
        """
        Update the widget's visual representation based on new data.

        Args:
            data: The data relevant to this widget (could be a dict,
                  specific values, an event object, etc.).
        """
        pass

    # Concrete implementations need to handle their own layout (pack, grid, etc.)
    # within the parent. Access to the underlying ui element might be useful.
    def get_ui_element(self):
        """Returns the underlying UI framework element (e.g., tk.Frame)."""
        return self._ui_element