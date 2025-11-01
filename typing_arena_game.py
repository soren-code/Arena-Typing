import tkinter as tk
from tkinter import ttk
import random
import string
import time
import ttkbootstrap as tb


class TypingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Practice – Neon Arena")
        self.root.attributes("-fullscreen", True)
        self.style = tb.Style("cyborg")
        self.root.configure(bg="#000010")

        self.target_text = ""
        self.start_time = None
        self.current_index = 0
        self.correct = 0
        self.incorrect = 0
        self.running = False
        self.completed = False

        # Header with better spacing
        header_frame = ttk.Frame(root)
        header_frame.pack(pady=30)
        
        title = ttk.Label(
            header_frame, text="⚡ TYPING ARENA ⚡",
            font=("Consolas", 38, "bold"), foreground="#00FFFF", background="#000010"
        )
        title.pack()
        
        subtitle = ttk.Label(
            header_frame, text="Cyber Neon Edition",
            font=("Consolas", 16), foreground="#FF69B4", background="#000010"
        )
        subtitle.pack(pady=5)

        # Control panel with better layout
        control_frame = ttk.Frame(root)
        control_frame.pack(pady=20)

        ttk.Label(control_frame, text="Mode:", font=("Consolas", 16), foreground="#00FF99").grid(row=0, column=0, padx=10)
        self.mode_combo = ttk.Combobox(control_frame, font=("Consolas", 14), state="readonly", width=15)
        self.mode_combo["values"] = ["Letters", "Numbers", "Symbols", "Mixed", "Words", "Phrases", "Paragraphs"]
        self.mode_combo.current(4)  # Default to Words
        self.mode_combo.grid(row=0, column=1, padx=10)

        self.start_btn = ttk.Button(control_frame, text="▶ Start", command=self.start_game, bootstyle="success", width=12)
        self.start_btn.grid(row=0, column=2, padx=10)

        self.next_btn = ttk.Button(control_frame, text="⏭ Next", command=self.next_practice, bootstyle="info", width=12)
        self.next_btn.grid(row=0, column=3, padx=10)
        self.next_btn.config(state="disabled")

        self.restart_btn = ttk.Button(control_frame, text="↻ Restart", command=self.restart_game, bootstyle="warning", width=12)
        self.restart_btn.grid(row=0, column=4, padx=10)

        exit_btn = ttk.Button(control_frame, text="✕ Exit", command=self.exit_game, bootstyle="danger", width=12)
        exit_btn.grid(row=0, column=5, padx=10)

        # Text display area with border effect
        display_container = ttk.Frame(root)
        display_container.pack(pady=40)

        self.text_display = tk.Text(
            display_container, font=("Consolas", 26), wrap="word", width=70, height=8,
            bg="#001020", fg="#00FFFF", relief="solid", bd=2, highlightthickness=2,
            highlightbackground="#00FFFF", highlightcolor="#FF69B4", padx=20, pady=20
        )
        self.text_display.pack()
        self.text_display.configure(state="disabled")

        # Finger hint with icon
        self.finger_label = ttk.Label(
            root, text="👆 Select a mode and press Start to begin",
            font=("Consolas", 18, "bold"),
            background="#000010", foreground="#FFD700"
        )
        self.finger_label.pack(pady=15)

        # Entry field with better styling
        entry_frame = ttk.Frame(root)
        entry_frame.pack(pady=20)
        
        entry_label = ttk.Label(entry_frame, text="Type here:", font=("Consolas", 14), foreground="#00FF99")
        entry_label.pack(side="left", padx=10)
        
        self.entry = ttk.Entry(entry_frame, font=("Consolas", 20), width=60)
        self.entry.pack(side="left")
        self.entry.bind("<KeyRelease>", self.check_input)

        # Stats panel with better visibility
        stats_frame = ttk.Frame(root)
        stats_frame.pack(pady=25)
        
        self.stats_label = ttk.Label(
            stats_frame, text="WPM: 0 | Accuracy: 100% | Correct: 0 | Errors: 0",
            font=("Consolas", 20, "bold"),
            background="#000010", foreground="#00FF99"
        )
        self.stats_label.pack()

    def get_finger_for_key(self, char):
        left_hand = {
            'Left Pinky': 'qaz1`~',
            'Left Ring': 'wsx2',
            'Left Middle': 'edc3',
            'Left Index': 'rfvtgb45'
        }
        right_hand = {
            'Right Index': 'yhnujm67',
            'Right Middle': 'ik,8',
            'Right Ring': 'ol.9',
            'Right Pinky': 'p;:/?0-=[]\\\'\"'
        }

        char_lower = char.lower()
        
        if char == ' ':
            return "Thumb (Spacebar)"
        
        for finger, keys in left_hand.items():
            if char_lower in keys:
                return finger
        for finger, keys in right_hand.items():
            if char_lower in keys:
                return finger
        
        return "Special Key"

    def start_game(self):
        self.running = True
        self.completed = False
        self.correct = 0
        self.incorrect = 0
        self.current_index = 0
        self.start_time = time.time()
        self.entry.delete(0, tk.END)
        self.entry.focus()
        self.entry.config(state="normal")
        
        self.next_btn.config(state="disabled")
        self.start_btn.config(state="disabled")

        mode = self.mode_combo.get()
        self.target_text = self.get_text(mode)
        self.update_display_highlight()
        self.update_stats()

    def get_text(self, mode):
        words = ["python", "keyboard", "practice", "speed", "accuracy", "focus", "typing", "developer", "neon", 
                 "challenge", "innovation", "digital", "technology", "interface", "software"]
        
        phrases = [
            "practice makes perfect",
            "type fast and clean",
            "never give up",
            "focus on accuracy first",
            "code hard stay sharp",
            "the quick brown fox jumps over the lazy dog",
            "always save your work before closing",
            "a clear plan prevents confusion",
            "hard work beats talent when talent doesn't work",
            "every line of code is a step forward",
            "collaboration is the key to success",
            "patience and persistence produce results",
            "attention to detail separates good from great",
            "efficient typing improves productivity",
            "success comes to those who persevere"
        ]
        
        paragraphs = [
            "Typing is a fundamental skill that improves focus and productivity in the digital age. Regular practice helps in achieving speed and precision simultaneously.",
            
            "The quick brown fox jumps over the lazy dog every day to stay fit and agile. Typing similar sentences enhances your overall rhythm and consistency.",
            
            "Effective communication builds trust and clarity in every relationship. It involves listening carefully and responding thoughtfully to others.",
            
            "Technology has transformed the modern world in extraordinary ways. It connects people across continents and drives innovation in every industry.",
            
            "Discipline is the foundation of every successful endeavor. It teaches individuals to remain consistent even when motivation fades away.",
            
            "Continuous learning keeps the mind active and adaptable in a rapidly evolving world. Acquiring new knowledge ensures relevance and confidence.",
            
            "Cybersecurity awareness is more critical than ever in today's digital age. Understanding risks and applying preventive measures protects our data."
        ]

        if mode == "Letters":
            return ''.join(random.choices(string.ascii_letters, k=15))
        elif mode == "Numbers":
            return ''.join(random.choices(string.digits, k=12))
        elif mode == "Symbols":
            return ''.join(random.choices("!@#$%^&*()_+[]{};:',.<>?/", k=12))
        elif mode == "Mixed":
            return ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%", k=15))
        elif mode == "Words":
            return ' '.join(random.choices(words, k=6))
        elif mode == "Phrases":
            return random.choice(phrases)
        elif mode == "Paragraphs":
            return random.choice(paragraphs)
        else:
            return "Welcome to Typing Arena!"

    def update_display_highlight(self):
        self.text_display.configure(state="normal")
        self.text_display.delete("1.0", tk.END)

        self.text_display.insert("1.0", self.target_text)
        self.text_display.tag_configure("normal", foreground="#00FFFF")
        self.text_display.tag_add("normal", "1.0", "end")

        if self.current_index < len(self.target_text):
            start = f"1.0 + {self.current_index} chars"
            end = f"1.0 + {self.current_index+1} chars"
            self.text_display.tag_configure("highlight", foreground="#000000", background="#FFD700", 
                                           font=("Consolas", 26, "bold"))
            self.text_display.tag_add("highlight", start, end)

            next_char = self.target_text[self.current_index]
            finger_hint = self.get_finger_for_key(next_char)
            if next_char == ' ':
                self.finger_label.configure(text=f"👆 Press SPACEBAR | Use: {finger_hint}")
            else:
                self.finger_label.configure(text=f"👆 Type: '{next_char}' | Use: {finger_hint}")
        else:
            self.finger_label.configure(text="✅ Practice Complete! Press Next or Restart")

        self.text_display.configure(state="disabled")

    def check_input(self, event):
        if not self.running or self.current_index >= len(self.target_text):
            return

        typed = self.entry.get()
        expected = self.target_text[:len(typed)]

        if typed == expected:
            self.correct = len(typed)
        else:
            self.incorrect += 1

        if len(typed) >= len(self.target_text):
            self.end_game()
            return

        self.current_index = len(typed)
        self.update_display_highlight()
        self.update_stats()

    def update_stats(self):
        if not self.start_time:
            return
            
        elapsed = max(time.time() - self.start_time, 1)
        wpm = round((self.correct / 5) / (elapsed / 60))
        total_chars = self.correct + self.incorrect
        accuracy = round((self.correct / max(total_chars, 1)) * 100, 1)
        
        self.stats_label.configure(
            text=f"WPM: {wpm} | Accuracy: {accuracy}% | Correct: {self.correct} | Errors: {self.incorrect}"
        )

    def end_game(self):
        self.running = False
        self.completed = True
        self.entry.config(state="disabled")
        self.next_btn.config(state="normal")
        self.start_btn.config(state="normal")
        
        elapsed = max(time.time() - self.start_time, 1)
        wpm = round((self.correct / 5) / (elapsed / 60))
        total_chars = self.correct + self.incorrect
        accuracy = round((self.correct / max(total_chars, 1)) * 100, 1)

        summary = (
            f"🎯 Practice Complete!\n\n"
            f"⚡ WPM: {wpm}\n"
            f"✓ Correct Characters: {self.correct}\n"
            f"✗ Errors: {self.incorrect}\n"
            f"📊 Accuracy: {accuracy}%\n"
            f"⏱ Time: {round(elapsed, 1)}s\n\n"
            f"Press 'Next' for a new challenge!"
        )

        self.text_display.configure(state="normal")
        self.text_display.delete("1.0", tk.END)
        self.text_display.insert("1.0", summary)
        self.text_display.tag_configure("summary", foreground="#00FF99", font=("Consolas", 20, "bold"))
        self.text_display.tag_add("summary", "1.0", "end")
        self.text_display.configure(state="disabled")
        
        self.finger_label.configure(text="🎉 Great job! Ready for the next challenge?")

    def next_practice(self):
        """Load next practice text in the same mode"""
        if not self.completed:
            return
        
        self.entry.config(state="normal")
        self.start_game()

    def restart_game(self):
        self.entry.delete(0, tk.END)
        self.entry.config(state="normal")
        self.stats_label.configure(text="WPM: 0 | Accuracy: 100% | Correct: 0 | Errors: 0")
        self.finger_label.configure(text="👆 Select a mode and press Start to begin")
        
        self.text_display.configure(state="normal")
        self.text_display.delete("1.0", tk.END)
        self.text_display.insert("1.0", "Ready to practice? Select your mode and hit Start!")
        self.text_display.tag_configure("ready", foreground="#FFD700")
        self.text_display.tag_add("ready", "1.0", "end")
        self.text_display.configure(state="disabled")
        
        self.next_btn.config(state="disabled")
        self.start_btn.config(state="normal")
        self.completed = False
        self.running = False

    def exit_game(self):
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = TypingGame(root)
    root.mainloop()
