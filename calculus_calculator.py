import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sympy as sp
from sympy import symbols, diff, integrate, limit, solve
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import json
import os


class CalculusCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("微积分计算器")
        self.root.geometry("1000x700")

        # 初始化笔记数据
        self.notes_data = []
        self.load_notes()

        # 创建主界面
        self.create_notebook()

    def create_notebook(self):
        """创建标签页界面"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.create_calculus_tab()
        self.create_arithmetic_tab()
        self.create_plot_tab()
        self.create_notes_tab()

    def create_calculus_tab(self):
        """创建微积分计算标签页"""
        calculus_frame = ttk.Frame(self.notebook)
        self.notebook.add(calculus_frame, text="微积分计算")

        # 标题
        title_label = ttk.Label(calculus_frame, text="微积分计算器",
                                font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))

        # 主框架
        main_frame = ttk.Frame(calculus_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20)

        # 计算类型选择
        type_frame = ttk.Frame(main_frame)
        type_frame.pack(fill=tk.X, pady=10)

        ttk.Label(type_frame, text="计算类型:").pack(side=tk.LEFT)
        self.calc_type = ttk.Combobox(type_frame, values=[
            "微分", "积分", "不定积分", "极限", "数值计算", "转折点分析", "求和运算"
        ], state="readonly", width=15)
        self.calc_type.set("微分")
        self.calc_type.pack(side=tk.LEFT, padx=10)
        self.calc_type.bind('<<ComboboxSelected>>', self.on_calc_type_change)

        # 函数表达式输入
        func_frame = ttk.Frame(main_frame)
        func_frame.pack(fill=tk.X, pady=10)

        ttk.Label(func_frame, text="函数表达式:").pack(side=tk.LEFT)
        self.function_entry = ttk.Entry(func_frame, font=('Arial', 14), width=30)
        self.function_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        self.function_entry.insert(0, "x**2")

        # 符号按钮行
        symbol_frame = ttk.Frame(main_frame)
        symbol_frame.pack(fill=tk.X, pady=5)

        symbols = ["x²", "x³", "x⁴", "x⁵", "xⁿ", "√x", "sin(x)", "cos(x)", "tan(x)",
                   "ln(x)", "log(x)", "e^x", "π", "∑"]
        for symbol in symbols:
            btn = ttk.Button(symbol_frame, text=symbol, width=6,
                             command=lambda s=symbol: self.insert_symbol(s))
            btn.pack(side=tk.LEFT, padx=2)

        # 参数框架 - 使用grid布局
        param_frame = ttk.Frame(main_frame)
        param_frame.pack(fill=tk.X, pady=10)

        # 变量输入
        ttk.Label(param_frame, text="变量:").grid(row=0, column=0, padx=(0, 5))
        self.variable_entry = ttk.Entry(param_frame, font=('Arial', 12), width=10)
        self.variable_entry.insert(0, "x")
        self.variable_entry.grid(row=0, column=1, padx=10)

        # 参数框架 - 使用grid布局
        self.limit_frame = ttk.Frame(param_frame)
        self.limit_frame.grid(row=0, column=2, padx=20)

        # 使用grid布局创建控件
        ttk.Label(self.limit_frame, text="下限:").grid(row=0, column=0, padx=(0, 5))
        self.lower_limit = ttk.Entry(self.limit_frame, width=8)
        self.lower_limit.grid(row=0, column=1, padx=5)

        ttk.Label(self.limit_frame, text="上限:").grid(row=0, column=2, padx=(0, 5))
        self.upper_limit = ttk.Entry(self.limit_frame, width=8)
        self.upper_limit.grid(row=0, column=3, padx=5)

        ttk.Label(self.limit_frame, text="极限点:").grid(row=0, column=4, padx=(0, 5))
        self.limit_point = ttk.Entry(self.limit_frame, width=8)
        self.limit_point.grid(row=0, column=5, padx=5)

        ttk.Label(self.limit_frame, text="计算点:").grid(row=0, column=6, padx=(0, 5))
        self.calc_point = ttk.Entry(self.limit_frame, width=8)
        self.calc_point.grid(row=0, column=7, padx=5)

        # 转折点分析参数
        ttk.Label(self.limit_frame, text="分析范围:").grid(row=0, column=8, padx=(0, 5))
        self.analysis_min = ttk.Entry(self.limit_frame, width=8)
        self.analysis_min.insert(0, "-10")
        self.analysis_min.grid(row=0, column=9, padx=5)

        ttk.Label(self.limit_frame, text="到").grid(row=0, column=10, padx=(0, 5))
        self.analysis_max = ttk.Entry(self.limit_frame, width=8)
        self.analysis_max.insert(0, "10")
        self.analysis_max.grid(row=0, column=11, padx=5)

        # 求和运算参数
        ttk.Label(self.limit_frame, text="起始:").grid(row=1, column=0, padx=(0, 5))
        self.sum_start = ttk.Entry(self.limit_frame, width=8)
        self.sum_start.insert(0, "1")
        self.sum_start.grid(row=1, column=1, padx=5)

        ttk.Label(self.limit_frame, text="终止:").grid(row=1, column=2, padx=(0, 5))
        self.sum_end = ttk.Entry(self.limit_frame, width=8)
        self.sum_end.insert(0, "10")
        self.sum_end.grid(row=1, column=3, padx=5)

        # 计算按钮
        calc_button = ttk.Button(main_frame, text="计算", command=self.calculate)
        calc_button.pack(pady=10)

        # 结果显示区域
        result_frame = ttk.LabelFrame(main_frame, text="计算结果")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.result_text = scrolledtext.ScrolledText(result_frame, font=('Arial', 11))
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 初始隐藏参数控件
        self.on_calc_type_change()

    def create_arithmetic_tab(self):
        """创建算术计算标签页"""
        arithmetic_frame = ttk.Frame(self.notebook)
        self.notebook.add(arithmetic_frame, text="算术计算")

        # 标题
        title_label = ttk.Label(arithmetic_frame, text="算术计算器",
                                font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))

        # 主框架
        main_frame = ttk.Frame(arithmetic_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20)

        # 表达式输入
        expr_frame = ttk.Frame(main_frame)
        expr_frame.pack(fill=tk.X, pady=10)

        ttk.Label(expr_frame, text="算术表达式:").pack(side=tk.LEFT)
        self.arithmetic_entry = ttk.Entry(expr_frame, font=('Arial', 14), width=30)
        self.arithmetic_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        self.arithmetic_entry.bind('<Return>', self.calculate_arithmetic)

        # 数字和运算符按钮
        button_frame = ttk.LabelFrame(main_frame, text="计算器")
        button_frame.pack(fill=tk.X, pady=10)

        # 按钮布局
        buttons = [
            ['7', '8', '9', '/', 'C'],
            ['4', '5', '6', '*', '('],
            ['1', '2', '3', '-', ')'],
            ['0', '.', '=', '+', '^']
        ]

        for row_buttons in buttons:
            row_frame = ttk.Frame(button_frame)
            row_frame.pack(fill=tk.X, padx=5, pady=2)
            for btn_text in row_buttons:
                btn = ttk.Button(row_frame, text=btn_text, width=8,
                                 command=lambda t=btn_text: self.arithmetic_button_click(t))
                btn.pack(side=tk.LEFT, padx=2)

        # 计算按钮
        calc_btn = ttk.Button(main_frame, text="计算", command=self.calculate_arithmetic)
        calc_btn.pack(pady=10)

        # 结果显示
        result_frame = ttk.LabelFrame(main_frame, text="计算结果")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.arithmetic_result = scrolledtext.ScrolledText(result_frame, font=('Arial', 12), height=8)
        self.arithmetic_result.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def create_plot_tab(self):
        """创建绘图标签页"""
        plot_frame = ttk.Frame(self.notebook)
        self.notebook.add(plot_frame, text="函数绘图")

        # 标题
        title_label = ttk.Label(plot_frame, text="函数绘图工具",
                                font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))

        # 主框架
        main_frame = ttk.Frame(plot_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20)

        # 函数表达式输入
        func_frame = ttk.Frame(main_frame)
        func_frame.pack(fill=tk.X, pady=10)

        ttk.Label(func_frame, text="函数表达式:").pack(side=tk.LEFT)
        self.plot_function_entry = ttk.Entry(func_frame, font=('Arial', 14), width=30)
        self.plot_function_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        self.plot_function_entry.insert(0, "x**2")

        # 绘图范围设置
        range_frame = ttk.Frame(main_frame)
        range_frame.pack(fill=tk.X, pady=10)

        ttk.Label(range_frame, text="x范围:").pack(side=tk.LEFT)
        self.plot_xmin = ttk.Entry(range_frame, width=8)
        self.plot_xmin.insert(0, "-10")
        self.plot_xmin.pack(side=tk.LEFT, padx=5)

        ttk.Label(range_frame, text="到").pack(side=tk.LEFT)
        self.plot_xmax = ttk.Entry(range_frame, width=8)
        self.plot_xmax.insert(0, "10")
        self.plot_xmax.pack(side=tk.LEFT, padx=5)

        # 绘图按钮
        plot_button = ttk.Button(main_frame, text="绘制函数图像", command=self.plot_function)
        plot_button.pack(pady=10)

        # 绘图区域
        self.plot_frame = ttk.Frame(main_frame)
        self.plot_frame.pack(fill=tk.BOTH, expand=True, pady=5)

    def create_notes_tab(self):
        """创建笔记标签页"""
        notes_frame = ttk.Frame(self.notebook)
        self.notebook.add(notes_frame, text="学习笔记")

        # 标题
        title_label = ttk.Label(notes_frame, text="学习笔记",
                                font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))

        # 主框架
        main_frame = ttk.Frame(notes_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20)

        # 笔记输入区域
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=10)

        ttk.Label(input_frame, text="笔记标题:").pack(side=tk.LEFT)
        self.note_title = ttk.Entry(input_frame, font=('Arial', 12), width=20)
        self.note_title.pack(side=tk.LEFT, padx=10)

        ttk.Label(input_frame, text="笔记内容:").pack(side=tk.LEFT)
        self.note_content = ttk.Entry(input_frame, font=('Arial', 12), width=40)
        self.note_content.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        self.note_content.bind('<Return>', self.add_note)

        # 添加笔记按钮
        add_button = ttk.Button(input_frame, text="添加笔记", command=self.add_note)
        add_button.pack(side=tk.LEFT, padx=10)

        # 笔记列表
        list_frame = ttk.LabelFrame(main_frame, text="笔记列表")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # 创建Treeview显示笔记
        self.notes_tree = ttk.Treeview(list_frame, columns=('title', 'content'), show='headings')
        self.notes_tree.heading('title', text='标题')
        self.notes_tree.heading('content', text='内容')
        self.notes_tree.column('title', width=150)
        self.notes_tree.column('content', width=400)
        self.notes_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 删除按钮
        delete_button = ttk.Button(list_frame, text="删除选中笔记", command=self.delete_note)
        delete_button.pack(pady=5)

        # 加载现有笔记
        self.refresh_notes()

    def on_calc_type_change(self, event=None):
        """根据计算类型显示/隐藏参数控件"""
        calc_type = self.calc_type.get()

        # 隐藏所有控件
        self.lower_limit.grid_remove()
        self.upper_limit.grid_remove()
        self.limit_point.grid_remove()
        self.calc_point.grid_remove()
        self.analysis_min.grid_remove()
        self.analysis_max.grid_remove()
        self.sum_start.grid_remove()
        self.sum_end.grid_remove()

        # 根据计算类型显示相应控件
        if calc_type == "积分":
            self.lower_limit.grid()
            self.upper_limit.grid()
        elif calc_type == "极限":
            self.limit_point.grid()
        elif calc_type == "数值计算":
            self.calc_point.grid()
        elif calc_type == "转折点分析":
            self.analysis_min.grid()
            self.analysis_max.grid()
        elif calc_type == "求和运算":
            self.sum_start.grid()
            self.sum_end.grid()

    def insert_symbol(self, symbol):
        """插入符号到函数表达式输入框"""
        current_text = self.function_entry.get()
        cursor_pos = self.function_entry.index(tk.INSERT)

        symbol_map = {
            "x²": "x**2", "x³": "x**3", "x⁴": "x**4", "x⁵": "x**5",
            "xⁿ": "x**n", "√x": "sqrt(x)", "sin(x)": "sin(x)",
            "cos(x)": "cos(x)", "tan(x)": "tan(x)", "ln(x)": "log(x)",
            "log(x)": "log10(x)", "e^x": "exp(x)", "π": "pi", "∑": "sum"
        }

        symbol_text = symbol_map.get(symbol, symbol)
        new_text = current_text[:cursor_pos] + symbol_text + current_text[cursor_pos:]
        self.function_entry.delete(0, tk.END)
        self.function_entry.insert(0, new_text)
        self.function_entry.focus_set()
        self.function_entry.icursor(cursor_pos + len(symbol_text))

    def calculate(self):
        """执行微积分计算"""
        try:
            # 获取输入
            function_text = self.function_entry.get().strip()
            variable_str = self.variable_entry.get().strip()
            calc_type = self.calc_type.get()

            if not function_text:
                messagebox.showerror("错误", "请输入函数表达式")
                return

            if not variable_str:
                messagebox.showerror("错误", "请输入变量")
                return

            # 定义符号变量
            x = symbols(variable_str)

            # 解析函数表达式
            try:
                function = sp.sympify(function_text)
            except:
                messagebox.showerror("错误", "函数表达式格式错误")
                return

            result = ""

            if calc_type == "微分":
                # 计算导数
                derivative = diff(function, x)
                result = f"函数: {function}\n"
                result += f"关于变量 {variable_str} 的导数:\n"
                result += f"d/d{variable_str}({function}) = {derivative}\n"
                result += f"简化形式: {sp.simplify(derivative)}\n"

                # 尝试数值计算
                try:
                    val = float(self.calc_point.get()) if hasattr(self,
                                                                  'calc_point') and self.calc_point.get().strip() else 1.0
                    numeric_result = derivative.subs(x, val)
                    result += f"在 {variable_str} = {val} 时，导数值 = {numeric_result}\n"
                except:
                    pass

            elif calc_type == "积分":
                # 检查控件是否存在
                if (hasattr(self, 'lower_limit') and hasattr(self, 'upper_limit') and
                        self.lower_limit.winfo_exists() and self.upper_limit.winfo_exists()):
                    lower_text = self.lower_limit.get().strip()
                    upper_text = self.upper_limit.get().strip()

                    if lower_text and upper_text:
                        # 定积分
                        try:
                            lower = float(lower_text)
                            upper = float(upper_text)
                            integral = integrate(function, (x, lower, upper))
                            result = f"函数: {function}\n"
                            result += f"从 {lower} 到 {upper} 的定积分:\n"
                            result += f"∫({function}) d{variable_str} = {integral}\n"
                            if isinstance(integral, sp.Float):
                                result += f"数值结果: {float(integral):.6f}\n"
                        except:
                            messagebox.showerror("错误", "积分上下限必须是有效数字")
                            return
                    else:
                        # 不定积分
                        integral = integrate(function, x)
                        result = f"函数: {function}\n"
                        result += f"关于变量 {variable_str} 的不定积分:\n"
                        result += f"∫({function}) d{variable_str} = {integral} + C\n"
                        result += f"简化形式: {sp.simplify(integral)} + C\n"
                else:
                    # 不定积分
                    integral = integrate(function, x)
                    result = f"函数: {function}\n"
                    result += f"关于变量 {variable_str} 的不定积分:\n"
                    result += f"∫({function}) d{variable_str} = {integral} + C\n"
                    result += f"简化形式: {sp.simplify(integral)} + C\n"

            elif calc_type == "不定积分":
                # 不定积分计算
                integral = integrate(function, x)
                result = f"函数: {function}\n"
                result += f"关于变量 {variable_str} 的不定积分:\n"
                result += f"∫({function}) d{variable_str} = {integral} + C\n"
                result += f"简化形式: {sp.simplify(integral)} + C\n"

            elif calc_type == "极限":
                if hasattr(self, 'limit_point') and self.limit_point.winfo_exists():
                    limit_point_text = self.limit_point.get().strip()
                    if not limit_point_text:
                        messagebox.showerror("错误", "请输入极限点")
                        return

                    try:
                        limit_val = float(limit_point_text)
                        limit_result = limit(function, x, limit_val)
                        result = f"函数: {function}\n"
                        result += f"当 {variable_str} → {limit_val} 时的极限:\n"
                        result += f"lim({function}) = {limit_result}\n"
                        if isinstance(limit_result, sp.Float):
                            result += f"数值结果: {float(limit_result):.6f}\n"
                    except:
                        messagebox.showerror("错误", "极限点必须是有效数字")
                        return

            elif calc_type == "数值计算":
                if hasattr(self, 'calc_point') and self.calc_point.winfo_exists():
                    calc_point_text = self.calc_point.get().strip()
                    if not calc_point_text:
                        messagebox.showerror("错误", "请输入计算点")
                        return

                    try:
                        calc_val = float(calc_point_text)
                        func_value = function.subs(x, calc_val)
                        result = f"函数: {function}\n"
                        result += f"在 {variable_str} = {calc_val} 时的函数值:\n"
                        result += f"f({calc_val}) = {func_value}\n"
                        if isinstance(func_value, sp.Float):
                            result += f"数值结果: {float(func_value):.6f}\n"
                    except:
                        messagebox.showerror("错误", "计算点必须是有效数字")
                        return

            elif calc_type == "转折点分析":
                if (hasattr(self, 'analysis_min') and hasattr(self, 'analysis_max') and
                        self.analysis_min.winfo_exists() and self.analysis_max.winfo_exists()):
                    min_text = self.analysis_min.get().strip()
                    max_text = self.analysis_max.get().strip()

                    if min_text and max_text:
                        try:
                            min_val = float(min_text)
                            max_val = float(max_text)
                            result = self.analyze_critical_points(function, x)
                        except:
                            messagebox.showerror("错误", "分析范围必须是有效数字")
                            return
                    else:
                        result = self.analyze_critical_points(function, x)
                else:
                    result = self.analyze_critical_points(function, x)

            elif calc_type == "求和运算":
                # 显示求和参数控件
                self.limit_frame.grid()
                self.lower_limit.grid_remove()
                self.upper_limit.grid_remove()
                self.limit_point.grid_remove()
                self.calc_point.grid_remove()
                self.analysis_min.grid_remove()
                self.analysis_max.grid_remove()
                self.sum_start.grid()
                self.sum_end.grid()

                # 检查求和参数
                if (hasattr(self, 'sum_start') and hasattr(self, 'sum_end') and
                        self.sum_start.winfo_exists() and self.sum_end.winfo_exists()):
                    start_text = self.sum_start.get().strip()
                    end_text = self.sum_end.get().strip()

                    if not start_text or not end_text:
                        messagebox.showerror("错误", "请输入求和的起始和终止值")
                        return

                    try:
                        start_val = int(start_text)
                        end_val = int(end_text)

                        if start_val > end_val:
                            messagebox.showerror("错误", "起始值不能大于终止值")
                            return

                        # 计算求和
                        total = 0
                        partial_terms = []

                        for i in range(start_val, end_val + 1):
                            term_value = function.subs(x, i)
                            total += term_value
                            if len(partial_terms) < 5:  # 只显示前5项
                                partial_terms.append(f"f({i}) = {term_value}")

                        result = f"函数: {function}\n"
                        result += f"求和运算: ∑({function}) 从 {variable_str} = {start_val} 到 {end_val}\n"
                        result += f"总和: {total}\n"

                        if isinstance(total, sp.Float):
                            result += f"数值结果: {float(total):.6f}\n"

                        result += f"\n部分项计算结果:\n"
                        for term in partial_terms:
                            result += f"{term}\n"

                        if len(partial_terms) < (end_val - start_val + 1):
                            result += f"... 还有 {end_val - start_val + 1 - len(partial_terms)} 项未显示\n"

                    except ValueError:
                        messagebox.showerror("错误", "求和起始和终止值必须是整数")
                        return
                    except Exception as e:
                        messagebox.showerror("错误", f"求和计算失败: {str(e)}")
                        return

            else:
                messagebox.showerror("错误", "未知的计算类型")
                return

            # 显示结果
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(1.0, result)

        except Exception as e:
            messagebox.showerror("错误", f"计算失败: {str(e)}")

    def analyze_critical_points(self, function, x):
        """分析函数的转折点"""
        try:
            # 计算一阶导数
            first_derivative = diff(function, x)

            # 计算二阶导数
            second_derivative = diff(first_derivative, x)

            # 求解一阶导数为零的点
            critical_points = solve(first_derivative, x)

            result = f"函数: {function}\n"
            result += f"一阶导数: {first_derivative}\n"
            result += f"二阶导数: {second_derivative}\n\n"

            if critical_points:
                result += "临界点分析:\n"
                for point in critical_points:
                    try:
                        # 计算二阶导数在临界点的值
                        second_deriv_value = second_derivative.subs(x, point)

                        if second_deriv_value > 0:
                            point_type = "局部最小值"
                        elif second_deriv_value < 0:
                            point_type = "局部最大值"
                        else:
                            point_type = "拐点或不确定"

                        result += f"在 {x} = {point}: {point_type}\n"
                    except:
                        result += f"在 {x} = {point}: 无法确定类型\n"
            else:
                result += "未找到临界点\n"

            return result

        except Exception as e:
            return f"转折点分析失败: {str(e)}"

    def arithmetic_button_click(self, text):
        """算术计算器按钮点击处理"""
        if text == 'C':
            self.arithmetic_entry.delete(0, tk.END)
        elif text == '=':
            self.calculate_arithmetic()
        else:
            current = self.arithmetic_entry.get()
            self.arithmetic_entry.delete(0, tk.END)
            self.arithmetic_entry.insert(0, current + text)

    def calculate_arithmetic(self, event=None):
        """执行算术计算"""
        try:
            expression = self.arithmetic_entry.get().strip()
            if not expression:
                return

            # 替换符号
            expression = expression.replace('^', '**')

            # 安全计算
            result = eval(expression)

            self.arithmetic_result.delete(1.0, tk.END)
            self.arithmetic_result.insert(1.0, f"表达式: {expression}\n结果: {result}")

        except Exception as e:
            self.arithmetic_result.delete(1.0, tk.END)
            self.arithmetic_result.insert(1.0, f"计算错误: {str(e)}")

    def plot_function(self):
        """绘制函数图像"""
        try:
            function_text = self.plot_function_entry.get().strip()
            if not function_text:
                messagebox.showerror("错误", "请输入函数表达式")
                return

            # 获取x范围
            try:
                xmin = float(self.plot_xmin.get())
                xmax = float(self.plot_xmax.get())
            except:
                xmin, xmax = -10, 10

            # 定义符号变量
            x = symbols('x')

            # 解析函数
            function = sp.sympify(function_text)

            # 转换为numpy函数
            func_np = sp.lambdify(x, function, 'numpy')

            # 生成x值
            x_vals = np.linspace(xmin, xmax, 1000)
            y_vals = func_np(x_vals)

            # 创建图形
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.plot(x_vals, y_vals, 'b-', linewidth=2)
            ax.set_xlabel('x')
            ax.set_ylabel('f(x)')
            ax.set_title(f'函数图像: {function_text}')
            ax.grid(True)

            # 清除旧的绘图
            for widget in self.plot_frame.winfo_children():
                widget.destroy()

            # 嵌入图形到Tkinter
            canvas = FigureCanvasTkAgg(fig, self.plot_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            messagebox.showerror("错误", f"绘图失败: {str(e)}")

    def load_notes(self):
        """加载笔记数据"""
        try:
            if os.path.exists('notes.json'):
                with open('notes.json', 'r', encoding='utf-8') as f:
                    self.notes_data = json.load(f)
        except:
            self.notes_data = []

    def save_notes(self):
        """保存笔记数据"""
        try:
            with open('notes.json', 'w', encoding='utf-8') as f:
                json.dump(self.notes_data, f, ensure_ascii=False, indent=2)
        except:
            pass

    def add_note(self, event=None):
        """添加笔记"""
        title = self.note_title.get().strip()
        content = self.note_content.get().strip()

        if not title or not content:
            messagebox.showerror("错误", "请输入笔记标题和内容")
            return

        self.notes_data.append({
            'title': title,
            'content': content
        })

        self.note_title.delete(0, tk.END)
        self.note_content.delete(0, tk.END)
        self.save_notes()
        self.refresh_notes()

    def delete_note(self):
        """删除选中笔记"""
        selection = self.notes_tree.selection()
        if not selection:
            messagebox.showerror("错误", "请选择要删除的笔记")
            return

        for item in selection:
            index = self.notes_tree.index(item)
            if 0 <= index < len(self.notes_data):
                self.notes_data.pop(index)

        self.save_notes()
        self.refresh_notes()

    def refresh_notes(self):
        """刷新笔记列表"""
        self.notes_tree.delete(*self.notes_tree.get_children())
        for note in self.notes_data:
            self.notes_tree.insert('', tk.END, values=(note['title'], note['content']))


def main():
    """主函数"""
    root = tk.Tk()
    app = CalculusCalculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()