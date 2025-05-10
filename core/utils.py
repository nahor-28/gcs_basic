import serial.tools.list_ports

def get_available_serial_ports():
    """
    Lists all available serial ports on the system.
    
    Returns:
        list: List of dictionaries with port information (device, description, etc.)
    """
    ports = []
    for port in serial.tools.list_ports.comports():
        ports.append({
            'device': port.device,
            'description': port.description,
            'manufacturer': port.manufacturer if hasattr(port, 'manufacturer') else None,
            'hwid': port.hwid
        })
    return ports

def get_connection_strings():
    """
    Returns a list of common connection strings including available serial ports.
    
    Returns:
        list: List of connection strings
    """
    # Standard connection strings
    conn_strings = [
        "udp:localhost:14550",
        "udp:localhost:14551",
        "tcp:localhost:5760"
    ]
    
    # Add available serial ports
    for port in get_available_serial_ports():
        conn_strings.append(port['device'])
    
    return conn_strings 