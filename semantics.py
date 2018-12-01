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
    
    # the semantics' entrance
    def Semantic(self):
        pass
    
    # calculate the result of expr
    def value_of_expr(self):
        pass
    
    # get next expr
    def get_next_expr(self):
        pass
    
    # judge whether you can start draw
    def can_draw(self):
        pass

    # get next line expr
    def next_line(self):
        pass
    
    def apply_expr(self,key,expr):
        # get a expr and its name
        # value of expr
        # apply_expr
        # flag for var for can_draw
        pass