import os
import sys
import platform

def setup_paths():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    bindings_dir = os.path.join(project_root, "cpplib", "python_bindings")

    if platform.system() == "Windows":
        bindings_dir = os.path.join(bindings_dir, "Release")
        if hasattr(os, 'add_dll_directory'):
            os.add_dll_directory(bindings_dir)

    if bindings_dir not in sys.path:
        sys.path.insert(0, bindings_dir)
    print("bindings_dir =", bindings_dir)
