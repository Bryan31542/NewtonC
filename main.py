import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror
from NewtonC import solve

if __name__ == '__main__':
    # Root window
    root = tk.Tk()
    root.title("Newton in Complex")
    root.minsize(250, 275)
    root.resizable(False, False)

    # Frame
    frame = ttk.Frame(root)

    # Field Options
    options = {"padx": 5, "pady": 5}

    # Labels
    title_label = ttk.Label(frame, text="Newton in Complex")
    title_label.grid(column=2, row=0, sticky="W", **options)

    f_label = ttk.Label(frame, text="f(x) = ")
    f_label.grid(column=1, row=1, sticky="E", **options)

    z_real_label = ttk.Label(frame, text="z real = ")
    z_real_label.grid(column=1, row=2, sticky="E", **options)

    z_imag_label = ttk.Label(frame, text="z imaginary = ")
    z_imag_label.grid(column=1, row=3, sticky="E", **options)

    tol_label = ttk.Label(frame, text="TOL = ")
    tol_label.grid(column=1, row=4, sticky="E", **options)

    filename_label = ttk.Label(frame, text="Filename = ")
    filename_label.grid(column=1, row=5)

    frame.grid(padx=10, pady=10)

    # Entries
    f_function = tk.StringVar()
    f_entry = ttk.Entry(frame, textvariable=f_function)
    f_entry.grid(column=2, row=1, **options)
    f_entry.focus()

    z_real_value = tk.StringVar()
    z_real_entry = ttk.Entry(frame, textvariable=z_real_value)
    z_real_entry.grid(column=2, row=2, **options)

    z_imag_value = tk.StringVar()
    z_imag_entry = ttk.Entry(frame, textvariable=z_imag_value)
    z_imag_entry.grid(column=2, row=3, **options)

    tol_value = tk.StringVar()
    tol_entry = ttk.Entry(frame, textvariable=tol_value)
    tol_entry.grid(column=2, row=4, **options)

    filename_value = tk.StringVar()
    filename_entry = ttk.Entry(frame, textvariable=filename_value)
    filename_entry.grid(column=2, row=5, **options)

    frame.grid(padx=10, pady=10)

    # Button function
    def handleCalculate():
        try:
            f = f_function.get()
            z0 = complex(float(z_real_value.get()), float(z_imag_value.get()))
            tol = eval(tol_value.get())
            filename = filename_value.get()

            try:
                solve(f, z0, tol, filename)
                result_label.config(text="PDF generated!")

            except ValueError as e:
                showerror(title="Error", message=str(e))
        except ValueError as e:
            showerror(title="Error", message=str(e))

    # Button
    calculate_button = ttk.Button(frame, text="Calculate")
    calculate_button.grid(column=2, row=6, **options)
    calculate_button.configure(command=handleCalculate)

    # Success message
    result_label = ttk.Label(frame)
    result_label.grid(column=2, row=7, **options)

    root.mainloop()
