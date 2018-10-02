import struct

class color:
    OK = '\033[92m'
    WARN = '\033[93m'
    NG = '\033[91m'
    END_CODE = '\033[0m'

def dbg(inDat):
    print("="*25)
    print("datasize={}".format(len(inDat)))
    print(inDat)
    print("="*25)
    print()

def getHex(inDat):
    _d = ["{0:02x}".format(x) for x in inDat]
    return _d

"""
def get(inBin, start, datlen, fmt):
    printHex(inBin[start:start+datlen])
    x = struct.unpack(fmt, inBin[start:start+datlen])
    if len(x)==1:
        return x[0]
    else:
        return x
"""

class TdoElementBase:
    def __init__(self, rawDat):
        self.rawData = rawDat
        self.parseHead()
    
    def parseHead(self):
        #self.datType, self.Unknown1, self.datNum = struct.unpack(">HHH", self.rawData[0:6])
        self.datType, self.datNum = struct.unpack(">HI", self.rawData[0:6])

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
        #rtn = rtn + "Type={}".format(self.datType)
        #rtn = rtn + "\nDatNum={}".format(self.datNum)
        rtn = rtn + "X={} Y={}".format(self.x, self.y)
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
        #rtn = rtn + "Type={}".format(self.datType)
        #rtn = rtn + "\nDatNum={}".format(self.datNum)
        rtn = rtn + "startPoint={} endPoint={}".format(self.startPoint, self.endPoint)

        return rtn

class TdoArc(TdoElementBase):
    def __init__(self, rawDat):
        super().__init__(rawDat)
        self.check(2)
        self.parse()
    
    def parse(self):
        #print("body size={}".format(len(self.getBody())))
        self.Unknown1 = struct.unpack(">H", self.getBody()[0:2])
        self.radius = struct.unpack(">d", self.getBody()[2:10])
        self.x, self.y = struct.unpack(">dd", self.getBody()[10:26])
        self.a, self.b, self.c = struct.unpack(">III", self.getBody()[26:38])
        self.Unknown2 = self.getBody()[38:]
    
    def __str__(self):
        rtn = ""
        #rtn = rtn + "Type={}".format(self.datType)
        rtn = rtn + "\nDatNum={}".format(self.datNum)
        rtn = rtn + "\nRaius={}".format(self.radius)
        rtn = rtn + "\nx={} y={}".format(self.x, self.y)
        rtn = rtn + "\na={} b={} c={}".format(self.a, self.b, self.c)
        #rtn = rtn + "\nBody={}".format(getHex(self.Unknown2))
        #rtn = rtn + "\n(Raw Data is {} byte)".format(len(self.rawData))

        return rtn

class TdoTrack(TdoElementBase):
    def __init__(self, rawDat):
        super().__init__(rawDat)
        self.check(4)
        self.parse()
    
    def parse(self):
        #print("body size={}".format(len(self.getBody())))
        self.Unknown1, self.Unknown2 = struct.unpack(">II", self.getBody()[0:8])
        self.trackLength = struct.unpack(">d", self.getBody()[8:16])[0]
        self.Unknown3= struct.unpack(">30H", self.getBody()[16:76])
        self.Unknown4 = self.getBody()[76:]
    
    def __str__(self):
        rtn = ""
        #rtn = rtn + "Type={}".format(self.datType)
        #rtn = rtn + "\nDatNum={}".format(self.datNum)

        rtn = rtn + "?1={} ?2={}".format(self.Unknown1, self.Unknown2)
        rtn = rtn + "\ntrackLength={}".format(self.trackLength)
        rtn = rtn + "\n?3={}".format(self.Unknown3)
        rtn = rtn + "\n?4={}".format(getHex(self.Unknown4))
        #rtn = rtn + "\n(Raw Data is {} byte)".format(len(self.rawData))

        return rtn

class TdoPosition(TdoElementBase):
    def __init__(self, rawDat):
        super().__init__(rawDat)
        self.check(0x0b)
        self.parse()
    
    def parse(self):
        self.Unknown1 = struct.unpack(">HHHH", self.getBody()[0:8])
        self.pos = struct.unpack(">dd", self.getBody()[8:24])
        self.Unknown2 = struct.unpack(">10H", self.getBody()[24:44])
        e1 = self.Unknown2[-1]
        if e1>0:
            self.Unknown22 = struct.unpack(">2L", self.getBody()[44:44+e1*8])
        else:
            self.Unknown22 = None
        self.Unknown3 = self.getBody()[44+e1*8:]
        self.Unknown4 = None
    
    def __str__(self):
        rtn = ""
        rtn = rtn + "Type={}".format(self.datType)
        rtn = rtn + "\nDatNum={}".format(self.datNum)

        rtn = rtn + "\n?1={}".format(self.Unknown1)
        rtn = rtn + "\npos={} {}".format(self.pos[0], self.pos[1])
        rtn = rtn + "\n?2={}".format(self.Unknown2)
        rtn = rtn + "\n?22={}".format(self.Unknown22)
        rtn = rtn + "\n?3={}".format(getHex(self.Unknown3))
        #rtn = rtn + "\n?4(Extra)={}".format(getHex(self.Unknown4))
        rtn = rtn + "\n?4(Extra)={}".format(self.Unknown4)
        #rtn = rtn + "\n(Raw Data is {} byte)".format(len(self.rawData))

        return rtn
    
    def isEnd(self):
        if len(self.Unknown3)==0:
            return 2
        
        rtn = True
        for x in self.Unknown3:
            rtn = rtn and (x == 0x00)
        
        if rtn:
            return 0
        else:
            return 1
    
    def addExtra(self, addDat):
        self.rawDara = self.rawData + addDat
        self.Unknown4 = struct.unpack(">{}H".format(int(len(addDat)/2)), addDat)


class Tdo:
    def __init__(self, filename):
        self.filename = filename
        self.headerSize = 1244
        self.readAll()
        self.readFileHeader()
        
        self.Points = list()
        self.Lines = list()
        self.Arcs = list()
        self.Tracks = list()
        self.Positions = list()
        self.Others = list()
        self.parseBody()
        
    
    def readAll(self):
        self.datAll = open(self.filename, "rb").read()
    
    def readFileHeader(self):
        self.header = self.datAll[:self.headerSize]

        self.fileType = self.header[:6]
        #dbg(fileType)

        self.timeStamp = self.header[6:30]
        #dbg(timeStamp)
    
        self.body = self.datAll[self.headerSize:]
    
    def parseBody(self):
        pointer=0
        while True:
            t = struct.unpack(">H", self.body[pointer:pointer+2])[0]
            print("Reading type", t)
            if t==1:
                self.Points.append(TdoPoint(self.body[pointer:pointer+30]))
                pointer = pointer + 30
            elif t==2:
                self.Arcs.append(TdoArc(self.body[pointer:]))
                #pointer = pointer + 22
                print("Arc is now under construction.")
                break
            elif t==3:
                self.Lines.append(TdoLine(self.body[pointer:pointer+22]))
                pointer = pointer + 22
            elif t==4:
                self.Tracks.append(TdoTrack(self.body[pointer:pointer+214]))
                pointer = pointer + 214
                #print("Track is now under construction.")
                #break
            elif t==0x0b:
                self.Positions.append(TdoPosition(self.body[pointer:pointer+58]))
                pointer = pointer + 58
                if self.Positions[-1].isEnd()==1:
                    self.Positions[-1].addExtra(self.body[pointer:pointer+68])
                    pointer = pointer +68
                elif self.Positions[-1].isEnd()==2:
                    self.Positions[-1].addExtra(self.body[pointer:pointer+124])
                    pointer = pointer +124
                    #break
            else:
                print(color.NG + "Unknown Type [{}]".format(t) + color.END_CODE)
                print(getHex(self.body[pointer:pointer+10]))
                self.Others.append(TdoElementBase(self.body[pointer:]))
                break
            
            if pointer >= len(self.body):
                break
    
    def __str__(self):
        rtn = ""
        rtn = rtn + "\n========== TDO object =========="
        rtn = rtn + "\n----- Points -----"
        if len(self.Points)==0:
            rtn = rtn + "\n(no Points)"
        for p in self.Points:
            rtn = rtn + "\n[Point {0}]".format(p.datNum)
            rtn = rtn + "\n" + p.__str__()
        rtn = rtn + "\n----- Lines -----"
        if len(self.Lines)==0:
            rtn = rtn + "\n(no Lines)"
        for p in self.Lines:
            rtn = rtn + "\n[Line {0}]".format(p.datNum)
            rtn = rtn + "\n" + p.__str__()
        rtn = rtn + "\n----- Arcs -----"
        if len(self.Arcs)==0:
            rtn = rtn + "\n(no Arcs)"
        for p in self.Arcs:
            rtn = rtn + "\n[Arc {0}]".format(p.datNum)
            rtn = rtn + "\n" + p.__str__()
        rtn = rtn + "\n----- Tracks -----"
        if len(self.Tracks)==0:
            rtn = rtn + "\n(no Tracks)"
        for p in self.Tracks:
            rtn = rtn + "\n[Track {0}]".format(p.datNum)
            rtn = rtn + "\n" + p.__str__()
        rtn = rtn + "\n----- Positions -----"
        if len(self.Positions)==0:
            rtn = rtn + "\n(no Positions)"
        for p in self.Positions:
            rtn = rtn + "\n[Position {0}]".format(p.datNum)
            rtn = rtn + "\n" + p.__str__()
        rtn = rtn + "\n----- Others -----"
        if len(self.Others)==0:
            rtn = rtn + "\n(no Others)"
        for i,p in enumerate(self.Others):
            rtn = rtn + "\n[Other {0}]".format(i)
            rtn = rtn + "\n" + p.__str__()
        return rtn+"\n========================================"

if __name__=="__main__":
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

    arc = "Overlays/tweLine_oneArc.tdo"

    oneTrackOnly = "Overlays/oneTrackOnly.tdo"
    twoTracksOnly = "Overlays/twoTracks_fromodr.tdo"

    twoTracksPos = "Overlays/twoTracks_fromodr_lane0.tdo"
    
    """
    t1 = Tdo(oneLine)
    print(t1)

    t2 = Tdo(oneLine2)
    print(t2)

    t3 = Tdo(twoLine2)
    print(t3)
    """

    #a = Tdo(arc)
    #print(a)

    #track = Tdo(twoTracksOnly)
    track = Tdo(twoTracksPos)
    print(track)

    exit()

