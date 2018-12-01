from Parser import ExprNode
from Parser import Parser

# Create Tree
def InsertNode(NowNode,value):
    newNode = ExprNode('int')
    newNode.set_content(value)
    if newNode.content < NowNode.content:
        NowNode.set_left_child(newNode)
    else:
        NowNode.set_right_child(newNode)
def FindInsertPosition(root,value):
    node = root
    while(node.child_number):
        if node.child_number == 3:
            if value < node.content:
                node = node.get_left_child()
                continue
            else:
                node = node.get_right_child()
                continue
        elif node.child_number == 1:
            if value < node.content:
                node = node.get_left_child()
                continue
            else:
                break
        elif node.child_number == 2:
            if value < node.content:
                break
            else:
                node = node.get_right_child()
                continue
    return node
def MiddleRangeTree(Root):
    node = Root
    if node is None:
        return
    print((node.TokenType,node.content))
    MiddleRangeTree(node.get_left_child())
    MiddleRangeTree(node.get_right_child())
def CreateTree(value_list):
    root = ExprNode('int')
    root.set_content(value_list[0])
    for value in value_list[1:]:
        node = FindInsertPosition(root,value)
        InsertNode(node,value)
    return root


if __name__ == "__main__":
    filename = input("Source filename:")
    parser = Parser(filename)
    parser.parser_program()
    parser.Print_paramters()