# Action Items

## Overview
This document contains prioritized, actionable tasks for the GCS Basic project. Each item is specific, measurable, and can be completed independently. This serves as a task queue for AI coding tools and developers.

**Last Updated**: December 2024  
**Next Review**: After each completed item  
**Current Sprint Focus**: Signal Flow Verification and Fixes

---

## 🔴 CRITICAL - Do First

### 1. Add Signal Flow Debug Logging
**Priority**: CRITICAL  
**Effort**: 1-2 hours  
**Dependencies**: None

#### Task Description
Add comprehensive logging to verify the signal flow chain works correctly.

#### Specific Actions
1. **VehicleController Logging**
   - Add debug prints in `handle_raw_telemetry_update()`
   - Log message type and parsed data
   - Log when model update methods are called

2. **VehicleModel Logging**  
   - Add debug prints in all `update_*()` methods
   - Log when signals are emitted
   - Log the data being emitted

3. **TelemetryView Logging**
   - Add debug prints in all `update_*_display()` methods
   - Log when signals are received
   - Log UI element updates

#### Files to Modify
- `controllers/vehicle_controller.py`
- `models/vehicle_model.py`  
- `views/layouts/telemetry_view.py`

#### Success Criteria
- Console shows clear signal flow when telemetry is received
- Can identify exactly where signal chain breaks (if it does)

---

### 2. Fix TelemetryView GPS Label Issues
**Priority**: CRITICAL  
**Effort**: 30 minutes  
**Dependencies**: None

#### Task Description
Fix missing GPS UI labels that cause errors in `update_gps_display()`.

#### Specific Actions
1. **Add Missing Labels**
   - Add `gps_fix_label` and `gps_sats_label` to `_create_position_group()`
   - Update grid layout to include GPS status information

2. **Fix Method Calls**
   - Review `update_gps_display()` method 
   - Ensure all referenced labels exist
   - Add proper error handling for missing attributes

#### Files to Modify
- `views/layouts/telemetry_view.py`

#### Success Criteria
- No AttributeError exceptions when GPS data is received
- GPS information displays correctly in UI

---

### 3. Create Simple Connection Test
**Priority**: CRITICAL  
**Effort**: 1 hour  
**Dependencies**: Debug logging completed

#### Task Description
Create a minimal test to verify the application can connect and receive data.

#### Specific Actions
1. **Test Script Creation**
   - Create `test_connection.py` script
   - Test UDP connection to localhost:14550
   - Verify signal flow with mock or SITL data

2. **Manual Verification**
   - Run application with SITL if available
   - Test with MAVProxy or other MAVLink source
   - Document expected vs actual behavior

#### Files to Create
- `tests/manual_connection_test.py`

#### Success Criteria
- Can confirm whether signal flow works end-to-end
- Clear documentation of what works and what doesn't

---

## 🟡 HIGH PRIORITY - Do Next

### 4. Fix Signal Connections (If Broken)
**Priority**: HIGH  
**Effort**: 2-4 hours  
**Dependencies**: Debug logging, connection test

#### Task Description
Fix any broken signal connections identified by the debug logging.

#### Specific Actions
1. **Identify Gaps**
   - Review debug output from logging
   - Find where signals are emitted but not received
   - Check signal connection syntax

2. **Fix Connections**
   - Ensure `connect_signals()` methods are called
   - Verify signal names match between emit and connect
   - Fix any threading issues

#### Files to Modify
- Any files with broken signal connections (TBD based on testing)

#### Success Criteria
- Telemetry data flows from TelemetryManager to UI
- All views update when data is received

---

### 5. Implement Mock Telemetry Test
**Priority**: HIGH  
**Effort**: 2 hours  
**Dependencies**: None

#### Task Description
Create a test that sends mock telemetry data to verify UI updates without requiring external MAVLink source.

#### Specific Actions
1. **Mock Data Generator**
   - Create realistic ATTITUDE, GPS, BATTERY test data
   - Emit data through SignalManager
   - Verify UI updates correctly

2. **Automated Test**
   - Create automated test script
   - Test all telemetry message types
   - Verify each UI element updates

#### Files to Create
- `tests/test_mock_telemetry.py`
- `tests/utils/mock_data_generator.py`

#### Success Criteria
- Can test UI updates without external dependencies
- All telemetry displays work with test data

---

### 6. Re-implement Basic Arm/Disarm UI
**Priority**: HIGH  
**Effort**: 2-3 hours  
**Dependencies**: Signal flow working

#### Task Description
Add basic arm/disarm buttons back to the UI and wire them to the controller.

#### Specific Actions
1. **UI Elements**
   - Add arm/disarm buttons to appropriate view
   - Add current arming status display
   - Style buttons appropriately

2. **Signal Wiring**
   - Connect buttons to controller methods
   - Update UI when arming status changes
   - Add proper error handling

#### Files to Modify
- `views/layouts/header_view.py` or create new control view
- `controllers/vehicle_controller.py`
- `core/signal_manager.py` (add arm/disarm signals)

#### Success Criteria
- Buttons appear in UI and respond to clicks
- Arming status updates when vehicle state changes

---

## 🟡 MEDIUM PRIORITY - Do Later

### 7. Enhance Map View with Basic Functionality
**Priority**: MEDIUM  
**Effort**: 4-6 hours  
**Dependencies**: Position telemetry working

#### Task Description
Replace map placeholder with basic working map display.

#### Specific Actions
1. **Map Integration**
   - Research Qt mapping options (QWebEngine, folium, etc.)
   - Implement basic map with vehicle position marker
   - Add zoom and pan controls

2. **Position Updates**
   - Connect to vehicle position updates
   - Update vehicle marker in real-time
   - Add trail/path display option

#### Files to Modify
- `views/layouts/map_view.py`
- `requirements.txt` (may need additional dependencies)

#### Success Criteria
- Map displays with vehicle position
- Position updates in real-time
- Basic map interaction works

---

### 8. Add Comprehensive Integration Tests
**Priority**: MEDIUM  
**Effort**: 4-8 hours  
**Dependencies**: Mock telemetry working

#### Task Description
Create comprehensive test suite for the MVC architecture.

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

### 9. Improve Status Message System
**Priority**: MEDIUM  
**Effort**: 2-3 hours  
**Dependencies**: Basic functionality working

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

### 10. Add Dark Theme Support
**Priority**: LOW  
**Effort**: 2-4 hours

#### Task Description
Implement dark theme option for the application.

#### Files to Modify
- All view files
- Add theme manager utility

---

### 11. Implement Keyboard Shortcuts
**Priority**: LOW  
**Effort**: 2-3 hours

#### Task Description
Add keyboard shortcuts for common actions.

#### Files to Modify
- `views/main_view.py`
- Add shortcut configuration

---

### 12. Add Tooltips and Help System
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