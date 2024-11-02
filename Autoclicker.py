import time
import json
import keyboard
import mouse
import tkinter as tk
from tkinter import ttk
from threading import Thread, Event

class AutoClickerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Auto Clicker")
        self.root.geometry("300x400")
        
        # Default settings
        self.default_settings = {
            "interval": 1.0,
            "toggle_key": "f6"
        }
        
        # Load or create settings
        self.settings = self.load_settings()
        
        # Control variables
        self.clicking = Event()
        self.running = True
        
        self.setup_gui()
        self.setup_hotkey()
        
        # Start the clicking thread
        self.click_thread = Thread(target=self.auto_click, daemon=True)
        self.click_thread.start()
    
    def load_settings(self):
        try:
            with open("autoclicker_settings.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return self.default_settings.copy()
    
    def save_settings(self):
        with open("autoclicker_settings.json", "w") as f:
            json.dump(self.settings, f)
    
    def setup_gui(self):
        # Interval settings
        interval_frame = ttk.LabelFrame(self.root, text="Click Interval", padding=10)
        interval_frame.pack(fill="x", padx=10, pady=5)
        
        self.interval_var = tk.StringVar(value=str(self.settings["interval"]))
        ttk.Label(interval_frame, text="Interval (seconds):").pack()
        interval_entry = ttk.Entry(interval_frame, textvariable=self.interval_var)
        interval_entry.pack(fill="x")
        
        # Hotkey settings
        hotkey_frame = ttk.LabelFrame(self.root, text="Toggle Hotkey", padding=10)
        hotkey_frame.pack(fill="x", padx=10, pady=5)
        
        self.hotkey_var = tk.StringVar(value=self.settings["toggle_key"])
        ttk.Label(hotkey_frame, text="Current hotkey:").pack()
        self.hotkey_label = ttk.Label(hotkey_frame, text=self.settings["toggle_key"])
        self.hotkey_label.pack()
        
        self.change_key_button = ttk.Button(hotkey_frame, text="Change Hotkey", command=self.change_hotkey)
        self.change_key_button.pack(pady=5)
        
        # Status
        status_frame = ttk.LabelFrame(self.root, text="Status", padding=10)
        status_frame.pack(fill="x", padx=10, pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Stopped")
        self.status_label.pack()
        
        # Apply button
        self.apply_button = ttk.Button(self.root, text="Apply Settings", command=self.apply_settings)
        self.apply_button.pack(pady=10)
    
    def setup_hotkey(self):
        keyboard.on_press_key(self.settings["toggle_key"], self.toggle_clicking)
    
    def change_hotkey(self):
        self.change_key_button.config(state="disabled")
        self.hotkey_label.config(text="Press any key...")
        
        def on_key(event):
            if event.name != "escape":  # Allow escape to cancel
                # Remove old hotkey
                keyboard.remove_hotkey(self.settings["toggle_key"])
                
                # Set new hotkey
                self.settings["toggle_key"] = event.name
                self.hotkey_label.config(text=event.name)
                self.setup_hotkey()
            
            self.change_key_button.config(state="normal")
            keyboard.unhook_all()
        
        keyboard.on_press(on_key)
    
    def apply_settings(self):
        try:
            self.settings["interval"] = float(self.interval_var.get())
            self.save_settings()
        except ValueError:
            self.interval_var.set(str(self.settings["interval"]))
    
    def toggle_clicking(self, _=None):
        if self.clicking.is_set():
            self.clicking.clear()
            self.status_label.config(text="Stopped")
        else:
            self.clicking.set()
            self.status_label.config(text="Running")
    
    def auto_click(self):
        while self.running:
            if self.clicking.is_set():
                mouse.click()
                time.sleep(self.settings["interval"])
    
    def run(self):
        try:
            self.root.mainloop()
        finally:
            self.running = False
            self.clicking.clear()

if __name__ == "__main__":
    app = AutoClickerApp()
    app.run()