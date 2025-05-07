# ArduPilot Ground Control Station (GCS) Basic

## Overview

This is a lightweight Ground Control Station (GCS) application designed to interface with ArduPilot autopilots. It provides real-time telemetry visualization and basic vehicle status monitoring through a Tkinter-based GUI, using an event-driven architecture for robust, thread-safe operation.

---

## Project Structure

- `main.py`: Application entry point. Initializes telemetry, UI, and connects components via the EventBus.
- `core/telemetry_manager.py` : Handles MAVLink connection, telemetry parsing, and event publishing.
- `core/vehicle_data.py` : (If used) Data structures for vehicle state.
- `ui/simple_display.py`: Tkinter-based GUI for displaying vehicle telemetry and status.
- `utils/event_bus.py`: Thread-safe publish/subscribe event bus for decoupled communication.
- `utils/constants.py`: (If used) Shared constants.
-  `tests/` : Contains all automated test files for core, UI, and utils modules.
    - `tests/utils/test_event_bus.py`: Unit tests for the event bus, including subscribing, unsubscribing, publishing, and error handling.
    - `tests/core/, tests/ui/`: (Currently contain `**init**.py` for package structure; add tests here as needed.)

---

## How It Works

1. **TelemetryManager** connects to the vehicle using MAVLink and listens for telemetry.
2. On receiving data, it publishes events (like `TELEMETRY_UPDATE` or `CONNECTION_STATUS_CHANGED`) via the **EventBus**.
3. The UI (**SimpleDisplay**) subscribes to these events and updates the display in real time.
4. The event-driven architecture ensures loose coupling and thread safety between data acquisition and the user interface.

---

## Features

- **MAVLink Protocol Support**: Communicates with ArduPilot using pymavlink.
- **Real-time Telemetry Display**: Shows position, attitude, GPS, battery, and vehicle status.
- **Event-Driven Architecture**: Uses a custom event bus for loose coupling between components.
- **Thread-Safe Operations**: Proper thread synchronization for GUI updates.
- **Comprehensive Logging**: For debugging and monitoring.
- **Connection Selection via UI**: Users can select the serial/UDP connection string and baud rate directly from the graphical interface—no code editing required.
- **Automated Tests**: Test suite using pytest for core event bus functionality and structure for future test expansion.

---

## Getting Started

1. **Install dependencies:**
    
```bash
pip install pymavlink pytest
```
    
2. **(Optional) Create and activate a virtual environment:**

```bash
python -m venv .venv 
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```    
3. **Connect your autopilot and run:**
    
```bash
python main.py
```
    
4. **Select your connection and baud rate in the UI, then connect.**

---

## Running Tests

To run the automated test suite (requires pytest):


```bash
pytest tests/
```

This will execute all available unit tests, currently focusing on the event bus logic. Expand the test suite for other modules as your project grows.

---

## Dependencies

- Python 3.x
- pymavlink
- tkinter (usually included with Python)
- pytest (for running tests)
- Standard Python libraries (`threading, queue, logging, etc.`)

---

## Current Status

- Basic telemetry visualization
- Connection management
- Status message display
- Thread-safe UI updates
- Event-based architecture for extensibility
- Automated tests for event bus

---

## Future Enhancements

### Core Functionality

- [ ] Waypoint mission planning and management
- [ ] Parameter configuration interface
- [ ] Multiple vehicle connections
- [ ] Data logging

### User Interface

- [ ] Map view for vehicle position visualization
- [ ] Customizable dashboard layouts
- [ ] UI themes
- [ ] Advanced status/history panel

### Advanced Features

- [ ] Geofencing support
- [ ] Failsafe configuration
- [ ] Camera controls
- [ ] Video streaming

### Code Quality & Maintenance

- [ ] Expand test coverage to core and UI modules
- [ ] CI/CD pipeline
- [ ] API documentation
- [ ] Improved error handling

### Performance

- [ ] Telemetry data processing optimizations
- [ ] Data compression for bandwidth
- [ ] Configurable telemetry update rates

---

## Known Issues

- Limited error recovery for connection drops
- Basic UI with limited customization options
- No data persistence for telemetry logs

---

## Contributions

Contributions, bug reports, and suggestions are welcome! Please open an issue or submit a pull request.