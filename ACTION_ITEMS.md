# Action Items

## Overview
This document contains prioritized, actionable tasks for the GCS Basic project. Each item is specific, measurable, and can be completed independently. This serves as a task queue for AI coding tools and developers.

**Last Updated**: May 2025  
**Next Review**: After each completed item  
**Current Sprint Focus**: Feature Development and Implementation

**🎉 MAJOR MILESTONE ACHIEVED**: Complete signal flow verified with live data - system is production-ready!

---

## ✅ COMPLETED - MOVED TO CHANGELOG.md

All completed items have been moved to [CHANGELOG.md](CHANGELOG.md) for historical tracking:
- ✅ Signal Flow Debug Infrastructure (May 2025)
- ✅ TelemetryView GPS Label Fixes (May 2025)  
- ✅ Complete Connection Test Infrastructure (May 2025)
- ✅ Complete Signal Flow with Live Data Verification (May 2025)
- ✅ All Signal Integration Issues Resolution (May 2025)

**Result**: Production-ready signal flow architecture verified with external SITL connection.

---

## 🔴 CRITICAL - Do Next

### 1. Re-implement Basic Arm/Disarm UI ⭐ TOP PRIORITY
**Priority**: CRITICAL  
**Effort**: 2-3 hours  
**Dependencies**: Signal flow working ✅

#### Task Description
Add basic arm/disarm buttons back to the UI and wire them to the controller. With the signal flow now verified working, this can be implemented confidently.

#### Specific Actions
1. **UI Elements**
   - Add arm/disarm buttons to appropriate view (likely HeaderView)
   - Add current arming status display with visual indicators
   - Style buttons appropriately with clear visual feedback

2. **Signal Wiring**
   - Connect buttons to controller methods via SignalManager
   - Update UI when arming status changes from vehicle
   - Add proper error handling and user feedback

3. **Controller Integration**
   - Implement arm/disarm command generation in VehicleController
   - Add arming status tracking in VehicleModel
   - Ensure commands are sent through verified telemetry system

#### Files to Modify
- `views/layouts/header_view.py` - Add arm/disarm UI elements
- `controllers/vehicle_controller.py` - Add arm/disarm command methods
- `models/vehicle_model.py` - Add arming status tracking
- `core/signal_manager.py` - Add arm/disarm signals

#### Success Criteria
- Buttons appear in UI and respond to clicks
- Arming status updates when vehicle state changes
- Commands successfully sent to vehicle via verified signal chain

---

### 2. Add Flight Mode Display and Control
**Priority**: HIGH  
**Effort**: 3-4 hours  
**Dependencies**: Signal flow working ✅

#### Task Description
Implement flight mode display and change functionality now that the communication system is proven working.

#### Specific Actions
1. **Mode Display**
   - Add current flight mode display to telemetry view
   - Parse HEARTBEAT messages for mode information
   - Format mode names user-friendly

2. **Mode Change UI**
   - Add mode selection dropdown or buttons
   - List available modes for vehicle type
   - Add confirmation for mode changes

3. **Integration**
   - Wire mode changes through verified signal system
   - Update display when mode changes from vehicle or GCS
   - Add error handling for invalid mode changes

#### Files to Modify
- `views/layouts/telemetry_view.py` - Add mode display
- `views/layouts/header_view.py` - Add mode change controls
- `controllers/vehicle_controller.py` - Add mode change commands
- `models/vehicle_model.py` - Add mode tracking

#### Success Criteria
- Current flight mode displays correctly
- Mode changes work through UI
- Mode updates from vehicle reflected in UI

---

## 🟡 HIGH PRIORITY - Do Next

### 3. Implement Mock Telemetry Test
**Priority**: HIGH  
**Effort**: 2 hours  
**Dependencies**: None

#### Task Description
Create a test that sends mock telemetry data to verify UI updates without requiring external MAVLink source. This will be useful for development and testing.

#### Specific Actions
1. **Mock Data Generator**
   - Create realistic ATTITUDE, GPS, BATTERY test data
   - Emit data through SignalManager to test complete signal chain
   - Verify UI updates correctly with test data

2. **Automated Test**
   - Create automated test script for development use
   - Test all telemetry message types systematically
   - Verify each UI element updates with mock data

#### Files to Create
- `tests/test_mock_telemetry.py`
- `tests/utils/mock_data_generator.py`

#### Success Criteria
- Can test UI updates without external dependencies
- All telemetry displays work with test data
- Useful for development without SITL setup

---

### 4. Enhance Map View with Basic Functionality
**Priority**: MEDIUM  
**Effort**: 4-6 hours  
**Dependencies**: Position telemetry working ✅

#### Task Description
Replace map placeholder with basic working map display now that position data flow is verified.

#### Specific Actions
1. **Map Integration**
   - Research Qt mapping options (QWebEngine, folium, etc.)
   - Implement basic map with vehicle position marker
   - Add zoom and pan controls

2. **Position Updates**
   - Connect to vehicle position updates via verified signal system
   - Update vehicle marker in real-time
   - Add trail/path display option

#### Files to Modify
- `views/layouts/map_view.py`
- `requirements.txt` (may need additional dependencies)

#### Success Criteria
- Map displays with vehicle position
- Position updates in real-time via signal system
- Basic map interaction works

---

## 🟡 MEDIUM PRIORITY - Do Later

### 5. Add Comprehensive Integration Tests
**Priority**: MEDIUM  
**Effort**: 4-8 hours  
**Dependencies**: Mock telemetry working

#### Task Description
Create comprehensive test suite for the MVC architecture, building on the proven signal flow.

#### Specific Actions
1. **Model Tests**
   - Test all model update methods
   - Verify signal emissions
   - Test data validation

2. **Controller Tests**
   - Test telemetry parsing
   - Test command generation
   - Test error handling

3. **View Tests**
   - Test UI updates
   - Test user interactions
   - Test signal connections

#### Files to Create
- `tests/integration/test_mvc_flow.py`
- `tests/models/test_vehicle_model.py`
- `tests/controllers/test_vehicle_controller.py`
- `tests/views/test_telemetry_view.py`

#### Success Criteria
- >80% code coverage for core functionality
- All tests pass consistently
- CI/CD pipeline can be implemented

---

### 6. Improve Status Message System
**Priority**: MEDIUM  
**Effort**: 2-3 hours  
**Dependencies**: Basic functionality working ✅

#### Task Description
Enhance the status message display and handling.

#### Specific Actions
1. **Message Formatting**
   - Add timestamps to status messages
   - Color-code by severity level
   - Add message filtering options

2. **Message Management**
   - Implement message history
   - Add clear/export functionality
   - Limit message buffer size

#### Files to Modify
- `models/status_model.py`
- `views/layouts/status_view.py`

#### Success Criteria
- Status messages are clearly formatted
- Message history is manageable
- Important messages are highlighted

---

## 🟢 LOW PRIORITY - Future Enhancement

### 7. Add Dark Theme Support
**Priority**: LOW  
**Effort**: 2-4 hours

#### Task Description
Implement dark theme option for the application.

#### Files to Modify
- All view files
- Add theme manager utility

---

### 8. Implement Keyboard Shortcuts
**Priority**: LOW  
**Effort**: 2-3 hours

#### Task Description
Add keyboard shortcuts for common actions.

#### Files to Modify
- `views/main_view.py`
- Add shortcut configuration

---

### 9. Add Tooltips and Help System
**Priority**: LOW  
**Effort**: 3-4 hours

#### Task Description
Add contextual help and tooltips throughout the interface.

#### Files to Modify
- All view files
- Add help documentation

---

## Completion Process

### For Each Action Item
1. **Review**: Read the task description and dependencies
2. **Plan**: Understand the specific actions required
3. **Implement**: Make the necessary code changes
4. **Test**: Verify the changes work as expected
5. **Update**: Mark the item as complete and update related documents

### Moving Items
- ✅ **Completed**: Move to IMPLEMENTED_FEATURES.md
- ❌ **Blocked**: Move to CURRENT_ISSUES.md with details
- 📈 **Priority Change**: Update priority level and rationale

### Documentation Updates
After completing each item, update:
- IMPLEMENTED_FEATURES.md (add new functionality)
- CURRENT_ISSUES.md (remove resolved issues)
- CHANGELOG.md (record changes)

---

## Notes for AI Coding Tools

### Task Selection Strategy
1. Always start with CRITICAL items
2. Complete dependencies before dependent tasks
3. Choose tasks matching available time/complexity budget
4. Focus on one complete task rather than partial work on multiple

### Quality Standards
- All code changes should include appropriate logging
- Test any UI changes manually if possible
- Follow existing code style and patterns
- Update documentation for significant changes

### Risk Management
- Test changes with simple cases first
- Keep backup of working code before major changes
- Add error handling for new functionality
- Verify changes don't break existing features 