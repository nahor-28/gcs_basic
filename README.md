# ArduPilot Ground Control Station (GCS) Basic

## Overview

This is a lightweight Ground Control Station (GCS) application designed to interface with ArduPilot autopilots. It provides real-time telemetry visualization and basic vehicle status monitoring through a PySide6-based GUI, using Qt's signal/slot mechanism for robust, thread-safe operation.

## Features

### Core Functionality
- **MAVLink Protocol Support**: Full integration with ArduPilot using pymavlink
- **Real-time Telemetry Display**: 
  - Position and attitude data
  - GPS status and satellite count
  - Battery voltage and remaining percentage
  - Vehicle mode and system status
- **Interactive Map**: 
  - OpenStreetMap integration with offline fallback
  - Real-time vehicle position tracking
  - Custom drone marker with orientation
- **Connection Management**:
  - Support for both serial and UDP connections
  - Automatic port detection
  - Configurable baud rates
  - Connection status monitoring

### User Interface
- **Modern Qt-based Interface**:
  - Clean, responsive design
  - Resizable panels
  - Light theme support
  - Status message display
- **Header Bar**:
  - Connection controls
  - Vehicle mode display
  - GPS status
  - Battery information
  - System ID display
  - Menu access
- **Parameter Panel**:
  - Real-time parameter monitoring
  - Parameter editing capability
  - Refresh functionality

### Technical Features
- **Thread-Safe Architecture**:
  - Qt signal/slot mechanism
  - Separate telemetry and UI threads
  - Robust error handling
- **Extensible Design**:
  - Modular component structure
  - Abstract base classes for future implementations
  - Clear separation of concerns

## Project Structure

```
gcs_basic/
├── main.py                 # Application entry point
├── core/
│   ├── telemetry_manager.py    # MAVLink communication
│   └── signal_manager.py       # Signal definitions
├── ui/
│   ├── main_window.py         # Main application window
│   ├── layouts/               # UI component layouts
│   │   ├── header_layout.py
│   │   ├── telemetry_layout.py
│   │   ├── map_layout.py
│   │   ├── status_layout.py
│   │   ├── connection_layout.py
│   │   └── config_panel.py
│   └── abstract/             # Abstract base classes
│       ├── base_window.py
│       └── base_widget.py
└── utils/                   # Utility functions
    └── event_bus.py         # Legacy event system
```

## Getting Started

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Create and activate a virtual environment (recommended):**
```bash
python -m venv .venv 
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Run the application:**
```bash
python main.py
```

4. **Connect to your vehicle:**
   - Select connection type (Serial/UDP)
   - Choose appropriate baud rate
   - Click "Connect"

## Dependencies

- Python 3.x
- PySide6 (Qt for Python)
- pymavlink
- pyserial
- Standard Python libraries

## Development Status

The application is currently in active development with the following status:

### Completed Features
- Basic telemetry visualization
- Connection management
- Map integration
- Parameter panel
- Status message system
- Light theme support

### In Progress
- Arm/Disarm functionality
- Enhanced error handling
- Improved map performance

### Planned Features
- Waypoint mission planning
- Multiple vehicle support
- Data logging
- Advanced telemetry visualization
- Customizable UI layouts

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE file for details.