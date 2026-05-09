#!/usr/bin/env python3
import os
import sys
import subprocess
import platform

# parse args
NOBUILD = any(arg.lower() == "nobuild" for arg in sys.argv[1:])

# set paths here
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# dynamic Godot binary path based on OS
if platform.system() == "Windows":
    GODOT_GLOB = os.path.join(ROOT, "bin", "godot", "Godot_v*_win64.exe")
else:
    GODOT_GLOB = os.path.join(ROOT, "bin", "godot", "Godot_v*_linux.x86_64")

import glob
matches = glob.glob(GODOT_GLOB)
if not matches:
    print(f"ERROR: No Godot executable found in {os.path.join(ROOT, 'bin', 'godot')}")
    print(f"Expected pattern: {os.path.basename(GODOT_GLOB)}")
    print(f"\nDownload Godot from here: https://godotengine.org/download")
    print(f"And put it in ./bin/godot folder")
    input("Press Enter to continue...")
    sys.exit(1)

GODOT = matches[0]
PROJECT = os.path.join(ROOT, "project")

print(f"Using Godot: {GODOT}")
print(f"Project:     {PROJECT}")
print(f"Root:        {ROOT}")

# clone godot-cpp if missing
GODOT_CPP = os.path.join(ROOT, "godot-cpp")
if not os.path.isdir(GODOT_CPP):
    print("godot-cpp not found, cloning...")
    result = subprocess.run(
        ["git", "clone", "--depth", "1",
         "https://github.com/godotengine/godot-cpp", "godot-cpp"],
        cwd=ROOT
    )
    if result.returncode != 0:
        print("ERROR: Failed to clone godot-cpp")
        input("Press Enter to continue...")
        sys.exit(1)
    print("godot-cpp cloned successfully.")

# compile if its on building mode
if not NOBUILD:
    print("Compiling extension...")
    plat = "windows" if platform.system() == "Windows" else "linux"
    result = subprocess.run(
        ["scons", f"platform={plat}", "target=template_debug"],
        cwd=ROOT
    )
    if result.returncode != 0:
        print("ERROR: Failed to compile")
        input("Press Enter to continue...")
        sys.exit(1)

# open godot
print("Opening project in Godot...")
subprocess.Popen([GODOT, "--path", PROJECT, "--editor"])
