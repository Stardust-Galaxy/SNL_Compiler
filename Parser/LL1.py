"""
@author: badmonkey
@software: PyCharm
@file: LL1.py
@time: 2021/4/14 上午10:34
"""

# 文法
grammar = {
    # 起始符
    "S": "Program",
    # 产生式
    "P": {
        "Program": {0: ["ProgramHead", "DeclarePart", "ProgramBody", "."]},
        "ProgramHead": {0: ["PROGRAM", "ProgramName"]},
        "ProgramName": {0: ["ID"]},
        "DeclarePart": {0: ["TypeDec", "VarDec", "ProcDec"]},
        "TypeDec": {0: ["ε"], 1: ["TypeDeclaration"]},
        "TypeDeclaration": {0: ["TYPE", "TypeDecList"]},
        "TypeDecList": {0: ["TypeId", "=", "TypeName", ";", "TypeDecMore"]},
        "TypeDecMore": {0: ["ε"], 1: ["TypeDecList"]},
        "TypeId": {0: ["ID"]},
        "TypeName": {0: ["BaseType"], 1: ["StructureType"], 2: ["ID"]},
        "BaseType": {0: ["INTEGER"], 1: ["CHAR"]},
        "StructureType": {0: ["ArrayType"], 1: ["RecType"]},
        "ArrayType": {0: ["ARRAY", "[", "Low", "..", "Top", "]", "OF", "BaseType"]},
        "Low": {0: ["INTC"]},
        "Top": {0: ["INTC"]},
        "RecType": {0: ["RECORD", "FieldDecList", "END"]},
        "FieldDecList": {
            0: ["BaseType", "IdList", ";", "FieldDecMore"],
            1: ["ArrayType", "IdList", ";", "FieldDecMore"],
        },
        "FieldDecMore": {0: ["ε"], 1: ["FieldDecList"]},
        "IdList": {0: ["ID", "IdMore"]},
        "IdMore": {0: ["ε"], 1: [",", "IdList"]},
        "VarDec": {0: ["ε"], 1: ["VarDeclaration"]},
        "VarDeclaration": {0: ["VAR", "VarDecList"]},
        "VarDecList": {0: ["TypeName", "VarIdList", ";", "VarDecMore"]},
        "VarDecMore": {0: ["ε"], 1: ["VarDecList"]},
        "VarIdList": {0: ["ID", "VarIdMore"]},
        "VarIdMore": {0: ["ε"], 1: [",", "VarIdList"]},
        "ProcDec": {0: ["ε"], 1: ["ProcDeclaration"]},
        "ProcDeclaration": {
            0: [
                "PROCEDURE",
                "ProcName",
                "(",
                "ParamList",
                ")",
                ";",
                "ProcDecPart",
                "ProcBody",
                "ProcDecMore",
            ]
        },
        "ProcDecMore": {0: ["ε"], 1: ["ProcDeclaration"]},
        "ProcName": {0: ["ID"]},
        "ParamList": {0: ["ε"], 1: ["ParamDecList"]},
        "ParamDecList": {0: ["Param", "ParamMore"]},
        "ParamMore": {0: ["ε"], 1: [";", "ParamDecList"]},
        "Param": {0: ["TypeName", "FormList"], 1: ["VAR", "TypeName", "FormList"]},
        "FormList": {0: ["ID", "FidMore"]},
        "FidMore": {0: ["ε"], 1: [",", "FormList"]},
        "ProcDecPart": {0: ["DeclarePart"]},
        "ProcBody": {0: ["ProgramBody"]},
        "ProgramBody": {0: ["BEGIN", "StmList", "END"]},
        "StmList": {0: ["Stm", "StmMore"]},
        "StmMore": {0: ["ε"], 1: [";", "StmList"]},
        "Stm": {
            0: ["ConditionalStm"],
            1: ["LoopStm"],
            2: ["InputStm"],
            3: ["OutputStm"],
            4: ["ReturnStm"],
            5: ["ID", "AssCall"],
        },
        "AssCall": {0: ["AssignmentRest"], 1: ["CallStmRest"]},
        "AssignmentRest": {0: ["VariMore", ":=", "Exp"]},
        "ConditionalStm": {
            0: ["IF", "RelExp", "THEN", "StmList", "ELSE", "StmList", "FI"]
        },
        "LoopStm": {0: ["WHILE", "RelExp", "DO", "StmList", "ENDWH"]},
        "InputStm": {0: ["READ", "(", "Invar", ")"]},
        "Invar": {0: ["ID"]},
        "OutputStm": {0: ["WRITE", "(", "Exp", ")"]},
        "ReturnStm": {0: ["RETURN", "(", "Exp", ")"]},
        "CallStmRest": {0: ["(", "ActParamList", ")"]},
        "ActParamList": {0: ["ε"], 1: ["Exp", "ActParamMore"]},
        "ActParamMore": {0: ["ε"], 1: [",", "ActParamList"]},
        "RelExp": {0: ["Exp", "OtherRelE"]},
        "OtherRelE": {0: ["CmpOp", "Exp"]},
        "Exp": {0: ["Term", "OtherTerm"]},
        "OtherTerm": {0: ["ε"], 1: ["AddOp", "Exp"]},
        "Term": {0: ["Factor", "OtherFactor"]},
        "OtherFactor": {0: ["ε"], 1: ["MultOp", "Term"]},
        "Factor": {0: ["(", "Exp", ")"], 1: ["INTC"], 2: ["Variable"]},
        "Variable": {0: ["ID", "VariMore"]},
        "VariMore": {0: ["ε"], 1: ["[", "Exp", "]"], 2: [".", "FieldVar"]},
        "FieldVar": {0: ["ID", "FieldVarMore"]},
        "FieldVarMore": {0: ["ε"], 1: ["[", "Exp", "]"]},
        "CmpOp": {0: ["<"], 1: ["="]},
        "AddOp": {0: ["+"], 1: ["-"]},
        "MultOp": {0: ["*"], 1: ["/"]},
    },
    # 非终极符
    "VN": [
        "ActParamList",
        "ActParamMore",
        "AddOp",
        "ArrayType",
        "AssCall",
        "AssignmentRest",
        "BaseType",
        "CallStmRest",
        "CmpOp",
        "ConditionalStm",
        "DeclarePart",
        "Exp",
        "Factor",
        "FidMore",
        "FieldDecList",
        "FieldDecMore",
        "FieldVar",
        "FieldVarMore",
        "FormList",
        "IdList",
        "IdMore",
        "InputStm",
        "Invar",
        "LoopStm",
        "Low",
        "MultOp",
        "OtherFactor",
        "OtherRelE",
        "OtherTerm",
        "OutputStm",
        "Param",
        "ParamDecList",
        "ParamList",
        "ParamMore",
        "ProcBody",
        "ProcDec",
        "ProcDecMore",
        "ProcDecPart",
        "ProcDeclaration",
        "ProcName",
        "Program",
        "ProgramBody",
        "ProgramHead",
        "ProgramName",
        "RecType",
        "RelExp",
        "ReturnStm",
        "Stm",
        "StmList",
        "StmMore",
        "StructureType",
        "Term",
        "Top",
        "TypeDec",
        "TypeDecList",
        "TypeDecMore",
        "TypeDeclaration",
        "TypeId",
        "TypeName",
        "VarDec",
        "VarDecList",
        "VarDecMore",
        "VarDeclaration",
        "VarIdList",
        "VarIdMore",
        "VariMore",
        "Variable",
    ],
    # 终极符
    "VT": [
        "(",
        ")",
        "*",
        "+",
        ",",
        "-",
        ".",
        "..",
        "/",
        ":=",
        ";",
        "<",
        "=",
        "ARRAY",
        "BEGIN",
        "CHAR",
        "DO",
        "ELSE",
        "END",
        "ENDWH",
        "FI",
        "ID",
        "IF",
        "INTC",
        "INTEGER",
        "OF",
        "PROCEDURE",
        "PROGRAM",
        "READ",
        "RECORD",
        "RETURN",
        "THEN",
        "TYPE",
        "VAR",
        "WHILE",
        "WRITE",
        "[",
        "]",
    ],
    # 空
    "NN": ["ε"],
}


def firstSet(grammar, leftSymbol):
    result = set()
    if leftSymbol in grammar["VT"] or leftSymbol == "ε":
        result.add(leftSymbol)
        return result
    sons = grammar["P"][leftSymbol]
    for i in range(len(sons)):
        son = sons[i]
        for grandSon in son:
            grandSonFirst = firstSet(grammar, grandSon)
            result = result.union(grandSonFirst - {"ε"})  # 先排除 ε
            if "ε" not in grandSonFirst:
                break
        if all("ε" in firstSet(grammar, s) for s in son):  # 所有符号可为空
            result.add("ε")
    return result


def followSet(grammar):
    """

    :param gram: 文法规则
    :return: follow set
    """
    # declare empty set for all VN
    allFollowSet = {}
    for vn in grammar["VN"]:
        allFollowSet[vn] = set()
    # start symbol init with '#'
    allFollowSet[grammar["S"]].add("#")

    done = False
    while not done:
        # print(allFollowSet)
        preStatus = [len(allFollowSet[vn]) for vn in grammar["VN"]]
        # loop all P
        for p in grammar["P"]:
            sons = grammar["P"][p]
            length = len(sons)
            for i in range(length):

                # 每个分支为一个son
                son = sons[i]
                # print(son)
                # 遍历每个son的节点
                sonNum = len(son)
                for j in range(sonNum):
                    grandSon = son[j]
                    # print(j,sonNum)
                    if grandSon not in grammar["VN"]:
                        continue
                    else:
                        if j == sonNum - 1:
                            allFollowSet[grandSon] = allFollowSet[grandSon].union(
                                allFollowSet[p]
                            )
                        else:
                            k = j + 1
                            backSon = son[k]
                            backSonFirst = firstSet(grammar, backSon)
                            while k < sonNum and "ε" in backSonFirst:
                                backSonFirst.remove("ε")
                                allFollowSet[grandSon] = allFollowSet[grandSon].union(
                                    backSonFirst
                                )
                                k += 1
                                if k == sonNum:
                                    allFollowSet[grandSon] = allFollowSet[
                                        grandSon
                                    ].union(allFollowSet[p])
                                    break
                                backSon = son[k]
                                backSonFirst = firstSet(grammar, backSon)
                            allFollowSet[grandSon] = allFollowSet[grandSon].union(
                                backSonFirst
                            )

        curStatus = [len(allFollowSet[vn]) for vn in grammar["VN"]]
        if curStatus == preStatus:
            done = True
    return allFollowSet


def ll1Table(grammar):
    first = {}
    table = {}
    for vn in grammar["VN"]:
        first[vn] = firstSet(grammar, vn)
        table[vn] = {}
        for vt in grammar["VT"]:
            table[vn][vt] = "error"
    follow = followSet(grammar)

    for p in grammar["P"]:
        sons = grammar["P"][p]
        for i in range(len(sons)):
            son = sons[i]
            head = son[0]
            if head in grammar["VT"]:
                table[p][head] = son
            else:
                possible = set()
                for element in son:
                    if element in grammar["VN"]:
                        tmp = first[element].copy()
                        if "ε" in tmp:
                            tmp.remove("ε")
                            possible = possible.union(tmp, follow[p])
                        else:
                            possible = possible.union(tmp)
                            break
                    elif element == "ε":
                        possible = possible.union(follow[p])
                    elif element in grammar["VT"]:
                        possible.add(element)
                        break
                for poss in possible:
                    table[p][poss] = son

    # 额外调试 VarDec
    print("VarDec 的表项：")
    for vt in grammar["VT"]:
        if table["VarDec"][vt] != "error":
            print(f"  {vt}: {table['VarDec'][vt]}")

    with open("first.txt", "w") as f:
        for vn in first:
            f.write(f"{vn}\t{first[vn]}\n")
    with open("follow.txt", "w") as f:
        for vn in follow:
            f.write(f"{vn}\t{follow[vn]}\n")

    return table


from Parser.AST import *


def generateAST(tokens):
    tokenStack = []
    table = ll1Table(grammar)

    # 填充 tokenStack 用于跟踪
    for token in tokens:
        token = eval(token.strip())
        tokenType = token[0]
        tokenStack.append(tokenType)

    stack = [grammar["S"]]  # 初始符号
    root = AstNode(grammar["S"])
    current = root

    i = 0  # token 索引
    while i < len(tokens) and stack:
        token = eval(tokens[i].strip())
        tokenType = token[0]
        tokenVal = token[1]

        top = stack[-1]  # 查看栈顶
        print(f"Step {i}: Stack={stack}, Top={top}, Token={tokenType}")  # 调试信息

        if top == "ε":  # 处理空产生式
            stack.pop()
            current.insertChild(AstNode("ε", "ε"))
            current = current.step()
            continue

        if top == tokenType:  # 终结符匹配
            stack.pop()
            tokenStack.pop(0)
            current.tokenType = tokenType
            current.tokenVal = tokenVal
            current = current.step()
            i += 1
        elif top in grammar["VT"]:  # 终结符不匹配
            print(f"错误：期望终结符 '{top}' 但得到 '{tokenType}' 在 token {token}")
            i += 1  # 跳过 token 尝试恢复
        else:  # 非终结符
            try:
                choice = table[top][tokenType]
                if choice == "error":
                    print(
                        f"错误：'{top}' 对于输入 '{tokenType}' 无有效产生式，在 token {token}"
                    )
                    i += 1  # 跳过 token 尝试恢复
                    continue
                stack.pop()  # 弹出非终结符
                # 将产生式逆序压栈
                for symbol in choice[::-1]:
                    stack.append(symbol)
                # 为产生式创建 AST 节点
                for symbol in choice:
                    current.insertChild(AstNode(symbol))
                current = current.child[0]
            except KeyError:
                print(f"错误：'{top}' 对于输入 '{tokenType}' 无表项，在 token {token}")
                i += 1  # 跳过 token 尝试恢复

    if stack:
        print(f"错误：解析未完成，栈中剩余：{stack}")
    if i < len(tokens):
        print(f"错误：未处理的 token：{tokens[i:]}")

    # 生成普通文本格式的 AST
    with open("ast.txt", "w", encoding="utf-8") as ast_file:
        root.dump(file=ast_file)

    # 生成 JSON 格式的 AST
    with open("ast_json.txt", "w", encoding="utf-8") as json_ast_file:
        json.dump(root, json_ast_file, cls=AstNodeEncoder)

    return root


def display(root):
    current = root
    from graphviz import Digraph

    graph = Digraph(name="ast", format="png")
    stack = []
    stack.append(current)
    while stack:
        node = stack.pop(0)
        color = "black"
        name = "node" + str(node.getId())
        label = node.getTokenType()
        if label == "ε":
            color = "yellow"
        elif label in grammar["VT"]:
            color = "red"
            if label in ["INTC", "ID"]:
                label = label + "\n" + str(node.getTokenVal())
        else:
            pass

        graph.node(name=name, label=label, color=color)
        for child in node.child:
            sonName = "node" + str(child.getId())
            stack.append(child)
            graph.edge(name, sonName)
    graph.render("ast", view=True)


if __name__ == "__main__":
    tokens = open(
        "../Lexer/bubble-Lexer.txt", "r"
    ).readlines()
    root = generateAST(tokens)
    display(root)
