# Tasmota Backup V1.0.2
A multi-language automated backup tool for Tasmota devices. Features auto-network scanning, high-speed multi-threaded downloads, and a modern GUI.
# 🚀 Tasmota Backup Tool V 1.0.2

![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)
![Status](https://img.shields.io/badge/status-stable-brightgreen.svg)

A professional, multi-language automated backup solution for **Tasmota** firmware devices (ESP8266 & ESP32). This tool features high-speed asynchronous network scanning and a modern, adaptive user interface.

---

## 🌍 Supported Languages / Limbi Suportate
| Language | Support | Status |
| :--- | :--- | :--- |
| **English 🇬🇧** | Full Support | ✅ |
| **Română 🇷🇴** | Suport Complet | ✅ |
| **Italiano 🇮🇹** | Supporto Completo | ✅ |
| **Français 🇫🇷** | Support Complet | ✅ |
| **Deutsch 🇩🇪** | Volle Unterstützung | ✅ |
| **Español 🇪🇸** | Soporte Completo | ✅ |
| **Polski 🇵🇱** | Pełne Wsparcie | ✅ |

---

## 📋 System Prerequisites
Before you begin, ensure you meet the following requirements:

* **Operating System**: Windows 10/11 (Optimized for dark/light mode).
* **Network**: PC must be connected to the same local network as the Tasmota devices.
* **Python (For Developers)**: Version 3.8 or higher.
* **Tasmota Settings**: Admin credentials (Username/Password) if you have password protection enabled on your devices.

---

## 🛠️ Installation & Setup

### 🔵 Option A: For Regular Users (Recommended)
This option does not require Python or any coding knowledge.
1.  Navigate to the **`dist/`** folder in this repository.
2.  Download the **`TasmotaBackupTool.exe`** file.
3.  Place it in a folder where you want your backups to be saved.
4.  Double-click to run!

### 🟢 Option B: For Developers (Source Code)
If you want to run the script manually or modify the code:
1.  **Clone the Repo**:
    ```bash
    git clone https://github.com/yourusername/tasmotabackuptool.git
    cd tasmotabackup
    ```
2.  **Install Dependencies**:
    ```bash
    pip install customtkinter requests
    ```
3.  **Run the App**:
    ```bash
    python main.py
    ```

---

## 📖 Detailed Instructions

### 1. Network Setup
* **Auto-Detect**: The tool automatically identifies your local IP range (e.g., 192.168.1.x).
* **Manual Subnet**: If you have a complex setup, uncheck "Auto-Detect" and enter your subnet manually (e.g., `192.168.1`).

### 2. Credentials & Format
* Enter your Tasmota **Web Admin** username and password.
* Choose a **File Name Format**:
    * **IP Only**: Saves as `192.168.1.50.dmp`.
    * **Tasmota Name**: Uses the FriendlyName set in the device.
    * **Both**: Combines them for easy identification.

### 3. Execution
* Click **START**. The tool will ping all 254 possible addresses simultaneously.
* Successful backups are logged in the console and saved in a folder named by today's date (e.g., `backups/17042026/`).

---

## 🔍 Troubleshooting (FAQ)

**Q: No devices are found during scan.**
* **A1**: Check if your Windows Firewall is blocking the app.
* **A2**: Ensure your PC is not on a "Guest" Wi-Fi network, as these usually block device-to-device communication (AP Isolation).
* **A3**: Verify the IP subnet is correct.

**Q: "Authentication Error" appears in the console.**
* **A**: Your Tasmota devices have a password set. Enter the correct credentials in the "Username" and "Password" fields before starting.

**Q: The scan is too slow or skips devices.**
* **A**: This tool uses 50 concurrent threads and a 5-second timeout to allow slow ESP8266 chips to respond. If your router is very old, it might struggle with the traffic. Try a more stable connection.

**Q: The EXE won't start or is flagged by Anti-Virus.**
* **A**: Since the EXE is "unsigned" (created with PyInstaller), some AVs might flag it as a false positive. You may need to add it to your "Exclusions" list.

---

## 🏗️ Compiling the EXE
I have provided a **`build.bat`** script for easy compilation:
1.  Ensure `main.py` and `icon.ico` are in the root folder.
2.  Run `build.bat`.
3.  The script will check for Python, install `pyinstaller`, and generate a single-file executable in the `dist/` folder.

---

## 👨‍💻 Author
**Cristian Florea**
*Created for the Smart Home community to make device maintenance easier and safer.*

---

## 📝 License
This project is licensed under the **MIT License**. You are free to use, modify, and distribute it.
