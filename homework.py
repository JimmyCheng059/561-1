import numpy as np
import random
import math
from copy import deepcopy
from Queue import Queue
from Queue import LifoQueue


class Zoo:
    def __init__(self, siz, liz, bd, klist, rw):
        self.size = siz
        self.numLizards = liz
        self.board = bd
        self.okList = klist
        self.row = rw


def parser(filename):
    files = open(filename, 'r').readlines()
    index = 0
    for line in files:
        if index == 0:
            search = line.strip()
        elif index == 1:
            size = int(line)
            cell = size*size
            board = np.arange(cell).reshape(size, size)
            list = np.arange(cell)
        elif index == 2:
            liz = int(line)
        else:
            num = 0
            for slot in line.strip():
                board[index - 3][num] = slot
                if int(slot) == 2:
                    tree = np.argwhere(list == ((index - 3) * size + num))
                    list = np.delete(list, tree)
                num += 1
        index += 1
    return dict(search=search, size=size, liz=liz, board=board, list=list)


def addLiz(board, spot, n, okList):
    if okList.size == 0:
        return None
    position = okList[spot]
    x = position / n
    y = position % n
    board[x][y] = 1
    liz = np.argwhere(okList == position)
    okList = np.delete(okList, liz)
    for x_u in range(x - 1, -1, -1):
        if board[x_u][y] == 2:
            break
        else:
            block = np.argwhere(okList == (x_u * n + y))
            okList = np.delete(okList, block)
    for x_d in range(x + 1, n):
        if board[x_d][y] == 2:
            break
        else:
            block = np.argwhere(okList == (x_d * n + y))
            okList = np.delete(okList, block)
    for y_u in range(y - 1, -1, -1):
        if board[x][y_u] == 2:
            break
        else:
            block = np.argwhere(okList == (x * n + y_u))
            okList = np.delete(okList, block)
    for y_d in range(y + 1, n):
        if board[x][y_d] == 2:
            break
        else:
            block = np.argwhere(okList == (x * n + y_d))
            okList = np.delete(okList, block)
    y_ul = y
    for x_ul in range(x - 1, -1, -1):
        y_ul -= 1
        if y_ul < 0:
            break
        elif board[x_ul][y_ul] == 2:
            break
        else:
            block = np.argwhere(okList == (x_ul * n + y_ul))
            okList = np.delete(okList, block)
    y_l = y
    for x_l in range(x + 1, n):
        y_l -= 1
        if y_l < 0:
            break
        elif board[x_l][y_l] == 2:
            break
        else:
            block = np.argwhere(okList == (x_l * n + y_l))
            okList = np.delete(okList, block)
    y_ur = y
    for x_ur in range(x - 1, -1, -1):
        y_ur += 1
        if y_ur > n - 1:
            break
        elif board[x_ur][y_ur] == 2:
            break
        else:
            block = np.argwhere(okList == (x_ur * n + y_ur))
            okList = np.delete(okList, block)
    y_r = y
    for x_r in range(x + 1, n):
        y_r += 1
        if y_r > n - 1:
            break
        elif board[x_r][y_r] == 2:
            break
        else:
            block = np.argwhere(okList == (x_r * n + y_r))
            okList = np.delete(okList, block)
    return dict(list=okList, post=x)


def treecheck(board, n):
    treelist = list()
    for x in range(0, n):
        for y in range(0,n):
            if board[x][y] == 2:
                treelist.append(x)
                break
    return treelist


def output(result, board, n):
    file_output = open("output.txt", 'w')
    file_output.write(result)
    if result == "OK":
        for x in range(0, n):
            file_output.write("\n")
            for y in range(0, n):
                file_output.write(str(board[x][y]))


class SAZoo:
    def __init__(self, siz, liz, bd, ll, ol, att):
        self.size = siz
        self.numLizards = liz
        self.board = bd
        self.lizlist = ll
        self.openlist = ol
        self.attack = att


def SAgen(zoo, liz):
    if liz > zoo.openlist.size:
        return False
    newList = [zoo.openlist[i] for i in random.sample(range(0, zoo.openlist.size), liz)]
    zoo.lizlist = np.asarray(newList)
    for item in zoo.lizlist:
        x = item / zoo.size
        y = item % zoo.size
        zoo.board[x][y] = 1
        liz = np.argwhere(zoo.openlist == item)
        zoo.openlist = np.delete(zoo.openlist, liz)
    return True


def attacks(zoo):
    zoo.attack = 0
    tmpatt = 0
    highest = 0
    king = list()
    for x in range(0, zoo.size):
        for y in range(0, zoo.size):
            if zoo.board[x][y] == 1:
                for x_u in range(x - 1, -1, -1):
                    if zoo.board[x_u][y] == 2:
                        break
                    elif zoo.board[x_u][y] == 1:
                        zoo.attack += 1
                        tmpatt += 1
                for x_d in range(x + 1, zoo.size):
                    if zoo.board[x_d][y] == 2:
                        break
                    elif zoo.board[x_d][y] == 1:
                        zoo.attack += 1
                        tmpatt += 1
                for y_u in range(y - 1, -1, -1):
                    if zoo.board[x][y_u] == 2:
                        break
                    elif zoo.board[x][y_u] == 1:
                        zoo.attack += 1
                        tmpatt += 1
                for y_d in range(y + 1, zoo.size):
                    if zoo.board[x][y_d] == 2:
                        break
                    elif zoo.board[x][y_d] == 1:
                        zoo.attack += 1
                        tmpatt += 1
                y_ul = y
                for x_ul in range(x - 1, -1, -1):
                    y_ul -= 1
                    if y_ul < 0:
                        break
                    elif zoo.board[x_ul][y_ul] == 2:
                        break
                    elif zoo.board[x_ul][y_ul] == 1:
                        zoo.attack += 1
                        tmpatt += 1
                y_l = y
                for x_l in range(x + 1, zoo.size):
                    y_l -= 1
                    if y_l < 0:
                        break
                    elif zoo.board[x_l][y_l] == 2:
                        break
                    elif zoo.board[x_l][y_l] == 1:
                        zoo.attack += 1
                        tmpatt += 1
                y_ur = y
                for x_ur in range(x - 1, -1, -1):
                    y_ur += 1
                    if y_ur > zoo.size - 1:
                        break
                    elif zoo.board[x_ur][y_ur] == 2:
                        break
                    elif zoo.board[x_ur][y_ur] == 1:
                        zoo.attack += 1
                        tmpatt += 1
                y_r = y
                for x_r in range(x + 1, zoo.size):
                    y_r += 1
                    if y_r > zoo.size - 1:
                        break
                    elif zoo.board[x_r][y_r] == 2:
                        break
                    elif zoo.board[x_r][y_r] == 1:
                        zoo.attack += 1
                        tmpatt += 1
                if tmpatt > highest:
                    king = list()
                    highest = tmpatt
                    king.append(x * zoo.size + y)
                elif tmpatt == highest:
                    king.append(x * zoo.size + y)
                tmpatt = 0
    return king


def neighborgen(zoo, king):
    newZoo = deepcopy(zoo)
    removeL = king
    i = random.randint(0, len(removeL) - 1)
    removeL = king[i]
    x = removeL / newZoo.size
    y = removeL % newZoo.size
    newZoo.board[x][y] = 0
    oliz = np.argwhere(newZoo.lizlist == removeL)
    newZoo.lizlist = np.delete(newZoo.lizlist, oliz)
    j = random.randint(0, newZoo.openlist.size - 1)
    addL = newZoo.openlist[j]
    x = addL / newZoo.size
    y = addL % newZoo.size
    newZoo.board[x][y] = 1
    nliz = np.argwhere(newZoo.openlist == addL)
    newZoo.openlist = np.delete(newZoo.openlist, nliz)
    newZoo.lizlist = np.append(newZoo.lizlist, addL)
    newZoo.openlist = np.append(newZoo.openlist, removeL)
    return newZoo

init = parser("input.txt")

if init["search"] == "DFS" or init["search"] == "BFS":

    treelist = treecheck(init["board"], init["size"])
    initialZoo = Zoo(init["size"], 0, init["board"], init["list"], 0)

    if init["search"] == "BFS":
        frontier = Queue()
    else:
        frontier = LifoQueue()
    frontier.put_nowait(initialZoo)
    answer = False
    while not frontier.empty():
        node = frontier.get_nowait()
        treeline = -1
        for x in range(0, node.okList.size):
            newBoard = deepcopy(node.board)
            newlist = addLiz(newBoard, x, init["size"], node.okList)
            if newlist is None:
                break
            elif newlist["post"] < node.row - 1:
                break
            elif treeline != -1:
                if newlist["post"] > treeline:
                    treeline = -1
                    break
            elif newlist["post"] > node.row:
                if node.row not in treelist:
                    break
                treeline = newlist["post"]
            newZoo = Zoo(init["size"], node.numLizards + 1, newBoard, newlist["list"], newlist["post"] + 1)
            frontier.put_nowait(newZoo)
        if node.numLizards == init["liz"]:
            output("OK", node.board, init["size"])
            answer = True
            break
    if not answer:
        output("FAIL", 0, init["size"])

elif init["search"] == "SA":

    SA = SAZoo(init["size"], 0, init["board"], 0, init["list"], 0)
    test = SAgen(SA, init["liz"])

    if not test:
        output("FAIL", 0, init["size"])
    elif init["liz"] == 0:
        output("OK", SA.board, init["size"])
    elif init["liz"] == init["list"].size:
        attacks(SA)
        if SA.attack != 0:
            output("FAIL", 0, init["size"])
        elif SA.attack == 0:
            output("OK", SA.board, init["size"])
    else:
        attacks(SA)
        T = 10000
        reset = 0
        answer = False
        while T > 0:
            kingSA = attacks(SA)
            newSA = neighborgen(SA, kingSA)
            attacks(newSA)
            delta = SA.attack - newSA.attack
            if delta > 0:
                SA = newSA
                if SA.attack == 0:
                    output("OK", SA.board, init["size"])
                    answer = True
                    break
            elif random.random() < math.exp(delta / T):
                SA = newSA
                if SA.attack == 0:
                    output("OK", SA.board, init["size"])
                    answer = True
                    break
            T -= 1
            if T == 0:
                if not answer:
                    if reset < 3:
                        init = parser("input.txt")
                        SA = SAZoo(init["size"], 0, init["board"], 0, init["list"], 0)
                        SAgen(SA, init["liz"])
                        attacks(SA)
                        T = 10000
                        reset += 1
                    else:
                        print "??"
                        output("FAIL", 0, init["size"])
