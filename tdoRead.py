import struct

blank = "Overlays/blank.tdo"
oneLine = "Overlays/oneLine.tdo"
oneLine2 = "Overlays/oneLine_2.tdo"
oneLine3 = "Overlays/oneLine_3.tdo"
oneLineAgain = "Overlays/oneLineAgain.tdo"
oneTrack = "Overlays/oneTrack.tdo"
oneTrackAgain = "Overlays/oneTrackAgain.tdo"
twoLine2 = "Overlays/twoLine_2.tdo"
oneLinesaveAs = "Overlays/oneLine_saveAs.tdo"
oneLinesaveAs2 = "Overlays/oneLine_saveAs2.tdo"
oneLinesaveAs3 = "Overlays/oneLine_saveAs3.tdo"

oneLinesaveAsr1 = "Overlays/oneLine_saveAs_r1.tdo"

def dbg(inDat):
    print("="*25)
    print("datasize={}".format(len(inDat)))
    print(inDat)
    print("="*25)
    print()

def getHex(inDat):
    _d = ["{0:02x}".format(x) for x in inDat]
    return _d

def get(inBin, start, datlen, fmt):
    printHex(inBin[start:start+datlen])
    x = struct.unpack(fmt, inBin[start:start+datlen])
    if len(x)==1:
        return x[0]
    else:
        return x

class TdoElementBase:
    def __init__(self, rawDat):
        self.rawData = rawDat
        self.parseHead()
    
    def parseHead(self):
        self.datType, self.Unknown1, self.datNum = struct.unpack(">HHH", self.rawData[0:6])

    def getBody(self):
        return self.rawData[6:]

    def __str__(self):
        rtn = ""
        rtn = rtn + "Type={}".format(self.datType)
        rtn = rtn + "\nDatNum={}".format(self.datNum)
        rtn = rtn + "\nBody={}".format(getHex(self.getBody()))
        return rtn
    
    def check(self, testNum):
        if self.datType!=testNum:
            print("[check]Test Error")
            exit()

class TdoPoint(TdoElementBase):
    def __init__(self, rawDat):
        super().__init__(rawDat)
        self.check(1)
        self.parse()
    
    def parse(self):
        #print("body size={}".format(len(self.getBody())))
        self.x, self.y = struct.unpack(">dd", self.getBody()[0:16])
        self.Unknown2= struct.unpack(">4H", self.getBody()[16:])
    
    def __str__(self):
        rtn = ""
        rtn = rtn + "Type={}".format(self.datType)
        rtn = rtn + "\nDatNum={}".format(self.datNum)
        rtn = rtn + "\nX={} Y={}".format(self.x, self.y)
        #rtn = rtn + "\n(Raw Data is {} byte)".format(len(self.rawData))

        return rtn

class TdoLine(TdoElementBase):
    def __init__(self, rawDat):
        super().__init__(rawDat)
        self.check(3)
        self.parse()
    
    def parse(self):
        #print("body size={}".format(len(self.getBody())))
        self.startPoint, self.endPoint = struct.unpack(">II", self.getBody()[0:8])
        self.Unknown2= struct.unpack(">4H", self.getBody()[8:])
    
    def __str__(self):
        rtn = ""
        rtn = rtn + "Type={}".format(self.datType)
        rtn = rtn + "\nDatNum={}".format(self.datNum)
        rtn = rtn + "\nstartPointNum={} endPointNum={}".format(self.startPoint, self.endPoint)

        return rtn

class Tdo:
    def __init__(self, filename):
        self.filename = filename
        self.headerSize = 1244
        self.readAll()
        self.readFileHeader()
        
        self.Points = list()
        self.Lines = list()
        self.Others = list()
        self.parseBody()
        
    
    def readAll(self):
        self.datAll = open(self.filename, "rb").read()
    
    def readFileHeader(self):
        self.header = self.datAll[:self.headerSize]

        self.fileType = header[:6]
        #dbg(fileType)

        self.timeStamp = header[6:30]
        #dbg(timeStamp)
    
    def readFileHeader(self):
        self.body = self.datAll[self.headerSize:]
    
    def parseBody(self):
        pointer=0
        while True:
            t = struct.unpack(">H", self.body[pointer:pointer+2])[0]
            if t==1:
                self.Points.append(TdoPoint(self.body[pointer:pointer+30]))
                pointer = pointer + 30
            elif t==3:
                self.Lines.append(TdoLine(self.body[pointer:pointer+22]))
                pointer = pointer + 22
            #elif t==3:
            #    self.Others.append(TdoElementBase(self.body[pointer:pointer+22]))
            #    pointer = pointer + 22
            else:
                print("Unknown Type", t)
                print(getHex(self.body[pointer:pointer+10]))
                break
            
            if pointer >= len(self.body):
                break
    
    def __str__(self):
        rtn = ""
        rtn = rtn + "\n========== TDO object =========="
        rtn = rtn + "\n----- Points -----"
        if len(self.Points)==0:
            rtn = rtn + "\n(no Points)"
        for i,p in enumerate(self.Points):
            rtn = rtn + "\n[Point {0}]".format(i)
            rtn = rtn + "\n" + p.__str__()
        rtn = rtn + "\n----- Lines -----"
        if len(self.Lines)==0:
            rtn = rtn + "\n(no Lines)"
        for i,p in enumerate(self.Lines):
            rtn = rtn + "\n[Line {0}]".format(i)
            rtn = rtn + "\n" + p.__str__()
        rtn = rtn + "\n----- Others -----"
        if len(self.Others)==0:
            rtn = rtn + "\n(no Others)"
        for i,p in enumerate(self.Others):
            rtn = rtn + "\n[Other {0}]".format(i)
            rtn = rtn + "\n" + p.__str__()
        return rtn+"\n========================================"

t1 = Tdo(oneLine)
print(t1)

t2 = Tdo(oneLine2)
print(t2)

t3 = Tdo(twoLine2)
print(t3)

exit()


def readtdo(fname):
    dat = open(fname, "rb").read()
    #print(dat)
    #print("Size = {} bytes".format(len(dat)))
    return dat





def analyze(inDat):
    headerSize = 1244
    header = inDat[:headerSize]
    rest = inDat[headerSize:]
    
    fileType = header[:6]
    dbg(fileType)

    timeStamp = header[6:30]
    dbg(timeStamp)
    
    dbg(rest)

    pointer=0
    while True:
        datHead = get(rest, pointer, 6, ">HHH")
        #print(datHead)
        pointer = pointer+6

        datXY = get(rest, pointer, 16, ">dd")
        pointer = pointer+16

        datExt = get(rest, pointer, 8, ">HHHH")
        pointer = pointer+8

        print(datHead, datXY, datExt)

        if pointer>len(rest):
            break
        

    #print(header)
    #print(rest)
    print("rest size = {} byte".format(len(rest)))

    return rest,header

def test(f):
    dat = readtdo(f)
    ret = analyze(dat)
    return ret

#print
#test(blank)
#test(oneLine)
test(oneLine2)
#test(twoLine2)
#test(oneLineAgain)
#test(oneTrack)
#test(oneTrackAgain)



#diff
#r1,h1 = test(oneLine)
#r2 = test(oneLine2)
"""
r1,h1 = test(oneLinesaveAs)
r2,h2 = test(oneLinesaveAsr1)
for i, (rr1,rr2) in enumerate(zip(h1, h2)):
    comp = rr1==rr2
    if not comp:
        print("[{0:04x}]\t{1}\t{2}\t{3}".format(i, comp, rr1, rr2))
"""
#for i, (rr1,rr2) in enumerate(zip(r1, r2)):
#    comp = rr1==rr2
#    print("[{0:04x}]\t{1}\t{2}\t{3}".format(i, comp, rr1, rr2))

#diff
"""
r1 = test(oneLine2)
r2s = test(twoLine2)
r2 = r2s[:142]
for i, (rr1,rr2) in enumerate(zip(r1, r2)):
    comp = rr1==rr2
    print("[{0:04d}]\t{1}\t{2}\t{3}".format(i, comp, rr1, rr2))
print()
r2 = r2s[142:]
for i, (rr1,rr2) in enumerate(zip(r1, r2)):
    comp = rr1==rr2
    print("[{0:04d}]\t{1}\t{2}\t{3}".format(i, comp, rr1, rr2))
"""
