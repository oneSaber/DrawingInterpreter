# 画图程序的词法分析器
from collections import namedtuple
import math
token = namedtuple('Token',['type','origin_value','value','function'])
# 保留关键字
token_table =[token('CONST ID','PI',3.1415926,None),
              token('CONST ID','E', 2.71828,None),
              token('T','T',0.0,None),
              token('FUNC','SIN',0.0,math.sin),
              token('FUNC','COS',0.0,math.cos),
              token('FUNC','TAN',0.0,math.tan),
              token('FUNC','LN',0.0,math.log),
              token('FUNC','EXP',0.0,math.exp),
              token('FUNC','SQRT',0.0,math.sqrt),
              token('ORIGIN',"ORIGIN",0.0,None),
              token('SCALE','SCALE',0.0,None),
              token('ROT','ROT',0.0,None),
              token('IS','IS',0.0,None),
              token('FOR','FOR',0.0,None),
              token('FROM','FROM',0.0,None),
              token('TO','FROM',0.0,None),
              token('STEP','STEP',0.0,None),
              token('DRAW','DRAW',0.0,None)
              ]
# 输入缓存，为一行对应代码
buffer = " "
# 扫描文件读取数据
def scanFile(filename,buffer):
    with open(filename) as source:
        while buffer is not "":
            buffer = source.readline()
            print(buffer)

# 查表判定读到的是什么玩意



if __name__ == "__main__":
    scanFile("helloworld.c",buffer)