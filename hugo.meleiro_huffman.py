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

def __frequency(dataIN, c):
    """
    :param dataIN: string
    :param c: character
    :return: frequency of the character c in the string dataIN
    """
    count = 0
    for i in range(len(dataIN)):
        if dataIN[i] == c:
            count += 1
    return count


def __inthelist(L, c):
    """
    :param L: list of Tuple(frequency, char)
    :param c: char
    :return: True if the character c is in the list L or False if not
    """
    for i in range(len(L)):
        if c == L[i][1]:
            return True
    return False


def buildfrequencylist(dataIN):
    """
    Builds a tuple list of the character frequencies in the input.
    """
    L = []
    for i in range(len(dataIN)):
        if not __inthelist(L, dataIN[i]):
            frequency = __frequency(dataIN, dataIN[i])
            L.append((frequency, dataIN[i]))
    return L


def buildHuffmantree(inputList):
    """
    Processes the frequency list into a Huffman tree according to the algorithm.
    """
def __listtree(inputList):
    """
    :param inputList: list of Tuple(frequency, char)
    :return: a bintree list where each bintree is a leaf and have a Tuple(frequency, char) as key
    """
    for i in range(len(inputList)):
        inputList[i] = bintree.BinTree((inputList[i][0], inputList[i][1]), None, None)
    return inputList


def __2minlist(inputList):
    """
    :param inputList: bintree list (result of __listtree(inputList))
    :return: input list but with a new bintree created from the 2 smallest frequency of the list
    """
    # first min
    mini1 = inputList[0]
    mini1freq = mini1.key[0]
    length = len(inputList)
    index = 0
    for i in range(length):
        if inputList[i].key[0] < mini1freq:
            mini1 = inputList[i]
            mini1freq = mini1.key[0]
            index = i
    (inputList[index], inputList[length - 1]) = (inputList[length - 1], inputList[index])
    mini1 = inputList.pop()
    # second min
    mini2 = inputList[0]
    mini2freq = mini2.key[0]
    index = 0
    length = len(inputList)
    for i in range(length):
        if inputList[i].key[0] < mini2freq:
            mini2 = inputList[i]
            mini2freq = mini2.key[0]
            index = i
    (inputList[index], inputList[length - 1]) = (inputList[length - 1], inputList[index])
    mini2 = inputList.pop()
    inputList.append(bintree.BinTree((mini1freq + mini2freq, None), mini1, mini2))
    return inputList


def __changeKey(B):
    """
    :param B: an huffman tree
    :return: the same huffman tree but the key as changed,
    """
    if B != None:
        if B.key[1] == '_':
            B.key = ' '
        else:
            B.key = B.key[1]
        __changeKey(B.left)
        __changeKey(B.right)
    return B


def buildHuffmantree(inputList):
    """
    Processes the frequency list into a Huffman tree according to the algorithm.
    """
    inputList = __listtree(inputList)
    while len(inputList) > 1:
        inputList = __2minlist(inputList)
    B = __changeKey(inputList[0])
    return B


def encodedata(huffmanTree, dataIN):
    """
    Encodes the input string to its binary string representation.
    """
    # FIXME
    pass


def encodetree(huffmanTree):
    """
    Encodes a huffman tree to its binary representation using a preOrder traversal:
        * each leaf key is encoded into its binary representation on 8 bits preceded by '1'
        * each time we go left we add a '0' to the result
    """
    # FIXME
    pass


def tobinary(dataIN):
    """
    Compresses a string containing binary code to its real binary value.
    """
    # FIXME
    pass


def compress(dataIn):
    """
    The main function that makes the whole compression process.
    """
    
    # FIXME
    pass

    
################################################################################
## DECOMPRESSION

def decodedata(huffmanTree, dataIN):
    """
    Decode a string using the corresponding huffman tree into something more readable.
    """
    # FIXME
    pass

    
def decodetree(dataIN):
    """
    Decodes a huffman tree from its binary representation:
        * a '0' means we add a new internal node and go to its left node
        * a '1' means the next 8 values are the encoded character of the current leaf         
    """
    # FIXME
    pass


def frombinary(dataIN, align):
    """
    Retrieve a string containing binary code from its real binary value (inverse of :func:`toBinary`).
    """
    # FIXME
    pass


def decompress(data, dataAlign, tree, treeAlign):
    """
    The whole decompression process.
    """
    # FIXME
    pass
