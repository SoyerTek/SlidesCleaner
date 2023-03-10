import fitz
import sys

def uglyContains(A, B) -> bool:#is B contained in A?
    #find all lines that aren't in A and B
    linesB = []
    for b in B:
        if b in A:
            A.pop(A.index(b))
        else:
            linesB.append(b.strip().replace("\n", " ").split(" "))
    
    linesA = [a.strip().replace("\n", " ").split(" ") for a in A]

    for lineB in linesB:#if all words of a lineB are in a single lineA it can be removed
        possibleBlockA = [*range(len(linesA))]
        for word in lineB:
            for i in possibleBlockA:
                if word not in linesA[i]:
                    possibleBlockA.pop(possibleBlockA.index(i))

        if len(possibleBlockA) == 1:
            linesB.remove(lineB)
            linesA.pop(possibleBlockA[0])

    return len(linesB) == 0

args = sys.argv
flag_r = False #run with -r to see all indexes-1 of removed slides
flag_k = False#run with -r to see all indexes-1 of kept slides

if len(args) == 1:
    print("cleaner.py path_to_pdf -r(rimosee) -k(tenute)")
    quit(0)

if len(args) > 0:
    flag_r = "-r" in args
    flag_k = "-k" in args

slides = fitz.open(args[1])
clean = []
dup = []

prev_blocks = []#blocks(lines) of the prvious slide

for i in range(len(slides)):#in reverse check if the current slides content <= of the previous slide
    blocks = [block[4].strip() for block in slides[len(slides)-i-1].get_text("blocks")]
        
    if not uglyContains(prev_blocks, blocks): 
        clean.append(len(slides)-i-1)
    else: 
        dup.append(len(slides)-i-1)

    prev_blocks = blocks 


clean.sort()
dup.sort()

if flag_k: print("Slides kept: " + str(clean))
if flag_r: print("Slides removed: " + str(dup))

slides.select(clean)#keep only the clean slides

path = args[1].split("\\")[:-1]#path of the file - file name

newfile = args[1].split("\\")[-1].split(".")[0] + "_clean.pdf"
newfile = "\\".join(path) +"\\"+ newfile
print("Saved in: " + newfile)
print("Removed: " + str(len(dup)) + "/" + str(len(dup) + len(clean)))
slides.save(newfile)
slides.close()


