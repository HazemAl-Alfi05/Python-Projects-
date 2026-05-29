import tkinter as tk
from tkinter import ttk
import requests


def fetch_rates_and_convert():
    """Fetches real-time exchange rates and calculates the conversion directly."""
    base_curr = base_currency_box.get()
    target_curr = target_currency_box.get()

    # Read the amount straight from the entry box and convert it to a float
    amount = float(amount_entry.get().strip())

    # Grab the live data from the public API
    url = f"https://open.er-api.com/v6/latest/{base_curr}"
    response = requests.get(url)
    data = response.json()

    # Read the target conversion multiplier from the rates dictionary
    rates = data["rates"]
    conversion_rate = rates[target_curr]

    # Calculate the conversion math
    final_result = amount * conversion_rate

    # Push the results directly onto the GUI window labels
    result_label.config(
        text=f"{amount:,.2f} {base_curr} = {final_result:,.2f} {target_curr}"
    )
    rate_info_label.config(
        text=f"Live Rate: 1 {base_curr} = {conversion_rate:.4f} {target_curr}"
    )


# =====================================================================
# GUI LAYOUT DESIGN
# =====================================================================

root = tk.Tk()
root.title("Currency Exchange Tracker")
root.geometry("450x380")
root.configure(bg="#1a1a2e")  # Deep navy background color tone

# Title Label
title_lbl = tk.Label(
    root,
    text="EXCHANGE ENGINE",
    font=("Courier", 18, "bold"),
    bg="#1a1a2e",
    fg="#00fff5",
)
title_lbl.pack(pady=20)

# Layout Grid Frame Workspace
main_frame = tk.Frame(root, bg="#1a1a2e")
main_frame.pack(pady=10)

# Amount Input Box
tk.Label(
    main_frame, text="Amount:", font=("Arial", 10), bg="#1a1a2e", fg="#ffffff"
).grid(row=0, column=0, sticky="w", pady=5)
amount_entry = tk.Entry(
    main_frame, font=("Arial", 11), width=15, bg="#2e2e4f", fg="#ffffff"
)
amount_entry.grid(row=0, column=1, pady=5, padx=5)

# Dropdown Menu Options List
currency_options = ["USD", "EUR", "GBP", "JOD", "AED", "SAR", "EGP", "JPY", "CAD"]

# From Currency Dropdown Menu
tk.Label(
    main_frame, text="From:", font=("Arial", 10), bg="#1a1a2e", fg="#ffffff"
).grid(row=1, column=0, sticky="w", pady=5)
base_currency_box = ttk.Combobox(
    main_frame, values=currency_options, width=13, state="readonly"
)
base_currency_box.grid(row=1, column=1, pady=5, padx=5)
base_currency_box.set("USD")

# To Currency Dropdown Menu
tk.Label(
    main_frame, text="To:", font=("Arial", 10), bg="#1a1a2e", fg="#ffffff"
).grid(row=2, column=0, sticky="w", pady=5)
target_currency_box = ttk.Combobox(
    main_frame, values=currency_options, width=13, state="readonly"
)
target_currency_box.grid(row=2, column=1, pady=5, padx=5)
target_currency_box.set("JOD")

# Action Button
convert_btn = tk.Button(
    root,
    text="CONVERT NOW",
    font=("Arial", 10, "bold"),
    bg="#00fff5",
    fg="#1a1a2e",
    command=fetch_rates_and_convert,
    relief="flat",
    padx=15,
    pady=5,
)
convert_btn.pack(pady=15)

# Results Display Frame Workspace
results_frame = tk.Frame(root, bg="#1a1a2e")
results_frame.pack(pady=5)

result_label = tk.Label(
    results_frame,
    text="0.00 USD = 0.00 JOD",
    font=("Arial", 13, "bold"),
    bg="#1a1a2e",
    fg="#ffffff",
)
result_label.pack(pady=3)

rate_info_label = tk.Label(
    results_frame,
    text="Live Rate: --",
    font=("Arial", 10, "italic"),
    bg="#1a1a2e",
    fg="#00fff5",
)
rate_info_label.pack(pady=2)

# Start running the interface window loop
root.mainloop()