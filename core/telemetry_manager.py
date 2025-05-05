# core/telemetry_manager.py (Plan D: Simplified - Receive All, Parse Known)

import threading
import time
import queue
import math
from pymavlink import mavutil
import sys

class TelemetryManager:
    def __init__(self, connection_string, baud=115200, data_queue=None):
        """
        Initializes the TelemetryManager. Simplified to receive all messages
        and parse known types, bypassing message_names/dialect issues.
        """
        self.connection_string = connection_string
        self.baud = baud
        self.master = None
        self.thread = None
        self.stop_event = threading.Event()
        self.data_queue = data_queue if data_queue is not None else queue.Queue()

        # Store desired frequencies using numeric IDs
        self.message_frequencies = {
            mavutil.mavlink.MAVLINK_MSG_ID_ATTITUDE: 100000,
            mavutil.mavlink.MAVLINK_MSG_ID_GPS_RAW_INT: 200000,
            mavutil.mavlink.MAVLINK_MSG_ID_GLOBAL_POSITION_INT: 200000,
            mavutil.mavlink.MAVLINK_MSG_ID_SYS_STATUS: 1000000,
            mavutil.mavlink.MAVLINK_MSG_ID_RC_CHANNELS: 500000,
            mavutil.mavlink.MAVLINK_MSG_ID_VFR_HUD: 200000,
            mavutil.mavlink.MAVLINK_MSG_ID_HEARTBEAT: 1000000,
            #mavutil.mavlink.MAVLINK_MSG_ID_RANGEFINDER: 200000,
        }
        # Store the names of message types we actually want to parse and queue
        # This filtering now happens *after* receiving the message.
        self.desired_message_types = [
            'ATTITUDE', 'GPS_RAW_INT', 'GLOBAL_POSITION_INT', 'SYS_STATUS',
            'RC_CHANNELS', 'VFR_HUD', 'HEARTBEAT', 'STATUSTEXT' # Add STATUSTEXT
            # Add 'RANGEFINDER' if needed
        ]


    def connect(self):
        """Establishes the MAVLink connection."""
        # No dialect handling needed here anymore
        if self.master:
             print("INFO: Already connected.")
             return True

        print(f"Connecting to {self.connection_string} at {self.baud} baud...")
        try:
            if self.connection_string.startswith(('udp:', 'tcp:')):
                 self.master = mavutil.mavlink_connection(self.connection_string, source_system=255)
            else:
                 self.master = mavutil.mavlink_connection(self.connection_string, baud=self.baud, source_system=255)

            if not self.master:
                 print("ERROR: mavutil.mavlink_connection failed.")
                 return False

            print("Waiting for heartbeat...")
            heartbeat = self.master.wait_heartbeat(timeout=10)

            if heartbeat:
                print(f"Heartbeat received from System {self.master.target_system} Component {self.master.target_component}")
                print("Connection successful.")
                return True
            else:
                print("Failed to receive heartbeat within timeout.")
                if self.master: self.master.close()
                self.master = None
                return False
        except Exception as e:
            print(f"Failed to connect: {type(e).__name__}: {e}")
            if self.master: self.master.close()
            self.master = None
            return False


    def _request_data_streams(self):
        """Sends commands to set message intervals."""
        # No dependency on message maps
        if not self.master:
            print("Not connected. Cannot request streams.")
            return

        print("Requesting data streams...")
        for msg_id, frequency in self.message_frequencies.items():
            if frequency > 0:
                try:
                    if not hasattr(self.master, 'mav'):
                         print(f"ERROR: master.mav missing, cannot send command for MSG ID {msg_id}")
                         continue

                    self.master.mav.command_long_send(
                        self.master.target_system,
                        self.master.target_component,
                        mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,
                        0, msg_id, frequency, 0, 0, 0, 0, 0
                    )
                    # Just log by ID, as we don't have the map readily available
                    print(f"Requested ID {msg_id} at interval {frequency} us")
                    time.sleep(0.05)
                except AttributeError as ae:
                     print(f"AttributeError sending interval command for MSG ID {msg_id}: {ae}. Check mav object.")
                     break
                except Exception as e:
                    print(f"Error requesting interval for MSG ID {msg_id}: {type(e).__name__}: {e}")
        print("Data stream requests sent.")


    def _receive_loop(self):
        """Receives ALL messages and parses the ones listed in desired_message_types."""
        print("Receive loop starting. Waiting for ANY MAVLink message...")
        active_connection = True
        while not self.stop_event.is_set() and active_connection:
            # Check connection status
            if not self.master or self.master.target_system == 0: # Simpler check now
                 if not self.master: print("Connection object is None. Stopping receive loop.")
                 else: print("Connection lost (target system 0). Stopping receive loop.")
                 active_connection = False
                 continue

            try:
                # *** Receive ANY message (type=None) ***
                msg = self.master.recv_match(blocking=True, timeout=2.0)

                if msg is None: continue # Timeout, just loop

                # Get the message type name (e.g., 'ATTITUDE')
                msg_type = msg.get_type()

                # *** Filter AFTER receiving, based on our desired list ***
                if msg_type not in self.desired_message_types:
                    # print(f"Ignoring msg type: {msg_type}") # Enable for debugging
                    continue # Skip messages we don't want to parse/queue


                # --- Parse the messages we DO want ---
                data = {"type": msg_type, "timestamp": time.time()}

                if msg_type == 'HEARTBEAT':
                    data['armed'] = bool(msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED)
                    data['mode'] = mavutil.mode_string_v10(msg) # Still useful
                    data['system_status'] = msg.system_status
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
                # elif msg_type == 'RANGEFINDER': # Add parsing if needed
                #     data['rangefinder_distance'] = msg.distance
                elif msg_type == 'VFR_HUD':
                    data['airspeed'] = msg.airspeed
                    data['groundspeed'] = msg.groundspeed
                    data['heading'] = msg.heading
                    data['throttle'] = msg.throttle
                    data['climb_rate'] = msg.climb
                elif msg_type == 'RC_CHANNELS':
                    data['rc_channels'] = [
                        msg.chan1_raw, msg.chan2_raw, msg.chan3_raw, msg.chan4_raw,
                        msg.chan5_raw, msg.chan6_raw, msg.chan7_raw, msg.chan8_raw ]
                elif msg_type == 'ATTITUDE':
                    data['roll'] = math.degrees(msg.roll)
                    data['pitch'] = math.degrees(msg.pitch)
                    data['yaw'] = math.degrees(msg.yaw)
                elif msg_type == 'STATUSTEXT':
                     data['text'] = msg.text.strip()
                     data['severity'] = msg.severity
                     # Still print important status messages directly
                     if data['severity'] <= mavutil.mavlink.MAV_SEVERITY_ERROR:
                         print(f"MAV STATUS [{data['severity']}]: {data['text']}")

                # --- End Parsing ---

                # Put data on queue if parsing added fields
                # (Should always be true if it passed the desired_message_types check)
                if len(data) > 2:
                    try:
                        self.data_queue.put_nowait(data)
                    except queue.Full:
                        print("Warning: Data queue is full. Dropping message.")
                # else: # Should not happen with current logic
                #    print(f"Warning: Parsed data for {msg_type} was empty?")


            except (ConnectionResetError, BrokenPipeError) as conn_e:
                print(f"{type(conn_e).__name__}. Stopping receive loop.")
                active_connection = False
            except mavutil.mavlink.MAVLinkError as mav_e:
                print(f"MAVLink Error in receive loop: {mav_e}. Continuing.") # Often recoverable
            except AttributeError as attr_e:
                 # Catch errors parsing fields if msg object is weird (less likely now)
                 print(f"Attribute Error in receive loop (parsing issue?): {attr_e}")
                 # Continue for now, maybe it was a bad message
            except Exception as e:
                print(f"Unhandled Exception in receive loop: {type(e).__name__}: {e}")
                time.sleep(0.1) # Prevent fast spinning

        print("Receive loop finished.")
        if self.master:
            print("Closing connection from receive loop exit.")
            try: self.master.close()
            except Exception as e: print(f"Error closing connection in loop: {e}")
            self.master = None


    # --- start, stop, get_data_queue remain unchanged ---
    def start(self):
        """Starts the telemetry manager: connects, requests streams, and starts the receiver thread."""
        if self.thread is not None and self.thread.is_alive():
            print("Manager already started and thread is alive.")
            return True
        if self.connect(): # Simplified connect
            self._request_data_streams()
            self.stop_event.clear()
            self.thread = threading.Thread(target=self._receive_loop, name="MAVLinkReceiver", daemon=True)
            self.thread.start()
            print("Telemetry manager started successfully.")
            return True
        else:
            print("Failed to start telemetry manager (connection failed).")
            if self.master:
                try: self.master.close()
                except Exception: pass
                self.master = None
            self.thread = None
            return False

    def stop(self):
        """Signals the receiver thread to stop and cleans up."""
        print("Stopping telemetry manager...")
        self.stop_event.set()
        thread_was_running = False
        if self.thread is not None:
             thread_was_running = True
             print("Waiting for receiver thread to join...")
             self.thread.join(timeout=3.0)
             if self.thread.is_alive():
                 print("Warning: Receive thread did not stop gracefully within timeout.")
             self.thread = None
        if self.master:
            if thread_was_running: print("Master connection ref still exists after thread join, closing.")
            else: print("Closing master connection during stop (thread was not running).")
            try: self.master.close()
            except Exception as e: print(f"Error during final close: {e}")
            self.master = None
        elif not thread_was_running:
             print("Stop called but manager was not fully running (no thread or master).")
        print("Telemetry manager stopped.")

    def get_data_queue(self):
        """Returns the queue instance used for data."""
        return self.data_queue