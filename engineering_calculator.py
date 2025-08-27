import sys
import math
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt

class EngineeringCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Engineering Calculator')
        self.setFixedSize(500, 350)
        self.memory = 0
        self.angle_mode = 'Deg'  # 각도 모드 (Degree 기본)
        self.expression = ''  # 현재 입력 수식
        self.init_ui()

    def init_ui(self):
        grid = QGridLayout()
        self.setLayout(grid)

        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setFixedHeight(40)
        self.display.setAlignment(Qt.AlignRight)
        grid.addWidget(self.display, 0, 0, 1, 6)

        buttons = [
            ['(', ')', 'mc', 'm+', 'm-', 'mr'],
            ['2nd', 'x²', 'x³', 'xʸ', 'eˣ', '10ˣ'],
            ['1/x', '2√x', '3√x', 'y√x', 'ln', 'log'],
            ['x!', 'sin', 'cos', 'tan', 'e', 'EE'],
            ['Deg', 'sinh', 'cosh', 'tanh', 'π', 'Rand'],
            ['AC', '+/-', '%', '÷', '×', '−'],
            ['7', '8', '9', '', '', ''],
            ['4', '5', '6', '', '', '+'],
            ['1', '2', '3', '', '', '='],
            ['0', '.', '', '', '', ''],
        ]

        for row, row_buttons in enumerate(buttons, 1):
            for col, btn_text in enumerate(row_buttons):
                if btn_text:
                    btn = QPushButton(btn_text)
                    btn.clicked.connect(self.button_pressed)
                    grid.addWidget(btn, row, col)

    def button_pressed(self):
        sender = self.sender()
        text = sender.text()

        if text == 'AC':
            self.expression = ''
            self.display.setText(self.expression)
        elif text == '=':
            self.calculate_result()
        elif text == '+/-':
            self.toggle_sign()
        elif text == 'mc':
            self.memory_clear()
        elif text == 'm+':
            self.memory_add()
        elif text == 'm-':
            self.memory_subtract()
        elif text == 'mr':
            self.memory_recall()
        elif text == 'Deg':
            self.toggle_angle_mode()
        else:
            self.append_expression(text)

    def append_expression(self, text):
        # 함수명 등 특수 처리가 필요한 경우 변환 추가 예시
        function_mappings = {
            '×': '*',
            '÷': '/',
            'π': str(math.pi),
            'EE': 'e',
        }
        if text in function_mappings:
            text = function_mappings[text]

        # 삼각함수 등 함수는 함수명 그대로 두고 계산 시 처리
        # 숫자 및 연산자 등 문자 누적
        self.expression += text
        self.display.setText(self.expression)

    def calculate_result(self):
        try:
            # 안전하게 함수 처리 위해 eval 전 수식 변환 필요
            # 예: sin, cos 등은 math.sin 형태로 바꾸기
            expr = self.expression
            expr = expr.replace('×', '*').replace('÷', '/').replace('^', '**')
            # 함수 변환 예시
            expr = expr.replace('sin', 'math.sin')
            expr = expr.replace('cos', 'math.cos')
            expr = expr.replace('tan', 'math.tan')
            expr = expr.replace('sinh', 'math.sinh')
            expr = expr.replace('cosh', 'math.cosh')
            expr = expr.replace('tanh', 'math.tanh')
            expr = expr.replace('ln', 'math.log')
            expr = expr.replace('log', 'math.log10')
            expr = expr.replace('π', 'math.pi')
            expr = expr.replace('e', 'math.e')

            # Degree 모드면 각도 -> 라디안 변환 필요 (sin, cos, tan 등)
            if self.angle_mode == 'Deg':
                # 변환 함수 삽입 필요 (복잡하므로 여기서는 생략 예시)
                pass

            result = eval(expr, {'math': math, '__builtins__': {}})
            self.display.setText(str(result))
            self.expression = str(result)
        except Exception as e:
            self.display.setText('Error')
            self.expression = ''

    def toggle_sign(self):
        try:
            if self.expression:
                if self.expression.startswith('-'):
                    self.expression = self.expression[1:]
                else:
                    self.expression = '-' + self.expression
                self.display.setText(self.expression)
        except Exception:
            self.display.setText('Error')
            self.expression = ''

    def memory_clear(self):
        self.memory = 0

    def memory_add(self):
        try:
            val = float(self.expression)
            self.memory += val
        except Exception:
            pass

    def memory_subtract(self):
        try:
            val = float(self.expression)
            self.memory -= val
        except Exception:
            pass

    def memory_recall(self):
        self.expression = str(self.memory)
        self.display.setText(self.expression)

    def toggle_angle_mode(self):
        self.angle_mode = 'Rad' if self.angle_mode == 'Deg' else 'Deg'
        self.display.setText(f'Mode:{self.angle_mode}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = EngineeringCalculator()
    calc.show()
    sys.exit(app.exec_())
