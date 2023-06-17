import tkinter as tk
import time
import pyrebase

class TypingSpeedLogger:
    def __init__(self):
        self.typing_start_time = 0
        self.typed_characters = []
        self.prev_key_press_time = None
        self.current_profile = None

    def on_key_press(self, event):
        if self.typing_start_time == 0:
            self.typing_start_time = time.time()

        current_time = time.time()
        key_press_time = current_time - self.typing_start_time
        key_press_delta = key_press_time - self.prev_key_press_time if self.prev_key_press_time else 0

        # Log the key and its time information
        self.typed_characters.append((event.char, key_press_delta, key_press_time))
        self.prev_key_press_time = key_press_time

        # Select profile based on key press
        if event.char == '1':
            self.select_profile("Suhaib")
        elif event.char == '2':
            self.select_profile("Salehin")
        elif event.char == '3':
            self.select_profile("Mustafa")

    def on_key_release(self, event):
        if event.char == '\r':  # Check if "Enter" key is pressed
            # Stop the typing speed logging when "Enter" key is pressed
            self.root.unbind("<KeyPress>")
            self.root.unbind("<KeyRelease>")
            print("Typing speed log:")
            for character, delta, time in self.typed_characters:
                print(f"Character: {character}\tDelta: {delta:.6f}s\tTime: {time:.6f}s")
            self.save_to_firebase()

    def select_profile(self, profile_name):
        self.current_profile = profile_name
        print(f"Selected profile: {profile_name}")

    def save_to_firebase(self):
        if self.current_profile is None:
            print("No profile selected. Please select a profile before saving.")
            return

        config = {
        "apiKey": "AIzaSyA3bH46x_LyPJUgsPZAtlh-fDDcZ50cao4",
        "authDomain": "suhaibhumid.firebaseapp.com",
        "databaseURL": "https://suhaibhumid-default-rtdb.firebaseio.com",
        "projectId": "suhaibhumid",
        "storageBucket": "suhaibhumid.appspot.com",
        "messagingSenderId": "924618277712",
        "appId": "1:924618277712:web:ce2ae64ba99745527ca255",
        "measurementId": "G-W9LQQ41SY7"
        }

        firebase = pyrebase.initialize_app(config)
        db = firebase.database()

        data = [{'character': char, 'delta': delta, 'time': time} for char, delta, time in self.typed_characters]
        db.child("typing_speed_logs").child(self.current_profile).push(data)
        print(f"Typing speed log saved to Firebase for profile: {self.current_profile}")

    def start_logging(self):
        self.typing_start_time = 0
        self.typed_characters = []
        self.prev_key_press_time = None
        self.current_profile = None

        self.root = tk.Tk()
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<KeyRelease>", self.on_key_release)
        self.root.mainloop()

# Create an instance of the TypingSpeedLogger and start logging
logger = TypingSpeedLogger()
logger.start_logging()
