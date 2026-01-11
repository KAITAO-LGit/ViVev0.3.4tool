#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ViVeTool Manager v3.9 - 主程序
"""

import os
import sys
from pathlib import Path

from style import config, Style, Font, DEFAULT_IDS
from utils import (
    is_admin, run_as_admin, find_vivetool,
    run_command_admin, validate_id, format_ids,
    get_default_ids, restart_pc
)

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog, scrolledtext
    import ctypes
except ImportError:
    print("错误：tkinter未安装。请安装Python后重试。")
    input("按回车键退出...")
    sys.exit(1)


class ViveToolApp:
    """ViVeTool Manager 主窗口"""
    
    def __init__(self, root):
        self.root = root
        self.vivetool_path = None
        self.current_ids = config.feature_ids.copy()
        
        # 所有需要刷新UI的组件引用
        self.ui_components = {}
        
        self.setup_window()
        self.setup_styles()
        self.create_ui()
        self.init_app()
    
    def setup_window(self):
        """设置窗口"""
        self.root.title(config.get("title"))
        self.root.geometry("1080x720")
        self.root.minsize(700, 600)
        self.root.configure(bg=Style.BG_DARK)
        
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception as e:
            self.log(f"设置DPI Awareness失败: {e}", "warning")
    
    def setup_styles(self):
        """配置样式"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # 配置ttk样式
        self.style.configure("TFrame", background=Style.BG_DARK)
        self.style.configure("TLabel", background=Style.BG_DARK, foreground=Style.TEXT_WHITE)
        self.style.configure("TButton", font=Font.BUTTON, foreground=Style.TEXT_WHITE)
    
    def create_ui(self):
        """创建界面"""
        # 主容器
        main = tk.Frame(self.root, bg=Style.BG_DARK, padx=20, pady=15)
        main.pack(fill=tk.BOTH, expand=True)
        

        self.create_header(main)
        

        content = tk.Frame(main, bg=Style.BG_DARK)
        content.pack(fill=tk.BOTH, expand=True, pady=15)
        
        
        left_panel = tk.Frame(content, bg=Style.BG_DARK)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # 右侧面板 - 日志
        right_panel = tk.Frame(content, bg=Style.BG_DARK, width=350)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH)
        
        # 配置区域
        self.create_config_panel(left_panel)
        
        # 功能区域
        self.create_features_panel(left_panel)
        
        # 操作按钮
        self.create_action_panel(left_panel)
        
        # 日志区域
        self.create_log_panel(right_panel)
        
        # 状态栏
        self.create_status_bar(main)
    
    def create_header(self, parent):
        """创建标题栏"""
        header = tk.Frame(parent, bg=Style.BG_DARK)
        header.pack(fill=tk.X, pady=(0, 15))
        
        # 标题
        self.ui_components['title'] = tk.Label(
            header,
            text="✨ " + config.get("title") + " " + config.get("version"),
            font=Font.TITLE,
            bg=Style.BG_DARK,
            fg=Style.PRIMARY
        )
        self.ui_components['title'].pack(side=tk.LEFT)
        
        # 语言切换按钮
        self.ui_components['lang_btn'] = tk.Button(
            header,
            text=config.get("btn_lang"),
            font=Font.BODY,
            bg=Style.BG_CARD,
            fg=Style.PRIMARY,
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=5,
            command=self.toggle_language,
            cursor="hand2"
        )
        self.ui_components['lang_btn'].pack(side=tk.RIGHT)
    
    def create_config_panel(self, parent):
        """创建配置面板"""
        # 卡片容器
        card = tk.Frame(parent, bg=Style.BG_CARD, bd=1, relief=tk.SOLID)
        card.pack(fill=tk.X, pady=(0, 10))
        
        inner = tk.Frame(card, bg=Style.BG_CARD, padx=15, pady=12)
        inner.pack(fill=tk.X)
        
        # 标题
        self.ui_components['config_title'] = tk.Label(
            inner,
            text=config.get("config_title"),
            font=Font.SUBTITLE,
            bg=Style.BG_CARD,
            fg=Style.PRIMARY
        )
        self.ui_components['config_title'].pack(anchor=tk.W, pady=(0, 10))
        
        # 路径行
        path_row = tk.Frame(inner, bg=Style.BG_CARD)
        path_row.pack(fill=tk.X, pady=(0, 8))
        
        self.ui_components['path_label'] = tk.Label(
            path_row,
            text=config.get("path_label"),
            font=Font.BODY,
            bg=Style.BG_CARD,
            fg=Style.TEXT_GRAY,
            width=16,
            anchor=tk.W
        )
        self.ui_components['path_label'].pack(side=tk.LEFT)
        
        self.path_var = tk.StringVar(value=config.get("path_searching"))
        self.ui_components['path_entry'] = tk.Entry(
            path_row,
            textvariable=self.path_var,
            font=Font.LOG,
            bg=Style.BG_INPUT,
            fg=Style.TEXT_WHITE,
            readonlybackground=Style.BG_INPUT,
            state="readonly",
            relief=tk.FLAT,
            bd=0
        )
        self.ui_components['path_entry'].pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        
        # 按钮行
        btn_row = tk.Frame(inner, bg=Style.BG_CARD)
        btn_row.pack(fill=tk.X, pady=(8, 0))
        
        self.ui_components['search_btn'] = self.create_tech_button(btn_row, config.get("btn_search"), self.search)
        self.ui_components['browse_btn'] = self.create_tech_button(btn_row, config.get("btn_browse"), self.browse, secondary=True)
    
    def create_features_panel(self, parent):
        """创建功能面板"""
        card = tk.Frame(parent, bg=Style.BG_CARD, bd=1, relief=tk.SOLID)
        card.pack(fill=tk.X, pady=(0, 10))
        
        inner = tk.Frame(card, bg=Style.BG_CARD, padx=15, pady=12)
        inner.pack(fill=tk.X)
        
        # 标题
        self.ui_components['features_title'] = tk.Label(
            inner,
            text=config.get("features_title"),
            font=Font.SUBTITLE,
            bg=Style.BG_CARD,
            fg=Style.PRIMARY
        )
        self.ui_components['features_title'].pack(anchor=tk.W, pady=(0, 10))
        
        # 当前列表
        self.ids_text = tk.Text(
            inner,
            height=6,
            font=Font.LOG,
            wrap=tk.WORD,
            bg=Style.BG_INPUT,
            fg=Style.SUCCESS,
            state="disabled",
            relief=tk.FLAT,
            bd=0
        )
        self.ids_text.pack(fill=tk.X, pady=(0, 10))
        
        # 添加行
        add_row = tk.Frame(inner, bg=Style.BG_CARD)
        add_row.pack(fill=tk.X)
        
        self.ui_components['feature_id_label'] = tk.Label(
            add_row,
            text=config.get("feature_id_label"),
            font=Font.BODY,
            bg=Style.BG_CARD,
            fg=Style.TEXT_GRAY
        )
        self.ui_components['feature_id_label'].pack(side=tk.LEFT)
        
        self.custom_id_var = tk.StringVar()
        self.ui_components['custom_id_entry'] = tk.Entry(
            add_row,
            textvariable=self.custom_id_var,
            font=Font.INPUT,
            bg=Style.BG_INPUT,
            fg=Style.TEXT_WHITE,
            relief=tk.FLAT,
            bd=0
        )
        self.ui_components['custom_id_entry'].pack(side=tk.LEFT, padx=(8, 5))
        self.ui_components['custom_id_entry'].bind('<Return>', lambda e: self.add_id())
        
        # 按钮行
        btn_row = tk.Frame(inner, bg=Style.BG_CARD)
        btn_row.pack(fill=tk.X, pady=(8, 0))
        
        self.ui_components['add_btn'] = self.create_tech_button(btn_row, config.get("btn_add"), self.add_id)
        self.ui_components['clear_btn'] = self.create_tech_button(btn_row, config.get("btn_clear"), self.clear_ids, secondary=True)
        self.ui_components['default_btn'] = self.create_tech_button(btn_row, config.get("btn_default"), self.restore_default, secondary=True)
    
    def create_action_panel(self, parent):
        """创建操作按钮面板"""
        btn_frame = tk.Frame(parent, bg=Style.BG_DARK)
        btn_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 启用按钮
        self.ui_components['enable_btn'] = self.create_tech_button(
            btn_frame,
            config.get("btn_enable"),
            self.enable,
            success=True,
            expand=True
        )
        self.ui_components['enable_btn'].config(state=tk.DISABLED)
        
        # 禁用按钮
        self.ui_components['disable_btn'] = self.create_tech_button(
            btn_frame,
            config.get("btn_disable"),
            self.disable,
            error=True,
            expand=True
        )
        self.ui_components['disable_btn'].config(state=tk.DISABLED)
    
    def create_log_panel(self, parent):
        """创建日志面板"""
        card = tk.Frame(parent, bg=Style.BG_CARD, bd=1, relief=tk.SOLID)
        card.pack(fill=tk.BOTH, expand=True)
        
        inner = tk.Frame(card, bg=Style.BG_CARD, padx=15, pady=12)
        inner.pack(fill=tk.BOTH, expand=True)
        
        # 标题和清空按钮同行
        title_row = tk.Frame(inner, bg=Style.BG_CARD)
        title_row.pack(fill=tk.X, pady=(0, 8))
        
        self.ui_components['log_title'] = tk.Label(
            title_row,
            text=config.get("log_title"),
            font=Font.SUBTITLE,
            bg=Style.BG_CARD,
            fg=Style.PRIMARY
        )
        self.ui_components['log_title'].pack(side=tk.LEFT)
        
        self.ui_components['clear_log_btn'] = self.create_tech_button(
            title_row, 
            config.get("btn_clear_log"), 
            self.clear_log, 
            small=True, 
            secondary=True
        )
        
        # 日志文本框
        self.log_text = scrolledtext.ScrolledText(
            inner,
            font=Font.LOG,
            bg=Style.BG_INPUT,
            fg=Style.TEXT_WHITE,
            state="disabled",
            relief=tk.FLAT,
            bd=0
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # 配置日志颜色标签
        self.log_text.tag_config("success", foreground=Style.SUCCESS)
        self.log_text.tag_config("error", foreground=Style.ERROR)
        self.log_text.tag_config("warning", foreground=Style.WARNING)
        self.log_text.tag_config("info", foreground=Style.PRIMARY)
        
        # 结果提示区域
        self.result_frame = tk.Frame(inner, bg=Style.BG_CARD)
        self.result_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.result_label = tk.Label(
            self.result_frame,
            text="",
            font=Font.BODY,
            bg=Style.BG_CARD,
            fg=Style.SUCCESS,
            wraplength=300,
            justify=tk.LEFT
        )
        self.result_label.pack(anchor=tk.W)
        
        self.ui_components['restart_btn'] = self.create_tech_button(
            self.result_frame,
            config.get("btn_restart"),
            self.restart,
            warning=True
        )
        self.ui_components['restart_btn'].pack(anchor=tk.W, pady=(8, 0))
        self.ui_components['restart_btn'].config(state=tk.DISABLED)
    
    def create_status_bar(self, parent):
        """创建状态栏"""
        status = tk.Frame(parent, bg=Style.BG_CARD, bd=1, relief=tk.SOLID)
        status.pack(fill=tk.X, pady=(10, 0))
        
        self.status_var = tk.StringVar(value=config.get("status_ready"))
        self.ui_components['status_label'] = tk.Label(
            status,
            textvariable=self.status_var,
            font=Font.STATUS,
            bg=Style.BG_CARD,
            fg=Style.TEXT_DIM,
            padx=12,
            pady=8
        )
        self.ui_components['status_label'].pack(side=tk.LEFT)
    
    def create_tech_button(self, parent, text, command, success=False, error=False, warning=False, secondary=False, small=False, expand=False):
        """创建科技风格按钮"""
        if success:
            bg = Style.SUCCESS
        elif error:
            bg = Style.ERROR
        elif warning:
            bg = Style.WARNING
        elif secondary:
            bg = Style.BG_INPUT
        else:
            bg = Style.PRIMARY
        
        btn = tk.Button(
            parent,
            text=text,
            font=Font.BODY if not small else Font.STATUS,
            bg=bg,
            fg=Style.TEXT_WHITE,
            relief=tk.FLAT,
            bd=0,
            padx=12 if not small else 8,
            pady=6 if not small else 4,
            command=command,
            cursor="hand2"
        )
        
        if expand:
            btn.pack(side=tk.LEFT, padx=(0, 8), fill=tk.X, expand=True)
        else:
            btn.pack(side=tk.LEFT, padx=(0, 5))
        
        return btn
    
    def init_app(self):
        """初始化"""
        self.root.after(500, self.auto_search)
        self.update_ids_display()
    
    # ============== 搜索功能 ==============
    def auto_search(self):
        """自动搜索"""
        self.log("🔍 " + config.get("status_searching"), "info")
        path = find_vivetool()
        if path:
            self.set_path(path)
            self.log("✅ " + config.get("status_found"), "success")
        else:
            self.log("⚠️ " + config.get("status_not_found"), "warning")
            self.status_var.set(config.get("status_not_found"))
    
    def search(self):
        """手动搜索"""
        path = find_vivetool()
        if path:
            self.set_path(path)
            self.log("✅ " + path, "success")
        else:
            self.log("⚠️ " + config.get("status_not_found"), "warning")
            messagebox.showwarning(config.get("error_title"), config.get("error_not_found"))
    
    def browse(self):
        """浏览文件夹"""
        folder = filedialog.askdirectory(
            title=config.get("btn_browse"),
            initialdir=str(Path.home() / "Downloads")
        )
        if folder:
            self.set_path(folder)
            self.log("📂 " + folder, "info")
    
    def set_path(self, path):
        """设置路径"""
        self.vivetool_path = path
        self.path_var.set(path)
        config.vivetool_path = path
        self.ui_components['enable_btn'].config(state=tk.NORMAL)
        self.ui_components['disable_btn'].config(state=tk.NORMAL)
        self.status_var.set(config.get("status_found"))
    
    # ============== ID管理 ==============
    def update_ids_display(self):
        """更新ID显示"""
        self.ids_text.config(state="normal")
        self.ids_text.delete(1.0, tk.END)
        
        if not self.current_ids:
            self.ids_text.insert(tk.END, "  " + config.get("status_not_found") + "\n")
        else:
            for fid in self.current_ids:
                self.ids_text.insert(tk.END, "  ● " + fid + "\n")
        
        self.ids_text.config(state="disabled")
        count = len(self.current_ids)
        self.log("📋 " + config.get("current_list") + ": " + str(count) + " 个ID", "info")
    
    def add_id(self):
        """添加ID"""
        new_id = self.custom_id_var.get().strip()
        
        if not new_id:
            self.log("⚠️ " + config.get("error_no_id"), "warning")
            messagebox.showwarning(config.get("error_title"), config.get("error_no_id"))
            return
        
        if not validate_id(new_id):
            self.log("⚠️ " + config.get("error_invalid_id"), "error")
            messagebox.showwarning(config.get("error_title"), config.get("error_invalid_id"))
            return
        
        if new_id in self.current_ids:
            self.log("ℹ️ " + config.get("info_already_exists") + new_id, "info")
            messagebox.showinfo(config.get("info_title"), config.get("info_already_exists") + new_id)
            return
        
        self.current_ids.append(new_id)
        self.custom_id_var.set("")
        self.update_ids_display()
        self.log("✅ " + config.get("info_id_added") + new_id, "success")
    
    def clear_ids(self):
        """清空ID"""
        if messagebox.askyesno(config.get("confirm_title"), config.get("confirm_clear")):
            self.current_ids = []
            self.update_ids_display()
            self.log("🗑️ " + config.get("info_ids_cleared"), "warning")
    
    def restore_default(self):
        """恢复默认"""
        self.current_ids = get_default_ids()
        self.update_ids_display()
        self.log("🔄 " + config.get("info_ids_restored"), "info")
    
    # ============== 日志功能 ==============
    def log(self, message, level="info"):
        """输出日志"""
        try:
            self.log_text.config(state="normal")
            self.log_text.insert(tk.END, message + "\n")
            
            # 尝试应用标签
            try:
                self.log_text.tag_add(level, "end-2c linestart", "end-1c")
            except:
                pass
            
            self.log_text.see(tk.END)
            self.log_text.config(state="disabled")
            self.root.update_idletasks()
        except Exception as e:
            print(f"日志输出失败: {e}")
    
    def clear_log(self):
        """清空日志"""
        self.log_text.config(state="normal")
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state="disabled")
        self.result_label.config(text="")
        self.ui_components['restart_btn'].config(state=tk.DISABLED)
    
    def show_result(self, success, message=""):
        """显示操作结果"""
        if success:
            self.log("✅ " + config.get("success_msg"), "success")
            self.result_label.config(
                text="✅ " + config.get("success_msg") + "\n\n🔄 " + config.get("restart_prompt"),
                fg=Style.SUCCESS
            )
            self.ui_components['restart_btn'].config(state=tk.NORMAL)
        else:
            error_msg = config.get("error_execution")
            if message:
                error_msg += ": " + message
            self.log("❌ " + error_msg, "error")
            self.result_label.config(
                text="❌ " + error_msg,
                fg=Style.ERROR
            )
            self.ui_components['restart_btn'].config(state=tk.DISABLED)
    
    # ============== 操作功能 ==============
    def enable(self):
        """启用功能"""
        self.execute("enable")
    
    def disable(self):
        """禁用功能"""
        self.execute("disable")
    
    def execute(self, operation):
        """执行操作"""
        if not self.vivetool_path:
            self.log("⚠️ " + config.get("error_not_found"), "error")
            messagebox.showerror(config.get("error_title"), config.get("error_not_found"))
            return
        
        if not self.current_ids:
            self.log("⚠️ " + config.get("error_no_selection"), "error")
            messagebox.showerror(config.get("error_title"), config.get("error_no_selection"))
            return
        
        # 确认
        msg_key = "confirm_" + operation
        if not messagebox.askyesno(
            config.get("confirm_title"),
            config.get(msg_key) + "\n\n" + "\n".join(self.current_ids)
        ):
            return
        
        # 构建命令
        ids_str = format_ids(self.current_ids)
        cmd = "vivetool /" + operation + " /id:" + ids_str
        
        # 禁用按钮
        self.ui_components['enable_btn'].config(state=tk.DISABLED)
        self.ui_components['disable_btn'].config(state=tk.DISABLED)
        self.ui_components['restart_btn'].config(state=tk.DISABLED)
        self.result_label.config(text="")
        
        self.log("\n" + "═" * 55, "info")
        self.log("⚡ " + config.get("status_running"), "warning")
        self.log("📋 " + config.get("current_list") + ": " + ids_str, "info")
        self.log("═" * 55, "info")
        
        # 执行命令
        result, msg = run_command_admin(cmd, self.vivetool_path)
        
        if result:
            self.log("\n" + "═" * 55, "success")
            self.log("✅ " + config.get("status_success"), "success")
            self.log("═" * 55, "success")
            self.show_result(True, "")
        else:
            self.log("\n❌ " + config.get("error_execution") + ": " + msg, "error")
            self.show_result(False, msg)
            # 弹出错误提示
            messagebox.showerror(config.get("error_title"), config.get("error_execution") + "\n\n" + msg)
        
        # 恢复按钮状态
        if self.vivetool_path:
            self.ui_components['enable_btn'].config(state=tk.NORMAL)
            self.ui_components['disable_btn'].config(state=tk.NORMAL)
    
    def restart(self):
        """重启计算机"""
        if messagebox.askyesno(config.get("restart_title"), config.get("restart_msg")):
            try:
                if restart_pc():
                    self.log("🔄 " + config.get("restart_success"), "info")
                else:
                    error_msg = config.get("error_restart")
                    self.log("❌ " + error_msg, "error")
                    messagebox.showerror(config.get("error_title"), error_msg)
            except Exception as e:
                error_msg = config.get("error_restart") + ": " + str(e)
                self.log("❌ " + error_msg, "error")
                messagebox.showerror(config.get("error_title"), error_msg)
    
    # ============== 语言切换 ==============
    def toggle_language(self):
        """切换语言"""
        new_lang = config.switch()
        self.ui_components['lang_btn'].config(text=config.get("btn_lang"))
        self.refresh_ui()
        config.save()
        self.log("🌐 " + ("Switched to English" if new_lang == "en" else "已切换到中文"), "info")
    
    def refresh_ui(self):
        """刷新界面所有文本"""
        # 窗口标题
        self.root.title(config.get("title"))
        self.ui_components['title'].config(text="✨ " + config.get("title") + " " + config.get("version"))
        
        # 配置区域
        self.ui_components['config_title'].config(text=config.get("config_title"))
        self.ui_components['path_label'].config(text=config.get("path_label"))
        self.ui_components['search_btn'].config(text=config.get("btn_search"))
        self.ui_components['browse_btn'].config(text=config.get("btn_browse"))
        
        # 功能区域
        self.ui_components['features_title'].config(text=config.get("features_title"))
        self.ui_components['feature_id_label'].config(text=config.get("feature_id_label"))
        self.ui_components['add_btn'].config(text=config.get("btn_add"))
        self.ui_components['clear_btn'].config(text=config.get("btn_clear"))
        self.ui_components['default_btn'].config(text=config.get("btn_default"))
        
        # 操作按钮
        self.ui_components['enable_btn'].config(text=config.get("btn_enable"))
        self.ui_components['disable_btn'].config(text=config.get("btn_disable"))
        
        # 日志区域
        self.ui_components['log_title'].config(text=config.get("log_title"))
        self.ui_components['clear_log_btn'].config(text=config.get("btn_clear_log"))
        
        # 重启按钮
        self.ui_components['restart_btn'].config(text=config.get("btn_restart"))
        
        # 刷新路径显示
        if self.vivetool_path:
            self.path_var.set(self.vivetool_path)
        else:
            self.path_var.set(config.get("path_searching"))
        
        # 刷新状态栏
        self.status_var.set(config.get("status_ready"))


def check_admin():
    """检查管理员权限"""
    if not is_admin():
        if messagebox.askyesno(config.get("admin_title"), config.get("admin_msg"), icon=messagebox.WARNING):
            if run_as_admin():
                sys.exit(0)
        messagebox.showwarning(config.get("admin_title"), config.get("admin_warning"))


def main():
    """主函数"""
    try:
        check_admin()
        root = tk.Tk()
        app = ViveToolApp(root)
        root.mainloop()
    except Exception as e:
        print(f"程序发生错误: {e}")
        messagebox.showerror("错误", f"程序发生错误:\n{e}")


if __name__ == "__main__":
    main()
