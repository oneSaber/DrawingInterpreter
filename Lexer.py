# 画图程序的词法分析器
from collections import namedtuple
import numpy as np

Token = namedtuple('Token',['type','value','function'])
LINETOKEN = namedtuple("LINETOKEN",['LineNo','Tokens'])


class Scanner:
    def __init__(self,filename):
        self.filename = filename
        self.special = ('*','/','-','+','(',')',',',';','.')

        # 保留关键字
        self.Token_table = {'PI': Token('CONST ID', np.pi,None),
              'E': Token('CONST ID', 2.71828,None),
              'T': Token('T', 0.0,None),
              'SIN': Token('FUNC', 0.0,np.sin),
              'COS': Token('FUNC', 0.0,np.cos),
              'TAN': Token('FUNC', 0.0,np.tan),
              'LN': Token('FUNC', 0.0,np.log),
              'EXP': Token('FUNC', 0.0,np.exp),
              'SQRT':Token('FUNC', 0.0,np.sqrt),
              'ORIGIN': Token('ORIGIN', 0.0,None),
              'SCALE': Token('SCALE',0.0,None),
              'ROT': Token('ROT', 0.0,None),
              'IS': Token('IS', 0.0,None),
              'FOR': Token('FOR', 0.0,None),
              'FROM': Token('FROM', 0.0,None),
              'TO': Token('TO', 0.0,None),
              'STEP': Token('STEP', 0.0,None),
              'DRAW': Token('DRAW', 0.0,None)
            }

        # 状态机转换而来的树
        self.DFA_tree = { 0: { 'letter': 1, 'digit': 2, '/': 6, '-': 7,'*':4,
                        '+': 8, ',': 9, ';': 10, '(': 11, ')': 12},
                    1 : {'letter' : 1, 'break':'ID'},
                    2 : {'digit': 2, '.': 3,'break':'CONST ID'},
                    3 : {'digit': 3, 'break': 'CONST ID'},
                    4 : {'*': 5 ,'break':'MULTIPLICATION'},
                    5 : {'break': 'POWER'},
                    6 : {'/': 13,'break': 'DIVISION'},
                    7 : {'-' : 13, 'break':'MINUS'},
                    8 : {'break': 'PLUS'},
                    9 : {'break': 'COMMA'},
                    10 : {'break': 'SEMICO'},
                    11 : {'break': 'L_BRACKET'},
                    12 : {'break': 'R_BRACKET'},
                    13 : {'break': 'COMMENT'}
                    }

        self.fina_statue = (5,8,9,10,11,12,13)

    # origin 出发状态, condition 转移条件
    def move(self,origin, condition):
        # 判定origin 是不是终态
        next_tree = self.DFA_tree[origin]
        return next_tree[condition]

    # 查表判定读到的是什么玩意
    def judgeWord(self,word,line):
        token = self.Token_table.get(word,None)
        if token is None:
            return Token("ERROR",word,None)
        else:
            return token

    def isFinal(self,statue,nextword):
        if statue in self.fina_statue:
            # 绝对终态，不管下一个是什么直接返回
            return self.DFA_tree[statue]['break']
        elif statue == 1 :
            if nextword.isalpha():
                return None
            else:
                return self.DFA_tree[statue]['break']
        elif statue == 2:
            if nextword.isdigit() or nextword== '.':
                return None
            else :
                return self.DFA_tree[statue]['break']
        elif statue == 3 :
            if nextword.isdigit():
                return None
            else:
                return self.DFA_tree[statue]['break']
        elif statue == 4:
            if nextword == "*":
                return None
            else:
                return self.DFA_tree[statue]['break']
        elif statue == 6:
            if nextword == "/":
                return None
            else:
                return self.DFA_tree[statue]['break']
        elif statue == 7:
            if nextword == '-':
                return None
            else:
                return self.DFA_tree[statue]['break']
        else:
            return None

    def eatSpace(self,buffer):
        for i in range(len(buffer)):
            if not buffer[i].isspace():
                return buffer[i:]
                

    # 具体的解析器，从buffer中逐个字符的读入，进行状态机move，
    # move每次返回可能是Token属性或者是下一个状态
    # 如果是到达终态返回属性则调用judge函数判断类型，错误返回None，正确返回Token元组，然后放入Token_list
    # 一直读取直到buffer结尾或者是明确行结束符号
    def Parser(self,buffer,line):
        statue = 0
        word = ""
        temp_token_list = []
        buffer = self.eatSpace(buffer)
        if buffer is None:
            return 
        for ch in buffer:
            token_type = self.isFinal(statue,ch)
            if token_type is not None:
                if token_type == 'ID':
                    temp_token_list.append(self.judgeWord(word,line))
                elif token_type == 'CONST ID':
                    temp_token_list.append(Token('CONST ID',float(word),None))
                elif token_type == 'COMMENT':
                    return
                else:
                    temp_token_list.append(Token(token_type,word,None))
                word = ""
                statue = 0
            if ch.isspace():
                continue
            if ch in self.special:
                statue = self.move(statue,ch)
            elif ch.isdigit():
                statue = self.move(statue,'digit')
            elif ch.isalpha():
                statue = self.move(statue,'letter')
            word += ch
        temp_token_list.append(Token("NoneToken",0.0,None))
        return temp_token_list

    # 扫描文件读取数据
    def scanFile(self,buffer = " "):
        Token_list = []
        with open(self.filename) as source:
            line = 0
            while buffer is not "":
                line += 1
                buffer = source.readline()
                Token_list.append(LINETOKEN(line,self.Parser(buffer,line)))
        return Token_list

if __name__ == "__main__":
    scan = Scanner("helloworld.c")
    print(scan.scanFile())