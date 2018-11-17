from Lexer import Scanner

class ErrorMessage:
    def __init__(self,message_code,line):
        if message_code == 1:
            self.error_message = "line {}: Error token type in this".format(line)
        if message_code ==2 :
            self.error_message == "line {}: Error token in this".format(line)
    def __repr__(self):
        return self.error_message

class Parser:
    def __init__(self,file_name):
        scan = Scanner(file_name)
        self.Token_list = scan.scanFile()
        self.Token_table = scan.Token_table
        self.T = 0.0  # 一个语法树中只有一个T,一行的第一个T给它复制，一行结束时重写为0.0
        temp = self.Token_list.pop(0)
        self.now_line_no = temp.LineNo
        self.now_tokens = temp.Tokens

    def get_token(self):
        if len(self.now_tokens)>0:
            return self.now_tokens.pop(0)
        else:
            return -1
    
    # 该符号是否和语法相对应，如果不是应该出现的返回一个ErrorMessage
    # 如果是，则返回True然后继续读下一个token
    def match_token(self,token,token_type):
        if token.type != token_type:
            return ErrorMessage(1,self.now_line_no)
        return True


    def make_exprNode(self,token):
        node = ExprNode(token.type)
        if token.type == 'CONST ID':
            node.set_content(token.value)
        elif token.type == 'T':
            node.set_content(self.T)

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

if __name__ == "__main__":
    parser = Parser("helloworld.c")
    print(parser.now_tokens)
        