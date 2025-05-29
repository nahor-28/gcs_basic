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
- ✅ Arm & Takeoff Feature Implementation (May 2025)
- ✅ Arm & Takeoff Feature Bug Fixes and ArduCopter SITL Compatibility (May 2025)

**Result**: Production-ready signal flow architecture verified with external SITL connection, plus comprehensive Arm & Takeoff functionality with safety validation, confirmed working with live ArduCopter SITL testing.

---

## 🔴 CRITICAL - Do Next

### 1. Add Flight Mode Display and Control ⭐ TOP PRIORITY
**Priority**: CRITICAL  
**Effort**: 2-3 hours  
**Dependencies**: Signal flow working ✅, Basic vehicle status display ✅, Arm & Takeoff working ✅

#### Task Description
Implement flight mode change functionality now that the communication system is proven working and vehicle control features are implemented and tested.

#### Specific Actions
1. **Mode Change UI**
   - Add mode selection dropdown or buttons to HeaderView
   - List available modes for vehicle type (ArduCopter modes)
   - Add confirmation for mode changes if needed

2. **Integration**
   - Wire mode changes through verified signal system
   - Update display when mode changes from vehicle or GCS
   - Add error handling for invalid mode changes
   - Use existing MAVLink command infrastructure from arm & takeoff feature

#### Files to Modify
- `views/layouts/header_view.py` - Add mode change controls
- `controllers/vehicle_controller.py` - Add mode change commands (similar to arm & takeoff)
- `core/telemetry_manager.py` - Use existing send_command_long method for mode changes
- `core/signal_manager.py` - Add mode change signals (similar to arm_takeoff_request)

#### Success Criteria
- Mode changes work through UI using verified signal architecture
- Mode updates from vehicle reflected in UI (already working)
- Safety validation for mode changes integrated with existing safety system

---

### 2. Add Basic Disarm Functionality ⭐ HIGH PRIORITY
**Priority**: HIGH  
**Effort**: 1-2 hours  
**Dependencies**: Arm & Takeoff working ✅, Signal flow working ✅

#### Task Description
Add disarm button functionality to complement the working arm & takeoff feature. This uses the same proven communication infrastructure.

#### Specific Actions
1. **UI Enhancement**
   - Update HeaderView ARM & TAKEOFF button to show DISARM when armed
   - Add confirmation dialog for disarm action
   - Update button styling for disarm state

2. **Signal Integration**
   - Add disarm signal to SignalManager
   - Use existing telemetry_manager.send_command_long() method
   - Connect to existing vehicle status monitoring

#### Files to Modify
- `views/layouts/header_view.py` - Update button behavior for disarm
- `controllers/vehicle_controller.py` - Add disarm command method
- `core/signal_manager.py` - Add disarm signal
- `core/telemetry_manager.py` - Add disarm command handler

#### Success Criteria
- Disarm button appears when vehicle is armed
- Disarm command successfully sent using proven infrastructure
- UI updates correctly when vehicle disarms

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