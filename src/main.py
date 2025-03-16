import tkinter as tk
from roulette import Roulette

def main():
    root = tk.Tk()
    root.title("Simple Roulette")
    app = Roulette(root)
    root.mainloop()

if __name__ == "__main__":
    main()