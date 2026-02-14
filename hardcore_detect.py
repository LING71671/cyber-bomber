import psutil
import win32gui
import win32process
import sys
import ctypes

# Set stdout to handle Chinese characters correctly in Windows console
sys.stdout.reconfigure(encoding='utf-8') # type: ignore

def get_hwnds_for_pid(pid):
    """
    Return a list of window handles (HWND) belonging to a specific Process ID (PID).
    """
    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            try:
                # Get the thread ID and process ID for this window
                _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                if found_pid == pid:
                    hwnds.append(hwnd)
            except Exception:
                pass
        return True # Continue enumeration

    hwnds = []
    try:
        win32gui.EnumWindows(callback, hwnds)
    except Exception as e:
        print(f"Error enumerating windows: {e}")
    return hwnds

def hardcore_detect():
    print(f"{'PID':<8} | {'Process Name':<20} | {'HWND':<10} | {'ClassName':<30} | {'Window Title'}")
    print("-" * 110)

    target_process_names = ["qq.exe", "wechat.exe", "wxwork.exe", "tim.exe"]
    
    # 1. Iterate over all running processes
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            p_name = proc.info['name']
            p_pid = proc.info['pid']
            
            if not p_name: 
                continue

            # Check if it's one of our targets (case-insensitive)
            if p_name.lower() in target_process_names:
                # 2. Find windows for this PID
                hwnds = get_hwnds_for_pid(p_pid)
                
                for hwnd in hwnds:
                    title = win32gui.GetWindowText(hwnd)
                    class_name = win32gui.GetClassName(hwnd)
                    
                    # Filter out some constantly-hidden or empty-title windows if preferred,
                    # but for "hardcore" detection, we show almost everything visible.
                    if title:
                        print(f"{p_pid:<8} | {p_name:<20} | {hwnd:<10} | {class_name:<30} | {title}")
                        
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

if __name__ == "__main__":
    print("正在通过进程列表暴力搜索聊天窗口...")
    try:
        hardcore_detect()
    except ImportError:
        print("缺少依赖！请运行: pip install psutil pywin32")
    except Exception as e:
        print(f"发生异常: {e}")
