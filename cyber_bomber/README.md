# 💣 Cyber Bomber (赛博轰炸机)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Cyber Bomber** 是一款基于 Python 开发的现代化 Windows 桌面自动化工具，专为消息发送测试、压力测试及自动化脚本设计。它结合了 `CustomTkinter` 的现代 UI 和 `Win32 API` 的底层控制能力，能够稳定、高效地向目标窗口（如微信、QQ、钉钉等）发送预设消息。

> **特别说明**：本项目已经过深层优化，采用 **单进程精准打击** 模式，相比多线程并发，极大提升了消息发送的稳定性和不丢包率（<1% 丢包）。（骗你的）

## ⚠️ 免责声明 (Disclaimer)

**严正声明：本项目仅供技术研究、自动化测试（如 IM 软件压力测试）及学习交流使用。**
* 请勿用于骚扰他人、恶意刷屏或任何非法用途。
* 使用者需自行承担因使用本工具产生的一切法律后果及连带责任。
* 作者不对任何滥用行为负责。

---

## ✨ 核心功能 (Features)

*   **🎯 精准识别**：基于底层进程扫描 (`psutil` + `win32gui`)，能精准识别 QQ (NT架构)、微信、企业微信、钉钉等 Electron 或 Native 开发的窗口。
*   **🚀 极速发送**：抛弃传统的模拟按键库，直接调用 `ctypes.windll.user32.keybd_event` 底层 API，实现毫秒级响应。
*   **🛡️ 稳定防封**：
    *   内置 **智能微延迟** 算法，模拟人类操作节奏，避免被判定为外挂。
    *   **Double-Enter** 策略：双重回车确保消息 100% 发出，解决网络波动导致的消息残留。
*   **🎨 现代界面**：使用 CustomTkinter 构建的深色模式 GUI，界面简洁美观，操作丝滑。
*   **🛑 紧急制动**：独立的监听线程，支持一键“紧急停止”，防止意外失控。

---

## 🛠️ 安装与运行 (Installation)

### 1. 环境准备
确保已安装 Python 3.8 或以上版本。

```bash
# 克隆仓库
git clone https://github.com/LING71671/cyber-bomber.git

# 进入目录
cd cyber-bomber/cyber_bomber

# 安装依赖
pip install -r requirements.txt
```

### 2. 运行程序
```bash
python main.py
```

### 3. 打包为 EXE (可选)
如果你想生成由单文件运行的 `.exe` 程序分享给朋友：
```bash
pyinstaller --noconsole --onefile --name "CyberBomber" --hidden-import=customtkinter --icon=icon.ico main.py
```
*(注：如果没有 icon.ico 可去掉 --icon 参数)*

---

## 🕹️ 使用指南 (Usage)

1.  **准备目标**：在电脑上打开微信或 QQ，并打开你要轰炸的聊天窗口（**必须保持独立窗口状态**，不要最小化）。
2.  **刷新列表**：点击软件左侧的 **[刷新进程]** 按钮。
3.  **选择目标**：在左侧列表中，**单选** 你要发送的目标窗口（如 "文件传输助手"）。
4.  **设置文案**：在右侧文本框输入内容，支持多行文本（会自动分段发送）。
5.  **配置参数**：
    *   **发送间隔**：建议 `0.1` - `0.5` 秒（过快可能被腾讯风控）。
    *   **发送次数**：设置你要循环发送的次数。
6.  **启动**：点击绿色 **[开始轰炸]** 按钮。
7.  **停止**：如需中途结束，点击红色 **[紧急停止]** 按钮。

---

## ❓ 常见问题 (FAQ)

**Q: 为什么找不到我的 QQ/微信 窗口？**
A: 请确保：
1. 聊天窗口是 **独立打开** 的（即把它从主面板拖出来，或者双击打开）。
2. 窗口 **没有被最小化** 到任务栏（即使被其他窗口遮挡也没关系，但不能最小化）。
3. 如果 软件是以管理员权限运行的，那么目标软件也需要相应的权限（通常普通运行即可）。

**Q: 发送过程中键盘无法使用？**
A: 这是正常现象。程序通过独占键盘焦点来模拟输入。点击 [紧急停止] 或等待任务结束即可恢复。
*如果程序意外崩溃导致 Ctrl 键卡死（表现为按 C 变成复制），请重新运行程序或按几下 Ctrl/Alt/Shift 键即可复位。*

**Q: 发送速度太慢或太快？**
A: 这是为了保证消息不丢失而特意调教的节奏。你可以在 `发送间隔` 中输入 `0` 来体验极速模式，但可能会导致少量消息丢失或顺序错乱。

---

## 📦 技术栈
*   **GUI**: [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
*   **Automation**: `pywin32`, `ctypes`, `psutil`
*   **Clipboard**: `pyperclip`

---
**Happy Testing!** 🚀
