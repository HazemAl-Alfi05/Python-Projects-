import tkinter as tk
from tkinter import messagebox


def start_timer():
    """Starts the countdown tracking loop if it isn't already running."""
    global is_running
    if not is_running:
        is_running = True
        countdown(time_left)


def pause_timer():
    """Pauses the active countdown loop."""
    global is_running
    is_running = False


def reset_timer():
    """Resets the timer back to the default 25-minute work block."""
    global is_running, time_left, current_mode
    is_running = False
    current_mode = "Work"
    time_left = 25 * 60  # 25 minutes back to seconds

    # Reset GUI labels
    mode_label.config(text="WORK SESSION", fg="#ff3333")
    update_timer_display(time_left)


def countdown(seconds):
    """The recursive engine that drops the time remaining by 1 every second."""
    global time_left, current_mode

    # Exit the loop immediately if the user hits the pause button
    if not is_running:
        return

    if seconds > 0:
        time_left = seconds - 1
        update_timer_display(time_left)
        # Tell Tkinter to run this exact function again in 1000 milliseconds (1 second)
        root.after(1000, countdown, time_left)
    else:
        # The clock hit 00:00! Switch between Work and Break modes automatically
        if current_mode == "Work":
            messagebox.showinfo("Break Time!", "Great job! Take a short 5-minute break.")
            current_mode = "Break"
            time_left = 5 * 60  # 5 minutes in seconds
            mode_label.config(text="BREAK TIME", fg="#00ffcc")
        else:
            messagebox.showinfo("Back to Work", "Break is over! Time to focus for 25 minutes.")
            current_mode = "Work"
            time_left = 25 * 60  # 25 minutes in seconds
            mode_label.config(text="WORK SESSION", fg="#ff3333")

        update_timer_display(time_left)
        countdown(time_left)


def update_timer_display(seconds):
    """Converts raw total seconds into a clean MM:SS format layout string."""
    minutes = seconds // 60
    secs = seconds % 60
    # format as 2 digits with a leading zero if needed (e.g., 05:09)
    time_string = f"{minutes:02d}:{secs:02d}"
    clock_label.config(text=time_string)


# =====================================================================
# GLOBAL STATE VARIABLES
# =====================================================================
is_running = False
current_mode = "Work"
time_left = 25 * 60  # 25 minutes translated natively into total seconds

# =====================================================================
# GUI LAYOUT DESIGN
# =====================================================================

root = tk.Tk()
root.title("Focus Timer Engine")
root.geometry("400x350")
root.configure(bg="#1c1c1e")  # High-contrast clean studio dark tone

# Current Mode Tracking Label
mode_label = tk.Label(
    root,
    text="WORK SESSION",
    font=("Arial", 14, "bold"),
    bg="#1c1c1e",
    fg="#ff3333",  # Punchy red for focus mode
)
mode_label.pack(pady=25)

# Giant Digital Clock Display Face
clock_label = tk.Label(
    root,
    text="25:00",
    font=("Consolas", 48, "bold"),
    bg="#1c1c1e",
    fg="#ffffff",
)
clock_label.pack(pady=10)

# Control Buttons Layout Container Row
button_frame = tk.Frame(root, bg="#1c1c1e")
button_frame.pack(pady=30)

start_button = tk.Button(
    button_frame,
    text="START",
    font=("Arial", 10, "bold"),
    bg="#00ffcc",
    fg="#1c1c1e",
    command=start_timer,
    relief="flat",
    width=8,
)
start_button.grid(row=0, column=0, padx=8)

pause_button = tk.Button(
    button_frame,
    text="PAUSE",
    font=("Arial", 10, "bold"),
    bg="#f0b90b",
    fg="#1c1c1e",
    command=pause_timer,
    relief="flat",
    width=8,
)
pause_button.grid(row=0, column=1, padx=8)

reset_button = tk.Button(
    button_frame,
    text="RESET",
    font=("Arial", 10, "bold"),
    bg="#3a3a3c",
    fg="#ffffff",
    command=reset_timer,
    relief="flat",
    width=8,
)
reset_button.grid(row=0, column=2, padx=8)

# Run the primary layout loop window execution step
root.mainloop()