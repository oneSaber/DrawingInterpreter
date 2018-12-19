from Lexer import Scanner
from Parser import Parser
from Drawing import DrawPricture
from semantics import Semantics
import sys
from multiprocessing import Process


def drawPicture(filename):
    drawing = DrawPricture(filename)
    parser = Parser(filename)
    parser.parser_program()
    sement = Semantics(paramter_list=parser.paramters,drawing=drawing)
    sement.Semantic()
    drawing.draw()

if __name__ == "__main__":
    filenames = sys.argv[1:]
    for filename in filenames:
        print(filename)
        p = Process(target=drawPicture,args=(filename,))
        p.start()