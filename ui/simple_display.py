# ui/simple_display.py
import time
import tkinter as tk
from tkinter import ttk # Use themed widgets for a slightly nicer look

class SimpleDisplay(tk.Tk):
    def __init__(self, telemetry_manager):
        """
        Initializes the simple Tkinter display window.

        Args:
            telemetry_manager: The TelemetryManager instance (needed for shutdown).
        """
        super().__init__()
        self.telemetry_manager = telemetry_manager

        self.title("ArduPilot GCS - Basic Telemetry")
        self.geometry("450x400") # Adjusted size slightly

        # --- Data Variables ---
        # Use StringVar to automatically update labels
        self.mode_var = tk.StringVar(value="Mode: ---")
        self.arm_var = tk.StringVar(value="Armed: ---")
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
        self.last_msg_var = tk.StringVar(value="Last Msg: None") # To show activity

        # --- UI Layout ---
        # Use frames for better organization
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Grid layout within the main frame
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Flight Status Section
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="5")
        status_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        ttk.Label(status_frame, textvariable=self.mode_var).pack(side=tk.LEFT, padx=5)
        ttk.Label(status_frame, textvariable=self.arm_var).pack(side=tk.LEFT, padx=5)

        # Position Section
        pos_frame = ttk.LabelFrame(main_frame, text="Position & Altitude", padding="5")
        pos_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        ttk.Label(pos_frame, textvariable=self.lat_var).pack(anchor="w")
        ttk.Label(pos_frame, textvariable=self.lon_var).pack(anchor="w")
        ttk.Label(pos_frame, textvariable=self.alt_agl_var).pack(anchor="w")
        ttk.Label(pos_frame, textvariable=self.alt_msl_var).pack(anchor="w")

        # Attitude Section
        att_frame = ttk.LabelFrame(main_frame, text="Attitude", padding="5")
        att_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        ttk.Label(att_frame, textvariable=self.roll_var).pack(anchor="w")
        ttk.Label(att_frame, textvariable=self.pitch_var).pack(anchor="w")
        ttk.Label(att_frame, textvariable=self.yaw_var).pack(anchor="w")
        ttk.Label(att_frame, textvariable=self.heading_var).pack(anchor="w") # Heading from VFR_HUD

        # Speed Section
        spd_frame = ttk.LabelFrame(main_frame, text="Speed & Climb", padding="5")
        spd_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        ttk.Label(spd_frame, textvariable=self.airspeed_var).pack(anchor="w")
        ttk.Label(spd_frame, textvariable=self.groundspeed_var).pack(anchor="w")
        ttk.Label(spd_frame, textvariable=self.climb_rate_var).pack(anchor="w")

        # GPS & Battery Section
        sens_frame = ttk.LabelFrame(main_frame, text="GPS & Battery", padding="5")
        sens_frame.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)
        ttk.Label(sens_frame, textvariable=self.gps_fix_var).pack(anchor="w")
        ttk.Label(sens_frame, textvariable=self.gps_sats_var).pack(anchor="w")
        ttk.Separator(sens_frame, orient='horizontal').pack(fill='x', pady=5) # Separator
        ttk.Label(sens_frame, textvariable=self.batt_volt_var).pack(anchor="w")
        ttk.Label(sens_frame, textvariable=self.batt_curr_var).pack(anchor="w")
        ttk.Label(sens_frame, textvariable=self.batt_rem_var).pack(anchor="w")

        # Last Message Indicator
        last_msg_frame = ttk.Frame(main_frame, padding="5")
        last_msg_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        ttk.Label(last_msg_frame, textvariable=self.last_msg_var).pack(anchor="w")

        # --- Graceful Shutdown ---
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """Handles window closing event."""
        print("Window closed by user.")
        if self.telemetry_manager:
            self.telemetry_manager.stop() # Signal the manager to stop
        self.destroy() # Close the Tkinter window

    def update_telemetry(self, data_update):
        """
        Updates the UI labels based on the received data dictionary.

        Args:
            data_update (dict): Dictionary containing telemetry data from the queue.
        """
        update_type = data_update.get("type")
        timestamp = data_update.get("timestamp", time.time())
        self.last_msg_var.set(f"Last Msg: {update_type} @ {timestamp:.2f}")

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
            # Yaw comes from ATTITUDE, Heading comes from VFR_HUD (often more stable)
            # Displaying both might be redundant, let's use Yaw here for now
            self.yaw_var.set(f"Yaw: {data_update.get('yaw', 'N/A'):.1f} °")

        elif update_type == "VFR_HUD":
            # Use None as default for get() to handle potential missing fields gracefully
            airspeed = data_update.get('airspeed')
            groundspeed = data_update.get('groundspeed')
            heading = data_update.get('heading')
            climb_rate = data_update.get('climb_rate')

            self.airspeed_var.set(f"Airspeed: {airspeed:.2f} m/s" if airspeed is not None else "Airspeed: --- m/s")
            self.groundspeed_var.set(f"Groundspeed: {groundspeed:.2f} m/s" if groundspeed is not None else "Groundspeed: --- m/s")
            self.heading_var.set(f"Heading: {heading}°" if heading is not None else "Heading: --- °")
            self.climb_rate_var.set(f"Climb Rate: {climb_rate:.2f} m/s" if climb_rate is not None else "Climb Rate: --- m/s")

        elif update_type == "GPS_RAW_INT":
            fix = data_update.get('gps_fix_type', -1)
            sats = data_update.get('gps_satellites', -1)
            # Basic fix type interpretation
            fix_map = {0: "No Fix", 1: "No Fix", 2: "2D Fix", 3: "3D Fix", 4: "DGPS", 5: "RTK Float", 6: "RTK Fixed"}
            self.gps_fix_var.set(f"GPS Fix: {fix_map.get(fix, f'Unknown ({fix})')}")
            self.gps_sats_var.set(f"GPS Sats: {sats if sats != -1 else '---'}")

        elif update_type == "SYS_STATUS":
            voltage = data_update.get('battery_voltage')
            current = data_update.get('battery_current') # Might be None
            remaining = data_update.get('battery_remaining') # Might be None

            self.batt_volt_var.set(f"Batt V: {voltage:.2f} V" if voltage is not None else "Batt V: --- V")
            self.batt_curr_var.set(f"Batt A: {current:.2f} A" if current is not None else "Batt A: --- A")
            self.batt_rem_var.set(f"Batt Rem: {remaining} %" if remaining is not None else "Batt Rem: --- %")

        # Add elif blocks for other desired types (e.g., RC_CHANNELS) if needed