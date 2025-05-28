# core/telemetry_manager.py (Handle Connection Events)

import threading
import time
import math
from pymavlink import mavutil
import sys
import logging 
from PySide6.QtCore import QObject, QThread, Signal, QTimer

# Import the global event bus instance and Events class
# from utils.event_bus import event_bus, Events

class TelemetryThread(QThread):
    """Thread for receiving telemetry data."""
    # Constants for connection monitoring
    HEARTBEAT_TIMEOUT = 5.0  # seconds
    MAX_RECONNECT_ATTEMPTS = 5
    RECONNECT_BACKOFF_BASE = 1.0  # seconds
    
    def __init__(self, master, signal_manager, stop_event):
        super().__init__()
        self.master = master
        self.signal_manager = signal_manager
        self.stop_event = stop_event
        self.last_heartbeat_time = time.time()
        self.reconnect_attempts = 0
        self.desired_message_types = [
            'ATTITUDE', 'GPS_RAW_INT', 'GLOBAL_POSITION_INT', 'SYS_STATUS',
            'RC_CHANNELS', 'VFR_HUD', 'HEARTBEAT', 'STATUSTEXT'
        ]
        
    def run(self):
        """Main thread loop for receiving telemetry."""
        logging.info("Telemetry thread starting.")
        active_connection = True
        
        while not self.stop_event.is_set() and active_connection:
            # Check connection status
            if not self.master or self.master.target_system == 0:
                errmsg = ""
                if not self.master: 
                    errmsg = "Connection object is None."
                else: 
                    errmsg = "Connection lost (target system 0)."
                self.signal_manager.connection_status_changed.emit("DISCONNECTED", errmsg, "")
                active_connection = False
                continue
                
            try:
                # Check for heartbeat timeout
                current_time = time.time()
                if current_time - self.last_heartbeat_time > self.HEARTBEAT_TIMEOUT:
                    errmsg = f"No heartbeat received for {self.HEARTBEAT_TIMEOUT} seconds"
                    self.signal_manager.connection_status_changed.emit("RECONNECTING", errmsg, "")
                    active_connection = False
                    
                    # Instead of emitting the signal, call the parent TelemetryManager
                    # Get a reference to the parent TelemetryManager
                    telemetry_manager = self.parent()
                    if telemetry_manager and hasattr(telemetry_manager, 'attempt_reconnect'):
                        telemetry_manager.attempt_reconnect()
                    continue
                
                # Receive ANY message
                msg = self.master.recv_match(blocking=True, timeout=2.0)
                
                if msg is None: 
                    continue  # Timeout, just loop
                    
                msg_type = msg.get_type()
                
                # Filter AFTER receiving
                if msg_type not in self.desired_message_types:
                    continue  # Skip messages we don't want
                    
                # --- Parse the messages we DO want ---
                data = {"type": msg_type, "timestamp": time.time()}
                publish_event = True
                
                if msg_type == 'HEARTBEAT':
                    self.last_heartbeat_time = time.time()  # Update heartbeat timestamp
                    data['armed'] = bool(msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED)
                    data['mode'] = mavutil.mode_string_v10(msg)
                    data['system_status'] = msg.system_status
                    # If connection was lost, receiving heartbeat means it's back
                    if self.reconnect_attempts > 0:
                        self.reconnect_attempts = 0  # Reset reconnect attempts
                        self.signal_manager.connection_status_changed.emit("CONNECTED", "Reconnected via Heartbeat", "")
                    
                elif msg_type == 'SYS_STATUS':
                    data['battery_voltage'] = msg.voltage_battery / 1000.0
                    data['battery_current'] = msg.current_battery / 100.0 if msg.current_battery != -1 else None
                    data['battery_remaining'] = msg.battery_remaining if msg.battery_remaining != -1 else None
                    
                elif msg_type == 'GPS_RAW_INT':
                    data['gps_fix_type'] = msg.fix_type
                    data['gps_satellites'] = msg.satellites_visible
                    
                elif msg_type == 'GLOBAL_POSITION_INT':
                    data['lat'] = msg.lat / 1e7
                    data['lon'] = msg.lon / 1e7
                    data['alt_msl'] = msg.alt / 1000.0
                    data['alt_agl'] = msg.relative_alt / 1000.0
                    
                elif msg_type == 'VFR_HUD':
                    data['airspeed'] = msg.airspeed
                    data['groundspeed'] = msg.groundspeed
                    data['heading'] = msg.heading
                    data['throttle'] = msg.throttle
                    data['climb_rate'] = msg.climb
                    
                elif msg_type == 'RC_CHANNELS':
                    data['rc_channels'] = [
                        msg.chan1_raw, msg.chan2_raw, msg.chan3_raw, msg.chan4_raw,
                        msg.chan5_raw, msg.chan6_raw, msg.chan7_raw, msg.chan8_raw
                    ]
                    
                elif msg_type == 'ATTITUDE':
                    data['roll'] = math.degrees(msg.roll)
                    data['pitch'] = math.degrees(msg.pitch)
                    data['yaw'] = math.degrees(msg.yaw)
                    
                elif msg_type == 'STATUSTEXT':
                    data['text'] = msg.text.strip()
                    data['severity'] = msg.severity
                    # Publish STATUSTEXT as a separate event
                    self.signal_manager.status_text_received.emit(data['text'], data['severity'])
                    # Don't publish this as a generic TELEMETRY_UPDATE event
                    publish_event = False
                    # Still log important status messages directly
                    if data['severity'] <= mavutil.mavlink.MAV_SEVERITY_ERROR:
                        logging.error(f"MAV STATUS [{data['severity']}]: {data['text']}")
                    else:
                        logging.info(f"MAV STATUS [{data['severity']}]: {data['text']}")
                        
                # --- Publish TELEMETRY_UPDATE event ---
                # Check len > 2 ensures type and timestamp are present plus actual data
                if publish_event and len(data) > 2:
                    logging.debug(f"TelemetryManager: Emitting telemetry_update signal with data: {data}")
                    self.signal_manager.telemetry_update.emit(data)
                    logging.debug(f"TelemetryManager: telemetry_update signal emitted for message type: {msg_type}")
                elif publish_event:
                    logging.warning(f"TelemetryManager: Skipping telemetry_update emission - insufficient data: {data}")
                else:
                    logging.debug(f"TelemetryManager: Skipping telemetry_update emission - publish_event=False for message type: {msg_type}")
                    
            except (ConnectionResetError, BrokenPipeError) as conn_e:
                errmsg = f"{type(conn_e).__name__} in receive loop."
                self.signal_manager.connection_status_changed.emit("ERROR", errmsg, "")
                active_connection = False  # Stop loop
                
            except Exception as e:
                if isinstance(e, mavutil.mavlink.MAVLinkError):
                    logging.warning(f"MAVLink Error in receive loop: {e}. Continuing.")
                else:
                    logging.error(f"Unhandled Exception in receive loop: {type(e).__name__}: {e}", exc_info=True)
                    time.sleep(0.1)  # Prevent fast spinning
                
        logging.info("Telemetry thread finished.")
        if self.master:
            logging.info("Closing connection from receive loop exit.")
            try: 
                self.master.close()
            except Exception as e:
                logging.error(f"Error closing connection: {e}")
                
    def reset_heartbeat(self):
        """Reset the heartbeat timer."""
        self.last_heartbeat_time = time.time()
        
    def increment_reconnect_attempt(self):
        """Increment the reconnect attempt counter and return the backoff time."""
        self.reconnect_attempts += 1
        if self.reconnect_attempts > self.MAX_RECONNECT_ATTEMPTS:
            return -1  # Signal to stop reconnecting
        return self.RECONNECT_BACKOFF_BASE * (2 ** (self.reconnect_attempts - 1))  # Exponential backoff


class TelemetryManager(QObject):
    """Manages the connection to the vehicle and telemetry data."""
    
    def __init__(self, initial_conn_string, initial_baud=115200, signal_manager=None):
        super().__init__()
        self._connection_string = initial_conn_string
        self._baud = initial_baud
        self.master = None
        self.thread = None
        self.stop_event = threading.Event()
        self.signal_manager = signal_manager
        self.current_status = "DISCONNECTED"
        self.reconnect_timer = None
        self._is_connecting = False  # Add flag to prevent multiple connection attempts
        
        # Store desired frequencies using numeric IDs
        self.message_frequencies = {
            mavutil.mavlink.MAVLINK_MSG_ID_ATTITUDE: 100000,
            mavutil.mavlink.MAVLINK_MSG_ID_GPS_RAW_INT: 200000,
            mavutil.mavlink.MAVLINK_MSG_ID_GLOBAL_POSITION_INT: 200000,
            mavutil.mavlink.MAVLINK_MSG_ID_SYS_STATUS: 1000000,
            mavutil.mavlink.MAVLINK_MSG_ID_RC_CHANNELS: 500000,
            mavutil.mavlink.MAVLINK_MSG_ID_VFR_HUD: 200000,
            mavutil.mavlink.MAVLINK_MSG_ID_HEARTBEAT: 1000000,
        }
        
        # Connect to signal manager signals
        if signal_manager:
            signal_manager.connection_request.connect(self.handle_connect_request)
            signal_manager.disconnect_request.connect(self.handle_disconnect_request)
            logging.info("TelemetryManager connected to signal manager.")
            
    def _update_status(self, new_status: str, message: str = ""):
        """Updates internal status and emits a status change signal."""
        print(f"DEBUG: TelemetryManager._update_status: Attempting to set status to '{new_status}' with message '{message}'") 
        # Ensure change if message is different OR status is different
        if new_status != self.current_status or (message and message != getattr(self, 'status_message', '')):
            self.current_status = new_status
            self.status_message = message # Store the message with the status
            logging.info(f"Connection Status: {new_status} - {message}")
            print(f"DEBUG: TelemetryManager._update_status: Emitting connection_status_changed: '{new_status}', '{message}', conn_str: '{self._connection_string}'")
            if self.signal_manager:
                self.signal_manager.connection_status_changed.emit(new_status, message, self._connection_string)
        else:
            print(f"DEBUG: TelemetryManager._update_status: Status '{new_status}' and message '{message}' did not change internal state. Current status: '{self.current_status}', current message: '{getattr(self, 'status_message', '')}'")
                
    def connect(self):
        """Establishes the MAVLink connection using internal connection string/_baud."""
        print(f"DEBUG: TelemetryManager.connect called. self._is_connecting={self._is_connecting}, self.master is None: {self.master is None}")
        if self._is_connecting:
            logging.info("Connection attempt already in progress.")
            return False
            
        if self.master:
            logging.info("Already connected.")
            return True
            
        self._is_connecting = True
        self._update_status("CONNECTING", f"Attempting connection to {self._connection_string}...")
        
        try:
            # Ensure any existing connection is properly closed
            if self.master:
                try:
                    self.master.close()
                except Exception as e:
                    logging.error(f"Error closing existing connection: {e}")
                self.master = None
            
            if self._connection_string.startswith(('udp:', 'tcp:')):
                self.master = mavutil.mavlink_connection(self._connection_string, source_system=255)
            else:
                self.master = mavutil.mavlink_connection(self._connection_string, baud=self._baud, source_system=255)
                
            if not self.master:
                self._update_status("ERROR", "mavutil.mavlink_connection failed")
                self._is_connecting = False
                print("DEBUG: TelemetryManager.connect: mavutil.mavlink_connection failed.")
                return False
                
            self._update_status("CONNECTING", "Waiting for heartbeat...")
            print("DEBUG: TelemetryManager.connect: Waiting for heartbeat...")
            heartbeat = self.master.wait_heartbeat(timeout=5) # Default MAVUtil timeout is 5s, can be increased
            
            if heartbeat:
                print(f"DEBUG: TelemetryManager.connect: Heartbeat received: {heartbeat}")
                self._update_status("CONNECTED", f"Connected to target {self.master.target_system}/{self.master.target_component}")
                self._is_connecting = False
                return True
            else:
                print("DEBUG: TelemetryManager.connect: No heartbeat received within timeout.")
                self._update_status("ERROR", "No heartbeat received within timeout.")
                if self.master: self.master.close()
                self.master = None
                self._is_connecting = False
                return False
                
        except Exception as e:
            print(f"DEBUG: TelemetryManager.connect: Exception occurred: {e}")
            self._update_status("ERROR", f"Connection failed: {e}")
            if self.master: self.master.close()
            self.master = None
            self._is_connecting = False
            return False
            
    def _request_data_streams(self):
        """Sends commands to set message intervals."""
        if not self.master:
            logging.warning("Not connected. Cannot request streams.")
            return
            
        logging.info("Requesting data streams...")
        for msg_id, frequency in self.message_frequencies.items():
            if frequency > 0:
                try:
                    if not hasattr(self.master, 'mav'):
                        logging.error(f"master.mav missing, cannot send command for MSG ID {msg_id}")
                        continue
                        
                    self.master.mav.command_long_send(
                        self.master.target_system,
                        self.master.target_component,
                        mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,
                        0, msg_id, frequency, 0, 0, 0, 0, 0
                    )
                    logging.debug(f"Requested ID {msg_id} at interval {frequency} us")
                    time.sleep(0.05)
                    
                except AttributeError as ae:
                    logging.error(f"AttributeError sending interval command for MSG ID {msg_id}: {ae}. Check mav object.", exc_info=True)
                    break
                except Exception as e:
                    logging.error(f"Error requesting interval for MSG ID {msg_id}: {type(e).__name__}: {e}", exc_info=True)
                    
        logging.info("Data stream requests sent.")
        
    def start(self):
        """Starts the telemetry thread."""
        if self.thread and self.thread.isRunning():
            logging.warning("Telemetry thread already running.")
            return True
            
        if not self.master:
            logging.error("Cannot start telemetry thread: Not connected.")
            return False
            
        self.stop_event.clear()
        self.thread = TelemetryThread(self.master, self.signal_manager, self.stop_event)
        # Set the TelemetryManager as the parent of the thread
        self.thread.setParent(self)
        self.thread.start()
        logging.info("Telemetry thread started.")
        return True
        
    def stop(self):
        """Stops the telemetry thread and closes the connection."""
        if self.thread and self.thread.isRunning():
            logging.info("Stopping telemetry thread...")
            self.stop_event.set()
            self.thread.wait()  # Wait for thread to finish
            logging.info("Telemetry thread stopped.")
            
        if self.master:
            logging.info("Closing connection...")
            try:
                self.master.close()
            except Exception as e:
                logging.error(f"Error closing connection: {e}")
            self.master = None
            
        self._update_status("DISCONNECTED", "Connection closed.")
        self._is_connecting = False  # Reset connection flag
        
    def handle_connect_request(self, conn_string, baud):
        """Handles a connection request signal."""
        logging.info(f"Connection request received: {conn_string} at {baud} baud")
        self._connection_string = conn_string
        self._baud = baud
        
        # Stop any existing connection first
        self.stop()
        
        if self.connect():
            self._request_data_streams()
            self.start()
            
    def handle_disconnect_request(self):
        """Handles a disconnect request signal."""
        logging.info("Disconnect request received")
        self.stop()
        
    def attempt_reconnect(self):
        """Attempts to reconnect to the vehicle."""
        if self._is_connecting:
            logging.info("Reconnection attempt already in progress.")
            return
            
        if self.thread and self.thread.isRunning():
            backoff_time = self.thread.increment_reconnect_attempt()
            if backoff_time < 0:
                self._update_status("ERROR", "Maximum reconnection attempts reached")
                self.stop()
                return
                
            self._update_status("RECONNECTING", f"Attempting reconnection (attempt {self.thread.reconnect_attempts})")
            
            # Schedule the reconnection attempt
            if self.reconnect_timer:
                self.reconnect_timer.stop()
            self.reconnect_timer = QTimer()
            self.reconnect_timer.setSingleShot(True)
            self.reconnect_timer.timeout.connect(self._perform_reconnect)
            self.reconnect_timer.start(int(backoff_time * 1000))  # Convert to milliseconds
            
    def _perform_reconnect(self):
        """Performs the actual reconnection attempt."""
        # Stop any existing connection first
        if self.master:
            try:
                self.master.close()
            except Exception as e:
                logging.error(f"Error closing old connection: {e}")
            self.master = None
            
        if self.connect():
            self._request_data_streams()
            if self.thread:
                self.thread.reset_heartbeat()
        else:
            self.attempt_reconnect()  # Try again if connection failed