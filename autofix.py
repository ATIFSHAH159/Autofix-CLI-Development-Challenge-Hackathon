#!/usr/bin/env python3
"""
autofix – Smart workspace auto-setup for developers.
Usage: python autofix.py [-n] [--help] [-v]
"""
import os
import sys
import subprocess
import pathlib
import json
from dataclasses import dataclass
from typing import Dict, List, Optional, Union
PROJECT_DETECTORS = {
    "node": ["package.json"],
    "python": ["requirements.txt", "pyproject.toml", "setup.py"],
    "rust": ["Cargo.toml"],
    "flutter": ["pubspec.yaml"],
    "git": [".git"]
}
VENV_PATHS = {
    "windows": {"python": "Scripts/python.exe", "pip": "Scripts/pip.exe"},
    "unix": {"python": "bin/python", "pip": "bin/pip"}
}
@dataclass
class RuntimeConfig:
    dry_run: bool = False
    verbose: bool = False
    is_windows: bool = os.name == 'nt'
    @property
    def venv_paths(self) -> Dict[str, str]:
        return VENV_PATHS["windows" if self.is_windows else "unix"]
class CommandRunner:
    def __init__(self, config: RuntimeConfig):
        self.config = config
    def execute(self, cmd: Union[str, List[str]], cwd: Optional[str] = None) -> bool:
        if self.config.dry_run:
            cmd_str = ' '.join(cmd) if isinstance(cmd, list) else cmd
            print(f"  [DRY] {cmd_str}")
            return True 
        shell_cmd = self._prepare_command(cmd)
        try:
            if self.config.verbose:
                cmd_display = ' '.join(cmd) if isinstance(cmd, list) else cmd
                print(f"  Running: {cmd_display}")      
            result = subprocess.run(shell_cmd, cwd=cwd, shell=self.config.is_windows, 
                                  check=True, capture_output=True, text=True)      
            if self.config.verbose and result.stdout.strip():
                print(f"  Output: {result.stdout.strip()}")
            return True
        except subprocess.CalledProcessError as e:
            self._handle_error(cmd, e)
            return False
        except FileNotFoundError:
            print(f"  ❌ Command not found: {cmd}")
            return False
    def _prepare_command(self, cmd: Union[str, List[str]]) -> Union[str, List[str]]:
        if self.config.is_windows and isinstance(cmd, list):
            return " ".join(str(x) for x in cmd)
        return cmd
    def _handle_error(self, cmd: Union[str, List[str]], error: subprocess.CalledProcessError):
        cmd_display = ' '.join(cmd) if isinstance(cmd, list) else cmd
        print(f"  ❌ Command failed: {cmd_display}")
        if self.config.verbose:
            print(f"  Error code: {error.returncode}")
            if error.stderr:
                print(f"  Error: {error.stderr.strip()}")
        elif error.stderr:
            last_error = error.stderr.strip().split('\n')[-1]
            print(f"  Error: {last_error}")
class ProjectDetector:
    @staticmethod
    def detect_languages() -> List[str]:
        return [lang for lang, files in PROJECT_DETECTORS.items()
                if any(pathlib.Path(f).exists() for f in files)]
    @staticmethod
    def get_package_manager() -> Optional[str]:
        lock_files = [("pnpm-lock.yaml", "pnpm"), ("yarn.lock", "yarn"), ("package-lock.json", "npm")]
        for lock_file, pm in lock_files:
            if pathlib.Path(lock_file).exists() and ProjectDetector._has_command(pm):
                return pm
        return next((pm for pm in ["npm", "pnpm", "yarn"] if ProjectDetector._has_command(pm)), None)
    @staticmethod
    def _has_command(cmd: str) -> bool:
        try:
            subprocess.run(f"{cmd} --version", shell=True, check=True, 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
class ProjectSetup:
    def __init__(self, config: RuntimeConfig, runner: CommandRunner):
        self.config = config
        self.runner = runner
    def setup_python(self) -> bool:
        print("🐍 Python setup...")
        venv_dir = pathlib.Path(".venv")
        venv_pip = venv_dir / self.config.venv_paths["pip"]
        if not venv_dir.exists():
            print("  Creating virtual environment...")
            if not self.runner.execute([sys.executable, "-m", "venv", ".venv"]):
                return False
        return self._install_python_deps(str(venv_pip))
    def _install_python_deps(self, pip_path: str) -> bool:
        if pathlib.Path("requirements.txt").exists():
            print("  Installing requirements.txt...")
            return self.runner.execute([pip_path, "install", "-r", "requirements.txt"])
        elif pathlib.Path("pyproject.toml").exists():
            print("  Installing pyproject.toml...")
            return self.runner.execute([pip_path, "install", "-e", "."])
        return True
    def setup_node(self) -> bool:
        print("📦 Node.js setup...")
        pm = ProjectDetector.get_package_manager()
        if not pm:
            print("  ❌ No package manager found. Install Node.js from https://nodejs.org/")
            return False
        print(f"  Using: {pm}")
        if pm == "npm" and pathlib.Path("package-lock.json").exists():
            if self.runner.execute("npm ci"):
                return True
        return self.runner.execute(f"{pm} install")
    def setup_rust(self) -> bool:
        print("🦀 Rust setup...")
        if not ProjectDetector._has_command("cargo"):
            print("  ❌ Cargo not found. Install from https://rustup.rs/")
            return False
        return self.runner.execute(["cargo", "fetch"])
    def setup_flutter(self) -> bool:
        print("🐦 Flutter setup...")
        if not ProjectDetector._has_command("flutter"):
            print("  ❌ Flutter not found. Install from https://flutter.dev/")
            return False
        success = self.runner.execute("flutter pub get")
        if self._has_build_runner():
            success &= self.runner.execute("flutter packages pub run build_runner build --delete-conflicting-outputs")
        return success
    def _has_build_runner(self) -> bool:
        pubspec = pathlib.Path("pubspec.yaml")
        if not pubspec.exists() or self.config.dry_run:
            return False
        try:
            return "build_runner:" in pubspec.read_text()
        except (IOError, OSError):
            return False
    def setup_git_hooks(self) -> bool:
        if not pathlib.Path(".pre-commit-config.yaml").exists():
            return True
        print("🔗 Pre-commit setup...")
        python_cmd = self._get_python_executable()
        return self.runner.execute([python_cmd, "-m", "pre_commit", "install"])
    def _get_python_executable(self) -> str:
        venv_python = pathlib.Path(".venv") / self.config.venv_paths["python"]
        return str(venv_python) if venv_python.exists() else sys.executable
class CodeFormatter:
    def __init__(self, config: RuntimeConfig, runner: CommandRunner):
        self.config = config
        self.runner = runner
    def format_all(self, detected_languages: List[str]) -> bool:
        success = True
        if "python" in detected_languages:
            success &= self._format_python()
        if "node" in detected_languages:
            success &= self._format_node()
        if "flutter" in detected_languages:
            success &= self._format_flutter()
        return success
    def _format_python(self) -> bool:
        venv_python = pathlib.Path(".venv") / self.config.venv_paths["python"]
        if not venv_python.exists():
            return True
        formatters = [("ruff", [str(venv_python), "-m", "ruff", "format", "."]),
                     ("black", [str(venv_python), "-m", "black", "."])]
        for formatter_name, cmd in formatters:
            if self._has_python_package(str(venv_python), formatter_name):
                print(f"✨ Formatting with {formatter_name}...")
                return self.runner.execute(cmd)
        return True
    def _format_node(self) -> bool:
        if self._has_npm_format_script():
            print("✨ Running npm format...")
            return self.runner.execute("npm run format")
        prettier_configs = [".prettierrc", "prettier.config.js", ".prettierrc.json"]
        if any(pathlib.Path(config).exists() for config in prettier_configs):
            print("✨ Formatting with Prettier...")
            return self.runner.execute("npx prettier --write .")
        return True
    def _format_flutter(self) -> bool:
        print("✨ Formatting Dart...")
        return self.runner.execute("dart format .")
    def _has_python_package(self, python_exe: str, package: str) -> bool:
        try:
            subprocess.run([python_exe, "-c", f"import {package}"], 
                         check=True, capture_output=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    def _has_npm_format_script(self) -> bool:
        package_json = pathlib.Path("package.json")
        if not package_json.exists():
            return False
        try:
            pkg_data = json.loads(package_json.read_text())
            return "format" in pkg_data.get("scripts", {})
        except (json.JSONDecodeError, IOError):
            return False
def parse_arguments() -> RuntimeConfig:
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        print("\nOptions:")
        print("  -n, --dry-run    Show what would be done without executing")
        print("  -v, --verbose    Show detailed output and error messages")
        print("  -h, --help       Show this help message")
        sys.exit(0)
    return RuntimeConfig(
        dry_run="--dry-run" in sys.argv or "-n" in sys.argv,
        verbose="--verbose" in sys.argv or "-v" in sys.argv
    )
def main():
    config = parse_arguments()
    runner = CommandRunner(config)
    setup = ProjectSetup(config, runner)
    formatter = CodeFormatter(config, runner)
    print("🔍 Detecting projects...")
    detected = ProjectDetector.detect_languages()
    if not detected:
        print("No supported projects found.")
        return
    print(f"✅ Found: {', '.join(detected)}")
    setup_methods = {
        "python": setup.setup_python, "node": setup.setup_node, "rust": setup.setup_rust,
        "flutter": setup.setup_flutter, "git": setup.setup_git_hooks
    }
    success = all(setup_methods[project_type]() for project_type in detected
                  if project_type in setup_methods)
    success &= formatter.format_all(detected)
    if success:
        print("\n🎉 Setup complete!")
        if "python" in detected:
            activate_cmd = (".venv\\Scripts\\activate" if config.is_windows 
                          else "source .venv/bin/activate")
            print(f"💡 Activate: {activate_cmd}")
    else:
        print("\n⚠️ Some steps failed.")
        if not config.verbose:
            print("💡 Run with -v flag for detailed errors")
        sys.exit(1)
if __name__ == "__main__":
    main()