__license__ = 'Junior (c) EPITA'
__docformat__ = 'reStructuredText'
__revision__ = '$Id: huffman.py 2022-04-17'

"""
Huffman homework
2022
@author: hugo.meleiro
"""

from algopy import bintree
from algopy import heap


###############################################################################
# Do not change anything above this line, except your login!
# Do not add any import

###############################################################################
## COMPRESSION

# --- AUX FUNCTIONS --- #

def __frequency(dataIN, dataC):
    count = 0
    for i in range(len(dataIN)):
        if dataIN[i] == dataC:
            count += 1
    return count


def __inthelist(L, dataC):
    for i in range(len(L)):
        if dataC == L[i][1]:
            return True
    return False
    
# --- END --- #

def buildfrequencylist(dataIN):
    L = []
    for i in range(len(dataIN)):
        if not __inthelist(L, dataIN[i]):
            frequency = __frequency(dataIN, dataIN[i])
            L.append((frequency, dataIN[i]))
    return L
    
# --- AUX FUNCTIONS --- #

def __listtree(inputList):
    for i in range(len(inputList)):
        inputList[i] = bintree.BinTree((inputList[i][0], inputList[i][1]), None, None)
    return inputList


def __buildminlist(inputList):
    min1 = inputList[0]
    freqencemin1 = min1.key[0]
    length = len(inputList)
    index = 0
    for i in range(length):
        if inputList[i].key[0] < freqencemin1:
            min1 = inputList[i]
            freqencemin1 = min1.key[0]
            index = i
    (inputList[index], inputList[length - 1]) = (inputList[length - 1], inputList[index])
    min1 = inputList.pop()
    # Next min
    min2 = inputList[0]
    freqencemin2 = min2.key[0]
    index = 0
    length = len(inputList)
    for i in range(length):
        if inputList[i].key[0] < freqencemin2:
            min2 = inputList[i]
            freqencemin2 = min2.key[0]
            index = i
    (inputList[index], inputList[length - 1]) = (inputList[length - 1], inputList[index])
    min2 = inputList.pop()
    inputList.append(bintree.BinTree((freqencemin1 + freqencemin2, None), min1, min2))
    return inputList


def __changeKey(B):
    if B != None:
        if B.key[1] == '_':
            B.key = ' '
        else:
            B.key = B.key[1]
        __changeKey(B.left)
        __changeKey(B.right)
    return B
    
# --- END --- #

def buildHuffmantree(inputList):
    """
    Processes the frequency list into a Huffman tree according to the algorithm.
    """
    inputList = __listtree(inputList)
    while len(inputList) > 1:
        inputList = __buildminlist(inputList)
    B = __changeKey(inputList[0])
    return B

# --- AUX FUNCTIONS --- #

def __listofoccurence(B, L=[], s=""):
    if B != None:
        if B.key != None:
            L.append((B.key, s))
        if B.left != None:
            __listofoccurence(B.left, L, s + "0")
        if B.right != None:
            __listofoccurence(B.right, L, s + "1")
    return L


def __charinlist(L, c):
    length = len(L)
    for i in range(length):
        if L[i][0] == '_' and c == ' ':
            return i, True
        if L[i][0] == c:
            return i, True
    return -1, False

# --- END --- #

def encodedata(huffmanTree, dataIN):
    """
    Encodes the input string to its binary string representation.
    """
    s = ""
    L = __listofoccurence(huffmanTree, [], "")
    length = len(dataIN)
    for i in range(length):
        (index, valid) = __charinlist(L, dataIN[i])
        if valid:
            s += L[index][1]
    return s

# --- AUX FUNCTIONS --- #

def __charbin(char):
    code = ord(char)
    s = ""
    while code > 0:
        s += str(code % 2)
        code = code // 2
    while len(s) < 8:
        s += '0'
    res = ""
    index = len(s) - 1
    while index >= 0:
        res += s[index]
        index -= 1
    return res


def __encodetreebis(B, s=""):
    if B:
        if B.key:
            return '1' + __charbin(B.key) + __encodetreebis(B.left, s) + __encodetreebis(B.right, s)
        else:
            return '0' + __encodetreebis(B.left, s) + __encodetreebis(B.right, s)
    return s

# --- END --- #

def encodetree(huffmanTree):
    """
    Encodes a huffman tree to its binary representation using a preOrder traversal:
        * each leaf key is encoded into its binary representation on 8 bits preceded by '1'
        * each time we go left we add a '0' to the result
    """
    return __encodetreebis(huffmanTree)


def tobinary(dataIN):
    """
    Compresses a string containing binary code to its real binary value.
    """
    nbChar = index = 0
    res = ""
    length = len(dataIN) - 1
    elocho = length // 8
    while nbChar < elocho:
        string = ""
        index2 = 0
        while index2 < 8:
            string += dataIN[index]
            index2 += 1
            index += 1
        res += __binarychar(string)
        nbChar += 1
    rest = length % 8 + 1
    first = 8 - rest
    string = ""
    while first > 0:
        string += '0'
        first -= 1
    while index <= length:
        string += dataIN[index]
        index += 1
    res += __binarychar(string)
    return res, 8 - rest


def compress(dataIn):
    """
    The main function that makes the whole compression process.
    """
    frequenceList = buildfrequencylist(dataIn)
    huffmanTree = buildHuffmantree(frequenceList)
    dataEncoded = encodedata(huffmanTree, dataIn)
    treeEncoded = encodetree(huffmanTree)
    return tobinary(dataEncoded), tobinary(treeEncoded)

    
################################################################################
## DECOMPRESSION

# --- AUX FUNCTIONS --- #
def __charintree(B, dataIn, index):
    isValid = True
    res = ""
    while isValid:
        if B.key != None:
            isValid = False
            if B.key == '_':
                res += ' '
            else:
                res = B.key
        elif dataIn[index] == '0':
            B = B.left
        else:
            B = B.right
        index += 1
    return res, index - 1

# --- END --- #

def decodedata(huffmanTree, dataIN):
    """
    Decode a string using the corresponding huffman tree into something more readable.
    """
    res = ""
    length = len(dataIN)
    nb = 0
    res2, nb = __charintree(huffmanTree, dataIN, nb)
    res += res2
    while nb < length:
        res2, nb = __charintree(huffmanTree, dataIN, nb)
        res += res2
    return res

# --- AUX FUNCTIONS --- #

def __binarychar(binstr):
    pow = 7
    i = res = 0
    while i < len(binstr):
        if binstr[i] == '1':
            res += 2**pow
        pow -= 1
        i += 1
    return chr(res)

def __reverseList(L):
    res = []
    nb = len(L) - 1
    while nb >= 0:
        res.append(L[nb])
        nb -= 1
    L = res
    return L

def __chartolist(dataIN):
    nb = 0
    L = []
    tree = []
    while nb < len(dataIN):
        string = ""
        if dataIN[nb] == '1':
            tree.append(dataIN[nb])
            nb += 1
            i = nb
            while i < nb + 8:
                string += dataIN[i]
                i += 1
            nb += 8
            L.append(__binarychar(string))
        else:
            tree.append(dataIN[nb])
            nb += 1
    L = __reverseList(L)
    tree = __reverseList(tree)
    return L, tree

def __decodetree(chartolist, tree):
    if len(tree) <= 0:
        return None
    indextree = len(tree) - 1
    if tree[indextree] == '1':
        tree.pop()
        index = len(chartolist) - 1
        key = chartolist[index]
        chartolist.pop()
        B = bintree.BinTree(key, None, None)
        return B
    elif tree[indextree] == '0':
        tree.pop()
        B = bintree.BinTree(None, None, None)
        B.left = __decodetree(chartolist, tree)
        B.right = __decodetree(chartolist, tree)
        return B
    return None

# --- END --- #

def decodetree(dataIN):
    """
    Decodes a huffman tree from its binary representation:
        * a '0' means we add a new internal node and go to its left node
        * a '1' means the next 8 values are the encoded character of the current leaf         
    """
    (chartolist, tree) = __chartolist(dataIN)
    res = __decodetree(chartolist, tree)
    return res

def frombinary(dataIN, align):
    """
    Retrieve a string containing binary code from its real binary value (inverse of :func:`toBinary`).
    """
    res = ""
    nb = 0
    while nb < len(dataIN) - 1:
        char = __charbin(dataIN[nb])
        res += char
        nb += 1
    charbin = __charbin(dataIN[nb])
    i = 0
    while i < len(charbin):
        if i < align:
            i += 1
            continue
        res += charbin[i]
        i += 1
    return res

def decompress(data, dataAlign, tree, treeAlign):
    """
    The whole decompression process.
    """
    bintree = frombinary(tree, treeAlign)
    decompressed = decodetree(bintree)
    bindata = frombinary(data, dataAlign)
    res = decodedata(decompressed, bindata)
    return res