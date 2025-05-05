# ui/simple_display.py (Use EventBus)

import tkinter as tk
from tkinter import ttk
import time # Keep for timestamp formatting

# Import Events, but not the bus instance directly (UI shouldn't know about globals ideally)
from utils.event_bus import Events

class SimpleDisplay(tk.Tk):
    # Remove telemetry_manager from __init__
    def __init__(self):
        """Initializes the simple Tkinter display window."""
        super().__init__()
        # self.telemetry_manager = telemetry_manager # REMOVED

        self.title("ArduPilot GCS - Basic Telemetry")
        self.geometry("450x450") # Increased height slightly for status

        # --- Data Variables ---
        self.mode_var = tk.StringVar(value="Mode: ---")
        self.arm_var = tk.StringVar(value="Armed: ---")
        # ... (other telemetry StringVars remain the same) ...
        self.lat_var = tk.StringVar(value="Lat: ---")
        self.lon_var = tk.StringVar(value="Lon: ---")
        self.alt_agl_var = tk.StringVar(value="Alt (AGL): --- m")
        self.alt_msl_var = tk.StringVar(value="Alt (MSL): --- m")
        self.roll_var = tk.StringVar(value="Roll: --- °")
        self.pitch_var = tk.StringVar(value="Pitch: --- °")
        self.yaw_var = tk.StringVar(value="Yaw: --- °")
        self.heading_var = tk.StringVar(value="Heading: --- °")
        self.airspeed_var = tk.StringVar(value="Airspeed: --- m/s")
        self.groundspeed_var = tk.StringVar(value="Groundspeed: --- m/s")
        self.climb_rate_var = tk.StringVar(value="Climb Rate: --- m/s")
        self.gps_fix_var = tk.StringVar(value="GPS Fix: ---")
        self.gps_sats_var = tk.StringVar(value="GPS Sats: ---")
        self.batt_volt_var = tk.StringVar(value="Batt V: --- V")
        self.batt_curr_var = tk.StringVar(value="Batt A: --- A")
        self.batt_rem_var = tk.StringVar(value="Batt Rem: --- %")

        # Status Variables
        self.connection_status_var = tk.StringVar(value="Status: DISCONNECTED")
        self.last_status_text_var = tk.StringVar(value="Vehicle Msg: ---")
        self.last_msg_type_var = tk.StringVar(value="Last Msg Type: None") # Renamed slightly

        # --- UI Layout ---
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Top Status Bar
        top_status_frame = ttk.Frame(main_frame)
        top_status_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=(0, 5))
        ttk.Label(top_status_frame, textvariable=self.connection_status_var, font="-weight bold").pack(side=tk.LEFT, padx=5)
        ttk.Label(top_status_frame, textvariable=self.last_msg_type_var).pack(side=tk.RIGHT, padx=5)

        # Flight Status Section (Mode/Arm)
        status_frame = ttk.LabelFrame(main_frame, text="Flight Status", padding="5")
        status_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        ttk.Label(status_frame, textvariable=self.mode_var).pack(side=tk.LEFT, padx=5)
        ttk.Label(status_frame, textvariable=self.arm_var).pack(side=tk.LEFT, padx=5)

        # Position Section
        pos_frame = ttk.LabelFrame(main_frame, text="Position & Altitude", padding="5")
        pos_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        # ... (Labels for lat, lon, alt remain the same) ...
        ttk.Label(pos_frame, textvariable=self.lat_var).pack(anchor="w")
        ttk.Label(pos_frame, textvariable=self.lon_var).pack(anchor="w")
        ttk.Label(pos_frame, textvariable=self.alt_agl_var).pack(anchor="w")
        ttk.Label(pos_frame, textvariable=self.alt_msl_var).pack(anchor="w")

        # Attitude Section
        att_frame = ttk.LabelFrame(main_frame, text="Attitude", padding="5")
        att_frame.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
        # ... (Labels for roll, pitch, yaw, heading remain the same) ...
        ttk.Label(att_frame, textvariable=self.roll_var).pack(anchor="w")
        ttk.Label(att_frame, textvariable=self.pitch_var).pack(anchor="w")
        ttk.Label(att_frame, textvariable=self.yaw_var).pack(anchor="w")
        ttk.Label(att_frame, textvariable=self.heading_var).pack(anchor="w")

        # Speed Section
        spd_frame = ttk.LabelFrame(main_frame, text="Speed & Climb", padding="5")
        spd_frame.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)
        # ... (Labels for airspeed, groundspeed, climb remain the same) ...
        ttk.Label(spd_frame, textvariable=self.airspeed_var).pack(anchor="w")
        ttk.Label(spd_frame, textvariable=self.groundspeed_var).pack(anchor="w")
        ttk.Label(spd_frame, textvariable=self.climb_rate_var).pack(anchor="w")

        # GPS & Battery Section
        sens_frame = ttk.LabelFrame(main_frame, text="GPS & Battery", padding="5")
        sens_frame.grid(row=3, column=1, sticky="nsew", padx=5, pady=5)
        # ... (Labels for gps, battery remain the same) ...
        ttk.Label(sens_frame, textvariable=self.gps_fix_var).pack(anchor="w")
        ttk.Label(sens_frame, textvariable=self.gps_sats_var).pack(anchor="w")
        ttk.Separator(sens_frame, orient='horizontal').pack(fill='x', pady=5)
        ttk.Label(sens_frame, textvariable=self.batt_volt_var).pack(anchor="w")
        ttk.Label(sens_frame, textvariable=self.batt_curr_var).pack(anchor="w")
        ttk.Label(sens_frame, textvariable=self.batt_rem_var).pack(anchor="w")


        # Last Status Text Message
        last_text_frame = ttk.Frame(main_frame, padding="5")
        last_text_frame.grid(row=4, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        ttk.Label(last_text_frame, textvariable=self.last_status_text_var, wraplength=400, justify=tk.LEFT).pack(anchor="w")

        # --- Graceful Shutdown ---
        # self.protocol("WM_DELETE_WINDOW", self.on_closing)
        # Let main loop handle shutdown on window close now

    # Removed on_closing method - main loop's finally block handles shutdown

    # --- Event Handlers ---

    def handle_telemetry_update(self, data_update):
        """
        EVENT HANDLER: Updates UI labels based on TELEMETRY_UPDATE event data.
        """
        update_type = data_update.get("type")
        timestamp = data_update.get("timestamp", time.time())
        self.last_msg_type_var.set(f"Last Msg Type: {update_type}") # Show type only

        # --- Parsing logic (same as before, just indented within handler) ---
        if update_type == "HEARTBEAT":
            self.mode_var.set(f"Mode: {data_update.get('mode', 'N/A')}")
            armed_status = data_update.get('armed')
            self.arm_var.set(f"Armed: {'Yes' if armed_status else 'No'}")
        elif update_type == "GLOBAL_POSITION_INT":
            self.lat_var.set(f"Lat: {data_update.get('lat', 'N/A'):.7f}")
            self.lon_var.set(f"Lon: {data_update.get('lon', 'N/A'):.7f}")
            self.alt_agl_var.set(f"Alt (AGL): {data_update.get('alt_agl', 'N/A'):.2f} m")
            self.alt_msl_var.set(f"Alt (MSL): {data_update.get('alt_msl', 'N/A'):.2f} m")
        elif update_type == "ATTITUDE":
            self.roll_var.set(f"Roll: {data_update.get('roll', 'N/A'):.1f} °")
            self.pitch_var.set(f"Pitch: {data_update.get('pitch', 'N/A'):.1f} °")
            self.yaw_var.set(f"Yaw: {data_update.get('yaw', 'N/A'):.1f} °")
        elif update_type == "VFR_HUD":
            airspeed = data_update.get('airspeed')
            groundspeed = data_update.get('groundspeed')
            heading = data_update.get('heading')
            climb_rate = data_update.get('climb_rate')
            self.airspeed_var.set(f"Airspeed: {airspeed:.2f} m/s" if airspeed is not None else "---")
            self.groundspeed_var.set(f"Groundspeed: {groundspeed:.2f} m/s" if groundspeed is not None else "---")
            self.heading_var.set(f"Heading: {heading}°" if heading is not None else "---")
            self.climb_rate_var.set(f"Climb Rate: {climb_rate:.2f} m/s" if climb_rate is not None else "---")
        elif update_type == "GPS_RAW_INT":
            fix = data_update.get('gps_fix_type', -1)
            sats = data_update.get('gps_satellites', -1)
            fix_map = {0: "No Fix", 1: "No Fix", 2: "2D Fix", 3: "3D Fix", 4: "DGPS", 5: "RTK Float", 6: "RTK Fixed"}
            self.gps_fix_var.set(f"GPS Fix: {fix_map.get(fix, f'Unknown ({fix})')}")
            self.gps_sats_var.set(f"GPS Sats: {sats if sats != -1 else '---'}")
        elif update_type == "SYS_STATUS":
            voltage = data_update.get('battery_voltage')
            current = data_update.get('battery_current') # Might be None
            remaining = data_update.get('battery_remaining') # Might be None
            self.batt_volt_var.set(f"Batt V: {voltage:.2f} V" if voltage is not None else "---")
            self.batt_curr_var.set(f"Batt A: {current:.2f} A" if current is not None else "---")
            self.batt_rem_var.set(f"Batt Rem: {remaining} %" if remaining is not None else "---")
        # Add elif for RC_CHANNELS if needed

    def handle_connection_status_change(self, status, message=""):
        """EVENT HANDLER: Updates the connection status label."""
        display_message = f"Status: {status}"
        if message:
            display_message += f" ({message})"
        self.connection_status_var.set(display_message)
        # You could change label color here too based on status

    def handle_status_text(self, text, severity, **kwargs): # Use **kwargs to ignore extra fields like timestamp
        """EVENT HANDLER: Updates the last status text message label."""
        # Maybe prepend severity level
        severity_map = {
             0: "EMERGENCY", 1: "ALERT", 2: "CRITICAL", 3: "ERROR",
             4: "WARNING", 5: "NOTICE", 6: "INFO", 7: "DEBUG"
        }
        sev_str = severity_map.get(severity, f"SEV {severity}")
        self.last_status_text_var.set(f"Vehicle Msg [{sev_str}]: {text}")