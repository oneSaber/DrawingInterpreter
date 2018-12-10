from Lexer import Token

class Semantics:
    def __init__(self,paramter_list):
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
        self.Paramter_list = paramter_list
        self.expr_tree

    # the semantics' entrance
    def Semantic(self):
        self.get_next_expr()
        while(self.expr_tree is not None):
            self.value_of_expr()
            self.get_next_expr()

    # calculate the result of expr
    def value_of_expr(self):
        pass
    
    # get next expr
    def get_next_expr(self):
        if len(self.Paramter_list) >0:
            self.expr_tree = self.Paramter_list.pop(0)
        else:
            return None
    
    # judge whether you can start draw
    def can_draw(self):
        pass

    # get next line expr
    def next_line(self):
        pass
    