```
   ________________   __  ___            _     
  / ____/  _/ ____/  /  |/  /___ _____  (_)___ 
 / / __ / // /_     / /|_/ / __ `/ __ \/ / __ \
/ /_/ // // __/    / /  / / /_/ / / / / / /_/ /
\____/___/_/      /_/  /_/\__,_/_/ /_/_/ .___/ 
                                      /_/      
```

All-in-one Python 3 script for creating annoying spinning, bouncing, or strobing GIFs. Can also create 4 tiles (upper left & right, lower left & right) from an image, or just save the image as an 80x80 emote.

Suitable for Slack (or whatever else).

Code originally cobbled together in an hour. What started off as a silly 20 line script has turned into a 400 line beast. There may be bugs. And there's probably a better way to do some of this things this script does. So no lols.

Takes an image (file) as input, converts the image to a 80x80 thumbnail, spins, bounces, or strobes, applies speed and rotation, and saves the spinning or bouncing GIF as output (file). Can also create 4 tiles (upper left, right & lower left, right) from an image, or just save the image as an 80x80 emote.

If the image is smaller than 80x80, it will work but may look weird.

USAGE:

Only save image as emote: gif-manip.py -i [input file] -o [output file]

Do some stuff with the image:
gif-manip.py -i [input file] -o [output file] -s [speed] -d [direction] -t [type]

Where [speed] is an integer. The lower the number, the faster the spin. 50-100 makes a good clean spin or bounce.

Where [direction] is either c for clockwise rotation or cc for counterclockwise rotation.

Where [type] is one of:

bounce (bounces the image)\
spin-c (spins the image clockwise)\
spin-cc (spins the image counterclockwise)\
strobe-red (strobes the image red with direction supplied in -d)\
strobe-yellow (strobes the image yellow with direction supplied in -d)\
strobe-orange (strobes the image orange with direction supplied in -d)\
create-four (creates 4 tiles, upper left & right and lower left & right)

If you choose an option where direction and/or speed doesn't matter, those inputs are required but ignored.

Requires: https://github.com/python-pillow/Pillow
