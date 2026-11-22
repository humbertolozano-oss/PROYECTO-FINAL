import tkinter as tk
from ui.app_gui import SimuladorGUI

def main():
    root = tk.Tk()
    app = SimuladorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
    