# xva2img
Extract IMG disk images from XVA files

USAGE:
xva2img.py [XVA FILE]

Will extract all disk images contained within the XVA file into the current directory.
IMG files are created with the filename "[XVA]-n.img", where n is a number incremented from 0.

xva2img-extract.py is an alternate version that will untar the XVA into the current directory before rebuilding the IMG files.
