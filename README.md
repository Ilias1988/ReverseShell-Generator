# 🐚 Python Reverse Shell Generator

[![Python 3](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-blue?style=for-the-badge)]()

A standalone, dark-themed GUI application for generating reverse shell payloads. Built as a modern desktop alternative to online tools like [revshells.com](https://revshells.com), this tool is designed specifically for penetration testers, red teamers, and CTF players who need quick access to a comprehensive library of reverse shell commands.

---

![App Screenshot](screenshot.png)

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🎨 **Modern Dark UI** | Built with `customtkinter` for a sleek, professional look that's easy on the eyes during long sessions. |
| 📚 **Extensive Library** | Includes **60+ Linux payloads** and specialized **Windows payloads** (MSBuild, PowerShell, ConPtyShell, Mshta, Regsvr32, and more). |
| ⚡ **Real-Time Generation** | Payload and Listener commands update **instantly** as you type your IP address and Port. |
| 🔐 **Smart Encoding** | Supports **Base64**, **URL Encode**, and **Double URL Encode** for bypassing filters. |
| 🛡️ **Raw String Support** | Correctly handles Windows file paths (backslashes) without Python syntax errors. |
| 📋 **One-Click Copy** | Dedicated buttons for instantly copying the listener command and the generated payload to your clipboard. |
| 🖥️ **Fullscreen Mode** | Press `F11` or use the button for a distraction-free, fullscreen view. |
| 🔄 **OS Switching** | Seamlessly switch between Linux and Windows payloads with a single dropdown. |

---

## 🎯 Supported Payloads

### Linux / Generic (60+ payloads)
- **Bash:** `-i`, `196`, `read line`, `5`, `UDP`
- **Netcat:** `mkfifo`, `-e`, `-c`, `BusyBox`
- **Ncat:** TCP and UDP variants
- **Python:** Python 2 & 3 variants, shortest one-liner
- **PHP:** PentestMonkey, Ivan Sincek, `system()`, `exec()`, `shell_exec()`, `popen()`, `proc_open()`, webshells
- **Languages:** Perl, Ruby, Java, Node.js, Lua, Golang, Awk, Dart, Crystal, Haskell, Vlang
- **Tools:** Socat (with TTY), OpenSSL, Telnet, zsh, sqlite3, curl

### Windows (30+ payloads)
- **PowerShell:** Multiple variants including Base64 encoded, hidden window, IEX download
- **Executables:** `nc.exe`, `ncat.exe`
- **Living off the Land:** MSBuild, Mshta, Regsvr32
- **Advanced:** ConPtyShell (fully interactive PTY)
- **Languages:** Python, Ruby, Perl, Lua, Golang, Java, Node.js, Groovy, Haskell

---

## 📦 Installation & Usage

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/RevShell-Generator.git

# Navigate to the project directory
cd RevShell-Generator

# Install dependencies
pip install -r requirements.txt

# Run the application
python revshell_generator.py
```

### Manual Installation

```bash
pip install customtkinter pyperclip
python revshell_generator.py
```

---

## 🖼️ How to Use

1. **Enter your IP address** (LHOST) in the IP field
2. **Enter your listening port** (LPORT) in the Port field
3. **Select the target OS** (Linux or Windows)
4. **Choose a payload** from the dropdown menu
5. **Select encoding** (optional): None, Base64, URL, or Double URL
6. **Copy the Listener command** and run it on your machine
7. **Copy the Payload** and execute it on the target

---

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `F11` | Toggle Fullscreen Mode |
| `Escape` | Exit Fullscreen Mode |

---

## 📁 Project Structure

```
RevShell-Generator/
├── revshell_generator.py   # Main GUI application
├── payloads_linux.py       # Linux/Generic payloads database
├── payloads_windows.py     # Windows payloads database
├── requirements.txt        # Python dependencies
├── README.md               # This documentation
├── LICENSE                 # MIT License
└── screenshot.png          # Application screenshot
```

---

## 🛠️ Adding Custom Payloads

You can easily extend the tool by adding your own payloads:

### Example: Adding a Linux payload
Edit `payloads_linux.py`:
```python
LINUX_PAYLOADS = {
    # ... existing payloads ...
    "My Custom Shell": "my_command {ip} {port}",
}
```

### Example: Adding a Windows payload
Edit `payloads_windows.py`:
```python
WINDOWS_PAYLOADS = {
    # ... existing payloads ...
    "My Custom Shell": "my_command.exe {ip} {port}",
}
```

> **Note:** Use `{ip}` and `{port}` as placeholders - they will be automatically replaced with user input.

---

## ⚠️ Legal Disclaimer

```
THIS TOOL IS PROVIDED FOR EDUCATIONAL PURPOSES AND AUTHORIZED SECURITY AUDITS ONLY.

By using this software, you agree that:

1. You will only use this tool on systems you own or have explicit written 
   permission to test.

2. You understand that unauthorized access to computer systems is illegal 
   and punishable by law.

3. The author(s) of this tool are NOT responsible for any misuse, damage, 
   or illegal activities conducted with this software.

4. You will comply with all applicable local, state, national, and 
   international laws and regulations.

USE AT YOUR OWN RISK. ALWAYS OBTAIN PROPER AUTHORIZATION BEFORE TESTING.
```

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- 🐛 Report bugs
- 💡 Suggest new features
- 🔧 Add new payloads
- 📝 Improve documentation

---

## 🙏 Acknowledgments

- Inspired by [revshells.com](https://revshells.com)
- Built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- Payload references from various security resources and the infosec community

---

<p align="center">
  <b>Made with ❤️ for penetration testers</b>
</p>
