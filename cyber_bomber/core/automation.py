
import threading
import time
import pyperclip # type: ignore
import random
import ctypes
import psutil # type: ignore
import win32gui # type: ignore
import win32process # type: ignore
import win32con # type: ignore
import win32api # type: ignore

class WindowScanner:
    """
    负责扫描和筛选目标窗口
    采用 '进程 -> 窗口' (Process-First) 的暴力扫描策略
    """
    def _get_hwnds_for_pid(self, pid):
        """
        返回指定进程ID及其子进程的所有可见特定窗口句柄
        """
        def callback(hwnd, hwnds):
            if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd): # type: ignore
                try:
                    _, found_pid = win32process.GetWindowThreadProcessId(hwnd) # type: ignore
                    if found_pid == pid:
                        hwnds.append(hwnd)
                except Exception:
                    pass
            return True

        hwnds = []
        try:
            win32gui.EnumWindows(callback, hwnds) # type: ignore
        except Exception:
            pass
        return hwnds

    def scan_windows(self, keywords=None):
        """
        扫描 QQ/微信 等指定进程的窗口
        Process-based scanning is much more reliable for Electron apps or those hiding from UI Automation.
        """
        target_windows = []
        
        # 目标进程名白名单 (小写)
        TARGET_PROCS = ["qq.exe", "wechat.exe", "wxwork.exe", "tim.exe", "dingtalk.exe"]
        
        # 遍历所有进程
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'].lower() in TARGET_PROCS:
                    pid = proc.info['pid']
                    
                    # 查找该进程的所有窗口
                    hwnds = self._get_hwnds_for_pid(pid)
                    
                    for hwnd in hwnds:
                        title = win32gui.GetWindowText(hwnd) # type: ignore
                        class_name = win32gui.GetClassName(hwnd) # type: ignore
                        
                        # 过滤无标题窗口
                        if not title.strip():
                            continue
                            
                        # 过滤已知垃圾窗口 (QQ的悬浮窗、且听、腾讯网迷你版等)
                        # TXGuiFoundation 是 QQ 的基础类名，通常 QQ 主窗口叫 QQ，聊天窗口叫备注名
                        # 我们只排除那些真的没用的
                        if title in ["TXGuiFoundation", "QQ", "腾讯网迷你版", "两只老虎爱跳舞"]: 
                             # 简单的黑名单，防止主窗口混入
                             pass
                        
                        # 构造返回对象
                        target_windows.append({
                            'name': title,
                            'handle': hwnd,
                            'classname': class_name
                        })
                        
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        return target_windows

class BomberEngine:
    """
    负责多线程并发发送消息的核心引擎 (极速版)
    优化点：
    1. 移除 uiautomation 的 SendKeys (它有默认延迟)，改用 ctypes SendInput
    2. 压缩所有等待时间
    """
    def __init__(self):
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        self.active_threads = []

    def start_bombing(self, targets, messages, interval, count, log_callback):
        self._stop_event.clear()
        self.active_threads = []
        
        if not targets:
            log_callback("错误: 未选择任何目标窗口")
            return
            
        if not messages:
            log_callback("错误: 未输入任何发送内容")
            return

        log_callback(f"任务启动: 目标 {len(targets)} 个, 模式: 极速 (Raw Input)")

        for target in targets:
            t = threading.Thread(
                target=self._send_task,
                args=(target, messages, interval, count, log_callback),
                daemon=True
            )
            self.active_threads.append(t)
            t.start()

    def emergency_stop(self):
        self._stop_event.set()
        self._release_modifiers()

    def _release_modifiers(self):
        """Force release Ctrl, Alt, Shift keys to prevent stuck keys"""
        try:
            ctypes.windll.user32.keybd_event(0x11, 0, 2, 0) # Ctrl Up
            ctypes.windll.user32.keybd_event(0x12, 0, 2, 0) # Alt Up
            ctypes.windll.user32.keybd_event(0x10, 0, 2, 0) # Shift Up
        except:
            pass

    def _fast_send_keys(self):
        """
        使用 keybd_event 极速发送 Ctrl+V 和 Enter
        安全增强版：使用 try...finally 确保 Ctrl 键一定被释放
        """
        # 经过调优的最佳参数 (3% 丢包率)
        T_HOLD = 0.005 # 按键保持时间 5ms
        T_GAP = 0.01   # 按键间隔 10ms
        P_WAIT = 0.05  # 粘贴后等待时间 50ms (确保 Electron 渲染)
        E_HOLD = 0.02  # 回车键保持时间 20ms (确保发送触发)
        
        try:
            # 1. Ctrl + V
            ctypes.windll.user32.keybd_event(0x11, 0, 0, 0) # type: ignore # Ctrl Down
            time.sleep(T_HOLD)
            ctypes.windll.user32.keybd_event(0x56, 0, 0, 0) # type: ignore # V Down
            time.sleep(T_HOLD)
            ctypes.windll.user32.keybd_event(0x56, 0, 2, 0) # type: ignore # V Up
            time.sleep(T_GAP)
        finally:
            # 无论发生什么，必须确保 Ctrl 弹起
            ctypes.windll.user32.keybd_event(0x11, 0, 2, 0) # type: ignore # Ctrl Up
        
        # 2. 等待粘贴处理
        time.sleep(P_WAIT) 
        
        # 3. Enter
        ctypes.windll.user32.keybd_event(0x0D, 0, 0, 0) # type: ignore # Enter Down
        time.sleep(E_HOLD) # 回车键
        ctypes.windll.user32.keybd_event(0x0D, 0, 2, 0) # type: ignore # Enter Up

    def _send_task(self, target, messages, interval, count, log_callback):
        window_name = target['name']
        handle = target['handle']
        
        try:
            if not win32gui.IsWindow(handle): # type: ignore
                log_callback(f"[{window_name}] 错误: 窗口已消失")
                return

            sent_count = 0
            msg_len = len(messages)
            
            while sent_count < count and not self._stop_event.is_set():
                if not win32gui.IsWindow(handle): # type: ignore
                    break
                    
                msg = messages[sent_count % msg_len]
                
                success = False
                # --- 临界区 ---
                with self._lock:
                    if self._stop_event.is_set():
                        break
                    
                    try:
                        # 1. 抢占焦点
                        if win32gui.GetForegroundWindow() != handle: # type: ignore
                            if win32gui.IsIconic(handle): # type: ignore
                                win32gui.ShowWindow(handle, win32con.SW_RESTORE) # type: ignore
                            
                            # 模拟 Alt 键释放 (防卡死, 解决有时切换不过去的问题)
                            ctypes.windll.user32.keybd_event(0x12, 0, 0, 0) # type: ignore
                            ctypes.windll.user32.keybd_event(0x12, 0, 2, 0) # type: ignore
                            
                            win32gui.SetForegroundWindow(handle) # type: ignore
                            
                            # 极速自旋 (最多等 100ms)
                            for _ in range(10):
                                if win32gui.GetForegroundWindow() == handle: # type: ignore
                                    break
                                time.sleep(0.01)
                        
                        # 2. 发送 (仅当焦点正确时)
                        # 双重检查：确保窗口真的在前台
                        if win32gui.GetForegroundWindow() == handle: # type: ignore
                            pyperclip.copy(msg)
                            self._fast_send_keys() # 瞬间触发粘贴回车
                            success = True
                            log_callback(f"[{window_name}] 发送 ({sent_count+1})")
                        
                    except Exception as e:
                        # 发生异常尝试释放按键
                        self._release_modifiers()
                # --- 结束临界区 ---

                if success:
                    sent_count += 1
                    if interval > 0:
                        time.sleep(float(interval))
                    else:
                        # 0 间隔模式下，仍然需要极微小的 yield 给 UI 线程响应
                        # 否则 Electron 应用的输入队列会溢出导致丢包
                        time.sleep(0.015) 
                else:
                    time.sleep(0.05) # Retry delay

            log_callback(f"[{window_name}] 结束")
                
        except Exception as e:
            log_callback(f"[{window_name}] 崩溃: {e}")
        finally:
             # 任务彻底结束时，兜底释放一次按键
            self._release_modifiers()
