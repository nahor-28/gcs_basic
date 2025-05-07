# ArduPilot Ground Control Station (GCS) Basic

## Overview

This is a lightweight Ground Control Station (GCS) application designed to interface with ArduPilot autopilots. It provides real-time telemetry visualization and basic vehicle status monitoring through a PySide6-based GUI, using Qt's signal/slot mechanism for robust, thread-safe operation.

---

## Project Structure

- `main.py`: Application entry point. Initializes telemetry, UI, and connects components via the SignalManager.
- `core/telemetry_manager.py`: Handles MAVLink connection, telemetry parsing, and signal emission.
- `core/signal_manager.py`: Centralizes signal definitions for the application.
- `ui/main_window.py`: PySide6-based GUI for displaying vehicle telemetry and status.
- `utils/`: (Legacy) Contains the old event bus implementation (to be removed).

---

## How It Works

1. **TelemetryManager** connects to the vehicle using MAVLink and listens for telemetry.
2. On receiving data, it emits signals (like `telemetry_update` or `connection_status_changed`) via the **SignalManager**.
3. The UI (**MainWindow**) connects to these signals and updates the display in real time.
4. The signal/slot architecture ensures loose coupling and thread safety between data acquisition and the user interface.

---

## Features

- **MAVLink Protocol Support**: Communicates with ArduPilot using pymavlink.
- **Real-time Telemetry Display**: Shows position, attitude, GPS, battery, and vehicle status.
- **Qt Signal/Slot Architecture**: Uses Qt's signal/slot mechanism for thread-safe communication.
- **Thread-Safe Operations**: Proper thread synchronization for GUI updates.
- **Comprehensive Logging**: For debugging and monitoring.
- **Connection Selection via UI**: Users can select the serial/UDP connection string and baud rate directly from the graphical interface—no code editing required.

---

## Getting Started

1. **Install dependencies:**
    
```bash
pip install -r requirements.txt
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

## Dependencies

- Python 3.x
- pymavlink
- PySide6
- pyserial
- Standard Python libraries (`threading, queue, logging, etc.`)

---

## Current Status

- Basic telemetry visualization
- Connection management
- Status message display
- Thread-safe UI updates
- Qt-based architecture for extensibility

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

- [ ] Expand test coverage
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