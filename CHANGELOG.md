# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Light theme support with Fusion style
- Improved map integration with offline fallback
- Parameter panel with real-time monitoring
- Enhanced header layout with better spacing and styling
- Status message system with severity levels
- Automatic port detection for serial connections

### Changed
- Migrated from event bus to Qt signal/slot mechanism
- Improved UI responsiveness and layout
- Enhanced error handling in connection management
- Updated map tile loading with fallback options
- Refactored code structure for better maintainability

### Fixed
- Map loading issues with Leaflet integration
- Connection status display inconsistencies
- UI theme inconsistencies across platforms
- Memory leaks in telemetry updates
- Thread safety issues in UI updates

## [Planned]

### Core Functionality
- [ ] Implement arm/disarm functionality
- [ ] Add waypoint mission planning
- [ ] Support multiple vehicle connections
- [ ] Implement data logging system
- [ ] Add geofencing support

### User Interface
- [ ] Add customizable dashboard layouts
- [ ] Implement dark theme option
- [ ] Add advanced telemetry visualization
- [ ] Create mission planning interface
- [ ] Add vehicle configuration wizard

### Performance
- [ ] Optimize telemetry data processing
- [ ] Implement data compression
- [ ] Add configurable update rates
- [ ] Improve map rendering performance
- [ ] Add telemetry data caching

### Code Quality
- [ ] Expand unit test coverage
- [ ] Add integration tests
- [ ] Implement CI/CD pipeline
- [ ] Add comprehensive API documentation
- [ ] Improve error handling and recovery

### Known Issues to Address
- Limited error recovery for connection drops
- Basic UI customization options
- No data persistence for telemetry logs
- Map performance with high update rates
- Memory usage optimization needed

## [Future Considerations]

### Advanced Features
- Camera control and video streaming
- Advanced mission planning
- Custom script support
- Plugin system
- Cloud integration

### Infrastructure
- Docker containerization
- Automated testing pipeline
- Performance monitoring
- Security enhancements
- Documentation system

### User Experience
- Tutorial system
- Customizable keyboard shortcuts
- Advanced data visualization
- Multi-language support
- Accessibility improvements 