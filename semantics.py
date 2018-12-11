from Lexer import Token
from Drawing import DrawPricture
from Parser import Parser,ExprNode
import numpy as np

class Semantics:
    def __init__(self,paramter_list,drawing):
        self.origin_x = 0.0
        self.origin_y = 0.0
        self.for_start = 0.0
        self.for_end = 0.0
        self.rot = 0.0
        self.scale_x = 0.0
        self.scale_y = 0.0
        self.for_step = 0.0
        self.start_x = 0.0
        self.start_y = 0.0
        self.T = None
        self.Paramter_list = paramter_list
        self.expr_map = None
        self.expr_tree = None
        self.drawing = drawing
        self.key_list = []

    # the semantics' entrance
    def Semantic(self):
        while len(self.Paramter_list) >0:
            self.next_line()
            for key in self.key_list:
                print(key,self.value_of_expr(self.expr_map.get(key)))
    
    
    
    # calculate the result of expr
    def value_of_expr(self,node):
        if node is None:
            return None
        if node.is_leaf():
            if node.TokenType == "CONST ID":
                return node.content
            if node.TokenType == "T":
                if self.T is None and \
                    self.for_end != 0.0 and \
                    self.for_step != 0.0:
                    self.T = np.linspace(self.for_start,self.for_end,
                        np.abs(self.for_end-self.for_start)/self.for_step)
                    return self.T
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
                return left * right
            elif node.TokenType == "POWER":
                return left ** right
            elif node.TokenType == "FUNC":
                return node.content(left)
            

    # judge whether you can start draw
    def can_draw(self,x,y):
        self.drawing.set_picture(x,y)

    # get next line expr
    def next_line(self):
        self.expr_map = self.Paramter_list.pop(0)
        self.key_list = self.expr_map.keys()

if __name__ == "__main__":
    drawing = DrawPricture()
    filename = input("Source filename:")
    parser = Parser(filename)
    parser.parser_program()
    parser.Print_paramters()
    sement = Semantics(paramter_list=parser.paramters,drawing=drawing)
    sement.Semantic()