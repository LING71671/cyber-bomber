import uiautomation as auto
import ctypes
import sys

# Set stdout encoding to utf-8 for Windows console
sys.stdout.reconfigure(encoding='utf-8')

def list_windows():
    print(f"{'Handle':<10} | {'ControlType':<15} | {'ClassName':<30} | {'Name'}")
    print("-" * 100)
    
    root = auto.GetRootControl() 
    for control in root.GetChildren():
        # Check visibility
        is_visible = False
        if control.NativeWindowHandle:
            is_visible = ctypes.windll.user32.IsWindowVisible(control.NativeWindowHandle)
        
        # We list EVERYTHING visible, not just WindowControl, to see if QQ is hiding as a Pane or something
        if is_visible:
            print(f"{control.NativeWindowHandle:<10} | {control.ControlTypeName:<15} | {control.ClassName:<30} | {control.Name}")

if __name__ == "__main__":
    list_windows()
