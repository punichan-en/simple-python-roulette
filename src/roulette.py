import tkinter as tk
import random
import time

class Roulette:
    def __init__(self, master):
        self.master = master
        self.master.geometry("400x300")
        
        # 結果表示用ラベル
        self.result_label = tk.Label(
            master,
            text="?",
            font=("Helvetica", 72)
        )
        self.result_label.pack(pady=20)
        
        # スタートボタン
        self.start_button = tk.Button(
            master,
            text="Start",
            command=self.spin,
            width=20,
            height=2
        )
        self.start_button.pack(pady=20)
        
        self.is_spinning = False
        
    def spin(self):
        if not self.is_spinning:
            self.is_spinning = True
            self.start_button.config(state='disabled')
            self.animate_spin()
    
    def animate_spin(self):
        if self.is_spinning:
            number = random.randint(0, 36)
            self.result_label.config(text=str(number))
            self.master.after(100, self.animate_spin)
        else:
            self.start_button.config(state='normal')
    
    def stop_spin(self):
        self.is_spinning = False
        final_number = random.randint(0, 36)
        self.result_label.config(text=str(final_number))
        self.start_button.config(state='normal')