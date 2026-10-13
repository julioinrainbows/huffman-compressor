from collections import Counter
import heapq
from logging import root
from termios import NL1
from pathlib import Path
from bitarray import bitarray

from tools import bitReader
from huff_tree import node

heap = []

p = Path("varass.txt")


with open(p,'wb') as fw:
    with open("./arquivoteste.hff", 'rb') as fr:
            buffer = fr.read(4)
            if buffer != b"HUFF":
                raise ValueError("Huffman Flag Not Found")

            length = int.from_bytes(fr.read(4),"big")
            totalBits = int.from_bytes(fr.read(8),"big")

            for i in range(length):

                character = fr.read(1)
                charFreq = int.from_bytes(fr.read(4),"big")

                newNode = node(character,charFreq)
                heap.append(newNode)

            heapq.heapify(heap)

            while(len(heap) >1):
                n1 = heapq.heappop(heap)
                n2 = heapq.heappop(heap)
                pnode = node(None,n1.freq + n2.freq)
                pnode.ln = n1
                pnode.rn = n2

                heapq.heappush(heap,pnode)



            br = bitReader(fr)
            n = heap[0]
            for _ in range(totalBits):
                bit = br.readIn()

                if bit is None:
                    break

                n = n.ln if bit == 0 else n.rn

                if n.is_leaf():
                    fw.write(n.char)
                    n = heap[0]
