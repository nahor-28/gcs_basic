# GCS_BASIC MVC Architecture Reference

## Overview

This project implements a robust Model-View-Controller (MVC) architecture for a Ground Control Station (GCS) application. It is designed for modularity, testability, and extensibility, leveraging PySide6 for the GUI and a central `SignalManager` for all inter-component communication.

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
```

---

## Components

### 1. Models

- **VehicleModel:**  
  Manages vehicle telemetry data. Receives updates from controllers and emits signals when data changes.

- **ConnectionModel:**  
  Handles connection parameters and state (connected/disconnected).

- **StatusModel:**  
  Tracks and emits application/system status messages.

### 2. Views

- **MainView:**  
  Integrates all sub-views and acts as the primary window.

- **HeaderView:**  
  UI for connection controls (connect/disconnect, input fields).

- **TelemetryView:**  
  Displays telemetry data (attitude, position, battery, speed, etc.).  
  *Note:* Handles both raw and structured data formats for compatibility.

- **MapView:**  
  Shows the vehicle’s position. Handles both raw and structured data formats.

- **StatusView:**  
  Displays status messages to the user.

### 3. Controllers

- **VehicleController:**  
  Manages vehicle operations, mediates between VehicleModel and other components.

- **ConnectionController:**  
  Handles connection logic and user actions.

- **StatusController:**  
  Manages status messages and their flow.

### 4. SignalManager

Acts as the central event bus, implemented using PySide6 signals and slots.  
All communication between models, views, and controllers is routed through the SignalManager, ensuring loose coupling and modularity.

---

## Data Flow

- **Telemetry:**  
  `TelemetryManager` emits telemetry data via `SignalManager.telemetry_update`.  
  Views (e.g., `TelemetryView`, `MapView`) listen for this signal and update their displays accordingly.

- **Connection:**  
  User actions in `HeaderView` trigger signals to `ConnectionController`, which updates `ConnectionModel` and emits state changes.

- **Status:**  
  System or user events trigger status updates, routed through `StatusModel` and displayed in `StatusView`.

---

## Best Practices

- **No Direct Cross-Talk:**  
  Models, views, and controllers never communicate directly; always use signals via `SignalManager`.

- **Recursion Guard:**  
  To prevent infinite loops, model update methods accept a `from_signal` parameter to distinguish between internal and signal-driven updates.

- **Data Format Compatibility:**  
  Views are designed to handle both the raw telemetry format (from live data) and structured format (from test scripts).

- **Extensibility:**  
  New telemetry types, UI features, or controllers can be added with minimal changes to existing code, thanks to the modular design.

---

## Example: Telemetry Signal Flow

1. `TelemetryManager` receives MAVLink data and emits:
   ```python
   self.signal_manager.telemetry_update.emit({
       "type": "ATTITUDE",
       "roll": ...,
       "pitch": ...,
       "yaw": ...
   })
   ```
2. `TelemetryView` receives the signal and updates UI elements:
   ```python
   def update_view(self, data):
       if data.get('type') == 'ATTITUDE':
           self.roll_label.setText(f"{data['roll']:.1f} deg")
   ```
3. The UI is updated in real time, reflecting the latest telemetry.

---

## Testing

- Use the provided test script (`test_telemetry.py`) to simulate telemetry data and verify that views update correctly.
- Both live and simulated data are supported, thanks to flexible data handling in the views.

---

## Summary

This codebase exemplifies a clean, maintainable MVC architecture for real-time telemetry applications.  
All components are decoupled and communicate through a central signal bus, ensuring clarity and ease of future development.

---

**For contributors:**  
- Always connect new features to the SignalManager.
- Maintain separation between models, views, and controllers.
- Follow the established data flow and signal connection patterns.

---

*This document is generated and maintained by GenAI tools for clarity, onboarding, and code navigation. For further questions, consult the codebase or reach out to the maintainers.*
