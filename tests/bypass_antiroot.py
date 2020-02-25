from RootBypass import *

import pyjadx
import frida
import pygments
import os
import sys
import pathlib

# pyjadx
jadx = pyjadx.Jadx()
app_path = pathlib.Path("panelpower.apk").resolve().absolute()
app = jadx.load(app_path.as_posix())

jscode = 'Java.perform(function() {\n' + MakeBypassScript(app) + '});\n'
print(jscode)

# frida binding
TargetPackage = "com.embrain.panelpower";
def on_message(message, data):
    print("{} -> {}".format(message, data))

try:
    device = frida.get_usb_device(timeout = 10)
    pid = device.spawn([TargetPackage])
    print("[+] Target App is Running..")
    process = device.attach(pid)
    device.resume(pid)
    script = process.create_script(jscode)
    script.on('message', on_message)
    print("[+] Running Frida")
    script.load()
    sys.stdin.read()

except Exception as e:
    print(e)