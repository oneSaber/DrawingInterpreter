from Lexer import Scanner
import os
base_path = os.getcwd()


if __name__ == "__main__":
    file_name = input("Source file name:")
    # file_path = os.path.join(base_path,file_name)
    scanner = Scanner(file_name)
    tokens_list = scanner.scanFile()
    for tokens in tokens_list:
        if tokens.Tokens is not None:
            print("line {}".format(tokens.LineNo))
            for token in tokens.Tokens:
                print(token)