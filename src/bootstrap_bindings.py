import os
import sys
import platform

def setup_paths():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    # Updated to use the new build location
    bindings_dir = os.path.join(project_root, "build", "python")

    if platform.system() == "Windows":
        # For Windows, we might need to adjust this path
        if hasattr(os, 'add_dll_directory'):
            os.add_dll_directory(bindings_dir)

    if bindings_dir not in sys.path:
        sys.path.insert(0, bindings_dir)
    print("bindings_dir =", bindings_dir)
