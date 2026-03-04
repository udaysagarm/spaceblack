<div align="center">

  <h1>🌌 Space Black & 👻 Ghost</h1>
  
  <p>
    <strong>Space Black is the ship. Ghost is the pilot.</strong>
  </p>

  <p>
    <a href="https://spaceblack.info"><img src="https://img.shields.io/badge/Website-spaceblack.info-blueviolet?style=for-the-badge" alt="Website"></a>
    <a href="https://github.com/udaysagarm/SpaceBlack/releases/latest"><img src="https://img.shields.io/github/v/release/udaysagarm/SpaceBlack?style=for-the-badge&color=00ff00" alt="Version 1.0.0"></a>
    <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+">
    <img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="License MIT">
    <br>
    <img src="https://img.shields.io/badge/macOS-000000?style=for-the-badge&logo=apple&logoColor=white" alt="macOS">
    <img src="https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows">
    <img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" alt="Linux">
  </p>
  
  <img src="https://textual.textualize.io/assets/images/gallery/code_browser.png" alt="Terminal UI" width="800">
</div>

<br>

## 🚀 What is Space Black?

**Space Black** is a terminal-based AI infrastructure designed to host autonomous agents. It provides the **body** (CLI, file system access, browser engine, encrypted memory) that an AI agent needs to live and work on your local machine.

**Ghost** is the default AI agent running on Space Black. It is a self-evolving, persistent personality that acts as your pair programmer, researcher, and automated assistant. Let Ghost surf the web, read your code, and manage your tasks.

---

## 🏗️ Tech Stack

Space Black leverages modern frameworks to run heavy agentic workloads natively:

| Component | Technology | Description |
|-----------|------------|-------------|
| **Core** | **Python 3.10+** | Extensible infrastructure and native bindings. |
| **Agent Mind** | **LangGraph / LangChain** | ReAct execution loops (Reason → Act → Observe). |
| **Interface** | **Textual** | A beautiful, high-performance Terminal UI. |
| **Browser Engine**| **Playwright & CDP** | Automates Chromium using Accessibility Trees for GUI vision. |
| **Security** | **OS Keychain & AES-256**| Fuses native OS keychains with an encrypted local file vault. |

---

## ✨ Key Features & Modular Skills

### 🧠 Persistent Mind & Security
- **Memory**: Ghost maintains a relationship with you, storing preferences in `brain/USER.md` and semantic facts in `brain/memory/`.
- **Vault System**: API keys and passwords are secure, prioritizing native OS Keychains over plaintext `config.json`.
- **Self-Evolution**: Ghost dynamically updates its own core personality prompt (`brain/SOUL.md`).

### 🛠️ Capabilities & Integrations
Space Black supports massive model variety (`gpt-4.5-preview`, `claude-3-7-sonnet`, `gemini-2.5-flash`, `deepseek-r1`) and provides Ghost with powerful tools:

<div align="center">

| Skill / Tool | Description |
|---|---|
| 🌐 **Autonomous Browser** | Surfs the live web, sees page structure natively, clicks, and navigates SPAs. |
| 👔 **Google Workspace** | Reads Gmail, parses Drive docs, and manages Calendar events via local OAuth. |
| 🍏 **macOS Control** | Deep native integration via AppleScript (Apple Mail, Notes, Reminders, Finder). |
| 🐙 **GitHub** | Control repositories, fetch issues, manipulate branches, and direct code commits. |
| 🎫 **Jira** | Natively manage Atlassian tickets, comments, and project states autonomously. |
| 💳 **Stripe & PayPal** | Secure billing interactions, invoice generation, and payouts. |
| 🗣️ **Native Voice** | Built-in seamless Speech-to-Text and auto Text-to-Speech (STT/TTS). |
| 🤖 **Discord/Slack/Telegram**| Run background bots to manage servers and chat with Ghost remotely. |

</div>

---

## ⚡ Quick Start

### Option 1: One-Line Install (macOS / Linux)
The fastest way to get started. Automatically detects your OS and installs the `.deb`, `.rpm`, or compiles from source.
```bash
curl -fsSL https://spaceblack.info/install.sh | bash
```

### Option 2: Manual Clone (All Platforms)
```bash
git clone https://github.com/udaysagarm/SpaceBlack.git
cd SpaceBlack

# Mac / Linux
./ghost start

# Windows (PowerShell)
.\ghost.bat start
```

*The `ghost start` command automatically creates a virtual environment, installs dependencies, and launches the UI.*

---

## 📚 Documentation

Dive deeper into the infrastructure and Agent mechanics inside the `docs/` folder:

| Guide | Description |
|---|---|
| [**CLI Commands**](docs/COMMANDS.md) | Full CLI reference (`ghost start`, `ghost daemon`, `ghost update`). |
| [**User Manual**](docs/USAGE.md) | Interaction guide, Voice Mode shortcuts, and integration prompts. |
| [**Installation**](docs/INSTALLATION.md) | Detailed requirements, advanced `.env` setup, and manual setups. |
| [**Browsing**](docs/BROWSING.md) | How Ghost converts React/Vue DOM structures into readable Contexts. |
| [**Architecture**](docs/ARCHITECTURE.md)| How Space Black's ReAct loop passes tools to the LangGraph runner. |
| [**Packaging**](docs/PACKAGING.md) | Guide for compiling the `.deb` and `.rpm` native Linux packages. |
| [**Security**](docs/SECURITY.md) | Details on AES vault encryption and token safety. |

---

## 📄 License
This project is licensed under the **[MIT License](LICENSE)**.
