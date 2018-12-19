from Lexer import Token
from Drawing import DrawPricture
from Parser import Parser, ExprNode
import numpy as np


class Semantics:
    def __init__(self, paramter_list, drawing):
        self.symbol_table = {}
        self.Paramter_list = paramter_list
        self.expr_map = None
        self.expr_tree = None
        self.drawing = drawing
        self.key_list = []

    # the semantics' entrance
    def Semantic(self):
        while len(self.Paramter_list) > 0:
            self.next_line()
            for key in self.key_list:
                if key == "can_draw" and self.expr_map[key]:
                    self.can_draw()
                    continue
                value = self.value_of_expr(self.expr_map.get(key))
                if (key == "start_x" or key == "start_y")and not isinstance(
                        value, np.ndarray):
                    value = np.linspace(value, value, int(np.abs(self.symbol_table.get(
                        "for_end") - self.symbol_table.get("for_start")) / self.symbol_table.get("for_step")))
                self.symbol_table[key] = value
                print(key, type(value), value)

    # calculate the result of expr

    def value_of_expr(self, node):
        if node is None:
            return None
        if node.is_leaf():
            if node.TokenType == "CONST ID":
                return node.content
            if node.TokenType == "T":
                if self.symbol_table.get("for_start", None) is not None and \
                        self.symbol_table.get("for_end", None) is not None:
                    T = np.linspace(
                        self.symbol_table.get("for_start"),
                        self.symbol_table.get("for_end"),
                        int(
                            np.abs(
                                self.symbol_table.get("for_end") -
                                self.symbol_table.get("for_start")) /
                            self.symbol_table.get("for_step")))
                    return T
        else:
            left = self.value_of_expr(node.get_left_child())
            right = self.value_of_expr(node.get_right_child())
            if node.TokenType == "PLUS":
                return left + right
            elif node.TokenType == "MINUS":
                return left - right
            elif node.TokenType == "MULTIPLICATION":
                return left * right
            elif node.TokenType == "DIVISION":
                return left / right
            elif node.TokenType == "POWER":
                return left ** right
            elif node.TokenType == "FUNC":
                return node.content(left)

    # judge whether you can start draw
    def can_draw(self):
        x = self.symbol_table.get('start_x', None)
        y = self.symbol_table.get('start_y', None)
        if x is not None and y is not None:
            self.drawing.set_origin(
                self.symbol_table.get(
                    'orign_x', 0.0), self.symbol_table.get(
                    'orign_y', 0.0))
            self.drawing.set_rot(self.symbol_table.get('rot', 0.0))
            self.drawing.set_scale(
                self.symbol_table.get(
                    "scale_x", 1), self.symbol_table.get(
                    'scale_y', 1))
            self.drawing.set_picture(x, y)
            self.symbol_table.pop("for_start")
            self.symbol_table.pop("for_end")
            self.symbol_table.pop("start_x")
            self.symbol_table.pop("start_y")
            self.symbol_table.pop("for_step")

    # get next line expr
    def next_line(self):
        self.expr_map = self.Paramter_list.pop(0)
        self.key_list = self.expr_map.keys()


if __name__ == "__main__":
    drawing = DrawPricture()
    # filename = input("Source filename:")
    parser = Parser("DrawSource")
    parser.parser_program()
    sement = Semantics(paramter_list=parser.paramters, drawing=drawing)
    sement.Semantic()
    drawing.draw()
