import Lexer

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
        self.Token_list = Lexer.scanFile(file_name," ")
        self.Token_table = Lexer.Token_table
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

    def __repr__(self):
        return "hello world"

if __name__ == "__main__":
    parser = Parser("helloworld.c")
    print(parser.now_tokens)
        