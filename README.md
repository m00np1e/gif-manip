```
   ________________   __  ___            _     
  / ____/  _/ ____/  /  |/  /___ _____  (_)___ 
 / / __ / // /_     / /|_/ / __ `/ __ \/ / __ \
/ /_/ // // __/    / /  / / /_/ / / / / / /_/ /
\____/___/_/      /_/  /_/\__,_/_/ /_/_/ .___/ 
                                      /_/      
```

An all-in-one Python 3 script for creating annoying spinning, flipping, or strobing GIFs.

Suitable for Slack (or whatever else).

Code cobbled together in an hour. There may be bugs. And there's probably a better way to do some of this things this script does. So no lols.

Takes an image (file) as input, converts the image to a 512x512 thumbnail, spins, flips, or strobes, applies speed and rotation, and saves the spinning or flipping GIF as output (file).

If the image is smaller than 512x512, it will work but may look weird.

USAGE:

gif-manip.py -i [input file] -o [output file] -s [speed] -d [direction] -t [type]

Where [speed] is an integer. The lower the number, the faster the spin. 150-175 makes a good clean spin or flip.

Where [direction] is either c for clockwise rotation or cc for counterclockwise rotation.

Where [type] is one of:

flip (flips the image)\
spin-c (spins the image clockwise)\
spin-cc (spins the image counterclockwise)\
strobe-red (strobes the image red with direction supplied in -d)\
strobe-yellow (strobes the image yellow with direction supplied in -d)\
strobe-orange (strobes the image orange with direction supplied in -d)

Requires: https://github.com/python-pillow/Pillow
