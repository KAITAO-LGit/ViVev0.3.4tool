#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ViVeTool Manager v3.9 - 未来科技风格
配置文件 - 包含多语言支持和样式定义
"""

import os
import json
from pathlib import Path


# ============== 未来科技风格配色 ==============
class Style:
    """科技风格样式定义"""
    
    # 主题色 - 赛博蓝
    PRIMARY = "#00D4FF"          # 霓虹蓝
    PRIMARY_DARK = "#0099CC"     # 深蓝
    PRIMARY_GLOW = "rgba(0, 212, 255, 0.3)"
    
    # 强调色
    ACCENT = "#FF6B6B"           # 珊瑚红
    SUCCESS = "#00FF88"          # 荧光绿
    WARNING = "#FFD93D"          # 亮黄
    ERROR = "#FF4757"            # 错误红
    
    # 背景色 - 深色主题
    BG_DARK = "#0A0E17"          # 深空黑
    BG_CARD = "#111827"          # 卡片黑
    BG_INPUT = "#1F2937"         # 输入框深灰
    BG_HOVER = "#374151"         # 悬停灰
    
    # 边框色
    BORDER = "#1E3A5F"           # 科技蓝边框
    BORDER_LIGHT = "#374151"     # 浅边框
    
    # 文字色
    TEXT_WHITE = "#FFFFFF"
    TEXT_GRAY = "#9CA3AF"
    TEXT_DIM = "#6B7280"
    
    # 渐变背景
    GRADIENT_DARK = "linear-gradient(135deg, #0A0E17 0%, #1E3A5F 100%)"
    GRADIENT_CARD = "linear-gradient(145deg, #111827 0%, #1F2937 100%)"


# ============== 字体定义 ==============
class Font:
    """字体配置"""
    # 使用系统原生字体，优先选择现代无衬线字体
    TITLE = ("Microsoft YaHei UI", 20, "bold")
    SUBTITLE = ("Microsoft YaHei UI", 14, "bold")
    BODY = ("Microsoft YaHei UI", 11)
    BUTTON = ("Microsoft YaHei UI", 10, "bold")
    INPUT = ("Microsoft YaHei UI", 11)
    LOG = ("Consolas", 10)
    STATUS = ("Microsoft YaHei UI", 9)


# ============== 多语言翻译 ==============
LANG = {
    "zh": {
        # 窗口
        "title": "ViVeTool Manager",
        "version": "v3.9 KAITAO-LGit",
        
        # 配置区域
        "config_title": "⚙️ 系统配置",
        "path_label": "📂 ViVeTool 路径",
        "path_searching": "🔍 正在自动搜索...",
        "path_found": "✅ ViVeTool 已就绪",
        "path_not_found": "❌ 未找到 ViVeTool",
        "btn_search": "🔍 智能搜索",
        "btn_browse": "📂 浏览文件夹",
        "btn_lang": "English",
        
        # 功能区域
        "features_title": "🎛️ 功能管理",
        "feature_id_label": "✨ 功能 ID",
        "feature_placeholder": "输入功能 ID（如：57048231）",
        "btn_add": "➕ 添加",
        "btn_clear": "🗑️ 清空",
        "btn_default": "🔄 恢复默认",
        "current_list": "📋 当前列表",
        
        # 操作按钮
        "btn_enable": "🚀 启用功能",
        "btn_disable": "🛑 禁用功能",
        "btn_clear_log": "✨ 清空日志",
        
        # 日志区域
        "log_title": "📊 执行日志",
        
        # 状态
        "status_ready": "✨ 就绪 - 等待操作",
        "status_searching": "🔍 正在搜索 ViVeTool...",
        "status_found": "✅ ViVeTool 路径已确定",
        "status_not_found": "⚠️ 请选择 ViVeTool 路径",
        "status_running": "⚡ 正在执行命令...",
        "status_success": "✅ 操作成功完成",
        "status_error": "❌ 执行过程中发生错误",
        
        # 成功提示
        "success_title": "🎉 成功",
        "success_msg": "命令已成功执行！系统更改已生效。",
        "restart_prompt": "🔄 请立即重启计算机以应用更改",
        "btn_restart": "🔄 立即重启",
        
        # 错误提示
        "error_title": "⚠️ 错误",
        "error_not_found": "未找到 ViVeTool 文件夹！请点击「浏览文件夹」手动选择路径。",
        "error_invalid_id": "无效的功能 ID！ID 必须是纯数字。",
        "error_no_id": "请输入功能 ID！",
        "error_no_selection": "请至少选择一个功能！",
        "error_execution": "命令执行失败",
        "error_restart": "无法重启计算机，请手动重启",
        "error_bat_create": "无法创建临时批处理文件",
        "error_command_send": "命令发送失败",
        
        # 确认对话框
        "confirm_title": "⚡ 确认操作",
        "confirm_clear": "确定要清空所有功能 ID 吗？",
        "confirm_enable": "确定要启用以下功能吗？",
        "confirm_disable": "确定要禁用以下功能吗？",
        
        # 信息提示
        "info_title": "ℹ️ 信息",
        "info_already_exists": "功能 ID 已在列表中：",
        "info_id_added": "功能 ID 已添加：",
        "info_ids_cleared": "已清空所有功能 ID",
        "info_ids_restored": "已恢复默认功能 ID",
        
        # 管理员
        "admin_title": "🛡️ 需要管理员权限",
        "admin_msg": "此操作需要管理员权限。是否立即以管理员身份重新运行？",
        "admin_warning": "⚠️ 权限不足！程序需要管理员权限才能执行此操作。",
        
        # 重启对话框
        "restart_title": "🔄 重启计算机",
        "restart_msg": "确定要重启计算机吗？请先保存所有未保存的工作！",
        "restart_success": "重启命令已发送",
        
        # 按钮
        "yes": "是",
        "no": "否",
        "ok": "确定",
        "cancel": "取消",
        "close": "关闭",
    },
    "en": {
        # Window
        "title": "ViVeTool Manager",
        "version": "v3.9 Future Edition",
        
        # Config section
        "config_title": "⚙️ System Config",
        "path_label": "📂 ViVeTool Path",
        "path_searching": "🔍 Auto searching...",
        "path_found": "✅ ViVeTool Ready",
        "path_not_found": "❌ ViVeTool Not Found",
        "btn_search": "🔍 Smart Search",
        "btn_browse": "📂 Browse Folder",
        "btn_lang": "中文",
        
        # Features section
        "features_title": "🎛️ Feature Management",
        "feature_id_label": "✨ Feature ID",
        "feature_placeholder": "Enter Feature ID (e.g., 57048231)",
        "btn_add": "➕ Add",
        "btn_clear": "🗑️ Clear",
        "btn_default": "🔄 Restore Default",
        "current_list": "📋 Current List",
        
        # Action buttons
        "btn_enable": "🚀 Enable Features",
        "btn_disable": "🛑 Disable Features",
        "btn_clear_log": "✨ Clear Log",
        
        # Log section
        "log_title": "📊 Execution Log",
        
        # Status
        "status_ready": "✨ Ready - Waiting for operation",
        "status_searching": "🔍 Searching for ViVeTool...",
        "status_found": "✅ ViVeTool path confirmed",
        "status_not_found": "⚠️ Please select ViVeTool path",
        "status_running": "⚡ Executing command...",
        "status_success": "✅ Operation completed successfully",
        "status_error": "❌ An error occurred during execution",
        
        # Success messages
        "success_title": "🎉 Success",
        "success_msg": "Command executed successfully! System changes have been applied.",
        "restart_prompt": "🔄 Please restart your computer now to apply changes",
        "btn_restart": "🔄 Restart Now",
        
        # Error messages
        "error_title": "⚠️ Error",
        "error_not_found": "ViVeTool folder not found! Click 'Browse Folder' to select the path manually.",
        "error_invalid_id": "Invalid Feature ID! ID must be numeric.",
        "error_no_id": "Please enter a Feature ID!",
        "error_no_selection": "Please select at least one feature!",
        "error_execution": "Command execution failed",
        "error_restart": "Cannot restart computer, please restart manually",
        "error_bat_create": "Cannot create temporary batch file",
        "error_command_send": "Failed to send command",
        
        # Confirmation dialogs
        "confirm_title": "⚡ Confirm Operation",
        "confirm_clear": "Are you sure you want to clear all Feature IDs?",
        "confirm_enable": "Are you sure you want to enable these features?",
        "confirm_disable": "Are you sure you want to disable these features?",
        
        # Info messages
        "info_title": "ℹ️ Info",
        "info_already_exists": "Feature ID already in list: ",
        "info_id_added": "Feature ID added: ",
        "info_ids_cleared": "All Feature IDs have been cleared",
        "info_ids_restored": "Default Feature IDs have been restored",
        
        # Admin
        "admin_title": "🛡️ Administrator Required",
        "admin_msg": "This operation requires administrator privileges. Restart as administrator now?",
        "admin_warning": "⚠️ Insufficient privileges! Administrator rights are required to perform this operation.",
        
        # Restart dialog
        "restart_title": "🔄 Restart Computer",
        "restart_msg": "Are you sure you want to restart? Please save all unsaved work first!",
        "restart_success": "Restart command sent",
        
        # Buttons
        "yes": "Yes",
        "no": "No",
        "ok": "OK",
        "cancel": "Cancel",
        "close": "Close",
    }
}


# ============== 配置管理 ==============
class Config:
    """配置管理器"""
    
    def __init__(self):
        self.config_file = Path(__file__).parent / "config.json"
        self.data = {
            "language": "zh",
            "vivetool_path": "",
            "feature_ids": ["57048231", "47205210", "56328729", "48433719"],
        }
        self.load()
    
    def load(self):
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    saved = json.load(f)
                    self.data.update(saved)
            except Exception as e:
                print(f"加载配置文件失败: {e}")
    
    def save(self):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"保存配置文件失败: {e}")
    
    @property
    def language(self):
        return self.data.get("language", "zh")
    
    @language.setter
    def language(self, value):
        self.data["language"] = value
        self.save()
    
    @property
    def vivetool_path(self):
        return self.data.get("vivetool_path", "")
    
    @vivetool_path.setter
    def vivetool_path(self, value):
        self.data["vivetool_path"] = value
        self.save()
    
    @property
    def feature_ids(self):
        return self.data.get("feature_ids", [])
    
    @feature_ids.setter
    def feature_ids(self, value):
        self.data["feature_ids"] = value
        self.save()
    
    def get(self, key):
        """获取当前语言文本"""
        lang = self.language
        if lang not in LANG:
            lang = "zh"
        return LANG[lang].get(key, key)
    
    def switch(self):
        """切换语言"""
        new_lang = "en" if self.language == "zh" else "zh"
        self.language = new_lang
        return new_lang


config = Config()


# ============== 默认值 ==============
DEFAULT_IDS = ["57048231", "47205210", "56328729", "48433719"]
