import sys
import os
import tarfile

def help():
    sys.stderr.write("Convert XVA file to IMG.\n")
    sys.stderr.write("USAGE: \n")
    sys.stderr.write(sys.argv[0]+" [XVA FILE]\n")

def build_img(source, outfilename):
    # Does output file already exist?
    if os.path.exists(outfilename):
        sys.stderr.write("ERROR: Output file already exists! ("+os.path.basename(outfilename)+")\n")
        sys.exit(7)

    # Create the output file
    try:
        outfile = open(outfilename, "wb")
    except:
        sys.stderr.write("ERROR: Cannot create output file! ("+os.path.basename(outfilename)+")\n")
        sys.exit(8)

    # Get source files
    pieces = []
    for i in os.listdir(source):
        if i.isdigit():
            pieces.append(i)

    pieces.sort()
    pieces_total = int(pieces[len(pieces)-1])
    pieces_count = 0

    print "IMAGE: "+os.path.basename(outfilename)

    for p in pieces:
        while int(p) != pieces_count:
            outfile.write("\0"*1048576)
            pieces_count += 1
        sys.stdout.write("\rWriting piece "+str(pieces_count)+"/"+str(pieces_total))
        piece = open(source+"/"+p, "rb")
        outfile.write(piece.read())
        piece.close()
        pieces_count += 1

    sys.stdout.write("\nDone!\n")
    outfile.close()



if len(sys.argv) < 2:
    sys.stderr.write("ERROR: Please specify an input file!\n\n")
    help()
    sys.exit(1)

# See if input file is a TAR archive
try:
    if tarfile.is_tarfile(sys.argv[1]) == False:
        sys.stderr.write("ERROR: Input file is not TAR!\n")
        sys.exit(2)
except:
    sys.stderr.write("ERROR: Cannot open input file!\n")
    sys.exit(3)

# Create temporary directory
tempdir = sys.argv[1]+".TEMP"
# Does it already exist?
if os.path.isdir(tempdir):
    sys.stderr.write("ERROR: Temporary directory already exists!\n")
    sys.exit(4)

try:
    os.mkdir(tempdir)
except:
    sys.stderr.write("ERROR: Cannot create temporary directory!\n")
    sys.exit(5)

# Open the input file
try:
    infile = tarfile.open(sys.argv[1], "r")
except:
    sys.stderr.write("ERROR: Cannot open input file!\n")
    sys.exit(3)

# Extract contents
print "Extracting "+sys.argv[1]+"..."
try:
    infile.extractall(tempdir+"/")
except:
    sys.stderr.write("ERROR: Failed to extract files!\n")
    sys.exit(6)

# Grant read to all files
for root, dirs, files in os.walk(tempdir):
    for d in dirs:
        os.chmod(os.path.join(root, d), 0700)
    for f in files:
        os.chmod(os.path.join(root, f), 0600)

# Build IMG
img_count = 0
for i in os.listdir(tempdir):
    if os.path.isdir(tempdir+"/"+i):
        build_img(tempdir+"/"+i+"/", sys.argv[1]+"-"+str(img_count)+".img")
        img_count += 1

