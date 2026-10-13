from bitarray import bitarray

class bitReader:
    def __init__(self,fr):
        self.reader = fr
        self.lbits: int = 0
        self.cbyte: bitarray = bitarray()

    def readIn(self):
        if self.lbits == 0:
            data = self.reader.read(1)
            if not data:
                return None

            self.cbyte.frombytes(data)
            self.lbits = 8

        self.lbits -= 1


        return self.cbyte.pop(0)


class bitWriter:
    def __init__(self,fw):
        self.fileWriter = fw
        self.byteBuffer = bitarray()

    def writeIn(self, bt: int) -> None:
        self.byteBuffer.extend(bitarray(bt))

        while len(self.byteBuffer) >= 8:
            writing = self.byteBuffer[:8]
            del self.byteBuffer[:8]

            self.fileWriter.write(writing.tobytes())

    def flush(self) -> None:

        if len(self.byteBuffer) > 0:
            self.byteBuffer.fill()
            self.fileWriter.write(self.byteBuffer.tobytes())
            self.byteBuffer.clear()
