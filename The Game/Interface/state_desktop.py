import tkinter as tk
import requests
import time
from threading import Thread
import gui_config  # Import the GUI configuration

# Function to get the current game state from the Flask API
def get_game_state():
    response = requests.get('http://127.0.0.1:5000/get_field')
    if response.status_code == 200:
        return response.json()['game_field']
    else:
        return None

# Function to update the GUI with the game field
def update_gui(root, field):
    for widget in root.winfo_children():
        widget.destroy()

    for i, row in enumerate(field):
        for j, cell in enumerate(row):
            cell_abbr = cell[:3]  # Abbreviate the cell name to 3 letters
            color = gui_config.CELL_COLORS.get(cell, "white")  # Use colors from the configuration
            label = tk.Label(root, text=cell_abbr, bg=color, width=4, height=2)
            label.grid(row=i, column=j)

# Function to periodically refresh the game state
def periodic_refresh(root, interval=1.0):
    while True:
        field = get_game_state()
        if field:
            root.after(0, update_gui, root, field)
        time.sleep(interval)

# Create the main window
root = tk.Tk()
root.title("Game State Visualization")

# Start the periodic refresh in a separate thread
Thread(target=periodic_refresh, args=(root, 1.0), daemon=True).start()

# Start the GUI event loop
root.mainloop()
