from sys import stdin

var = {}
VS = {}

def A(inst, j):
    if len(inst) != 4:
        print("Error in line ", {j+1+len(var)},": 3 operands required for type A")

    if (
        (inst[1] not in RS)
        or (inst[2] not in RS)
        or (inst[3] not in RS)
    ):
        
        print("Error in line ",{j+1+len(var)},": register not valid")
        
    if (inst[1] == "FLAGS") or (inst[2] == "FLAGS") or (inst[3] == "FLAGS"):
        print("Error in line ",{j+1+len(var)}," Type A instruction cannot be used for FLAG register")

    return True
    
def b(ntc, NOB):
    if ntc == 0:
        return "0" * NOB
    a = ""
    while ntc >= 2:
        a = str(ntc % 2) + a
        ntc = ntc // 2
    a = "1" + a
    BL = NOB - len(a)
    if BL >= 1:
        a = ("0" * BL) + a
    return a


def B(inst, j):
    if len(inst) != 3:
        print("Error in line", {j+1+len(var)},":  INCORRECT command for Type B")

    if (inst[1] in reg.keys()) and ("$" in inst[2]) and (int(inst[2][1:]) < 256):

        if inst[1] != "FLAGS":
            return True
        else:
            print("Error in line", {j+1+len(var)},": Cannot write to the flag register.")

    if inst[1] not in reg.keys():
        print("Error in line", {j+1+len(var)},": INVALID register")

    else:
        print("Error in line", {j+1+len(var)},":  INVALID immediate value")

def dec(SB):
    BN = str(SB)
    TR = 0
    n = len(BN)
    for i in range(n):
        if BN[n - i - 1] == "1":
            TR = TR + 2**i
        else:
            continue
    return TR

def C(inst, j):
    if not (len(inst) == 3):
        print("Error in line", {j+1+len(var)},": wrong command given for Type C")

    if inst[1] == "FLAGS":
        print("Error in line ", {j+1+len(var)},": Values cannot be written in FLAGS register.")

    if inst[1] in reg.keys() and inst[2] in reg.keys():
        return True
    if not (inst[1] in reg.keys()):
        print("Error in line no", {j+1+len(var)},": INVALID register")

    if not (inst[2] in reg.keys()):
        print("Error in line no", {j+1+len(var)},":", {inst[2]}," INVALID register")
    return False

def OR(a,b):
    return a | b

def cmp(a,b):
    if(a>b):
        return a
    else:
        return b

def bin(n):
     
    if n >= 1:
        bin(n // 2)
    print(n % 2, end = '')

def D(inst, j):
    if (
        (inst[1] in reg.keys())
        and (inst[2] in var.keys())
        and (inst[1] != "FLAGS")
    ):
        return True
    if not (len(inst) == 3):
        print("Error in line ", {j+1+len(var)},": INCORRECT command given for Type D")

    elif (inst[1] == "FLAGS") or not (inst[1] in reg.keys()):
        print("Error in line ", {j+1+len(var)}, {inst[1]}," INVALID value for reg")

    elif not (inst[2] in var.keys()):
        print("Error in line ", {j+1+len(var)},{inst[2]},": INVALID variable""")
    return False


def E(inst, j):
    if len(inst) != 2:
        print("Error in line", {j+1+len(var)},": memory address", ( {len(inst)-1} ),"specified")

    if inst[1] not in l.keys():
        if inst[1] in var.keys():
            print("Error in line", {j+1+len(var)},": Variable specified instead of label")

        print("Error in line", {j+1+len(var)},": LABEL DOES NOT EXIST")

    return True


flags = [False] * 2**2
l = {}
memory = [[0, 0]] * 2**8
out = []
INST = []

for i in range(256):
    memory.append([0, 0])

OPC = {
    "ls": "11001","xor": "11010","or": "11011","and": "11100","not": "11101", "cmp": "11110","jmp": "11111","jlt": "01100","jgt": "01101","je": "01111","hlt": "01010","add": "10000","sub": "10001","movI": "10010","movR": "10011","ld": "10100","st": "10101","mul": "10110","div": "10111","rs": "11000",

}
def add(a,b):
    return a+b

def sub(a,b):
    return a-b

def mul(a,b):
    return(a*b)

reg = {
    "FLAGS": "111","R0": "000","R1": "001","R2": "010","R3": "011","R4": "100","R5": "101", "R6": "110",

}
def xor(a,b):
    return a^b

def AND(a,b):
    return a & b  

def div(a,b):
    return a/b

RS = {
   "FLAGS": 0, "R0": 0,"R1": 0,"R2": 0,"R3": 0,"R4": 0,"R5": 0,"R6": 0,
 
}


def TA(inst, j):
    w = ""
    PWI = inst

    w = w+ OPC[PWI[0]]
    w = w+"00"
    if len(PWI) > 3:
        R1 = PWI[2]
        R2 = PWI[3]
        RRN = PWI[1]
        
        if "FLAGS" in PWI:
            print("Error in line", {j+1+len(var)},": cannot use FLAGS register for a Type A instruction.")
        elif (
            (R1 not in RS)
            or (R2 not in RS)
            or (RRN not in RS)
        ):
            print("Error in line", {j+1+len(var)},":Invalid register provided")

        w = w+ b(int(RRN[-1:]), 3)
        w = w+ b(int(R1[-1:]), 3)
        w = w+ b(int(R2[-1:]), 3)
        o1 = RS[R1]
        o2 = RS[R2]
        fin = 0

        if PWI[0] == "sub":
            fin = sub(o1,o2)
            if fin < 0:
                fin = 0
                flags[0] = True

        elif PWI[0] == "mul":
            fin = mul(o1 ,o2)

            RIB = b(fin, 16)
            if len(RIB) > 16:
                RIB = RIB[-16:]
                flags[0] = True
                fin = dec(RIB)

        elif PWI[0] == "add":
            fin = add(o1,o2)
            RIB = b(fin, 16)
            if len(RIB) > 16:
                RIB = RIB[-16:]
                flags[0] = True
                fin = dec(RIB)

        elif PWI[0] == "or":
            fin = OR(o1, o2)
        elif PWI[0] == "xor":
            fin = xor(o1,o2)
        elif PWI[0] == "and":
           fin = AND(o1, o2)
        RS[RRN] = fin
    else:
        print("Error in line", {j+1+len(var)},": Illegal type A instruction")


    return w


def TB(value, j):
    cl = "movI" if (value[0] == "mov") else value[0]
    imm = int(value[-1].split("$")[-1])
    if (imm > 255) or (imm < 0):
        print("Error in line", {j+1+len(var)},": The immediate value should lie between 0 and 255")

    REB = b(imm, 8)
    TS = str(b(RS[value[1]], 16))
    SB = "0" * imm

    if cl == "ls":
        TC = TS + SB
        awer = TC[-16:]
        awer = dec(awer)
    elif cl == "movI":
        awer = imm

    elif cl == "rs":
        TC = SB + TS
        awer = TC[:16]
        awer = dec(awer)

    RS[value[1]] = awer
    MBIN = OPC[cl] + reg[value[1]] + REB
    return MBIN
   
def TD(inst, j):
    if inst[1] == "FLAGS":
        print("Error in the line no", {j+1+len(var)},": load and store are invalid commands for the FLAGS reg.")

    elif inst[0] == "ld":
        RS[inst[1]] = VS[inst[2]]

    if inst[0] == "st":
        VS[inst[2]] = RS[inst[1]]
    return (
        OPC[inst[0]] + reg[inst[1]] + b(int(var[inst[2]]), 8)
    )

def TC(inst, j):

    if inst[0] == "cmp": 
        reg1 = RS[inst[1]]
        reg2 = RS[inst[2]]
        if reg1 > reg2:
            flags[-2] = True
        elif reg2 > reg1:
            flags[-3] = True
        else:
            flags[-1] = True
    elif inst[0] == "mov":   
        RS[inst[1]] = RS[inst[2]]
        return (
            OPC[inst[0] + "R"] + ("0" * 5) + reg[inst[1]] + reg[inst[2]]
        )
    elif inst[0] == "not": 

        ntf = b(RS[inst[2]], 16)

        oppp = ""
        for ch in range(len(ntf)):
            if ntf[ch] == "1":
                oppp = oppp + "0"
            else:
                oppp = oppp + "1"

        rev1 = dec(oppp)

        RS[inst[1]] = rev1
    elif inst[0] == "div":  
        q = (RS[inst[1]]) // (RS[inst[2]])
        r = RS[inst[1]] % RS[inst[2]]
        RS["R0"] = q
        RS["R1"] = r


    return OPC[inst[0]] + ("0" * 5) + reg[inst[1]] + reg[inst[2]]
def TE(inst, FC, j):
    w = ""
    ltj = -1
    w = w+ OPC[inst[0]]
    w = w+ "0" * 3

    if inst[1] not in l.keys():
        print("Error in the line no", {j+1+len(var)},": Illegal label has been specified")


    if inst[0] == "je":
        if FC[-1]:
            ltj = l[inst[1]] - len(VS)
    elif inst[0] == "jgt":
        if FC[-2]:
            ltj = l[inst[1]] - len(VS)
    elif inst[0] == "jlt":
        if FC[-3]:
            ltj = l[inst[1]] - len(VS)
    elif inst[0] == "jmp":
        ltj = l[inst[1]] - len(VS)

    w = w+ b(l[inst[1]] - len(VS), 8)

    return [ltj, w]

vd = "f"
hltr = "f"
tln = 0
for line in stdin:
    tln =tln + 1
    line = line.strip()
    if hltr!="f":

        if line != "":
            print("Error in the line no", {tln},": hlt must be the last instruction")
        break

    elif len(INST) == 256:
        print("Error in the line no", {tln},":Memory overflow has occured and the 256 lines limit has been reached!")


    elif line == "":
        continue

    elif vd =="f" and line[0:3] != "var":
        vd = "t"

    elif vd !="f" and line[0:3] == "var":
        print("Error in the line no", {tln},":Variables must be declared in the starting only.")

    if "hlt" in str(line):
        if ":" in line:
            LN = len(INST)

            splin = line.index(":")
            if " " in line[0:splin]:
                print("Error in the line no", {tln},": should have space between label name and : ")

            v3 = line[0:splin]
            if (
                v3 in OPC.keys()
                or (not (v3.replace("_", "").isalnum()))
                or (v3 == "var")
            ):  
                print("Error in the line no", {tln},": Improper name declaration for label")

            l[line[0:splin]] = LN
            INST.append((line[splin + 1:]).strip())

        elif "hlt" != line:
            print("Error in the line no", {tln},":  Improper use of hlt statement")

        else:
            INST.append(line)

        hltr = "t"
        continue

    if ":" in line:
        LN = len(INST)
        splin = line.index(":")
        if " " in line[0:splin]:
            print("Error in the line no", {tln},":  should not have spaces between label name and :")

        v3 = line[0:splin]
        if (
            v3 in OPC.keys()
            or (not (v3.replace("_", "").isalnum()))
            or (v3 == "var")
        ):  
            print("Error in the line no", {tln},"Improper name declaration of label")


        l[line[0:splin]] = LN
        INST.append((line[splin + 1:]).strip())
        continue

    INST.append(line)

if "hlt" not in INST[-1]:
    print("Missing/impropper use of Hlt instruction")

cn = 0
for i in INST:
    if "var" not in i:
        break
    cn = cn+ 1
NL = len(INST) - cn

for i in range(cn):
    k = (INST[i]).split()

    if len(k) != 2:
        print("Error in the line no", {i+1},"Invalid syntax of variable declaration")

    elif (
        (k[-1] in OPC.keys())
        or (not (k[-1].replace("_", "").isalnum()))
        or (k[-1] == "var")
    ):
        print("Error in the line no", {i+1},"Variables not properly declaraed")


    var[k[1]] = NL + i
    VS[k[1]] = 0


RI = INST[cn:]
j = 0
while j < len(RI):

    cfs = flags[::]

    PI = -1
    if True in cfs:
        PI = cfs.index(True)
        flags[PI] = False
        PI = 3 - PI

    elif PI != -1:
        RS["FLAGS"] = 2 ** PI
    else:
        RS["FLAGS"] = 0

    i = RI[j]
    i = i.split()
    CO = i[0]


    if CO == "mov":
        if "$" in i[-1] and B(i, j):
            out.append(TB(i, j))
        elif C(i, j):
            out.append(TC(i, j))
    elif (
        CO == "add" or CO == "sub"or CO == "mul" or CO == "xor" or CO == "or" or CO == "and"
    ) and A(i, j):
        out.append(TA(i, j))
    elif (CO == "ld" or CO == "st") and D(i, j):
        out.append(TD(i, j))
    elif (CO == "rs" or CO == "ls") and B(i, j):
        out.append(TB(i, j))

    elif (CO == "div" or CO == "not" or CO == "cmp") and C(i, j):
        out.append(TC(i, j))

    elif CO == "hlt":
        out.append(OPC[CO] + ("0" * 11))
    elif (
        (CO == "jmp") or (CO == "jlt") or (CO == "jgt")
        or (CO == "je")
            ) and E(i, j):
        fin = TE(i, cfs, j)
        if fin[0] == -1:
            out.append(fin[1])
        else:
            out.append(fin[1])

    else:
        print("Wrong OpCode provided at line", {j+1+len(var)})

    j = j+ 1

for i in out:
    print(i)