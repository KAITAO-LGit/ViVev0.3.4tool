#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ViVeTool Manager v3.9 - 工具函数模块
"""

import os
import sys
import subprocess
import threading
import ctypes
import time
from pathlib import Path
from typing import Optional, Tuple


def is_admin() -> bool:
    """检查管理员权限"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print(f"检查管理员权限失败: {e}")
        return False


def run_as_admin(script_path: Optional[str] = None) -> bool:
    """以管理员身份运行"""
    if script_path is None:
        script_path = os.path.abspath(sys.argv[0])
    try:
        ret = ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, f'"{script_path}"', None, 1
        )
        return ret > 32
    except Exception as e:
        print(f"请求管理员权限失败: {e}")
        return False


def find_vivetool() -> Optional[str]:
    """搜索ViVeTool文件夹"""
    search_paths = [
        Path.home() / "Downloads",
        Path.home() / "Desktop",
        Path.home() / "Documents",
        Path("C:/Downloads"),
        Path("D:/Downloads"),
    ]
    names = [
        "ViVeTool-v0.3.4-IntelAmd",
        "ViVeTool-v0.3.4",
        "ViVeTool-v0.3.3",
        "ViVeTool-v0.3.2",
        "ViVeTool",
    ]
    for base in search_paths:
        if not base.exists():
            continue
        for name in names:
            path = base / name
            if path.is_dir():
                return str(path)
    return None


def run_command_admin(command: str, working_dir: Optional[str] = None) -> Tuple[bool, str]:
    """以管理员身份执行命令"""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        bat_path = os.path.join(script_dir, "temp_run.bat")

        # 创建批处理文件 - 使用UTF-8编码，避免latin-1编码问题
        try:
            with open(bat_path, 'w', encoding='utf-8') as f:
                f.write("@echo off\n")
                f.write("chcp 65001 >nul\n")
                f.write("echo ======================================================\n")
                f.write("echo                  KAITAO-LGit v3.9 \n")#cmd标题
                f.write("echo ======================================================\n")
                f.write("echo.\n")
                if working_dir and os.path.isdir(working_dir):
                    f.write(f'cd /d "{working_dir}"\n')
                f.write(f"{command}\n")
                f.write("echo.\n")
                f.write("echo ======================================================\n")
                f.write("echo Done. Press any key to exit...\n")
                f.write("pause >nul\n")
        except Exception as e:
            return False, f"创建批处理文件失败: {str(e)}"

        # 以管理员身份执行
        try:
            ret = ctypes.windll.shell32.ShellExecuteW(
                None, "runas", "cmd.exe", f'/c "{bat_path}"', None, 1
            )
            if ret <= 32:
                return False, "ShellExecuteW 执行失败"
        except Exception as e:
            return False, f"执行命令失败: {str(e)}"

        # 延迟清理临时文件
        def cleanup():
            try:
                time.sleep(5)
                if os.path.exists(bat_path):
                    os.remove(bat_path)
            except Exception as e:
                print(f"清理临时文件失败: {e}")

        threading.Thread(target=cleanup, daemon=True).start()
        return True, "命令已发送"

    except Exception as e:
        return False, f"执行过程中发生错误: {str(e)}"


def validate_id(text: str) -> bool:
    """验证功能ID"""
    return bool(text.strip().isdigit())


def format_ids(ids: list) -> str:
    """格式化ID列表"""
    valid = [i.strip() for i in ids if i.strip().isdigit()]
    return ",".join(valid)


def get_default_ids() -> list:
    """获取默认ID"""
    return ["57048231", "47205210", "56328729", "48433719"]


def restart_pc() -> bool:
    """重启计算机"""
    try:
        # 使用 shutdown 命令重启（兼容性更好，支持所有Windows版本）
        import subprocess
        result = subprocess.run(
            ["shutdown", "/r", "/t", "0"],
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        if result.returncode == 0:
            return True
        else:
            # 如果上述方法失败，尝试使用 Windows API
            try:
                ctypes.windll.shell32.ShutdownSystem(2)
                return True
            except:
                return False
    except Exception as e:
        print(f"重启计算机失败: {e}")
        return False
