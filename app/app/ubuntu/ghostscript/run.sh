service strace-docker restart

# convert ps to pdf
"ps2pdf test.ps"

# convert pdf to ps
"pdf2ps test.pdf"

# convert eps to png
docker run --rm -v "$PWD":/home/ -w /home/ mypdf2ps bash -c "sleep 1; gs  -dSAFER -dBATCH -dNOPAUSE -sDEVICE=png16m -dGraphicsAlphaBits=4 -sOutputFile=testimage_eps2png.png testimage.eps;"

# render at 300 dpi
docker run --rm -v "$PWD":/home/ -w /home/ mypdf2ps bash -c "sleep 1; gs -dSAFER -dBATCH -dNOPAUSE -sDEVICE=png16m -r300 -sOutputFile=testimage_300dpi.png testimage.eps;"

# render a figure in grayscale
docker run --rm -v "$PWD":/home/ -w /home/ mypdf2ps bash -c "sleep 1; gs -dSAFER -dBATCH -dNOPAUSE -sDEVICE=pnggray -sOutputFile=testimage_grayscale.png testimage.pdf;"
