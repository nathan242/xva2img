import sys
import os
import tarfile

def help():
    sys.stderr.write("Convert XVA file to IMG.\n")
    sys.stderr.write("USAGE: \n")
    sys.stderr.write(sys.argv[0]+" [XVA FILE]\n")

def build_img(source, files, outfilename):
    # Does output file already exist?
    if os.path.exists(outfilename):
        sys.stderr.write("ERROR: Output file already exists! ("+os.path.basename(outfilename)+")\n")
        sys.exit(5)

    # Create the output file
    try:
        outfile = open(outfilename, "wb")
    except:
        sys.stderr.write("ERROR: Cannot create output file! ("+os.path.basename(outfilename)+")\n")
        sys.exit(6)

    namepathpos = files[0].find("/")+1

    files_total = int(files[len(files)-1][namepathpos:])
    files_count = 0

    print "IMAGE: "+os.path.basename(outfilename)

    for f in files:
        while int(f[namepathpos:]) != files_count:
            outfile.write("\0"*1048576)
            files_count += 1
        sys.stdout.write("\rWriting piece "+str(files_count)+"/"+str(files_total))
        piece = source.extractfile(f)
        outfile.write(piece.read())
        piece.close()
        files_count += 1

    sys.stdout.write("\nDone!\n")
    outfile.close()

if len(sys.argv) < 2:
    sys.stderr.write("ERROR: Please specify an input file!\n\n")
    help()
    sys.exit(1)

# Does the input file exist?
if not os.path.isfile(sys.argv[1]):
    sys.stderr.write("ERROR: Input file does not exist!\n")
    sys.exit(2)

# See if input file is a TAR archive
try:
    if not tarfile.is_tarfile(sys.argv[1]):
        sys.stderr.write("ERROR: Input file is not TAR!\n")
        sys.exit(3)
except:
    sys.stderr.write("ERROR: Cannot open input file!\n")
    sys.exit(4)

# Open the input file
print "Reading data from "+sys.argv[1]+"..."
try:
    infile = tarfile.open(sys.argv[1], "r")
except:
    sys.stderr.write("ERROR: Cannot open input file!\n")
    sys.exit(4)

# Read contents
contents = infile.getnames()

# Get root directory names - those aren't marked as dirs in the TAR file so we have to look for "/"
rootdirs = []
for i in contents:
    if "/" in i:
        name = i[:i.find("/")]
        if name not in rootdirs:
            rootdirs.append(name)

# Build IMG
img_count = 0
for i in rootdirs:
    files = []
    for f in contents:
        if f.startswith(i+"/") and f[f.find("/")+1:].isdigit():
            files.append(f)
    files.sort()
    build_img(infile, files, sys.argv[1]+"-"+str(img_count)+".img")
    img_count += 1

