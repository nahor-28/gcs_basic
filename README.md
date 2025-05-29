# ArduPilot Ground Control Station (GCS) Basic

## Overview

This is a lightweight Ground Control Station (GCS) application designed to interface with ArduPilot autopilots. It provides real-time telemetry visualization and basic vehicle status monitoring through a sophisticated PySide6-based GUI, implementing a robust MVC (Model-View-Controller) architecture with Qt's signal/slot mechanism for thread-safe operation.

**Current Status**: Advanced Architecture Complete - Integration & Stabilization Phase  
**Completion**: ~75-80% - Approaching beta-ready state

## 📖 Documentation & Development Resources

### For Developers & AI Tools
- **[📋 Action Items](ACTION_ITEMS.md)** - Prioritized tasks for immediate development
- **[✅ Implemented Features](IMPLEMENTED_FEATURES.md)** - Complete list of working functionality  
- **[🐛 Current Issues](CURRENT_ISSUES.md)** - Known issues and debugging priorities
- **[🗺️ Development Roadmap](DEVELOPMENT_ROADMAP.md)** - Long-term development strategy
- **[🏗️ MVC Architecture Reference](MVC_ARCHITECTURE.md)** - Technical architecture details
- **[📝 Changelog](CHANGELOG.md)** - Development history and changes

## Features

### Core Architecture ✅
- **Modern MVC Pattern**: Complete separation of Models, Views, and Controllers
- **Signal-Based Communication**: Centralized SignalManager using Qt signal/slot mechanism
- **Thread-Safe Operation**: Dedicated telemetry thread with safe UI updates
- **Extensible Design**: Base classes and modular components for easy extension

### Communication Layer ✅
- **MAVLink Protocol Support**: Full integration with ArduPilot using pymavlink
- **Connection Types**: Both serial and UDP connections supported
- **Automatic Reconnection**: Intelligent reconnection with exponential backoff
- **Real-time Processing**: Efficient telemetry filtering and parsing

### User Interface ✅
- **Professional Layout**: Modern PySide6-based responsive design
- **Real-time Telemetry Display**: 
  - Attitude data (roll, pitch, yaw, heading)
  - Position and GPS information
  - Battery voltage and remaining percentage
  - Speed and navigation data
- **Interactive Controls**:
  - Connection management with status monitoring
  - Real-time connection status display
  - Parameter configuration interface
- **Status System**: Comprehensive message display with severity levels

### Current Capabilities
- ✅ Vehicle connection and telemetry reception
- ✅ Real-time attitude and position display
- ✅ Battery and system status monitoring
- ✅ Connection status management
- ✅ Professional UI layout with responsive design
- ✅ Interactive map with real-time vehicle tracking
- ✅ Smart map updates (immediate first fix, then every 5 seconds)
- ✅ Flight path visualization and GPS coordinate display
- 🔄 Signal flow integration (under verification)
- 📋 Vehicle control features (planned for re-implementation)

## Project Structure

```
gcs_basic/
├── main.py                     # Application entry point
├── core/                       # Core system components
│   ├── signal_manager.py       # Centralized signal management
│   ├── telemetry_manager.py    # MAVLink communication & threading
│   └── utils.py               # Utility functions
├── models/                     # Data models (MVC)
│   ├── vehicle_model.py        # Vehicle telemetry data management
│   ├── connection_model.py     # Connection state management
│   ├── status_model.py         # Status message handling
│   └── base_model.py          # Base model class
├── views/                      # User interface views (MVC)
│   ├── main_view.py           # Main application window
│   ├── layouts/               # UI component layouts
│   │   ├── header_view.py     # Connection controls & status
│   │   ├── telemetry_view.py  # Telemetry data display
│   │   ├── map_view.py        # Vehicle position map
│   │   ├── status_view.py     # Status messages
│   │   └── connection_view.py # Connection management
│   └── base_view.py           # Base view class
├── controllers/                # Business logic controllers (MVC)
│   ├── vehicle_controller.py   # Vehicle operations & telemetry parsing
│   ├── connection_controller.py # Connection management logic
│   ├── status_controller.py    # Status message handling
│   └── base_controller.py     # Base controller class
└── tests/                     # Test suite
    ├── core/                  # Core component tests
    ├── models/                # Model tests  
    └── integration/           # Integration tests
```

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Virtual environment (recommended)

### Quick Start

1. **Clone and setup environment:**
```bash
git clone <repository-url>
cd gcs_basic
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python main.py
```

4. **Connect to your vehicle:**
   - Select connection type (Serial/UDP)
   - Configure connection parameters
   - Click "Connect"
   - Monitor telemetry in real-time

### Testing Connection
- **ArduPilot SITL**: Use Software In The Loop for testing
- **UDP Simulator**: Connect to 0.0.0.0:14550 for MAVLink data
- **Hardware**: Connect directly to autopilot via serial/radio

## Development Status & Next Steps

### ✅ Completed (Phase 1a)
- Complete MVC architecture implementation
- Thread-safe telemetry processing
- Professional UI framework
- Connection management system
- Basic telemetry display components

### 🔄 Current Focus (Phase 1b)
- Signal flow verification and debugging
- UI component integration testing
- Connection stability improvements
- Basic vehicle control re-implementation

### 📋 Immediate Priorities
1. **Signal Flow Debugging** - Verify telemetry data reaches UI components
2. **GPS Label Fixes** - Complete telemetry view implementation
3. **Connection Testing** - Validate with real MAVLink sources
4. **Control Features** - Re-implement arm/disarm functionality

See **[Action Items](ACTION_ITEMS.md)** for detailed task breakdown.

## Dependencies

### Core Dependencies
- **PySide6**: Qt6 Python bindings for modern GUI
- **pymavlink**: MAVLink protocol implementation
- **pyserial**: Serial communication support
- **pytest**: Testing framework

### Development Tools
- **pytest-qt**: Qt application testing
- **folium**: Map integration (planned)

## Contributing

This project follows modern development practices with comprehensive documentation for AI-assisted development.

### Development Workflow
1. Check **[Action Items](ACTION_ITEMS.md)** for current priorities
2. Review **[Current Issues](CURRENT_ISSUES.md)** for known problems
3. Follow **[MVC Architecture](MVC_ARCHITECTURE.md)** patterns
4. Update documentation after changes

### Code Quality
- Follow existing MVC patterns
- Add appropriate logging for debugging
- Include tests for new functionality
- Update helper documentation as needed

## Architecture Highlights

### Signal Flow
```
MAVLink Source → TelemetryManager → VehicleController → VehicleModel → Views
```

### Key Design Patterns
- **MVC Architecture**: Clean separation of concerns
- **Signal/Slot Communication**: Decoupled, thread-safe messaging
- **Observer Pattern**: Views react to model changes
- **Command Pattern**: User actions processed through controllers

### Thread Safety
- Telemetry reception in dedicated thread
- All UI updates via Qt signals to main thread
- Thread-safe data models with proper locking

## Future Vision

This project aims to become a comprehensive, professional-grade Ground Control Station with:

- **Phase 2**: Mission planning, enhanced telemetry, improved UX
- **Phase 3**: Multi-vehicle support, advanced operations
- **Phase 4**: Professional features, compliance tools
- **Phase 5**: Plugin ecosystem, cloud integration

See **[Development Roadmap](DEVELOPMENT_ROADMAP.md)** for detailed planning.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support & Documentation

- **Technical Reference**: [MVC Architecture Documentation](MVC_ARCHITECTURE.md)
- **Development Status**: [Current Issues](CURRENT_ISSUES.md) & [Action Items](ACTION_ITEMS.md)
- **Long-term Planning**: [Development Roadmap](DEVELOPMENT_ROADMAP.md)
- **Change History**: [Changelog](CHANGELOG.md)

---

**Note**: This is an actively developed project with sophisticated architecture designed for professional Ground Control Station operations. The current focus is on completing the integration phase to achieve stable, reliable basic functionality.