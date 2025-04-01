"""
@author: badmonkey
@software: PyCharm
@file: scanner.py
@time: 2021/4/7 上午9:50
"""


class State:
    START = "start"
    ASSIGN = "assign"
    COMMENT = "comment"
    NUM = "num"
    ID = "id"
    CHAR = "char"
    RANGE = "range"
    DONE = "done"


from Lexer.token import *

HELP = '''
Usage: scanner filename output
Example: scanner demo-sort.txt result.txt
'''


def Scan(scanner):
    state = State.START
    tokenList = list()
    line = 1
    nxt = 0
    length = len(scanner)
    while nxt < length:
        if state == State.START:
            nxtChar = scanner[nxt]
            while nxt < length and (nxtChar == ' ' or nxtChar == '\n' or nxtChar == '\r' or nxtChar == '\t'):
                if nxtChar == '\n':
                    line += 1
                nxt += 1
                if nxt == length:
                    break
                nxtChar = scanner[nxt]
            if nxt == length:
                break
            if nxtChar.isalpha() or nxtChar == '_':
                state = State.ID
            elif nxtChar.isnumeric():
                state = State.NUM
            else:
                if nxt + 1 < length and nxtChar == '.' and scanner[nxt + 1] == '.':  # 添加边界检查
                    nxt += 1
                    nxtChar = ".."
                elif nxt + 1 < length and nxtChar == ":" and scanner[nxt + 1] == '=':  # 添加边界检查
                    nxt += 1
                    nxtChar = ":="
                elif nxtChar == "{":
                    while nxt < length and nxtChar != "}":
                        nxt += 1
                        if nxt == length:
                            break
                        nxtChar = scanner[nxt]
                    if nxt < length:
                        nxt += 1
                        if nxt < length:
                            nxtChar = scanner[nxt]
                    state = State.START
                    continue
                if nxtChar in tokenType.Types:
                    tokenList.append((nxtChar, nxtChar, line))
                    nxt += 1
                    state = State.START
                else:
                    print(nxt, nxtChar, state, "error", line, scanner[nxt:])
                    break
        elif state == State.ID:
            currentId = ""
            nxtChar = scanner[nxt]
            while nxt < length and (nxtChar.isalpha() or nxtChar.isnumeric() or nxtChar == '_'):
                currentId += nxtChar
                nxt += 1
                if nxt == length:
                    break
                nxtChar = scanner[nxt]
            if currentId.lower() in tokenType.KEYWORDS:
                tokenList.append((currentId.upper(), currentId, line))
            else:
                tokenList.append((tokenType.IDENTIFIERS, currentId, line))
            state = State.START
        elif state == State.NUM:
            currentNum = ""
            nxtChar = scanner[nxt]
            while nxt < length and nxtChar.isnumeric():
                currentNum += nxtChar
                nxt += 1
                if nxt == length:
                    break
                nxtChar = scanner[nxt]
            tokenList.append((tokenType.INTC, int(currentNum), line))
            state = State.START
    return tokenList


if __name__ == '__main__':
    scanner = list(open("../CodeGenerator/testalltwo.txt", "r").read())
    tokens = Scan(scanner)
    out = open("testalltwo-Lexer.txt", "w")
    for i in tokens:
        out.write(str(i) + "\n")
    out.close()
