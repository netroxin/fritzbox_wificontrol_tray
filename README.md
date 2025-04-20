# WLAN Tray

WLAN Tray is a Python application that allows you to control the WLAN functionality of a FritzBox router directly from the system tray. It provides a simple interface to enable or disable WLAN and manage router settings.

## Features
- Enable or disable WLAN on your FritzBox with a single click.
- Configure FritzBox settings such as IP address, username, and password.
- Modern dark theme for a visually appealing interface.
- System tray integration for quick access to all features.

## Requirements
- Python 3.8 or higher.
- Required Python libraries: PyQt6, fritzconnection, cryptography.

## Installation
1. Clone the repository: `git clone https://github.com/netroxin/fritzbox_wificontrol_tray`
2. Navigate to the project directory: `cd fritzbox_wificontrol_tray`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the application: `fritzbox_wificontrol_tray.py`

## Usage
1. Start the application.
2. Right-click the tray icon to access the menu.
3. Options include:
   - "WLAN ON" to enable WLAN.
   - "WLAN OFF" to disable WLAN.
   - "Settings" to configure FritzBox connection details.
   - "Quit" to exit the application.

 Compiled Version for Windows: https://github.com/netroxin/fritzbox_wificontrol_tray/releases

## Configuration
- On first run, a default configuration file (config.json) is created.
- Use the "Settings" menu to update the FritzBox IP, username, and password.
- Configuration data is encrypted using the cryptography library for security.

Please note that this application has only been tested with the FritzBox 7490 model. Compatibility with other models is not guaranteed.

## Security
- The configuration file is encrypted to protect sensitive data.
- A unique encryption key is stored in a separate file (config.key).

## License
This project is licensed under the [MIT License].


## Disclaimer
Use this application at your own risk. The author assumes no responsibility for any damages, direct or indirect, that may result from the use of this software. Please ensure you have proper backups and security measures in place before using this application.
