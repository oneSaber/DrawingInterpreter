# 画图程序的词法分析器
from collections import namedtuple
import math

Token = namedtuple('Token',['type','value','function'])
ERRORTOKEN = namedtuple('ERRORTOKEN',['line','word'])

special = ('*','/','-','+','(',')',',',';','.')

Error_list = []
Token_list = []

# 保留关键字
Token_table = {'PI': Token('CONST ID', 3.1415926,None),
              'E': Token('CONST ID', 2.71828,None),
              'T': Token('T', 0.0,None),
              'SIN': Token('FUNC', 0.0,math.sin),
              'COS': Token('FUNC', 0.0,math.cos),
              'TAN': Token('FUNC', 0.0,math.tan),
              'LN': Token('FUNC', 0.0,math.log),
              'EXP': Token('FUNC', 0.0,math.exp),
              'SQRT':Token('FUNC', 0.0,math.sqrt),
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
DFA_tree = { 0: { 'letter': 1, 'digit': 2, '/': 6, '-': 7,'*':4,
                  '+': 8, ',': 9, ';': 10, '(': 11, ')': 12},
             1 : {'letter' : 1, 'break':'ID'},
             2 : {'digit': 2, '.': 3},
             3 : {'digit': 3, 'break': 'CONST ID'},
             4 : {'*': 5 ,'break':'MULTIPLICATION'},
             5 : {'break': 'POWER'},
             6 : {'/': 13,'break': 'DIVISION'},
             7 : {'-' : 13, 'break':'SUBDUCTION'},
             8 : {'break': 'PLUS'},
             9 : {'break': 'SEMICO'},
             10 : {'break': 'SEMICO'},
             11 : {'break': 'L_BRACKET'},
             12 : {'break': 'R_BRACKET'},
             13 : {'break': 'COMMENT'}
            }

fina_statue = (8,9,10,11,12,13)

# origin 出发状态, condition 转移条件
def move(origin, condition):
    # 判定origin 是不是终态
    next_tree = DFA_tree[origin]
    return next_tree[condition]

# 查表判定读到的是什么玩意
def judgeWord(word,line):
    token = Token_table.get(word,None)
    if token is None:
        Error_list.append(ERRORTOKEN(line,word))
        return 'error'
    else:
        Token_list.append(token)
        return token.type

def isFinal(statue,nextword):
    if statue in fina_statue:
        # 绝对终态，不管下一个是什么直接返回
        return DFA_tree[statue]['break']
    elif statue == 1 :
        if nextword.isalpha():
            return None
        else:
            return DFA_tree[statue]['break']
    elif statue == 3 :
        if nextword.isdigit():
            return None
        else:
            return DFA_tree[statue]['break']
    elif statue == 4:
        if nextword == "*":
            return None
        else:
            return DFA_tree[statue]['break']
    elif statue == 6:
        if nextword == "/":
            return None
        else:
             return DFA_tree[statue]['break']
    elif statue == 7:
        if nextword == '-':
            return None
        else:
             return DFA_tree[statue]['break']
    else:
        return None

def eatSpace(buffer):
    for i in range(len(buffer)):
        if not buffer[i].isspace():
            return buffer[i:]
            

# 具体的解析器，从buffer中逐个字符的读入，进行状态机move，
# move每次返回可能是Token属性或者是下一个状态
# 如果是到达终态返回属性则调用judge函数判断类型，错误返回None，正确返回Token元组，然后放入Token_list
# 一直读取直到buffer结尾或者是明确行结束符号
def Parser(buffer,line):
    statue = 0
    word = ""
    buffer = eatSpace(buffer)
    if buffer is None:
        return 
    for ch in buffer:
        token_type = isFinal(statue,ch)
        if token_type is not None:
            if token_type == 'ID':
                judgeWord(word,line)
            elif token_type == 'CONST ID':
                Token_list.append(Token('CONST ID',float(word),None))
            elif token_type == 'COMMENT':
                return
            else:
                Token_list.append(Token(token_type,word,None))
            word = ""
            statue = 0
        if ch.isspace():
            continue
        if ch in special:
            statue = move(statue,ch)
        elif ch.isdigit():
            statue = move(statue,'digit')
        elif ch.isalpha():
            statue = move(statue,'letter')
        word += ch

# 扫描文件读取数据
def scanFile(filename,buffer):
    with open(filename) as source:
        line = 0
        while buffer is not "":
            line += 1
            buffer = source.readline()
            Parser(buffer,line)


if __name__ == "__main__":
    buffer = " "
    scanFile("helloworld.c",buffer)
    print('error: ')
    print(Error_list)
    print('\n token: ')
    print(Token_list)