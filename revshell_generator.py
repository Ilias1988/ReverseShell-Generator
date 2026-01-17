#!/usr/bin/env python3
"""
Reverse Shell Generator - A modern GUI tool for generating reverse shell payloads
Similar to revshells.com but as a standalone desktop application
"""

import customtkinter as ctk
import base64
import urllib.parse

# Import payloads from separate files
from payloads_linux import LINUX_PAYLOADS
from payloads_windows import WINDOWS_PAYLOADS

# Try to import pyperclip for clipboard support
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False


class RevShellGenerator(ctk.CTk):
    """Main Application Window"""
    
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("🐚 Reverse Shell Generator")
        self.geometry("1200x800")
        self.minsize(900, 600)
        
        # Set dark mode
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Variables
        self.ip_var = ctk.StringVar(value="10.10.10.10")
        self.port_var = ctk.StringVar(value="4444")
        self.os_var = ctk.StringVar(value="Linux")
        self.encoding_var = ctk.StringVar(value="None")
        self.payload_name_var = ctk.StringVar(value="")
        self.is_fullscreen = False
        
        # Build the UI
        self.create_widgets()
        
        # Bind variables to update function
        self.ip_var.trace_add("write", self.on_input_change)
        self.port_var.trace_add("write", self.on_input_change)
        self.encoding_var.trace_add("write", self.on_input_change)
        
        # Bind keyboard shortcuts
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.exit_fullscreen)
        
        # Initial setup - set first payload and generate
        self.update_payload_dropdown()
        self.update_listener()
        
    def create_widgets(self):
        """Create all UI widgets"""
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # ========== HEADER ==========
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="🐚 Reverse Shell Generator",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.title_label.pack(side="left")
        
        # Fullscreen button
        self.fullscreen_btn = ctk.CTkButton(
            self.header_frame,
            text="⛶ Fullscreen",
            width=100,
            command=self.toggle_fullscreen
        )
        self.fullscreen_btn.pack(side="right", padx=5)
        
        # ========== MAIN CONTENT ==========
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=2)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # ========== LEFT PANEL (Settings) ==========
        self.left_panel = ctk.CTkFrame(self.main_frame)
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        self.left_panel.grid_columnconfigure(0, weight=1)
        
        # Section: Connection Settings
        self.connection_label = ctk.CTkLabel(
            self.left_panel,
            text="🔌 Connection Settings",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.connection_label.grid(row=0, column=0, sticky="w", padx=15, pady=(15, 10))
        
        # IP Address
        self.ip_label = ctk.CTkLabel(self.left_panel, text="IP Address (LHOST):")
        self.ip_label.grid(row=1, column=0, sticky="w", padx=15, pady=(5, 0))
        
        self.ip_entry = ctk.CTkEntry(
            self.left_panel,
            textvariable=self.ip_var,
            placeholder_text="e.g., 10.10.10.10",
            height=35,
            font=ctk.CTkFont(size=14)
        )
        self.ip_entry.grid(row=2, column=0, sticky="ew", padx=15, pady=(5, 10))
        
        # Port
        self.port_label = ctk.CTkLabel(self.left_panel, text="Port (LPORT):")
        self.port_label.grid(row=3, column=0, sticky="w", padx=15, pady=(5, 0))
        
        self.port_entry = ctk.CTkEntry(
            self.left_panel,
            textvariable=self.port_var,
            placeholder_text="e.g., 4444",
            height=35,
            font=ctk.CTkFont(size=14)
        )
        self.port_entry.grid(row=4, column=0, sticky="ew", padx=15, pady=(5, 15))
        
        # Separator
        self.sep1 = ctk.CTkFrame(self.left_panel, height=2, fg_color="gray40")
        self.sep1.grid(row=5, column=0, sticky="ew", padx=15, pady=10)
        
        # Section: OS Selection
        self.os_label = ctk.CTkLabel(
            self.left_panel,
            text="💻 Operating System",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.os_label.grid(row=6, column=0, sticky="w", padx=15, pady=(10, 10))
        
        self.os_dropdown = ctk.CTkOptionMenu(
            self.left_panel,
            variable=self.os_var,
            values=["Linux", "Windows"],
            command=self.on_os_change,
            height=35,
            font=ctk.CTkFont(size=14)
        )
        self.os_dropdown.grid(row=7, column=0, sticky="ew", padx=15, pady=(5, 15))
        
        # Separator
        self.sep2 = ctk.CTkFrame(self.left_panel, height=2, fg_color="gray40")
        self.sep2.grid(row=8, column=0, sticky="ew", padx=15, pady=10)
        
        # Section: Payload Selection (CTkOptionMenu dropdown)
        self.payload_label = ctk.CTkLabel(
            self.left_panel,
            text="🎯 Payload Selection",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.payload_label.grid(row=9, column=0, sticky="w", padx=15, pady=(10, 10))
        
        # Get initial payload list
        initial_payloads = list(LINUX_PAYLOADS.keys())
        
        # Payload Dropdown (CTkOptionMenu)
        self.payload_dropdown = ctk.CTkOptionMenu(
            self.left_panel,
            variable=self.payload_name_var,
            values=initial_payloads,
            command=self.on_payload_change,
            height=35,
            font=ctk.CTkFont(size=14),
            dynamic_resizing=False,
            width=300
        )
        self.payload_dropdown.grid(row=10, column=0, sticky="ew", padx=15, pady=(5, 15))
        
        # Separator
        self.sep3 = ctk.CTkFrame(self.left_panel, height=2, fg_color="gray40")
        self.sep3.grid(row=11, column=0, sticky="ew", padx=15, pady=10)
        
        # Section: Encoding
        self.encoding_label = ctk.CTkLabel(
            self.left_panel,
            text="🔐 Encoding Options",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.encoding_label.grid(row=12, column=0, sticky="w", padx=15, pady=(10, 10))
        
        self.encoding_options = ctk.CTkSegmentedButton(
            self.left_panel,
            values=["None", "Base64", "URL", "Double URL"],
            variable=self.encoding_var
        )
        self.encoding_options.grid(row=13, column=0, sticky="ew", padx=15, pady=(5, 20))
        
        # Spacer to push content up
        self.left_panel.grid_rowconfigure(14, weight=1)
        
        # ========== RIGHT PANEL (Output) ==========
        self.right_panel = ctk.CTkFrame(self.main_frame)
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.right_panel.grid_rowconfigure(1, weight=0)
        self.right_panel.grid_rowconfigure(3, weight=1)
        
        # Listener Section
        self.listener_label = ctk.CTkLabel(
            self.right_panel,
            text="👂 Listener Command",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.listener_label.grid(row=0, column=0, sticky="w", padx=15, pady=(15, 10))
        
        self.listener_frame = ctk.CTkFrame(self.right_panel)
        self.listener_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 15))
        self.listener_frame.grid_columnconfigure(0, weight=1)
        
        self.listener_textbox = ctk.CTkTextbox(
            self.listener_frame,
            height=60,
            font=ctk.CTkFont(family="Consolas", size=14),
            wrap="none"
        )
        self.listener_textbox.grid(row=0, column=0, sticky="ew", padx=(10, 5), pady=10)
        
        self.copy_listener_btn = ctk.CTkButton(
            self.listener_frame,
            text="📋 Copy",
            width=80,
            command=lambda: self.copy_to_clipboard(self.listener_textbox)
        )
        self.copy_listener_btn.grid(row=0, column=1, padx=(5, 10), pady=10)
        
        # Payload Section
        self.payload_output_label = ctk.CTkLabel(
            self.right_panel,
            text="⚡ Generated Payload",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.payload_output_label.grid(row=2, column=0, sticky="w", padx=15, pady=(10, 10))
        
        self.payload_frame = ctk.CTkFrame(self.right_panel)
        self.payload_frame.grid(row=3, column=0, sticky="nsew", padx=15, pady=(0, 15))
        self.payload_frame.grid_columnconfigure(0, weight=1)
        self.payload_frame.grid_rowconfigure(0, weight=1)
        
        self.payload_textbox = ctk.CTkTextbox(
            self.payload_frame,
            font=ctk.CTkFont(family="Consolas", size=13),
            wrap="word"
        )
        self.payload_textbox.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.copy_payload_btn = ctk.CTkButton(
            self.payload_frame,
            text="📋 Copy Payload",
            command=lambda: self.copy_to_clipboard(self.payload_textbox)
        )
        self.copy_payload_btn.grid(row=1, column=0, pady=(0, 10))
        
        # ========== FOOTER ==========
        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.footer_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(10, 20))
        
        self.status_label = ctk.CTkLabel(
            self.footer_frame,
            text="Ready - Select a payload to generate",
            font=ctk.CTkFont(size=12),
            text_color="gray60"
        )
        self.status_label.pack(side="left")
        
        self.credits_label = ctk.CTkLabel(
            self.footer_frame,
            text="Made with ❤️ for penetration testers",
            font=ctk.CTkFont(size=12),
            text_color="gray60"
        )
        self.credits_label.pack(side="right")
        
    def get_current_payloads(self):
        """Get the payload dictionary based on current OS selection"""
        if self.os_var.get() == "Linux":
            return LINUX_PAYLOADS
        else:
            return WINDOWS_PAYLOADS
    
    def update_payload_dropdown(self):
        """Update the payload dropdown based on OS selection"""
        payloads = self.get_current_payloads()
        payload_names = list(payloads.keys())
        
        # Update dropdown values
        self.payload_dropdown.configure(values=payload_names)
        
        # Auto-select first payload so menu is never empty
        if payload_names:
            self.payload_name_var.set(payload_names[0])
            self.generate_payload()
        
        # Update status
        self.status_label.configure(
            text=f"Found {len(payload_names)} payloads for {self.os_var.get()}"
        )
        
    def on_payload_change(self, selected_payload: str):
        """Handle payload selection change from dropdown"""
        self.payload_name_var.set(selected_payload)
        self.generate_payload()
        
    def on_os_change(self, *args):
        """Handle OS selection change"""
        self.update_payload_dropdown()
        self.update_listener()
        
    def on_input_change(self, *args):
        """Handle IP/Port/Encoding changes"""
        self.update_listener()
        if self.payload_name_var.get():
            self.generate_payload()
            
    def update_listener(self):
        """Update the listener command"""
        port = self.port_var.get() or "4444"
        
        # Generate listener based on OS
        if self.os_var.get() == "Linux":
            listener = f"nc -lvnp {port}"
        else:
            listener = f"nc.exe -lvnp {port}"
        
        self.listener_textbox.delete("1.0", "end")
        self.listener_textbox.insert("1.0", listener)
        
    def generate_payload(self):
        """Generate the selected payload with IP/Port substitution and encoding"""
        payload_name = self.payload_name_var.get()
        if not payload_name:
            return
            
        # Get payload template
        payloads = self.get_current_payloads()
            
        if payload_name not in payloads:
            return
            
        payload = payloads[payload_name]
        
        # Replace placeholders
        ip = self.ip_var.get() or "10.10.10.10"
        port = self.port_var.get() or "4444"
        
        payload = payload.replace("{ip}", ip)
        payload = payload.replace("{port}", port)
        
        # Apply encoding
        encoding = self.encoding_var.get()
        if encoding == "Base64":
            payload = base64.b64encode(payload.encode()).decode()
        elif encoding == "URL":
            payload = urllib.parse.quote(payload)
        elif encoding == "Double URL":
            payload = urllib.parse.quote(urllib.parse.quote(payload))
            
        # Update output
        self.payload_textbox.delete("1.0", "end")
        self.payload_textbox.insert("1.0", payload)
        
        # Update status
        encoding_info = f" ({encoding} encoded)" if encoding != "None" else ""
        self.status_label.configure(
            text=f"Generated: {payload_name}{encoding_info}"
        )
        
    def copy_to_clipboard(self, textbox: ctk.CTkTextbox):
        """Copy text from textbox to clipboard"""
        text = textbox.get("1.0", "end").strip()
        
        if CLIPBOARD_AVAILABLE:
            pyperclip.copy(text)
            self.status_label.configure(text="✅ Copied to clipboard!")
        else:
            # Fallback using tkinter
            self.clipboard_clear()
            self.clipboard_append(text)
            self.status_label.configure(text="✅ Copied to clipboard!")
            
        # Reset status after 2 seconds
        self.after(2000, lambda: self.status_label.configure(
            text=f"Ready - {self.payload_name_var.get() or 'Select a payload'}"
        ))
        
    def toggle_fullscreen(self, event=None):
        """Toggle fullscreen mode"""
        self.is_fullscreen = not self.is_fullscreen
        self.attributes("-fullscreen", self.is_fullscreen)
        
        if self.is_fullscreen:
            self.fullscreen_btn.configure(text="⛶ Exit Fullscreen")
        else:
            self.fullscreen_btn.configure(text="⛶ Fullscreen")
            
    def exit_fullscreen(self, event=None):
        """Exit fullscreen mode"""
        if self.is_fullscreen:
            self.is_fullscreen = False
            self.attributes("-fullscreen", False)
            self.fullscreen_btn.configure(text="⛶ Fullscreen")


def main():
    """Main entry point"""
    app = RevShellGenerator()
    app.mainloop()


if __name__ == "__main__":
    main()
