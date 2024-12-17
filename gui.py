import tkinter as tk
from tkinter import filedialog, messagebox
from pdf_processor import replace_highlight_colors_hex

# 预设的颜色映射
COLOR_MAPPING = {
    "#f0ff00": "#FFFBAB",
    "#00b036": "#CDE7B4",
    "#00f0ff": "#C2EBFF"
}

def execute_color_replacement(input_entry, output_entry):
    """执行 PDF 高亮颜色替换。"""
    input_pdf = input_entry.get()
    output_pdf = output_entry.get()
    
    if not input_pdf or not output_pdf:
        messagebox.showerror("错误", "请填写所有必要信息！")
        return
    
    try:
        replace_highlight_colors_hex(input_pdf, output_pdf, COLOR_MAPPING, tolerance=0.3)
        messagebox.showinfo("成功", f"处理完成！文件已保存到: {output_pdf}")
    except Exception as e:
        messagebox.showerror("错误", f"处理失败：{e}")

def select_input_file(entry):
    """弹出文件选择器选择输入文件。"""
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)

def select_output_file(entry):
    """弹出文件选择器选择输出文件路径。"""
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)

def create_gui():
    """创建 GUI 界面。"""
    root = tk.Tk()
    root.title("PDF 高亮颜色替换工具")
    
    tk.Label(root, text="输入 PDF 文件:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    input_entry = tk.Entry(root, width=50)
    input_entry.grid(row=0, column=1, padx=5, pady=5)
    tk.Button(root, text="选择文件", command=lambda: select_input_file(input_entry)).grid(row=0, column=2, padx=5, pady=5)
    
    tk.Label(root, text="输出 PDF 文件:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    output_entry = tk.Entry(root, width=50)
    output_entry.grid(row=1, column=1, padx=5, pady=5)
    tk.Button(root, text="选择路径", command=lambda: select_output_file(output_entry)).grid(row=1, column=2, padx=5, pady=5)
    
    tk.Button(root, text="开始处理", command=lambda: execute_color_replacement(input_entry, output_entry)).grid(row=2, column=0, columnspan=3, pady=10)
    
    root.mainloop()

