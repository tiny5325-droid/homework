import sys
import numpy as np
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog, QSizePolicy,QGraphicsView
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt, QEvent
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from ui_window import Ui_MainWindow
from qt_material import apply_stylesheet
import calculate as calc  # 导入后端模块

plt.rcParams['font.family'] = 'SimHei'  # 设置为黑体，支持中文
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

# -------------------------- 解析函数（UI层负责字符串到数值的转换） --------------------------
def parse_coord(text):
    """解析 '(1,4)' 或 '1,4' 格式的坐标，返回 (x,y) 浮点数"""
    if not text or not text.strip():
        raise ValueError("坐标输入不能为空")
    
    # 去除首尾空格，并移除可能的外层括号
    text = text.strip().replace(' ', '')
    if text.startswith('(') and text.endswith(')'):
        text = text[1:-1]
    
    parts = text.split(',')
    if len(parts) != 2:
        raise ValueError("坐标格式错误，应为 x,y 或 (x,y)，例如 (1.5,-2.3)")
    
    try:
        x = float(parts[0])
        y = float(parts[1])
        return x, y
    except ValueError:
        raise ValueError("坐标必须为数字，例如 (1.5,-2.3)")

def parse_line_expression(expr):
    """
    解析形如 "3x+5y-1=0" 的直线表达式，返回直线上的两个点
    支持系数为整数或小数，自动处理缺失项
    """
    if not expr or not expr.strip():
        raise ValueError("直线表达式不能为空")

    expr = expr.replace(' ', '')
    if '=' not in expr:
        raise ValueError("表达式必须包含等号，例如 3x+5y-1=0")

    left, right = expr.split('=')
    try:
        const_right = float(right) if right else 0
    except ValueError:
        raise ValueError("等号右边必须是数字，例如 0 或 3")

    # 将左边表达式标准化为 ax+by+c 的形式
    # 使用正则表达式提取项
    import re
    # 匹配形如 [+-]?[0-9.]*[xy]? 的项，并捕获系数和变量
    pattern = re.compile(r'([+-]?[0-9.]*)([xy]?)')
    terms = re.findall(pattern, left)
    a = b = c = 0.0
    for coef_str, var in terms:
        if not coef_str and not var:
            continue
        # 处理系数
        if coef_str in ('', '+'):
            coef = 1.0
        elif coef_str == '-':
            coef = -1.0
        else:
            try:
                coef = float(coef_str)
            except ValueError:
                raise ValueError(f"无效的系数: {coef_str}")
        if var == 'x':
            a += coef
        elif var == 'y':
            b += coef
        else:
            c += coef

    A, B, C = a, b, c - const_right
    if abs(A) < 1e-6 and abs(B) < 1e-6:
        raise ValueError("直线系数不能全为零，至少 x 或 y 的系数非零")

    # 从一般式 Ax+By+C=0 取两个点
    points = []
    if abs(B) > 1e-6:
        points.append((0, -C / B))
    if abs(A) > 1e-6:
        points.append((-C / A, 0))
    if len(points) < 2:
        if abs(B) > 1e-6:
            # 取 x=1 求 y
            points.append((1, -(C + A) / B))
        else:  # B≈0, A≠0，直线垂直于 x 轴
            x0 = -C / A
            points.append((x0, 1))  # 取 y=1 得点 (x0, 1)

    return np.array(points[0]), np.array(points[1])

# -------------------------- 主窗口类 --------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 增大画布
        self.figure = Figure(figsize=(12, 9), dpi=100, constrained_layout=True)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        scene = self.ui.graphicsView.scene()
        if scene is None:
            from PySide6.QtWidgets import QGraphicsScene
            scene = QGraphicsScene()
            self.ui.graphicsView.setScene(scene)
        self.proxy = scene.addWidget(self.canvas)

        # 明确启用滚动条
        self.ui.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.ui.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.ui.graphicsView.viewport().installEventFilter(self)
        self.ui.graphicsView.setRenderHints(
            QPainter.Antialiasing | QPainter.SmoothPixmapTransform
        )
        
        # 连接信号
        self.ui.pushButton.clicked.connect(self.generate_random)  # 生成随机值
        self.ui.pushButton_2.clicked.connect(self.calculate)      # 确定
        self.ui.pushButton_3.clicked.connect(self.clear_all)      # 取消
        self.ui.pushButton_4.clicked.connect(self.export_result)  # 导出
        self.ui.pushButton_5.clicked.connect(self.show_help)      # 帮助文档
        
    def generate_random(self):
        """生成随机值填充输入框"""
        self.ui.A_point.setText(calc.random_coord_str())
        self.ui.B_point.setText(calc.random_coord_str())
        self.ui.C_point.setText(calc.random_coord_str())
        self.ui.line_edit.setText(calc.random_line_expression_str())

    def clear_all(self):
        """清空所有输入和显示内容"""
        self.ui.A_point.clear()
        self.ui.B_point.clear()
        self.ui.C_point.clear()
        self.ui.line_edit.clear()
        self.ui.textEdit.clear()
        self.figure.clear()
        self.canvas.draw()

    def parse_inputs(self):
        """解析输入，返回三角形顶点数组和直线两点"""
        v1 = parse_coord(self.ui.A_point.text())
        v2 = parse_coord(self.ui.B_point.text())
        v3 = parse_coord(self.ui.C_point.text())
        triangle = np.array([v1, v2, v3])
        p1, p2 = parse_line_expression(self.ui.line_edit.text())
        return triangle, p1, p2

    def eventFilter(self, obj, event):
        """事件过滤器，处理 graphicsView 的滚轮缩放"""
        if obj == self.ui.graphicsView.viewport() and event.type() == QEvent.Type.Wheel:
            delta = event.angleDelta().y()
            factor = 1.2 if delta > 0 else 1 / 1.2
            self.ui.graphicsView.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
            self.ui.graphicsView.scale(factor, factor)
            return True
        # 其他事件必须返回基类处理结果（或 False）
        return super().eventFilter(obj, event)
            
    def calculate(self):
        try:
            triangle, p1, p2 = self.parse_inputs()
        except Exception as e:
            QMessageBox.critical(self, "输入错误", f"解析输入失败：{str(e)}")
            return

        try:
            # 使用带步骤的新函数
            result_text, tri_target, tri_original, steps_triangles, basic_matrices, (line_p1, line_p2) = calc.compute_reflection_with_steps(triangle, p1, p2)
        except Exception as e:
            QMessageBox.critical(self, "计算错误", f"计算失败：{str(e)}")
            return

        # 显示文本结果
        self.ui.textEdit.setText(result_text)

        # 绘制多步骤图形
        self.plot_steps(tri_original, steps_triangles, line_p1, line_p2)

    def plot_steps(self, orig, steps_triangles, line_p1, line_p2):
        """绘制初始三角形和5个变换步骤（2行3列）"""
        self.figure.clear()
        # 创建2行3列的子图
        axes = self.figure.subplots(2, 3)
        axes = axes.flatten()

        # 计算所有点的范围以便统一坐标轴
        all_points = np.vstack([orig] + steps_triangles + [line_p1, line_p2])
        margin = 2.0
        x_min, x_max = all_points[:, 0].min() - margin, all_points[:, 0].max() + margin
        y_min, y_max = all_points[:, 1].min() - margin, all_points[:, 1].max() + margin
        x_lim = [x_min, x_max]
        y_lim = [y_min, y_max]

        point_labels = ['A', 'B', 'C']
        final_tri = steps_triangles[-1]  # 最终三角形

        # 子图0：初始位置
        ax = axes[0]
        # 坐标系
        ax.axhline(0, color='darkgray', linewidth=1.8)
        ax.axvline(0, color='darkgray', linewidth=1.8)
        # 对称轴
        ax.axline(line_p1, line_p2, color='black', linestyle='-', linewidth=2, label='对称轴')
        # 初始三角形
        tri_closed = np.vstack([orig, orig[0]])
        ax.fill(tri_closed[:, 0], tri_closed[:, 1], color='#1976D2', alpha=0.4)
        ax.plot(tri_closed[:, 0], tri_closed[:, 1], color='#0D47A1', linewidth=2.5)
        for i, (x, y) in enumerate(orig):
            ax.text(x+0.2, y+0.2, point_labels[i], fontsize=12, fontweight='bold', color='#0D47A1')
        # 目标三角形虚线
        tri_final_closed = np.vstack([final_tri, final_tri[0]])
        ax.plot(tri_final_closed[:, 0], tri_final_closed[:, 1], color='#1976D2', linestyle='--', linewidth=1.8, label='目标位置', alpha=0.7)

        ax.set_xlim(x_lim)
        ax.set_ylim(y_lim)
        ax.set_aspect('equal')
        ax.grid(True, linestyle=':', alpha=0.3)
        ax.legend(loc='upper right', fontsize=9)
        ax.set_title("初始位置", fontsize=12, fontweight='bold')

        # 步骤1-5
        step_names = ["平移至直线上的点", "旋转至与x轴重合", "关于x轴反射", "旋转回原方向", "平移回原位"]
        prev_tri = orig.copy()
        for idx in range(5):
            ax = axes[idx+1]
            curr_tri = steps_triangles[idx]

            # 坐标系
            ax.axhline(0, color='darkgray', linewidth=1.8)
            ax.axvline(0, color='darkgray', linewidth=1.8)
            # 对称轴
            ax.axline(line_p1, line_p2, color='black', linestyle='-', linewidth=2)
            # 初始三角形（红色虚线）
            tri_orig_closed = np.vstack([orig, orig[0]])
            ax.plot(tri_orig_closed[:, 0], tri_orig_closed[:, 1], color='#D32F2F', linestyle='--', linewidth=1.8, alpha=0.7)
            # 目标三角形（蓝色虚线）
            tri_final_closed = np.vstack([final_tri, final_tri[0]])
            ax.plot(tri_final_closed[:, 0], tri_final_closed[:, 1], color='#1976D2', linestyle='--', linewidth=1.8, alpha=0.7)
            # 上一步三角形（灰色虚线）
            prev_closed = np.vstack([prev_tri, prev_tri[0]])
            ax.plot(prev_closed[:, 0], prev_closed[:, 1], color='gray', linestyle='--', linewidth=1.8, alpha=0.8)
            # 当前三角形（绿色高亮）
            curr_closed = np.vstack([curr_tri, curr_tri[0]])
            ax.fill(curr_closed[:, 0], curr_closed[:, 1], color='#4CAF50', alpha=0.4)
            ax.plot(curr_closed[:, 0], curr_closed[:, 1], color='#2E7D32', linewidth=2.5)
            for i, (x, y) in enumerate(curr_tri):
                ax.text(x+0.2, y+0.2, point_labels[i], fontsize=12, fontweight='bold', color='#2E7D32')

            # 位移箭头
            center_prev = np.mean(prev_tri, axis=0)
            center_curr = np.mean(curr_tri, axis=0)
            ax.annotate('', xy=center_curr, xytext=center_prev,
                        arrowprops=dict(arrowstyle='->', color='gray', lw=3, alpha=0.8))

            ax.set_xlim(x_lim)
            ax.set_ylim(y_lim)
            ax.set_aspect('equal')
            ax.grid(True, linestyle=':', alpha=0.3)
            ax.set_title(f"步骤 {idx+1}：{step_names[idx]}", fontsize=12, fontweight='bold')

            prev_tri = curr_tri.copy()

        self.canvas.draw()

    def export_result(self):
        """导出文本结果到文件"""
        text = self.ui.textEdit.toPlainText()
        if not text.strip():
            QMessageBox.warning(self, "导出失败", "没有可导出的内容")
            return
        file_path, _ = QFileDialog.getSaveFileName(self, "保存文件", "", "文本文件 (*.txt);;所有文件 (*)")
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                QMessageBox.information(self, "导出成功", f"文件已保存至：{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "导出失败", str(e))

    def show_help(self):
        """在文本显示区显示使用说明"""
        help_text = """
        <h2>使用说明</h2>
        <p>本程序用于计算三角形关于任意直线的反射变换。</p>
        <h3>输入格式：</h3>
        <ul>
            <li><b>A点坐标、B点坐标、C点坐标</b>：格式为 (x,y) 或 x,y，例如 (1.5, -2.3) 或 3,4</li>
            <li><b>直线表达式</b>：格式为 ax+by+c=0，例如 3x+5y-7=0 或 2x-y+1=0</li>
        </ul>
        <h3>操作步骤：</h3>
        <ol>
            <li>在输入框中填入坐标和直线表达式（或点击“生成随机值”自动填充示例）</li>
            <li>点击“确定”进行计算，右侧图形区会显示初始三角形（蓝色）和反射后的三角形（绿色虚线），下方文本区显示详细的计算矩阵和结果</li>
            <li>点击“取消”可清空所有输入和显示内容</li>
            <li>点击“导出计算结果”可将文本区的内容保存为 .txt 文件</li>
        </ol>
        <p>如有任何问题，请联系开发者。</p>
        """
        self.ui.textEdit.setHtml(help_text)

# -------------------------- 程序入口 --------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='light_blue.xml')
    window = MainWindow()
    window.show()
    sys.exit(app.exec())