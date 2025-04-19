# examples/bootstrap.py
import os
import sys
def apply():

    sys.path.append('src')
    sys.path.append('src/pygame')
    sys.path.append('src/config')

    import bootstrap_bindings
    from bootstrap_bindings import setup_paths
    setup_paths()

