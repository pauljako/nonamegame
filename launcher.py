#!/bin/python3
import nogamename
import customtkinter


def set_status(status: str):
    label.configure(text=f"Status: {status}")


def start_callback():
    if entry.get() == "":
        set_status("Please Enter Username")
    else:
        print(entry.get())


app = customtkinter.CTk()
app.title("NoNameGame Launcher")
app.geometry("350x200")
app.grid_columnconfigure(0, weight=1)


entry = customtkinter.CTkEntry(app, placeholder_text="Username")
entry.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
button = customtkinter.CTkButton(app, text="Start", command=start_callback)
button.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
label = customtkinter.CTkLabel(app, text="")
label.grid(row=3, column=0, padx=20, pady=20, sticky="ew")

set_status("Ready")

app.mainloop()
