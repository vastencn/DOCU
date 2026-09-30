import sys
import os

# Ensure the root directory is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.ui.app import FileBrowserApp

def main():
    initial_dir = r"E:\DOCU"
    if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
        initial_dir = sys.argv[1]
        
    app = FileBrowserApp(initial_dir=initial_dir)
    app.mainloop()

if __name__ == "__main__":
    main()
