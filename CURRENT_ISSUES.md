# Current Issues

## Overview
This document tracks active issues, bugs, and integration problems in the GCS Basic project. This serves as a reference for AI coding tools and developers to understand what needs immediate attention.

**Last Updated**: December 2024  
**Priority**: Address before adding new features  
**Status**: Ready for debugging and fixes

---

## 🔴 Critical Issues

### Signal Flow Integration
**Status**: Suspected but not confirmed  
**Impact**: High - Core functionality may not work

#### Problem Description
The MVC architecture is structurally complete, but the signal routing chain may have gaps:
```
TelemetryManager → VehicleController → VehicleModel → Views
```

#### Specific Concerns
- **VehicleController**: Raw telemetry parsing appears correct, but model updates may not trigger
- **Model Signals**: VehicleModel emits signals, but views may not receive them consistently
- **View Updates**: TelemetryView has signal connections, but display updates unverified

#### Debug Actions Needed
1. Add logging to `VehicleController.handle_raw_telemetry_update()`
2. Add logging to `VehicleModel.update_*()` methods  
3. Add logging to `TelemetryView.update_*()` methods
4. Test with live MAVLink data source

---

## 🟡 High Priority Issues

### Missing Signal Connections
**Status**: Architecture review needed  
**Impact**: Medium - Some features may not work

#### TelemetryView Signal Issues
- GPS-related labels (`gps_fix_label`, `gps_sats_label`) referenced but not created in UI setup
- `update_gps_display()` method tries to update non-existent labels
- Method signature mismatch in some update functions

#### MapView Integration
- Map view exists but actual map rendering unverified
- Position update integration with vehicle tracking not tested
- WebEngine dependency may need configuration

### Test Coverage Gaps
**Status**: Development needed  
**Impact**: Medium - Hard to verify fixes

#### Missing Integration Tests
- No end-to-end signal flow tests
- No UI update verification tests  
- No live telemetry connection tests
- Mock data tests incomplete

#### Testing Infrastructure
- Test files exist but appear incomplete
- No automated test runner configuration
- No continuous integration setup

---

## 🟡 Medium Priority Issues

### Feature Completeness
**Status**: Temporarily removed during refactoring  
**Impact**: Medium - Missing expected functionality

#### Temporarily Disabled Features
- **Arm/Disarm Controls**: Controller methods exist but not wired to UI
- **Mode Changes**: Framework exists but not implemented
- **RC Channel Display**: Removed during MVC refactor
- **Vehicle Commands**: Signal definitions exist but not implemented

#### Map Functionality
- Basic MapView placeholder exists
- No actual map tiles or rendering
- Vehicle position markers not implemented
- No map interaction controls

### UI Polish Issues
**Status**: Functional but could be improved  
**Impact**: Low - Usability concerns

#### Visual Design
- Basic styling applied but could be enhanced
- No dark theme option
- Limited customization options
- Status messages need better formatting

#### User Experience
- No tooltips or help text
- Error messages could be more user-friendly
- No progress indicators for connection attempts
- No keyboard shortcuts

---

## 🟢 Low Priority Issues

### Code Quality
**Status**: Architecture is good, minor improvements possible  
**Impact**: Low - Maintenance and future development

#### Documentation
- Some inline comments could be expanded
- API documentation could be more comprehensive
- Type hints could be more specific in some places

#### Error Handling
- Most error cases handled, but some edge cases missed
- Error messages could be more specific
- Recovery mechanisms could be enhanced

### Performance Considerations
**Status**: Not critical for current scale  
**Impact**: Low - Future optimization

#### Telemetry Processing
- Message filtering is efficient but could be optimized
- Memory usage monitoring not implemented
- Update rate optimization could be improved

---

## Known Workarounds

### TelemetryView GPS Labels
**Issue**: Missing GPS UI elements  
**Workaround**: Remove GPS-specific update calls until UI elements are added

### Map Display
**Issue**: No actual map rendering  
**Workaround**: Use placeholder text until map integration is complete

### Command Functions
**Issue**: Arm/disarm not wired  
**Workaround**: Use external GCS for vehicle control during testing

---

## Debug Strategies

### Signal Flow Debugging
1. **Add Logging**: Insert print statements or logging calls at each signal emission and reception point
2. **Signal Viewer**: Use Qt's signal debugging tools if available
3. **Step-by-Step**: Test each component in isolation before integration

### Connection Testing
1. **SITL Testing**: Use ArduPilot SITL for consistent test environment
2. **UDP Loopback**: Test with known working MAVLink stream
3. **Serial Simulation**: Use virtual serial ports for testing

### UI Verification
1. **Mock Data**: Create test data to verify UI updates work
2. **Manual Updates**: Call view update methods directly to test UI
3. **Widget Inspector**: Use Qt widget debugging tools

---

## Issue Resolution Process

### For AI Coding Tools
1. **Identify**: Choose one issue from this document
2. **Investigate**: Add logging/debugging to understand the problem
3. **Fix**: Implement minimal fix for the specific issue
4. **Test**: Verify fix works with simple test case
5. **Update**: Mark issue as resolved and update this document

### Priority Order
1. Critical signal flow issues first
2. Missing UI elements that cause errors
3. Feature completeness for basic functionality
4. UI polish and user experience
5. Performance and optimization

---

## Notes for Development

### Most Likely Root Cause
Based on code analysis, the most probable issue is incomplete signal connections between VehicleModel and Views. The architecture is sound, but some signals may not be properly connected.

### Quick Verification Test
1. Run the application
2. Attempt to connect to a MAVLink source (SITL or simulator)
3. Check if telemetry data appears in the TelemetryView
4. Verify connection status updates in HeaderView

### Expected Behavior
When working correctly:
- Connection status should change from DISCONNECTED → CONNECTING → CONNECTED
- Telemetry labels should update with live data
- Status messages should appear in StatusView
- No console errors or exceptions 