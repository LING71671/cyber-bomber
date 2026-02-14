import customtkinter as ctk # type: ignore
import threading
import sys
import os
import time
import win32gui # type: ignore

# Ensure core package is importable
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.automation import WindowScanner, BomberEngine # type: ignore

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class CyberBomberApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Cyber Bomber - 赛博轰炸机")
        self.geometry("1200x800")
        
        # Initialize Core Logic
        self.scanner = WindowScanner()
        self.engine = BomberEngine()
        
        # Initialize State
        self.window_map = {}
        self.selected_window_var = ctk.StringVar(value="")

        # UI Layout Registration
        self._init_ui()
        
    def _init_ui(self):
        # Grid Layout Configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar (Left) ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="CYBER\nBOMBER", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.refresh_btn = ctk.CTkButton(self.sidebar_frame, text="刷新进程", command=self.refresh_process_list)
        self.refresh_btn.grid(row=1, column=0, padx=20, pady=10)
        
        self.window_list_label = ctk.CTkLabel(self.sidebar_frame, text="目标窗口列表:", anchor="w")
        self.window_list_label.grid(row=2, column=0, padx=20, pady=(10, 0))

        # Checkbox Scrollable Frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self.sidebar_frame, label_text="检测到的窗口")
        self.scrollable_frame.grid(row=3, column=0, padx=20, pady=(10, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)


        # --- Main Content (Right) ---
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_rowconfigure(1, weight=1) # Text area expands
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Message Input Area
        self.msg_label = ctk.CTkLabel(self.main_frame, text="轰炸文案 (自动按换行符分割):", anchor="w")
        self.msg_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        
        self.msg_textbox = ctk.CTkTextbox(self.main_frame, width=400)
        self.msg_textbox.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="nsew")
        self.msg_textbox.insert("0.0", "你好！\n测试消息\n赛博轰炸机启动！")

        # Configuration Area
        self.config_frame = ctk.CTkFrame(self.main_frame)
        self.config_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        
        self.interval_label = ctk.CTkLabel(self.config_frame, text="发送间隔(秒):")
        self.interval_label.grid(row=0, column=0, padx=10, pady=10)
        self.interval_entry = ctk.CTkEntry(self.config_frame, width=80)
        self.interval_entry.grid(row=0, column=1, padx=10, pady=10)
        self.interval_entry.insert(0, "0.5")
        
        self.count_label = ctk.CTkLabel(self.config_frame, text="发送次数(循环):")
        self.count_label.grid(row=0, column=2, padx=10, pady=10)
        self.count_entry = ctk.CTkEntry(self.config_frame, width=80)
        self.count_entry.grid(row=0, column=3, padx=10, pady=10)
        self.count_entry.insert(0, "10")

        # Control Buttons
        self.start_btn = ctk.CTkButton(self.config_frame, text="开始轰炸", fg_color="green", command=self.start_bombing)
        self.start_btn.grid(row=0, column=4, padx=20, pady=10)
        
        self.stop_btn = ctk.CTkButton(self.config_frame, text="紧急停止", fg_color="red", command=self.stop_bombing)
        self.stop_btn.grid(row=0, column=5, padx=20, pady=10)
        self.stop_btn.configure(state="disabled")

        # --- Footer Log (Bottom) ---
        self.log_textbox = ctk.CTkTextbox(self, height=150)
        self.log_textbox.grid(row=1, column=1, padx=20, pady=20, sticky="ew")
        self.log_textbox.configure(state="disabled")
        
        self.log_msg("系统就绪...")

    def log_msg(self, msg):
        """Append message to log safely from any thread"""
        def _log():
            self.log_textbox.configure(state="normal")
            self.log_textbox.insert("end", msg + "\n")
            self.log_textbox.see("end")
            self.log_textbox.configure(state="disabled")
        self.after(0, _log)

    def refresh_process_list(self):
        # Clear existing checkboxes
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        self.window_map = {}
        self.check_vars = []
        
        # Scan windows
        windows = self.scanner.scan_windows()
        
        if not windows:
            label = ctk.CTkLabel(self.scrollable_frame, text="未检测到目标窗口\n请确保QQ/微信已打开且独立窗口可见", text_color="gray")
            label.pack(pady=10)
            return

        # Create RadioButtons for single selection
        # We need a single invalid variable to hold the selected value
        # But since the list is dynamic, we can't easily bind one StringVar to generated buttons without value management.
        # However, keeping it simple: use RadioButton, all sharing one variable.
        


        for win in windows:
            # Value needs to be unique, we use handle as string
            win_handle_str = str(win['handle'])
            
            # Display text
            display_text = f"{win['name']}"
            
            rb = ctk.CTkRadioButton(
                self.scrollable_frame, 
                text=display_text, 
                variable=self.selected_window_var,
                value=win_handle_str
            )
            rb.pack(fill="x", padx=5, pady=2)
            
            # We store the full window object in a dict to retrieve later
            self.window_map[win_handle_str] = win
            
        self.log_msg(f"刷新完成: 找到 {len(windows)} 个窗口")

    def start_bombing(self):
        # Assuming self.is_running is managed elsewhere or will be added.
        # For now, just apply the provided logic.
        # if self.is_running:
        #     self.stop_bombing()
        #     return

        # Get selected target
        selected_handle = self.selected_window_var.get()
        if not selected_handle or not hasattr(self, 'window_map') or selected_handle not in self.window_map:
            self.log_msg("请先选择一个目标窗口！") # Changed from self.log to self.log_msg
            return

        target = self.window_map[selected_handle]
        
        # Double check if window still exists
        try:
            if not win32gui.IsWindow(target['handle']):
                self.log_msg("错误: 目标窗口已失效，请重新刷新！")
                self.refresh_process_list()
                return
        except Exception:
            self.log_msg("错误: 无法检测窗口状态")
            return

        targets = [target] # Engine expects a list

        # 2. Collect Messages
        raw_text = self.msg_textbox.get("1.0", "end").strip()
        if not raw_text:
            self.log_msg("错误: 请输入文案！")
            return
        messages = [line for line in raw_text.split('\n') if line.strip()]

        # 3. Collect Config
        try:
            interval = float(self.interval_entry.get())
            count = int(self.count_entry.get())
        except ValueError:
            self.log_msg("错误: 间隔和次数必须是数字！")
            return

        # 4. Update UI State
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.refresh_btn.configure(state="disabled")
        
        # 5. Start Engine
        # Re-instantiate/Reset engine in Main Thread to avoid race condition with Stop button
        self.engine = BomberEngine()
        self.engine.start_bombing(targets, messages, interval, count, self.log_msg)
        
        # 6. Start Monitor Thread
        threading.Thread(target=self._monitor_progress, daemon=True).start()

    def _monitor_progress(self):
        """Monitor engine threads and reset UI when done"""
        while True:
            # Check if any tasks are still running
            if not self.engine.active_threads:
                # If thread list is empty wait a bit or just break if not started yet?
                # start_bombing populates it immediately.
                # However, we should check if they are alive.
                pass
            
            still_running = any(t.is_alive() for t in self.engine.active_threads)
            if not still_running:
                break
                
            time.sleep(0.5)
            
        self.log_msg("所有任务线程已结束")
        self.after(0, self._reset_ui)

    def stop_bombing(self):
        self.log_msg("正在紧急停止...")
        self.engine.emergency_stop()
        
    def _reset_ui(self):
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.refresh_btn.configure(state="normal")

if __name__ == "__main__":
    app = CyberBomberApp()
    app.mainloop()
