from PySide6.QtCore import QObject

class VehicleModel(QObject):
    """Model for vehicle state and telemetry data."""
    
    def __init__(self, signal_manager):
        super().__init__()
        self.signal_manager = signal_manager
        self.data = {
            # 'armed': False,  # Commented out as we're not implementing arm/disarm
            'mode': 'UNKNOWN',
            'position': {'lat': 0, 'lon': 0, 'alt': 0},
            'attitude': {'roll': 0, 'pitch': 0, 'yaw': 0},
            'battery': {'voltage': 0, 'current': 0, 'remaining': 0},
            'gps': {'fix_type': 0, 'satellites': 0},
            'speed': {'air': 0, 'ground': 0},
            'heading': 0,
            'throttle': 0,
            'climb_rate': 0
        }
        
        # Connect to signal manager
        if signal_manager:
            signal_manager.telemetry_update.connect(self.update_telemetry)
            
    def update_telemetry(self, data):
        """Update vehicle data based on telemetry message."""
        msg_type = data.get('type')
        
        if msg_type == 'HEARTBEAT':
            # self.data['armed'] = data.get('armed', False)  # Commented out as we're not implementing arm/disarm
            self.data['mode'] = data.get('mode', 'UNKNOWN')
            
        elif msg_type == 'GLOBAL_POSITION_INT':
            self.data['position'] = {
                'lat': data.get('lat', 0),
                'lon': data.get('lon', 0),
                'alt': data.get('alt_msl', 0)
            }
            
        elif msg_type == 'ATTITUDE':
            self.data['attitude'] = {
                'roll': data.get('roll', 0),
                'pitch': data.get('pitch', 0),
                'yaw': data.get('yaw', 0)
            }
            
        elif msg_type == 'SYS_STATUS':
            self.data['battery'] = {
                'voltage': data.get('battery_voltage', 0),
                'current': data.get('battery_current', 0),
                'remaining': data.get('battery_remaining', 0)
            }
            
        elif msg_type == 'GPS_RAW_INT':
            self.data['gps'] = {
                'fix_type': data.get('gps_fix_type', 0),
                'satellites': data.get('gps_satellites', 0)
            }
            
        elif msg_type == 'VFR_HUD':
            self.data['speed'] = {
                'air': data.get('airspeed', 0),
                'ground': data.get('groundspeed', 0)
            }
            self.data['heading'] = data.get('heading', 0)
            self.data['throttle'] = data.get('throttle', 0)
            self.data['climb_rate'] = data.get('climb_rate', 0) 