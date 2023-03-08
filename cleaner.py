import fitz
import sys

def contained(A, B) -> bool:
    for x in B:
        if x not in A:
            return False
    return True

def uglyContains(A, B) -> bool:#B is contained in A?
    linesA = []
    linesB = []
    for a in A:
        linesA.append(a.strip().replace("\n", " ").split(" "))
    for b in B:
        if b in A:
            A.pop(A.index(b))
        else:
            linesB.append(b.strip().replace("\n", " ").split(" "))

        for lineB in linesB:
            possibleBlockA = [*range(len(linesA))]
            for word in lineB:
                for i in possibleBlockA:
                    if word not in linesA[i]:
                        possibleBlockA.pop(possibleBlockA.index(i))

            if len(possibleBlockA) == 1:
                linesB.remove(lineB)

    return len(linesB) == 0

    

def slimBlock(A) :
    return [A[4].strip(), A[6]]


args = sys.argv
flag_r = False
flag_k = False

if len(args) == 1:
    print("cleaner.py path -r(rimosee) -k(tenute)")
    quit(0)

if len(args) > 0:
    flag_r = "-r" in args
    flag_k = "-r" in args

slides = fitz.open(args[1])
clean = []
dup = []

prev_blocks = []
for i in range(len(slides)):
    blocks = []
    for block in slides[len(slides)-i-1].get_text("blocks"):
        blocks.append(block[4].strip())

    


    if not uglyContains(prev_blocks, blocks) : 
        #print(len(slides)-i-1)
        clean.append(len(slides)-i-1)
    else: dup.append(len(slides)-i-1)
    prev_blocks = blocks 

clean.sort()
dup.sort()
if flag_k:
    print("Slides kept: " + str(clean))
if flag_r:
    print("Slides removed: " + str(dup))
slides.select(clean)

path = args[1].split("\\")[:-1]

newfile = args[1].split("\\")[-1].split(".")[0] + "_clean.pdf"
newfile = "\\".join(path) +"\\"+ newfile
print("Saved in: " + newfile)
slides.save(newfile)
slides.close()


