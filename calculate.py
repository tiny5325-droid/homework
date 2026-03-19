import numpy as np
import math
import random

# -------------------------- 基础工具函数（保持不变） --------------------------
def to_homogeneous(points):
    """二维点 → 齐次坐标 (N,2) → (3,N)"""
    if points.ndim == 1:
        points = points.reshape(-1, 2)
    n = points.shape[0]
    return np.vstack([points[:,0], points[:,1], np.ones(n)])

def from_homogeneous(hpoints):
    """齐次坐标 → 二维点 (3,N) → (N,2)"""
    return np.vstack([hpoints[0]/hpoints[2], hpoints[1]/hpoints[2]]).T

def apply_transform(points, matrix):
    """对二维点集应用齐次变换矩阵"""
    h_points = to_homogeneous(points)
    h_transformed = matrix @ h_points
    return from_homogeneous(h_transformed)

def translation_matrix(tx, ty):
    """生成平移矩阵"""
    return np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ], dtype=np.float64)

def rotation_matrix(angle):
    """绕原点逆时针旋转矩阵（angle为弧度）"""
    c, s = math.cos(angle), math.sin(angle)
    return np.array([
        [c, -s, 0],
        [s,  c, 0],
        [0,  0, 1]
    ], dtype=np.float64)

def reflection_matrix_x():
    """关于X轴的反射矩阵"""
    return np.array([
        [1, 0, 0],
        [0, -1, 0],
        [0, 0, 1]
    ], dtype=np.float64)

# -------------------------- 随机数据生成 --------------------------
def random_line_expression_str():
    """生成随机直线表达式，如 '3x+5y-7=0'"""
    a = round(random.uniform(-3, 3), 1)
    b = round(random.uniform(-3, 3), 1)
    c = round(random.uniform(-5, 5), 1)
    while abs(a) < 1e-3 and abs(b) < 1e-3:
        a = round(random.uniform(-3, 3), 1)
        b = round(random.uniform(-3, 3), 1)

    # 格式化系数：整数不显示 .0，小数保留一位
    def fmt_num(val):
        if abs(val) < 1e-6:
            return ''
        if val.is_integer():
            return str(int(val))
        else:
            s = f"{val:.1f}"
            if s.endswith('.0'):
                return s[:-2]
            return s

    parts = []
    # 处理 x 项
    if abs(a) > 1e-6:
        a_str = fmt_num(a)
        if a_str == '1':
            parts.append('x')
        elif a_str == '-1':
            parts.append('-x')
        else:
            parts.append(f"{a_str}x")
    # 处理 y 项
    if abs(b) > 1e-6:
        b_str = fmt_num(b)
        sign = '+' if b > 0 and parts else ''
        if b_str == '1':
            parts.append(f"{sign}y")
        elif b_str == '-1':
            parts.append(f"{sign}-y")
        else:
            parts.append(f"{sign}{b_str}y")
    # 处理常数项
    if abs(c) > 1e-6:
        c_str = fmt_num(abs(c))
        sign = '+' if c > 0 and parts else ''
        if c < 0:
            sign = '-' if not parts else ' - '
            parts.append(f"{sign}{c_str}")
        else:
            parts.append(f"{sign}{c_str}")

    expr = ''.join(parts)
    if not expr:
        expr = '0'  # 理论上不会发生
    return expr + "=0"

def random_coord_str():
    """生成随机坐标字符串，格式如 '(-1.25,4.5)'"""
    x = round(random.uniform(-5, 5), 2)
    y = round(random.uniform(-5, 5), 2)
    return f"({x},{y})"

# -------------------------- 核心计算 --------------------------
def compute_reflection(triangle, line_p1, line_p2):
    """
    计算三角形关于直线 line_p1->line_p2 的反射
    参数：
        triangle: (3,2) numpy array
        line_p1, line_p2: (2,) numpy array
    返回：
        result_text: 包含详细矩阵和结果的字符串
        tri_target: 反射后的三角形顶点 (3,2)
        tri_original: 原始三角形 (3,2)（方便绘图）
        line_pts: (line_p1, line_p2) 直线两点
    """
    tri_original = np.array(triangle)
    dx, dy = line_p2 - line_p1
    line_angle = math.atan2(dy, dx)
    line_angle_deg = math.degrees(line_angle)

    # 步骤1：平移矩阵
    T1 = translation_matrix(-line_p1[0], -line_p1[1])
    # 步骤2：旋转矩阵（顺时针）
    R = rotation_matrix(-line_angle)
    # 步骤3：反射矩阵
    S = reflection_matrix_x()
    # 步骤4：逆旋转矩阵
    R_inv = rotation_matrix(line_angle)
    # 步骤5：逆平移矩阵
    T2 = translation_matrix(line_p1[0], line_p1[1])

    # 合成矩阵
    H_final = T2 @ R_inv @ S @ R @ T1
    tri_target = apply_transform(tri_original, H_final)

    # 构建输出文本
    lines = []
    lines.append("="*60)
    lines.append("          二维三角形直线反射变换计算报告")
    lines.append("="*60)
    lines.append("【初始三角形顶点】")
    for i, (x, y) in enumerate(tri_original):
        lines.append(f"   顶点 {chr(65+i)}: ({x:.2f}, {y:.2f})")
    lines.append(f"\n【对称轴】")
    lines.append(f"   点1: ({line_p1[0]:.2f}, {line_p1[1]:.2f})")
    lines.append(f"   点2: ({line_p2[0]:.2f}, {line_p2[1]:.2f})")
    lines.append(f"   直线与X轴夹角: {line_angle_deg:.1f}°")

    lines.append("\n【步骤1：平移矩阵 T1】")
    lines.append(str(np.round(T1, 4)))
    lines.append("【步骤2：旋转矩阵 R】")
    lines.append(str(np.round(R, 4)))
    lines.append("【步骤3：反射矩阵 S】")
    lines.append(str(np.round(S, 4)))
    lines.append("【步骤4：逆旋转矩阵 R_inv】")
    lines.append(str(np.round(R_inv, 4)))
    lines.append("【步骤5：逆平移矩阵 T2】")
    lines.append(str(np.round(T2, 4)))

    lines.append("\n【最终合成变换矩阵 H】")
    lines.append(str(np.round(H_final, 4)))

    lines.append("\n【反射后的三角形顶点】")
    for i, (x, y) in enumerate(tri_target):
        lines.append(f"   顶点 {chr(65+i)}': ({x:.2f}, {y:.2f})")
    lines.append("="*60)

def compute_reflection_with_steps(triangle, line_p1, line_p2):
    """
    计算三角形关于直线的反射，并返回所有中间步骤的三角形
    参数：
        triangle: (3,2) numpy array
        line_p1, line_p2: (2,) numpy array
    返回：
        result_text: 包含详细矩阵和结果的字符串
        tri_target: 反射后的三角形顶点 (3,2)
        tri_original: 原始三角形 (3,2)
        steps_triangles: 列表，包含每一步变换后的三角形（共5步，顺序与 basic_matrices 一致）
        basic_matrices: 列表，包含5个基本矩阵
        line_pts: (line_p1, line_p2)
    """
    tri_original = np.array(triangle)
    dx, dy = line_p2 - line_p1
    line_angle = math.atan2(dy, dx)

    T1 = translation_matrix(-line_p1[0], -line_p1[1])
    R = rotation_matrix(-line_angle)
    S = reflection_matrix_x()
    R_inv = rotation_matrix(line_angle)
    T2 = translation_matrix(line_p1[0], line_p1[1])

    basic_matrices = [T1, R, S, R_inv, T2]
    step_names = ["平移至直线上的点", "旋转至与x轴重合", "关于x轴反射", "旋转回原方向", "平移回原位"]

    # 计算每一步的三角形
    cumulative_M = np.eye(3)
    steps_triangles = []
    for mat in basic_matrices:
        cumulative_M = mat @ cumulative_M
        tri_step = apply_transform(tri_original, cumulative_M)
        steps_triangles.append(tri_step)

    H_final = T2 @ R_inv @ S @ R @ T1
    tri_target = apply_transform(tri_original, H_final)

    # 构建输出文本
    lines = []
    lines.append("="*60)
    lines.append("          二维三角形直线反射变换计算报告")
    lines.append("="*60)
    lines.append("【初始三角形顶点】")
    for i, (x, y) in enumerate(tri_original):
        lines.append(f"   顶点 {chr(65+i)}: ({x:.2f}, {y:.2f})")
    lines.append(f"\n【对称轴】")
    lines.append(f"   点1: ({line_p1[0]:.2f}, {line_p1[1]:.2f})")
    lines.append(f"   点2: ({line_p2[0]:.2f}, {line_p2[1]:.2f})")
    lines.append(f"   直线与X轴夹角: {math.degrees(line_angle):.1f}°")

    for idx, (mat, name) in enumerate(zip(basic_matrices, step_names)):
        lines.append(f"\n【步骤{idx+1}：{name} 矩阵】")
        lines.append(str(np.round(mat, 4)))

    lines.append("\n【最终合成变换矩阵 H】")
    lines.append(str(np.round(H_final, 4)))

    lines.append("\n【反射后的三角形顶点】")
    for i, (x, y) in enumerate(tri_target):
        lines.append(f"   顶点 {chr(65+i)}': ({x:.2f}, {y:.2f})")
    lines.append("="*60)

    return "\n".join(lines), tri_target, tri_original, steps_triangles, basic_matrices, (line_p1, line_p2)