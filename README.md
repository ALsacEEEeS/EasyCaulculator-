Multi-functional Mathematical Calculator  
A comprehensive mathematical tool featuring calculus computation, arithmetic calculation, and note-taking functionality.  

**Current Features**  
1. **Calculus Computation**  
   - Differentiation: Compute derivatives of functions  
   - Integration: Compute indefinite and definite integrals  
   - Limit Calculation: Evaluate limits of functions at specific points  
   - Numerical Calculation: Compute function values at given points  

2. **Arithmetic Calculation**  
   - Basic Operations: Addition, subtraction, multiplication, division, exponentiation  
   - Calculator Interface: Number and operator buttons  
   - Real-time Calculation: Direct expression input for instant evaluation  
   - Precise Results: Supports accurate floating-point computations  

3. **Note-taking Functionality**  
   - Note Management: Create, save, and view mathematical notes  
   - Timestamps: Automatically records creation and modification times  
   - Local Storage: Notes saved in local files  
   - Quick Preview: Note list and content preview  

**Feature Tabs**  
- **Calculus Tab**  
  Differentiation, integration, limits, numerical calculation  
  Quick input via symbol buttons  
  Intelligent expression preprocessing  

- **Arithmetic Tab**  
  Basic arithmetic operations  
  Calculator-style button interface  
  Supports complex expression evaluation  

- **Math Notes Tab**  
  Note creation and editing  
  Note list management  
  Content preview functionality  

**Installation Dependencies**  
```bash  
pip install sympy  
```  

**Usage**  
1. Run `python calculus_calculator.py` or double-click `run_calculator.bat`  
2. Select different tabs to access corresponding features  
3. Each tab operates independently without interference  

**Arithmetic Examples**  
```  
2 + 3 * 4 → 14  
(5 + 3) / 2 → 4.0  
2^3 + 4^2 → 24  
```  

**Calculus Examples**  
```  
Derivative of x^2 → 2*x  
Integral of sin(x) → -cos(x) + C  
Limit of sin(x)/x as x→0 → 1  
```  

**Note-taking**  
- Input title and content to save notes  
- Notes automatically saved to local files  
- View and edit existing notes anytime  

**Supported Mathematical Functions**  
- Calculus operations: symbolic differentiation/integration, limit evaluation, numerical computation  
- Arithmetic operations: basic four operations, exponentiation, parenthesis priority  

**Notes**  
- Note data is saved in `math_notes.json` in the current directory  
- Arithmetic calculations use Python's `eval` function—ensure input safety

# 多功能数学计算器

一个功能全面的数学工具，包含微积分计算、算术计算和笔记功能。

## 当前功能特性

### 1. 微积分计算功能
- **微分计算**：计算函数的导数
- **积分计算**：计算不定积分和定积分
- **极限计算**：计算函数在特定点的极限
- **数值计算**：计算函数在特定点的数值

### 2. 算术计算功能
- **基本运算**：加减乘除、幂运算
- **计算器界面**：数字按钮和运算符按钮
- **实时计算**：支持直接输入表达式计算
- **精确结果**：支持浮点数精确计算

### 3. 笔记功能
- **笔记管理**：创建、保存、查看数学笔记
- **时间戳**：自动记录创建和修改时间
- **本地存储**：笔记数据保存在本地文件
- **快速预览**：笔记列表和内容预览

## 功能标签页

### 微积分计算标签页
- 微分、积分、极限、数值计算
- 符号按钮快速输入
- 智能表达式预处理

### 算术计算标签页
- 基本算术运算
- 计算器式按钮界面
- 支持复杂表达式计算

### 数学笔记标签页
- 笔记创建和编辑
- 笔记列表管理
- 内容预览功能

## 安装依赖

```bash
pip install sympy
```

## 使用方法

1. 运行 `python calculus_calculator.py` 或双击 `run_calculator.bat`
2. 选择不同的标签页使用相应功能
3. 各功能标签页独立操作，互不影响

## 算术计算示例
- `2 + 3 * 4` → `14`
- `(5 + 3) / 2` → `4.0`
- `2^3 + 4^2` → `24`

## 微积分计算示例
- `x^2` 的微分 → `2*x`
- `sin(x)` 的积分 → `-cos(x) + C`
- `sin(x)/x` 在 x->0 的极限 → `1`

## 笔记功能
- 输入标题和内容保存笔记
- 笔记自动保存到本地文件
- 可随时查看和编辑已有笔记

## 支持的数学功能

  ### 微积分运算
  - 符号微分和积分
  - 极限计算
  - 数值计算

  ### 算术运算
  - 基本四则运算
  - 幂运算
  - 括号优先级

## 注意事项
- 笔记数据保存在当前目录的math_notes.json文件中
- 算术计算使用Python的eval函数，请确保输入安全
