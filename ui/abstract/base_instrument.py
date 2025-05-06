# ui/abstract/base_instrument.py

from abc import ABC # No need for abstractmethod if no new methods are added yet
from .base_widget import AbstractWidget

class AbstractInstrument(AbstractWidget):
    """
    Abstract base class for instrument displays (e.g., Artificial Horizon, Compass).
    Inherits the basic requirements from AbstractWidget.
    """

    # No additional abstract methods are strictly required by all instruments *yet*.
    # Specific instrument implementations will define how they use `update_data`
    # or might implement more specific update methods like `update_attitude`.
    # If common methods emerge (e.g., set_range, set_units), they could be added here.
    def __init__(self, parent, event_bus, *args, **kwargs):
        super().__init__(parent, event_bus, *args, **kwargs)

    # Inherits abstract method update_data(self, data) from AbstractWidget