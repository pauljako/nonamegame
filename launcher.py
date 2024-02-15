#!/bin/python3
import nogamename
import customtkinter
import threading

entry: customtkinter.CTkEntry
label: customtkinter.CTkLabel


def set_status(status: str):
    global label
    label.configure(text=f"Status: {status}")


def start():
    global entry
    if entry.get() == "":
        set_status("Please Enter Username")
    else:
        set_status("Initializing")
        nogamename.init((740, 600), f"NoGameName (Player: {entry.get()})", "Times New Roman", 12, entry.get())
        set_status("Running")
        nogamename.main()
        set_status("Ready")


def start_callback():
    run_thread = threading.Thread(target=start)
    run_thread.start()


def main():
    global entry, label
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


if __name__ == '__main__':
    main()
