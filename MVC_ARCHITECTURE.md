# GCS_BASIC MVC Architecture Reference

## Overview

This project implements a robust Model-View-Controller (MVC) architecture for a Ground Control Station (GCS) application. It is designed for modularity, testability, and extensibility, leveraging PySide6 for the GUI and a central `SignalManager` for all inter-component communication.

**Current Status**: Architecture Complete ✅ - Integration Phase 🔄  
**Documentation**: See [IMPLEMENTED_FEATURES.md](IMPLEMENTED_FEATURES.md) for detailed feature status

---

## 📖 Related Documentation

- **[📋 Action Items](ACTION_ITEMS.md)** - Current development tasks
- **[🐛 Current Issues](CURRENT_ISSUES.md)** - Known integration issues
- **[✅ Implemented Features](IMPLEMENTED_FEATURES.md)** - Complete feature tracking
- **[🗺️ Development Roadmap](DEVELOPMENT_ROADMAP.md)** - Future architecture evolution

---

## Architectural Diagram

```
+-----------------+      +-----------------+      +-----------------+
|     Models      |<---->|  SignalManager  |<---->|     Views       |
+-----------------+      +-----------------+      +-----------------+
        ^                        ^                        ^
        |                        |                        |
        +-------------------+    |    +-------------------+
                            |    v    |
                     +----------------------+
                     |    Controllers       |
                     +----------------------+
                            ^
                            |
                     +----------------------+
                     |  TelemetryManager    |
                     +----------------------+
```

---

## Implementation Status

### ✅ Fully Implemented Components

#### 1. Models (Data Layer)
- **VehicleModel**: Complete telemetry data management
  - Attitude storage (roll, pitch, yaw, heading)
  - Position storage (GPS coordinates, altitude, speed)
  - System status (battery, arming state, flight mode)
  - Signal emission for all data updates
- **ConnectionModel**: Complete connection state management
  - Connection parameters and status tracking
  - External status update integration
  - Real-time status change notifications
- **StatusModel**: Complete message management
  - Application and system message handling
  - Severity-based message categorization
  - Event tracking and notification

#### 2. Views (User Interface Layer)
- **MainView**: Complete primary window integration
  - Splitter layout with responsive panels
  - Sub-view integration and management
- **HeaderView**: Complete connection controls
  - Connection status display
  - User interaction handling
- **TelemetryView**: Complete telemetry display
  - Real-time attitude, position, speed, battery data
  - Signal-based UI updates
  - Professional formatting and layout
- **StatusView**: Complete message display
  - Severity-based message visualization
  - Real-time status updates
- **ConnectionView**: Complete connection management
  - Port selection and configuration
  - Connection parameter handling
- **MapView**: Basic position display (placeholder for enhancement)

#### 3. Controllers (Business Logic Layer)
- **VehicleController**: Complete telemetry processing
  - Raw MAVLink message parsing
  - Model update coordination
  - Data validation and filtering
- **ConnectionController**: Complete connection logic
  - User action processing
  - Connection state management
- **StatusController**: Complete message handling
  - Status message processing and routing

#### 4. Core Infrastructure
- **SignalManager**: Complete centralized communication
  - All inter-component signal definitions
  - Thread-safe signal routing
  - Typed signal emissions
- **TelemetryManager**: Complete MAVLink integration
  - Dedicated telemetry thread
  - Connection monitoring and reconnection
  - Message filtering and parsing
  - Heartbeat monitoring with timeout detection

### 🔄 Integration Phase Components

#### Signal Flow Chain
**Target Flow**: `TelemetryManager → VehicleController → VehicleModel → Views`
- **Status**: Architecture complete, verification in progress
- **Focus**: Confirming all signal connections work end-to-end
- **Issues**: See [CURRENT_ISSUES.md](CURRENT_ISSUES.md) for specific concerns

---

## Data Flow Architecture

### Primary Telemetry Flow
```
MAVLink Source 
    ↓
TelemetryManager (TelemetryThread)
    ↓ (telemetry_update signal)
VehicleController.handle_raw_telemetry_update()
    ↓ (calls model.update_* methods)
VehicleModel (update_attitude/position/gps/status)
    ↓ (emits specific signals: vehicle_attitude_updated, etc.)
Views (TelemetryView, MapView)
    ↓ (UI updates)
User Interface Display
```

### Connection Status Flow
```
User Action (Connect/Disconnect)
    ↓
HeaderView → ConnectionView
    ↓ (connection_request/disconnect_request signals)
ConnectionController
    ↓ (forwards to TelemetryManager)
TelemetryManager
    ↓ (connection_status_changed signal)
ConnectionModel
    ↓ (connection_model_changed signal)
HeaderView → Status Display Update
```

### Status Message Flow
```
System Event/MAVLink STATUSTEXT
    ↓
TelemetryManager
    ↓ (status_text_received signal)
StatusModel
    ↓ (status_model_new_message signal)
StatusView
    ↓ (UI display update)
Status Message Display
```

---

## Signal Reference

### Core Telemetry Signals
```python
# Raw telemetry from TelemetryManager
telemetry_update = Signal(dict)

# Specific model update signals
vehicle_attitude_updated = Signal(dict)   # roll, pitch, yaw, heading
vehicle_position_updated = Signal(dict)   # lat, lon, altitude, speeds
vehicle_gps_updated = Signal(dict)        # fix_type, satellites
vehicle_status_updated = Signal(dict)     # battery, arming, mode
```

### Connection Management Signals
```python
# User-initiated connection requests
connection_request = Signal(str, int)     # conn_string, baud_rate
disconnect_request = Signal()

# System status updates
connection_status_changed = Signal(str, str, str)  # status, message, conn_string
connection_model_changed = Signal(dict)   # complete connection state
```

### Status System Signals
```python
# System and user messages
status_text_received = Signal(str, int)   # text, severity
status_model_new_message = Signal(dict)   # formatted message data
```

---

## Component Interaction Patterns

### Model Update Pattern
```python
# In VehicleController
def handle_raw_telemetry_update(self, raw_data):
    # Parse raw MAVLink data
    parsed_data = self.parse_message(raw_data)
    
    # Update appropriate model
    self.model.update_attitude(parsed_data)
    # Model automatically emits vehicle_attitude_updated signal

# In VehicleModel  
def update_attitude(self, data):
    self.attitude.update(data)
    if self.signal_manager:
        self.signal_manager.vehicle_attitude_updated.emit(self.attitude.copy())

# In TelemetryView
def update_attitude_display(self, attitude_data):
    if 'roll' in attitude_data:
        self.roll_label.setText(f"{attitude_data['roll']:.1f} deg")
```

### Signal Connection Pattern
```python
# In View __init__
def connect_signals(self):
    if self.signal_manager:
        self.signal_manager.vehicle_attitude_updated.connect(self.update_attitude_display)
        self.signal_manager.vehicle_position_updated.connect(self.update_position_display)
```

### Thread Safety Pattern
```python
# All UI updates automatically thread-safe via Qt signals
# TelemetryManager runs in separate thread
# All signal emissions automatically queued to main thread
# No direct cross-thread UI calls needed
```

---

## Architecture Principles

### 1. Loose Coupling
- **No Direct References**: Components never directly reference each other
- **Signal-Only Communication**: All interaction through SignalManager
- **Interface-Based Design**: Components depend on signals, not implementations

### 2. Single Responsibility
- **Models**: Data storage and business rules only
- **Views**: UI presentation and user interaction only  
- **Controllers**: Business logic and data transformation only
- **SignalManager**: Communication routing only

### 3. Thread Safety
- **Qt Signal System**: Automatic thread-safe communication
- **Main Thread UI**: All UI updates on main thread via signals
- **Worker Threads**: Background processing (telemetry) in separate threads
- **Data Isolation**: Models accessed only through signal interface

### 4. Testability
- **Mockable Components**: All dependencies injectable
- **Signal Testing**: Can test signal emissions and receptions
- **Isolated Testing**: Each component testable in isolation
- **Integration Testing**: Full signal flow testable

---

## Development Guidelines

### Adding New Features
1. **Identify Layer**: Determine if feature belongs in Model, View, or Controller
2. **Define Signals**: Add any new signals to SignalManager
3. **Follow Patterns**: Use existing base classes and patterns
4. **Update Documentation**: Add to [IMPLEMENTED_FEATURES.md](IMPLEMENTED_FEATURES.md)

### Signal Design
- **Specific Signals**: Use typed, specific signals rather than generic ones
- **Data Copying**: Always emit copies of data to prevent threading issues
- **Naming Convention**: Use descriptive names (e.g., `vehicle_attitude_updated`)
- **Documentation**: Document signal data structure and usage

### Testing Strategy
- **Unit Tests**: Test each component in isolation with mock signals
- **Integration Tests**: Test signal flow between components
- **UI Tests**: Test view updates with mock data
- **End-to-End Tests**: Test complete data flow with real or simulated data

---

## Current Development Focus

### Immediate Priorities (Phase 1b)
1. **Signal Flow Verification** - Confirm telemetry reaches UI
2. **Integration Testing** - Test with real MAVLink sources  
3. **UI Completion** - Fix missing GPS labels and components
4. **Error Handling** - Robust error recovery and user feedback

### Quality Assurance
- **Logging**: Add comprehensive debug logging to verify signal flow
- **Testing**: Create test suite for MVC components
- **Documentation**: Keep architecture docs updated with changes
- **Code Review**: Ensure all changes follow MVC patterns

---

## Extension Points

### Adding New Telemetry Types
1. Add parsing logic to `VehicleController.handle_raw_telemetry_update()`
2. Add storage to appropriate model (VehicleModel, new model)
3. Add signal definition to SignalManager
4. Create view component to display data
5. Connect signals in view's `connect_signals()` method

### Adding New Views
1. Inherit from `BaseView`
2. Implement `setup_ui()` and `connect_signals()` methods
3. Connect to appropriate model signals
4. Add to MainView layout if needed

### Adding New Controllers
1. Inherit from `BaseController`
2. Implement business logic methods
3. Connect to appropriate signals in `connect_signals()`
4. Update models based on processed data

---

## Notes for AI Coding Tools

### Current Status Understanding
- **Architecture**: Complete and well-structured ✅
- **Implementation**: Most components working ✅  
- **Integration**: Under verification 🔄
- **Testing**: Needs development 📋

### Development Strategy
1. **Start with**: [ACTION_ITEMS.md](ACTION_ITEMS.md) for current tasks
2. **Check for Issues**: [CURRENT_ISSUES.md](CURRENT_ISSUES.md) before coding
3. **Follow Patterns**: Use established MVC patterns consistently
4. **Test Changes**: Verify signal flow after modifications
5. **Update Docs**: Keep feature tracking current

### Best Practices
- Always use SignalManager for component communication
- Follow Qt signal/slot patterns for thread safety
- Add logging for debugging signal flow issues
- Test UI updates with mock data when possible
- Maintain clear separation between MVC layers

---

*This architecture provides a solid foundation for a professional Ground Control Station. The current focus is completing the integration phase to ensure all components work together seamlessly.*
