import tkinter as tk
from tkinter import messagebox, ttk
import psutil


def update_metrics():
    """Fetches system metrics and updates the GUI labels instantly."""
    try:
        # 1. Fetch system CPU and Memory data
        cpu_usage = psutil.cpu_percent()
        memory = psutil.virtual_memory()

        # 2. Update the progress bars and labels
        cpu_label.config(text=f"CPU Usage: {cpu_usage}%")
        cpu_bar["value"] = cpu_usage

        mem_gb_used = memory.used / (1024**3)  # Convert bytes to GB
        mem_gb_total = memory.total / (1024**3)
        mem_label.config(
            text=f"RAM: {mem_gb_used:.2f} GB / {mem_gb_total:.1f} GB ({memory.percent}%)"
        )
        mem_bar["value"] = memory.percent

        # 3. Clear and refresh the Process Tree view list
        # Save what row PID you currently have selected before wiping the table
        selected_item = item_table.selection()
        selected_pid = (
            item_table.item(selected_item[0])["values"][0] if selected_item else None
        )

        # Clear the old rows out of the table
        for row in item_table.get_children():
            item_table.delete(row)

        # Grab running processes and sort them by memory consumption
        processes = []
        for proc in psutil.process_iter(["pid", "name", "memory_percent"]):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        top_processes = sorted(
            processes, key=lambda x: x["memory_percent"], reverse=True
        )[:10]

        # Insert fresh process data rows into our visual table
        for proc in top_processes:
            row_id = item_table.insert(
                "",
                "end",
                values=(
                    proc["pid"],
                    proc["name"],
                    f"{proc['memory_percent']:.1f}%",
                ),
            )
            # Re-apply the selection highlight if this row matches your saved selection
            if selected_pid and proc["pid"] == selected_pid:
                item_table.selection_set(row_id)

    except Exception as e:
        print(f"Error reading metrics: {e}")

    # Tell Tkinter to auto-run this exact function again in 2000 milliseconds (2 seconds)
    root.after(2000, update_metrics)


def kill_process():
    """Terminates the highlighted process in the table interface."""
    selected = item_table.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a process first.")
        return

    # Grab the data values from the highlighted row matrix
    row_values = item_table.item(selected[0])["values"]
    pid = int(row_values[0])
    name = row_values[1]

    # Double check with the user via a quick popup box
    confirm = messagebox.askyesno(
        "Confirm", f"Are you sure you want to stop {name} (PID: {pid})?"
    )
    if confirm:
        try:
            process = psutil.Process(pid)
            process.terminate()  # Closes down the app safely
            messagebox.showinfo("Success", f"Process {name} was closed.")
            update_metrics()  # Instantly update the list display
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            messagebox.showerror(
                "Error", "Could not close this process. Access Denied."
            )


# =====================================================================
# GUI LAYOUT DESIGN
# =====================================================================

root = tk.Tk()
root.title("Simple System Monitor")
root.geometry("550x500")
root.configure(bg="#212121")

# --- CPU and RAM Section ---
stats_frame = tk.LabelFrame(
    root,
    text=" Resource Usage ",
    bg="#212121",
    fg="#00ffcc",
    font=("Arial", 10, "bold"),
)
stats_frame.pack(fill="x", padx=15, pady=10)

cpu_label = tk.Label(
    stats_frame, text="CPU Usage: 0%", bg="#212121", fg="#ffffff", font=("Arial", 10)
)
cpu_label.pack(anchor="w", padx=10, pady=(5, 0))

cpu_bar = ttk.Progressbar(stats_frame, orient="horizontal", mode="determinate")
cpu_bar.pack(fill="x", padx=10, pady=(0, 10))

mem_label = tk.Label(
    stats_frame, text="RAM: 0%", bg="#212121", fg="#ffffff", font=("Arial", 10)
)
mem_label.pack(anchor="w", padx=10, pady=(5, 0))

mem_bar = ttk.Progressbar(stats_frame, orient="horizontal", mode="determinate")
mem_bar.pack(fill="x", padx=10, pady=(0, 10))

# --- Processes Table Section ---
proc_frame = tk.LabelFrame(
    root,
    text=" Top Processes by Memory ",
    bg="#212121",
    fg="#00ffcc",
    font=("Arial", 10, "bold"),
)
proc_frame.pack(fill="both", expand=True, padx=15, pady=10)

# Build a clean data grid layout using Treeview columns
item_table = ttk.Treeview(
    proc_frame, columns=("pid", "name", "mem"), show="headings", selectmode="browse"
)
item_table.heading("pid", text="PID")
item_table.heading("name", text="Process Name")
item_table.heading("mem", text="Memory Usage")

item_table.column("pid", width=70, anchor="center")
item_table.column("name", width=280, anchor="w")
item_table.column("mem", width=100, anchor="center")
item_table.pack(side="left", fill="both", expand=True, padx=5, pady=5)

# Add a basic scrollbar next to the grid list frame
table_scroll = ttk.Scrollbar(proc_frame, orient="vertical", command=item_table.yview)
item_table.configure(yscrollcommand=table_scroll.set)
table_scroll.pack(side="right", fill="y")

# --- Action Button ---
kill_button = tk.Button(
    root,
    text="End Selected Process",
    bg="#ff3333",
    fg="#ffffff",
    font=("Arial", 10, "bold"),
    command=kill_process,
)
kill_button.pack(pady=(0, 15))

# Kick off our initial update function loop cycle manually
update_metrics()

# Run the primary layout application interface loop window
root.mainloop()