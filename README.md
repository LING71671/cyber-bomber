# 💣 Cyber Bomber (赛博轰炸机)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

[English](#english) | [中文](#chinese)

---

<a name="english"></a>
## 🌏 English

### Introduction
**Cyber Bomber** is a modern Windows desktop automation tool based on Python, designed for message sending testing, stress testing, and automated script design. Combining the modern UI of `CustomTkinter` with the low-level control of `Win32 API`, it delivers stable and efficient message sending to target windows (such as WeChat, QQ, DingTalk, etc.).

> **Note**: This project has been deeply optimized with a **Single-Process Precision Targeting** mode. Compared to multi-threaded concurrency, it significantly improves stability and ensures <1% packet loss.

### ⚠️ Disclaimer
**This project is strictly for technical research, automated testing (e.g., IM software stress testing), and educational purposes.**
*   **DO NOT** use this tool for harassment, spamming, or any illegal activities.
*   The user assumes all legal responsibilities and liabilities arising from the use of this tool.
*   The author is not responsible for any misuse.

### ✨ Features
*   **🎯 Precision Targeting**: Uses low-level process scanning (`psutil` + `win32gui`) to accurately identify Electron or Native windows like QQ (NT), WeChat, DingTalk, etc.
*   **🚀 High-Speed Sending**: Bypasses traditional simulation libraries and calls `ctypes.windll.user32.keybd_event` directly for millisecond-level response.
*   **🛡️ Stability & Anti-Ban**:
    *   **Smart Micro-Delay**: Simulates human operation rhythm to avoid being flagged as a bot.
    *   **Safe Key Release**: Improved safety mechanism ensures `Ctrl/Alt` keys are never stuck, even if the program stops unexpectedly.
*   **🎨 Modern UI**: Built with CustomTkinter for a sleek, dark-themed interface.
*   **🛑 Emergency Stop**: Independent monitoring thread supports one-click "Emergency Stop" to prevent loss of control.

### 🛠️ Installation & Usage

#### 1. Requirements
Ensure you have Python 3.8+ installed.

```bash
# Clone repository
git clone https://github.com/LING71671/cyber-bomber.git

# Enter directory
cd cyber-bomber

# Install dependencies
pip install -r requirements.txt
```

#### 2. Run
```bash
python main.py
```

#### 3. How to Use
1.  **Prepare**: Open WeChat or QQ and open the chat window you want to test (must be an **independent window**, not minimized).
2.  **Refresh**: Click the **[Refresh Process]** button on the left.
3.  **Select**: Choose the target window from the list (Single selection mode).
4.  **Compose**: Enter your text in the right text box. Support multi-line text.
5.  **Configure**:
    *   **Interval**: Recommended `0.1` - `0.5` seconds.
    *   **Count**: Number of times to send.
6.  **Start**: Click the green **[Start Bombing]** button.
7.  **Stop**: Click the red **[Emergency Stop]** button if needed.

---

<a name="chinese"></a>
## 🇨🇳 中文

### 简介
**Cyber Bomber** 是一款基于 Python 开发的现代化 Windows 桌面自动化工具，专为消息发送测试、压力测试及自动化脚本设计。它结合了 `CustomTkinter` 的现代 UI 和 `Win32 API` 的底层控制能力，能够稳定、高效地向目标窗口（如微信、QQ、钉钉等）发送预设消息。

> **特别说明**：本项目已经过深层优化，采用 **单进程精准打击** 模式，相比多线程并发，极大提升了消息发送的稳定性和不丢包率（<1% 丢包）（骗你的，没那么低）。

### ⚠️ 免责声明
**严正声明：本项目仅供技术研究、自动化测试（如 IM 软件压力测试）及学习交流使用。**
*   请勿用于骚扰他人、恶意刷屏或任何非法用途。
*   使用者需自行承担因使用本工具产生的一切法律后果及连带责任。
*   作者不对任何滥用行为负责。

### ✨ 核心功能
*   **🎯 精准识别**：基于底层进程扫描 (`psutil` + `win32gui`)，能精准识别 QQ (NT架构)、微信、企业微信、钉钉等 Electron 或 Native 开发的窗口。
*   **🚀 极速发送**：直接调用 `ctypes.windll.user32.keybd_event` 底层 API，实现毫秒级响应。
*   **🛡️ 稳定防封**：
    *   内置 **智能微延迟** 算法，模拟人类操作节奏。
    *   **安全按键释放**：新增安全机制，即使程序异常退出也能确保 Ctrl/Alt 键不会卡死。
*   **🎨 现代界面**：使用 CustomTkinter 构建的深色模式 GUI，界面简洁美观。
*   **🛑 紧急制动**：独立的监听线程，支持一键“紧急停止”，防止意外失控。

### 🛠️ 安装与运行

#### 1. 环境准备
确保已安装 Python 3.8 或以上版本。

```bash
# 克隆仓库
git clone https://github.com/LING71671/cyber-bomber.git

# 进入目录
cd cyber-bomber

# 安装依赖
pip install -r requirements.txt
```

#### 2. 运行程序
```bash
python cyber_bomber/main.py
```
*(注：如果下载的是 Release 中的 .exe 版本，直接双击运行即可)*

### 🕹️ 使用指南
1.  **准备目标**：在电脑上打开微信或 QQ，并打开你要轰炸的聊天窗口（**必须保持独立窗口状态**，不要最小化）。
2.  **刷新列表**：点击软件左侧的 **[刷新进程]** 按钮。
3.  **选择目标**：在左侧列表中，**单选** 你要发送的目标窗口。
4.  **设置文案**：在右侧文本框输入内容，支持多行文本（会自动分段发送）。
5.  **配置参数**：
    *   **发送间隔**：建议 `0.1` - `0.5` 秒。
    *   **发送次数**：设置你要循环发送的次数。
6.  **启动**：点击绿色 **[开始轰炸]** 按钮。
7.  **停止**：如需中途结束，点击红色 **[紧急停止]** 按钮。

---

## 📦 Tech Stack / 技术栈
*   **GUI**: [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
*   **Automation**: `pywin32`, `ctypes`, `psutil`
*   **Clipboard**: `pyperclip`

---
**Happy Testing!** 🚀
