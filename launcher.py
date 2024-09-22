#!/bin/python3
import json
import os.path

import nogamename
import customtkinter
import threading

name_entry: customtkinter.CTkEntry
room_entry: customtkinter.CTkEntry
label: customtkinter.CTkLabel
config: dict


def save_config(new_config: dict):
    config_path = os.environ.get("VAR_DIR", ".")
    config_path = config_path + "/config.json"
    with open(config_path, "w") as f:
        f.write(json.dumps(new_config))


def load_config() -> dict:
    config_path = os.environ.get("VAR_DIR", ".")
    config_path = config_path + "/config.json"
    config: dict
    defaults = {
        "name": "",
        "color": "black",
        "room_code": ""
    }
    if not os.path.exists(config_path):
        config = defaults
    else:
        with open(config_path, "rb") as f:
            config = json.load(f)
    for req_objects in defaults.keys():
        if req_objects not in config:
            print(f"Warning: Corrupt Config File: no '{req_objects}' ")
            config[req_objects] = defaults[req_objects]
    print(config)
    return config


def set_status(status: str):
    global label
    label.configure(text=f"Status: {status}")


def start():
    global name_entry, config, room_entry
    if name_entry.get() == "":
        set_status("Please Enter Username")
    elif room_entry.get() == "":
        set_status("Please Enter Room Code")
    else:
        config["name"] = name_entry.get()
        config["room_code"] = room_entry.get()
        set_status("Initializing")
        print(config['color'])
        nogamename.init((740, 600), f"NoGameName (Player: {config['name']})", "Times New Roman", 12, config['name'], config['color'], config['room_code'])
        set_status("Running")
        nogamename.main()
        set_status("Ready")


def start_callback():
    start()
    # run_thread = threading.Thread(target=start)
    # run_thread.start()


def main():
    global name_entry, label, config, room_entry

    os.chdir(os.environ.get("APP_DIR", "./"))

    app = customtkinter.CTk(className="NoGameName")
    app.title("NoGameName Launcher")
    app.geometry("350x250")
    app.columnconfigure(0, weight=1)
    app.grid_rowconfigure(0, weight=1)

    config = load_config()

    status_frame = customtkinter.CTkFrame(app)
    status_frame.grid(row=3, column=0, padx=20, pady=20, sticky="ew")
    name_entry = customtkinter.CTkEntry(app, placeholder_text="Username")
    if len(config["name"]) != 0:
        name_entry.setvar(config["name"])
    name_entry.grid(row=0, column=0, padx=20, pady=20, sticky="new")
    room_entry = customtkinter.CTkEntry(app, placeholder_text="Room Code")
    if len(config["room_code"]) != 0:
        room_entry.setvar(config["room_code"])
    room_entry.grid(row=1, column=0, padx=20, pady=20, sticky="new")
    button = customtkinter.CTkButton(app, text="Start", command=start_callback)
    button.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
    label = customtkinter.CTkLabel(status_frame, text="")
    label.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

    set_status("Ready")

    app.mainloop()
    save_config(config)


if __name__ == '__main__':
    main()
