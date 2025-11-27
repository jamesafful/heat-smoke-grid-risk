# Ensure 'src' is on sys.path for local execution without installation
import sys, os
root = os.path.dirname(__file__)
src_path = os.path.join(root, "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)
