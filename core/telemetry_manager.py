# core/telemetry_manager.py (Integrate EventBus)

import threading
import time
# import queue # No longer needed
import math
from pymavlink import mavutil
import sys
import logging # Use logging

# Import the global event bus instance and Events class
from utils.event_bus import event_bus, Events

class TelemetryManager:
    def __init__(self, connection_string, baud=115200, bus=event_bus): # Accept bus instance
        """
        Initializes the TelemetryManager using an EventBus.
        """
        self.connection_string = connection_string
        self.baud = baud
        self.master = None
        self.thread = None
        self.stop_event = threading.Event()
        # self.data_queue = data_queue if data_queue is not None else queue.Queue() # REMOVED
        self.event_bus = bus # Store the event bus instance

        self.current_status = "DISCONNECTED" # Add status tracking

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
        # Store the names of message types we actually want to parse and publish
        self.desired_message_types = [
            'ATTITUDE', 'GPS_RAW_INT', 'GLOBAL_POSITION_INT', 'SYS_STATUS',
            'RC_CHANNELS', 'VFR_HUD', 'HEARTBEAT', 'STATUSTEXT'
            # Add 'RANGEFINDER' if needed
        ]


    def _update_status(self, new_status: str, message: str = ""):
        """Updates internal status and publishes a status change event."""
        if new_status != self.current_status:
            self.current_status = new_status
            logging.info(f"Connection Status: {new_status} - {message}")
            # Use publish_safe as status updates might be handled by UI
            self.event_bus.publish_safe(
                Events.CONNECTION_STATUS_CHANGED,
                status=new_status,
                message=message
            )
        elif message: # Publish even if status is same, if there's a new message
             logging.info(f"Connection Status Info: {message}")
             self.event_bus.publish_safe(
                Events.CONNECTION_STATUS_CHANGED,
                status=self.current_status, # Send current status again
                message=message
            )


    def connect(self):
        """Establishes the MAVLink connection and updates status."""
        if self.master:
             logging.info("INFO: Already connected.")
             return True

        self._update_status("CONNECTING", f"Attempting connection to {self.connection_string}...")
        # print(f"Connecting to {self.connection_string} at {self.baud} baud...") # Replaced by status update
        try:
            if self.connection_string.startswith(('udp:', 'tcp:')):
                 self.master = mavutil.mavlink_connection(self.connection_string, source_system=255)
            else:
                 self.master = mavutil.mavlink_connection(self.connection_string, baud=self.baud, source_system=255)

            if not self.master:
                 # print("ERROR: mavutil.mavlink_connection failed.") # Replaced
                 self._update_status("ERROR", "mavutil.mavlink_connection failed")
                 return False

            self._update_status("CONNECTING", "Waiting for heartbeat...")
            # print("Waiting for heartbeat...") # Replaced
            heartbeat = self.master.wait_heartbeat(timeout=10)

            if heartbeat:
                msg = f"Heartbeat received (Sys:{self.master.target_system}/Comp:{self.master.target_component})"
                # print(f"Heartbeat received from System {self.master.target_system} Component {self.master.target_component}") # Replaced
                self._update_status("CONNECTED", msg)
                # print("Connection successful.") # Replaced
                return True
            else:
                # print("Failed to receive heartbeat within timeout.") # Replaced
                self._update_status("ERROR", "Heartbeat timed out")
                if self.master: self.master.close()
                self.master = None
                return False
        except Exception as e:
            errmsg = f"Connection failed: {type(e).__name__}: {e}"
            # print(f"Failed to connect: {type(e).__name__}: {e}") # Replaced
            self._update_status("ERROR", errmsg)
            if self.master: self.master.close()
            self.master = None
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


    def _receive_loop(self):
        """Receives messages and publishes events via the EventBus."""
        logging.info("Receive loop starting.")
        active_connection = True
        while not self.stop_event.is_set() and active_connection:
            # Check connection status
            if not self.master or self.master.target_system == 0:
                 errmsg = ""
                 if not self.master: errmsg = "Connection object is None."
                 else: errmsg = "Connection lost (target system 0)."
                 self._update_status("DISCONNECTED", errmsg) # Update status on loss
                 active_connection = False
                 continue

            try:
                # Receive ANY message
                msg = self.master.recv_match(blocking=True, timeout=2.0)

                if msg is None: continue # Timeout, just loop

                msg_type = msg.get_type()

                # Filter AFTER receiving
                if msg_type not in self.desired_message_types:
                    continue # Skip messages we don't want

                # --- Parse the messages we DO want ---
                data = {"type": msg_type, "timestamp": time.time()}
                publish_event = True # Assume we publish unless parsing fails

                if msg_type == 'HEARTBEAT':
                    data['armed'] = bool(msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED)
                    data['mode'] = mavutil.mode_string_v10(msg)
                    data['system_status'] = msg.system_status
                    # If connection was lost, receiving heartbeat means it's back
                    if self.current_status != "CONNECTED":
                         self._update_status("CONNECTED", "Reconnected via Heartbeat")

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
                # elif msg_type == 'RANGEFINDER': ...
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
                     # Publish STATUSTEXT as a separate event
                     self.event_bus.publish_safe(Events.STATUS_TEXT_RECEIVED, **data)
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
                    # Use publish_safe to handle potential UI subscribers correctly
                    self.event_bus.publish_safe(Events.TELEMETRY_UPDATE, data_update=data)

            except (ConnectionResetError, BrokenPipeError) as conn_e:
                errmsg = f"{type(conn_e).__name__} in receive loop."
                self._update_status("ERROR", errmsg)
                active_connection = False # Stop loop
            except mavutil.mavlink.MAVLinkError as mav_e:
                logging.warning(f"MAVLink Error in receive loop: {mav_e}. Continuing.")
            except AttributeError as attr_e:
                 logging.error(f"Attribute Error in receive loop (parsing issue?): {attr_e}", exc_info=True)
                 # Continue for now, maybe it was a bad message
            except Exception as e:
                logging.error(f"Unhandled Exception in receive loop: {type(e).__name__}: {e}", exc_info=True)
                time.sleep(0.1) # Prevent fast spinning

        logging.info("Receive loop finished.")
        if self.master:
            logging.info("Closing connection from receive loop exit.")
            try: self.master.close()
            except Exception as e: logging.error(f"Error closing connection in loop: {e}")
            self.master = None
        # Ensure status is updated if loop exits cleanly via stop_event while connected
        if self.current_status == "CONNECTED" and self.stop_event.is_set():
             self._update_status("DISCONNECTED", "Manager stopped by user.")
        elif self.current_status != "DISCONNECTED" and self.current_status != "ERROR":
             # If loop exited for other reason while not Disconnected/Error state
             self._update_status("DISCONNECTED", "Receive loop exited unexpectedly.")


    def start(self):
        """Starts the telemetry manager: connects, requests streams, and starts the receiver thread."""
        if self.thread is not None and self.thread.is_alive():
            logging.warning("Manager already started.")
            return True
        # Reset stop event in case it was previously set
        self.stop_event.clear()
        # Connect will update status
        if self.connect():
            self._request_data_streams()
            self.thread = threading.Thread(target=self._receive_loop, name="MAVLinkReceiver", daemon=True)
            self.thread.start()
            logging.info("Telemetry manager started successfully.")
            return True
        else:
            # connect() already updated status to ERROR or DISCONNECTED
            logging.error("Failed to start telemetry manager (connection failed).")
            self.thread = None
            return False


    def stop(self):
        """Signals the receiver thread to stop and cleans up."""
        logging.info("Stopping telemetry manager...")
        if self.thread is None and self.current_status == "DISCONNECTED":
             logging.info("Manager already stopped or was never started.")
             return

        self.stop_event.set() # Signal the loop to stop

        thread_was_running = False
        if self.thread is not None:
             thread_was_running = True
             logging.info("Waiting for receiver thread to join...")
             self.thread.join(timeout=3.0)
             if self.thread.is_alive():
                 logging.warning("Warning: Receive thread did not stop gracefully within timeout.")
             self.thread = None

        # Clean up connection if thread didn't
        if self.master:
            logging.info("Closing master connection during stop.")
            try: self.master.close()
            except Exception as e: logging.error(f"Error during final close: {e}")
            self.master = None

        # Ensure final status is DISCONNECTED if it wasn't already
        if self.current_status != "DISCONNECTED":
             self._update_status("DISCONNECTED", "Manager stopped.")

        logging.info("Telemetry manager stopped.")


    # --- Command Handling (Example - Not yet used) ---
    # We would subscribe this method to Events.CONNECTION_REQUEST later
    def handle_connection_request(self, conn_string, baud):
         logging.info(f"Received connection request: {conn_string} @ {baud}")
         if self.current_status != "DISCONNECTED":
              logging.warning("Ignoring connection request: Manager already connected or busy.")
              return
         # Update internal settings and start
         self.connection_string = conn_string
         self.baud = baud
         self.start()


    # --- get_data_queue REMOVED ---
    # def get_data_queue(self):
    #     """Returns the queue instance used for data."""
    #     return self.data_queue