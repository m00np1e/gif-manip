```
   ________________   __  ___            _     
  / ____/  _/ ____/  /  |/  /___ _____  (_)___ 
 / / __ / // /_     / /|_/ / __ `/ __ \/ / __ \
/ /_/ // // __/    / /  / / /_/ / / / / / /_/ /
\____/___/_/      /_/  /_/\__,_/_/ /_/_/ .___/ 
                                      /_/      
```

All-in-one Python 3 script for creating annoying spinning or bouncing GIFs. Can also create 4 tiles (upper left & right, lower left & right) from an image, or just save the image as an 80x80 emote.

Suitable for Slack (or whatever else).

Takes an image (file) as input, converts the image to a 80x80 thumbnail, spins or bounces, applies speed and rotation, and saves the spinning or bouncing GIF as output (file). Can also create 4 tiles (upper left, right & lower left, right) from an image, or just save the image as an 80x80 emote.

If the image is smaller than 80x80, it will work but may look weird.

USAGE:

Only save image as emote: gif-manip.py -i [input file] -o [output file]

Do some stuff with the image:
gif-manip.py -i [input file] -o [output file] -s [speed] -d [do-something]

Where [speed] is an integer. The lower the number, the faster the spin. 50-100 makes a good clean spin or bounce, 20 is turbo speed.

Where [do-something] is one of:

b - bounces the image\
c - spins the image clockwise\
cc - spins the image counterclockwise\
f - creates 4 tiles (upper left & right and lower left & right)\
e - just save as an emote

EXAMPLE:\
Create a clockwise spinning GIF from a JPG file:\
<br>
```gif-manip.py -i file.jpg -o spinning-gif.gif -s 50 -d c```

Requires: https://github.com/python-pillow/Pillow
