from collections import Counter
import heapq
from termios import NL1
from pathlib import Path
from bitarray import bitarray

from tools import bitWriter
from huff_tree import node

with open("./src/asd.txt", 'rb') as fr:
    content = fr.read()
    freq = Counter(content)


heap = []

for k,v in freq.items():
    newNode = node(k,v)
    heap.append(newNode)

heapq.heapify(heap)

while(len(heap) >1):
    n1 = heapq.heappop(heap)
    n2 = heapq.heappop(heap)
    pnode = node(None,n1.freq + n2.freq)
    pnode.ln = n1
    pnode.rn = n2

    heapq.heappush(heap,pnode)

hRoot = heap[0] if heap else None

heapDict = dict()
def dictGen(n : node, prefix : str):
    if n is None:
        return
    if n.ln is None and n.rn is None:
        heapDict[n.char] = prefix if prefix else "0"
        return

    dictGen(n.rn,prefix + '1')
    dictGen(n.ln,prefix + '0')

if hRoot:
    dictGen(hRoot,"")



totalBits : int = 0

for k,v in freq.items():
    totalBits += v*len(heapDict[k])

def genFile(file_path : Path):
    with open(file_path,'wb') as fw:
        fw.write(b"HUFF")
        fw.write(len(freq).to_bytes(4,"big"))
        fw.write(totalBits.to_bytes(8,"big"))
        for p, f in freq.items():
            fw.write(p.to_bytes(1,"big"))
            fw.write(f.to_bytes(4,"big"))

        bw = bitWriter(fw)
        for b in content:
            bw.writeIn(heapDict[b])
        bw.flush()

        ## contentpopfront > dicionario > correspondente
        ## correspondente > bw

p = Path("arquivoteste.hff")

genFile(p)
