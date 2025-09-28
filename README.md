# 🚀 AutoFix: Smart Workspace Auto-Setup

> **A one-command tool that eliminates the 20-minute setup nightmare every developer faces when cloning a new repo.**

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

---

## ❌ The Problem

Every time developers clone a new repository, they face the same frustrating ritual:

- **Which package manager do I use?** (npm, yarn, pnpm?)
- **Do I need a Python virtual environment?**
- **What's the right sequence of commands?**
- **Why won't the dependencies install?**
- **What tools are already configured?**
- **How do I set up the development environment?**
- **Why is my setup different from the team?**

This results in:
- **20+ minutes of wasted setup time per project**
- **Constant context switching between tools**
- **Inconsistent environments causing mysterious bugs**
- **Frustration and productivity loss**
- **Time spent reading documentation instead of coding**
- **Manual configuration of linters, formatters, and hooks**

---

## ✅ The Solution

**AutoFix** is a revolutionary Python script that automatically detects your project type and sets up the perfect development environment with **zero configuration**.

### 🎯 What AutoFix Does:
- **Intelligent Detection**: Automatically identifies Python, Node.js, Rust, and Flutter projects
- **One-Command Setup**: Single command sets up everything you need
- **Smart Package Management**: Chooses the right package manager (npm, yarn, pnpm, pip, cargo)
- **Code Formatting**: Automatically configures and runs formatters (Black, Prettier, Ruff)
- **Git Integration**: Sets up pre-commit hooks and development tools
- **Cross-Platform**: Works seamlessly on Windows, macOS, and Linux

> **One command. Every environment. Zero friction. Maximum productivity.**

---

## 📊 Line Count Verification

![Line Count](Screenshots/Linescount.png)

*Total lines of code: 248*

---

## ⚡ Installation & Usage

### Quick Start

```bash
# Download the script
curl -O https://raw.githubusercontent.com/ATIFSHAH159/Autofix-CLI-Development-Challenge-Hackathon/main/autofix.py

# Run in any project directory
python autofix.py
```

### 🎯 What Happens Next:
1. **Detection Phase**: AutoFix scans your project for configuration files
2. **Analysis Phase**: Identifies the best tools and package managers
3. **Setup Phase**: Creates environments and installs dependencies
4. **Configuration Phase**: Sets up formatters, linters, and git hooks
5. **Verification Phase**: Ensures everything is working correctly

### PowerShell Users (Windows)

If you're using PowerShell, use this command instead:

```powershell
Invoke-WebRequest https://raw.githubusercontent.com/ATIFSHAH159/Autofix-CLI-Development-Challenge-Hackathon/main/autofix.py -OutFile autofix.py
```

### Global Installation (Recommended)

For convenience, you can install AutoFix globally:

1. **Create a Scripts folder** in permanent storage (e.g., `C:\Scripts\` or `D:\Scripts\`)
2. **Download autofix.py** to this folder
3. **Create autofix.bat** in the same Scripts folder
4. **Add the folder to your PATH** environment variable

#### Step-by-Step Commands:

```powershell
# 1. Create Scripts directory (choose C: or D:)
mkdir C:\Scripts
# OR
mkdir D:\Scripts

# 2. Download autofix.py to your chosen directory
Invoke-WebRequest https://raw.githubusercontent.com/ATIFSHAH159/Autofix-CLI-Development-Challenge-Hackathon/main/autofix.py -OutFile C:\Scripts\autofix.py
# OR
Invoke-WebRequest https://raw.githubusercontent.com/ATIFSHAH159/Autofix-CLI-Development-Challenge-Hackathon/main/autofix.py -OutFile D:\Scripts\autofix.py

# 3. Create autofix.bat wrapper (adjust path as needed)
@"
@echo off
python C:\Scripts\autofix.py %*
"@ | Out-File -FilePath C:\Scripts\autofix.bat -Encoding ASCII

# 4. Add to PATH (run as Administrator)
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Scripts", "User")
```

#### Manual PATH Setup:
1. Open **System Properties** → **Environment Variables**
2. Under **User variables**, select **Path** and click **Edit**
3. Click **New** and add `C:\Scripts` (or your chosen path)
4. Click **OK** to save

![Path Configuration](Screenshots/Path.png)

![Environment Variable Setup](Screenshots/EnvirnomentVariable.png)


After setup, you can run `autofix` from anywhere on your system!

---

## 🧑‍💻 Example Workflows

> **Note**: After global installation, you can simply run `autofix` from any project directory!

### 🐍 Python Project

#### Manual Method (Download script each time):
```bash
cd my-python-project/
python autofix.py
```

#### Global Method (Recommended):
```bash
cd my-python-project/
autofix
```

**What it does:**
- ✅ Creates `.venv` virtual environment
- ✅ Installs dependencies from `requirements.txt` or `pyproject.toml`
- ✅ Sets up pre-commit hooks
- ✅ Formats code with Black & Ruff

### 📦 Node.js Project

#### Manual Method:
```bash
cd my-react-app/
python autofix.py
```

#### Global Method (Recommended):
```bash
cd my-react-app/
autofix
```

**What it does:**
- ✅ Detects pnpm from `pnpm-lock.yaml`
- ✅ Runs `pnpm install`
- ✅ Sets up Prettier formatting
- ✅ Configures dev environment

### 🔄 Multi-Language Project (Python + Node.js)

#### Manual Method:
```bash
cd fullstack-app/
python autofix.py
```

#### Global Method (Recommended):
```bash
cd fullstack-app/
autofix
```

**What it does:**
- ✅ Detects Python backend + Node.js frontend
- ✅ Sets up both environments intelligently
- ✅ Configures all necessary tooling

### 🦀 Rust Project

#### Manual Method:
```bash
cd my-rust-app/
python autofix.py
```

#### Global Method (Recommended):
```bash
cd my-rust-app/
autofix
```

**What it does:**
- ✅ Detects `Cargo.toml`
- ✅ Runs `cargo build` / installs dependencies
- ✅ Configures Rust development environment

### 📱 Flutter Project

#### Manual Method:
```bash
cd my-flutter-app/
python autofix.py
```

#### Global Method (Recommended):
```bash
cd my-flutter-app/
autofix
```

**What it does:**
- ✅ Detects Flutter project from `pubspec.yaml`
- ✅ Runs `flutter pub get`
- ✅ Automates build_runner if needed
- ✅ Configures Flutter environment for smooth development

---

## 📸 Screenshots

### Example 1: Python Project Setup
![Python Setup Example](Screenshots/Example3.png)

### Example 2: Node.js Project Setup
![Node.js Setup Example](Screenshots/Example1.png)

### Example 3: Multi-language Project Setup
![Multi-language Setup Example](Screenshots/Example2.png)

---

## 🛠️ Supported Technologies

| Technology | Detection | Package Manager | Formatting |
|------------|-----------|-----------------|------------|
| **Python** | `requirements.txt`, `pyproject.toml`, `setup.py` | pip | Black, Ruff |
| **Node.js** | `package.json` | npm, yarn, pnpm | Prettier |
| **Rust** | `Cargo.toml` | cargo | Built-in |
| **Flutter** | `pubspec.yaml` | flutter pub | dart format |

---

## 🎯 Features

- **Smart Detection**: Automatically identifies project types
- **Zero Configuration**: Works out of the box
- **Multi-Language Support**: Python, Node.js, Rust, Flutter
- **Package Manager Detection**: Automatically chooses the right tool
- **Code Formatting**: Sets up and runs formatters
- **Git Hooks**: Configures pre-commit hooks
- **Cross-Platform**: Windows, macOS, Linux support
- **Verbose Mode**: Detailed output with `-v` flag
- **Dry Run**: Test without executing with `-n` flag

---

## 🤝 Contributing

Pull requests are welcome! If you'd like to add support for more languages or tools, open an issue first to discuss the changes.

### 🚀 How to Contribute

1. **Fork the repository** and clone your fork
2. **Create a feature branch** for your changes
3. **Make your changes** following our coding standards
4. **Test with different project types** to ensure compatibility
5. **Submit a pull request** with a clear description

### 🛠️ Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/Autofix-CLI-Development-Challenge-Hackathon.git
cd Autofix-CLI-Development-Challenge-Hackathon

# Test the script
python autofix.py 

# Run tests with different project types
python autofix.py  # Test in a sample project
```

### 🎯 Areas for Contribution
- **New Language Support**: Add support for Go, Java, C#, PHP, etc.
- **Enhanced Detection**: Improve project type detection algorithms
- **Additional Tools**: Support for more linters, formatters, and build tools
- **Documentation**: Improve documentation and add more examples
- **Testing**: Add comprehensive test coverage
- **Performance**: Optimize setup speed and resource usage

### 📋 Contribution Guidelines
- Follow the existing code style and structure
- Add comments for complex logic
- Test your changes with multiple project types
- Update documentation for new features
- Ensure cross-platform compatibility

---

## 📜 License

MIT License – free to use and modify.

---

## 🙏 Acknowledgments

- **Built for developers, by developers** - Solving real-world problems
- **Inspired by frustration** - Born from the pain of setting up new projects
- **Open-source community** - Special thanks to all contributors and supporters
- **Tool creators** - Thanks to the creators of Black, Prettier, Ruff, and other amazing tools
- **Developer community** - For feedback, suggestions, and continuous improvement

### 🌟 Special Thanks
- **Python community** for the amazing ecosystem
- **Node.js community** for the rich package ecosystem
- **Rust community** for the excellent tooling
- **Flutter team** for the comprehensive development platform
- **All developers** who face the setup challenge daily

---

## 📈 Impact & Statistics

- **Time Saved**: 20+ minutes per project setup
- **Projects Supported**: 4+ major languages and frameworks
- **Package Managers**: 6+ supported package managers
- **Formatters**: 8+ code formatting tools
- **Platforms**: Windows, macOS, Linux support

---

<div align="center">

**⭐ Star this repo if AutoFix saved you time! ⭐**
</div>
