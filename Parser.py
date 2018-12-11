from Lexer import Scanner
from Lexer import Token

class ErrorMessage(Exception):
    def __init__(self,message_code,error_word,line):
        if message_code == 1:
            self.error_message = "line {}: Error token {} type in this".format(line,error_word)
        if message_code ==2 :
            self.error_message == "line {}: Error token {}in this".format(line,error_word)
        if message_code == 3:
            self.error_message == "line {}: had empty".format(line)

    def __repr__(self):
        return self.error_message

class ExprNode:
    def __init__(self,token_type):
        self.child_number = 0
        self.TokenType = token_type
        self.left_child = None
        self.right_child = None

    def set_content(self,content):
        self.content = content
    
    def set_left_child(self,left_child):
        self.child_number += 1
        self.left_child = left_child

    def set_right_child(self,right_child):
        self.child_number += 2
        self.right_child = right_child

    def get_left_child(self):
        if self.child_number == 1 or self.child_number == 3:
            return self.left_child 
        else:
            return None
    def get_right_child(self):
        if self.child_number == 2 or self.child_number == 3:
            return self.right_child
        else:
            return None

    def is_leaf(self):
        # if the node is a leaf
        # return true
        if self.child_number == 0:
            return True
        else:
            return False

# parser all lines
class Parser:
    def __init__(self,filename):
        self.scanner = Scanner(filename)
        self.Tokens_list = self.scanner.scanFile()
        self.paramters = []
    
    # use lineparser parser ever line
    def parser_program(self):
        Token_list = self.Tokens_list.pop(0)
        while(Token_list.Tokens!=None):
            line_parser = LineParser(Token_list.Tokens,Token_list.LineNo)
            line_parser.parser()
            self.paramters.append(line_parser.parameter)
            Token_list = self.Tokens_list.pop(0)
    # print a exper tree
    def traceTree(self,treeRoot,space_count):
        if treeRoot.TokenType == "PLUS":
            print("\t"*space_count+"+")
        elif treeRoot.TokenType == "MINUS":
            print("\t"*space_count+"-")
        elif treeRoot.TokenType == "MULTIPLICATION":
            print("\t"*space_count+"*")
        elif treeRoot.TokenType == "DIVISION":
            print("\t"*space_count+"/")
        elif treeRoot.TokenType == "POWER":
            print("\t"*space_count+"**")
        elif treeRoot.TokenType == "FUNC":
            print("\t"*space_count+str(treeRoot.content))
        elif treeRoot.TokenType == "CONST ID":
                print("\t"*space_count+str(treeRoot.content))
        elif treeRoot.TokenType == "T":
            print("\t"*space_count+"T")
        else:
            print("\t"*space_count+"Error node!")
        if treeRoot.TokenType == "CONST ID" or treeRoot.TokenType == "T":
            return
        elif treeRoot.TokenType == "FUNC":
            self.traceTree(treeRoot.get_left_child(),space_count+1)
        else:
            self.traceTree(treeRoot.get_left_child(),space_count+1)
            self.traceTree(treeRoot.get_right_child(), space_count+1)
    
    # print all paramter
    def Print_paramters(self):
        line = 1
        for paramter in self.paramters:
            print("line {}".format(line))
            for key in paramter.keys():
                if key == "can_draw":
                    continue
                print("the {} expr tree is :".format(key))
                self.traceTree(paramter[key],0)
            line += 1

class LineParser:
    def __init__(self,Token_list,line):
        self.T = 0.0
        self.token_list = Token_list
        self.parameter = {}
        self.token = None
        self.line = line

    def get_token(self):
        if len(self.token_list):
            self.token = self.token_list.pop(0)
            if self.token.type == "Error":
                raise ErrorMessage(2,self.token.value,self.line)
        else:
            self.token = Token("NoneToken",None,None)

    def match_token(self,aimed):
        if self.token.type == aimed:
            self.get_token()
            return True
        else:
            raise ErrorMessage(1,self.token.value,self.line)

    def parser(self):
        self.get_token()
        self.pargram()

    def pargram(self):
        while(self.token.type != "NoneToken"):
            self.Statement()
            if self.token.type == "SEMICO" or self.token.type=="NoneToken":
                break

    def Statement(self):
        if self.token.type == "ORIGIN":
            self.OriginStatement()
        elif self.token.type == "ROT":
            self.RotStatement()  
        elif self.token.type == "SCALE":
            self.ScaleStatement()
        elif self.token.type == "FOR":
            self.ForStatement()
        else:
            raise ErrorMessage(1,self.token.value,self.line)
        
    def OriginStatement(self):
        self.match_token("ORIGIN")
        self.match_token("IS")
        self.match_token("L_BRACKET")
    
        # origin_x
        origin_x = self.Expression()
        self.parameter['origin_x'] = origin_x
        self.match_token("COMMA")

        # origin_y
        origin_y = self.Expression()
        self.parameter['origin_y'] = origin_y
        self.match_token("R_BRACKET")

    def RotStatement(self):
        self.match_token("ROT")

        self.match_token("IS")
       
        rot_angle = self.Expression()
        self.parameter['rot_angele'] = rot_angle

    def ScaleStatement(self):
        self.match_token("SCALE")
 
        self.match_token("IS")

        self.match_token("L_BRACKET")
        
        scale_x = self.Expression()
        self.parameter['scale_x'] = scale_x

        self.match_token("COMMA")
        
        scale_y = self.Expression()
        self.parameter['scale_y']  = scale_y

        self.match_token("R_BRACKET")
        
    def ForStatement(self):
        self.match_token("FOR")
        self.match_token("T")
        self.match_token("FROM")
        
        # for start 
        start = self.Expression()
        self.parameter['for_start'] = start
        self.match_token("TO")
        
        # for end
        end = self.Expression()
        self.parameter['for_end'] = end
        self.match_token("STEP")
    
        step = self.Expression()
        self.parameter['for_step'] = step

        self.match_token("DRAW")
        self.match_token("L_BRACKET")

        start_x = self.Expression()
        self.parameter['start_x'] = start_x
        self.match_token("COMMA")

        start_y = self.Expression()
        self.parameter['start_y'] = start_y
        self.match_token("R_BRACKET")
        self.parameter['can_draw'] = True

    def Expression(self):
        left = None
        right = None
        temp_type = None
        left = self.Term()
        while(self.token.type == "PLUS" or self.token.type == "MINUS"):
            temp_type = self.token.type
            self.match_token(temp_type)
            right = self.Term()
            left = self.make_expr_node(temp_type,None,left,right)
        # self.get_token()
        return left

    def Term(self):
        left = self.Factory()
        while(self.token.type == "MULTIPLICATION" or self.token.type == "DIVISION"):
            tmp_type = self.token.type
            self.match_token(tmp_type)
            right = self.Factory()
            left = self.make_expr_node(tmp_type,None,left,right)
        return left

    def Factory(self):
        left = ExprNode(None)
        right = ExprNode(None)
        if self.token.type == "PLUS":
            self.match_token("PLUS")
            right = self.Factory()
        elif self.token.type == "MINUS":
            self.match_token("MINUS")
            right = self.Factory()
            left.TokenType = "CONST ID"
            left.set_content(0.0)
            right = self.make_expr_node("MINUS",None,left,right)
        else:
            right = self.Component()
        return right

    def Component(self):
        right = ExprNode(None)
        left = self.Atom()
        if self.token.type == "POWER":
            self.match_token("POWER")
            right = self.Component()
            left = self.make_expr_node("POWER",None,left,right)
        return left
    
    def Atom(self):
        address = ExprNode(None)
        tmp = ExprNode(None)
        if self.token.type == "CONST ID":
            tmp_token = self.token
            self.match_token("CONST ID")
            address = self.make_expr_node("CONST ID",tmp_token.value)
        elif self.token.type == "T":
            self.match_token("T")
            address = self.make_expr_node("T")
        elif self.token.type == "FUNC":
            tmp_token = self.token
            self.match_token("FUNC")
            self.match_token("L_BRACKET")
            tmp = self.Expression()
            address = self.make_expr_node("FUNC",tmp_token.function,tmp)
            self.match_token("R_BRACKET")
        elif self.token.type == "L_BRACKET":
            self.match_token("L_BRACKET")
            address = self.Expression()
            self.match_token("R_BRACKET")
        else:
            raise ErrorMessage(1,self.token.value,self.line)
        return address
        
    def make_expr_node(self,token_type,token_value = None,left_child = None,right_child =None):
        node = ExprNode(token_type)
        if node.TokenType == "CONST ID":
            node.set_content(token_value)
        elif node.TokenType == "T":
            node.set_content(self.T)
        elif node.TokenType == "FUNC":
            node.set_content(token_value)
            node.set_left_child(left_child)
        else:
            node.set_left_child(left_child)
            node.set_right_child(right_child)
        return node        