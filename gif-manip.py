#!/usr/bin/env python3

from PIL import Image, ImageOps
from sys import exit
import argparse

# python 3 script to convert an image to a 80x80
# spinning, bouncing, or strobing gif
# also will create 4 cropped tiles
# or just save the image as an 80x80 .gif file
# suitable for use with custom emotes in slack
# Ken Mininger, kmininger@us.ibm.com
# June 2021

# usage
usage = '''
        Takes an image and resizes to 80x80 (maintaining aspect ratio and quality),
        applies speed, performs the requested action: bounce, spin (clockwise or counterclockwise),
		strobe red, yellow, or orange (clockwise or counterclockwise), or create 4 tiles, and saves as an
		animated .gif file or set of 4 tile files.
		Input and output file are required. Other arguments are optional and if not supplied,
		will save the image as an 80x80 .gif file.
		If create-four is used for -t, all other arguments (except input and output file(s))
		will be ignored.
        If image is smaller than 80x80, it will not resize but will perform the requested action as-is.
		The -d argument is ignored when bouncing.

        EXAMPLE (spinning .gif): gif-manip.py -i test.jpg -o test.gif -t spin-c -s 50 -d c
        EXAMPLE (save emote only): gif-manip.py -i test.jpg -o test.gif
        '''


# arguments
def check_args():
    parser = argparse.ArgumentParser(
        description="Create 4 tiles, spin, bounce, or strobe that GIF!\n\nOnly -i and -o are "
                    "required.\nIf "
                    "no other options provided, will just save the file as an 80x80 .gif file.", prog="GIF-Manip",
        usage="%(prog)s "
              "[options]")
    parser.add_argument("-i", help="Input file - The file you want to create 4 tiles from, spin, bounce, or strobe",
                        required=True)
    parser.add_argument("-o", help="Output file - Must specify .gif extension or .jpg for tiles", required=True)
    parser.add_argument("-s", help="Spin speed", type=int)
    parser.add_argument("-t", help="Create tiles, spin, bounce, or strobe (bounce, spin-c, spin-cc, strobe-red, "
                                   "strobe-orange, "
                                   "strobe-yellow, create-four)")
    parser.add_argument("-d", help="Direction (c or cc)")
    args1 = parser.parse_args()
    return (args1)


# check that arguments are supplied and just save as an emote if necessary
def error_check(infile, spinfile, speed, type, dir):
    if not infile:
        logo()
        print("Input file not provided: use -i")
        exit(1)
    if not spinfile:
        logo()
        print("Output file not provided: use -o")
        exit(1)
    if not speed or not type or not dir:
        create_emote(infile, spinfile)
        exit(1)


# what are we going to do with this image
def check_type(type):
    if type == "strobe-red":
        return type
    elif type == "strobe-orange":
        return type
    elif type == "strobe-yellow":
        return type
    elif type == "spin-cc":
        return type
    elif type == "bounce":
        return type
    elif type == "create-four":
        return type
    elif type == "spin-c":
        return type
    else:
        return type


# open file and get image
def open_file(option, what):
    try:
        logo()
        if what == "bounce":
            doing = "bouncing."
        elif (what == "spin-c") or (what == "spin-cc"):
            doing = "spinning."
        elif what == "create-four":
            doing = "tile creation."
        elif what == "strobe-red" or what == "strobe-yellow" or what == "strobe-orange":
            doing = "strobing."
        else:
            doing = "emote creating."
        image_open = Image.open(option, 'r')
        print("Opened", option, "for", doing)
        if (image_open.height < 80) or (image_open.width < 80):
            print("WARNING: Image smaller than 80x80. The", (doing[:-1]), "may look weird.")
        if image_open.format == "PNG":
            bg_color = (255, 255, 255)
            rgb_img = rem_trans(image_open, bg_color)
            return (rgb_img)
        else:
            image_open = image_open.convert("P", palette=Image.ADAPTIVE, colors=256)
            return image_open
    except IOError:
        print("Error: Cannot open input file for reading or input file not found.")
    exit(1)


# figure out what to do
# probably a better way to do this
def get_manip(picture, what_do, things):
    if what_do == "spin-c":
        spin_clockwise(picture, (things.i), (things.s), (things.o))
    elif what_do == "spin-cc":
        spin_counterclockwise(picture, (things.i), (things.s), (things.o))
    elif what_do == "create-four":
        create_four(picture, (things.o))
    elif what_do == "bounce":
        bouncy(picture, (things.i), (things.s), (things.o))
    elif what_do == "strobe-red" and (things.d) == "c":
        strobe_spin_clockwise(picture, (things.i), (things.s), (things.o), "red")
    elif what_do == "strobe-red" and (things.d) == "cc":
        strobe_spin_counterclockwise(picture, (things.i), (things.s), (things.o), "red")
    elif what_do == "strobe-orange" and (things.d) == "c":
        strobe_spin_clockwise(picture, (things.i), (things.s), (things.o), "orange")
    elif what_do == "strobe-orange" and (things.d) == "cc":
        strobe_spin_counterclockwise(picture, (things.i), (things.s), (things.o), "orange")
    elif what_do == "strobe-yellow" and (things.d) == "c":
        strobe_spin_clockwise(picture, (things.i), (things.s), (things.o), "yellow")
    elif what_do == "strobe-yellow" and (things.d) == "cc":
        strobe_spin_counterclockwise(picture, (things.i), (things.s), (things.o), "yellow")
    else:
        print("I don't know what you're trying to do.")
        exit(1)


# logos
def logo():
    print("""\
   ________________   __  ___            _     
  / ____/  _/ ____/  /  |/  /___ _____  (_)___ 
 / / __ / // /_     / /|_/ / __ `/ __ \/ / __ \\
/ /_/ // // __/    / /  / / /_/ / / / / / /_/ /
\____/___/_/      /_/  /_/\__,_/_/ /_/_/ .___/ 
                                      /_/      """)


def logo_spin():
    print("""\
   _____       _          __  __          __     ________________
  / ___/____  (_)___     / /_/ /_  ____ _/ /_   / ____/  _/ ____/
  \__ \/ __ \/ / __ \   / __/ __ \/ __ `/ __/  / / __ / // /_    
 ___/ / /_/ / / / / /  / /_/ / / / /_/ / /_   / /_/ // // __/    
/____/ .___/_/_/ /_/   \__/_/ /_/\__,_/\__/   \____/___/_/       
    /_/                                                          """)


def logo_strobe():
    print("""\
   _____ __             __            __  __          __     ________________
  / ___// /__________  / /_  ___     / /_/ /_  ____ _/ /_   / ____/  _/ ____/
  \__ \/ __/ ___/ __ \/ __ \/ _ \   / __/ __ \/ __ `/ __/  / / __ / // /_    
 ___/ / /_/ /  / /_/ / /_/ /  __/  / /_/ / / / /_/ / /_   / /_/ // // __/    
/____/\__/_/   \____/_.___/\___/   \__/_/ /_/\__,_/\__/   \____/___/_/       
                                                                             """)


def logo_bounce():
    print("""\
    ____                                 __  __          __     ________________   
   / __ )____  __  ______  ________     / /_/ /_  ____ _/ /_   / ____/  _/ ____/   
  / __  / __ \/ / / / __ \/ ___/ _ \   / __/ __ \/ __ `/ __/  / / __ / // /_       
 / /_/ / /_/ / /_/ / / / / /__/  __/  / /_/ / / / /_/ / /_   / /_/ // // __/       
/_____/\____/\__,_/_/ /_/\___/\___/   \__/_/ /_/\__,_/\__/   \____/___/_/          
                                                                             """)


def logo_tiles():
    print("""\
   ______                __          __ __     __  _ __         
  / ____/_______  ____ _/ /____     / // /    / /_(_) /__  _____
 / /   / ___/ _ \/ __ `/ __/ _ \   / // /_   / __/ / / _ \/ ___/
/ /___/ /  /  __/ /_/ / /_/  __/  /__  __/  / /_/ / /  __(__  ) 
\____/_/   \___/\__,_/\__/\___/     /_/     \__/_/_/\___/____/  
                                                                """)


# resize image to 80x80, maintaining aspect ratio and quality
# resize to anything smaller than this and there is quality loss
# if the image is smaller than 80x80, it will not resize
# but will perform the requested action (may look weird)
def resize_image(r_image):
    img_height = 80
    img_width = 80
    if (r_image.height <= img_height) or (r_image.width <= img_width):
        return r_image
    if (r_image.width != img_width) & (r_image.height != img_height):
        r2_image = ImageOps.fit(r_image, [img_width, img_height], Image.ANTIALIAS)
        return r2_image
    else:
        return r_image


# bounce the image
def bounce(b_image):
    images = []
    degrees = range(1, 360, 40)
    degrees2 = range(360, 1, -40)
    for deg in degrees:
        trans_img = b_image.rotate(deg)
        images.append(trans_img)
    for deg2 in degrees2:
        trans_img = b_image.rotate(deg2)
        images.append(trans_img)
    return images


# rotate the image clockwise
def clockwise(c_image):
    images = []
    degrees = -1
    while degrees >= -360:
        trans_img = c_image.rotate(degrees)
        images.append(trans_img)
        degrees -= 20
    return images


# rotate the image counterclockwise
def counterclockwise(cc_image):
    images = []
    degrees = 1
    while degrees <= 360:
        trans_img = cc_image.rotate(degrees)
        images.append(trans_img)
        degrees += 20
    return images


# create-four tiles
def create_four(f_image, tilefile):
    logo_tiles()
    width, height = f_image.size
    q1 = int(width / 2)
    q2 = int(height / 2)
    tiled_jpg = f_image.convert("RGB")
    crop_lr = (q1, q2, width, height)
    crop_ll = (0, q2, q1, height)
    crop_ur = (q1, 0, width, q2)
    crop_ul = (0, 0, q1, q2)
    region_lr = tiled_jpg.crop(crop_lr)
    region_ll = tiled_jpg.crop(crop_ll)
    region_ur = tiled_jpg.crop(crop_ur)
    region_ul = tiled_jpg.crop(crop_ul)
    try:
        region_lr.save("lr_" + tilefile, "jpeg")
        region_ll.save("ll_" + tilefile, "jpeg")
        region_ur.save("ur_" + tilefile, "jpeg")
        region_ul.save("ul_" + tilefile, "jpeg")
        print("Tiles created. Filenames prepended with lr_, ll_, ur_, ul_")
    except IOError:
        print("Error: Cannot open output file(s)")
        exit(1)


# spin the image clockwise and save
def spin_clockwise(image, infile, speed, spinfile):
    logo_spin()
    print("Spinning", infile, "clockwise with speed =", str(speed) + ".")
    resized = resize_image(image)
    clockwised = clockwise(resized)
    try:
        clockwised[0].save(spinfile, 'GIF', save_all=True, append_images=clockwised[1:],
                           duration=speed,
                           loop=0,
                           optimize=True, quality=100)
        print("Spinning GIF created:", spinfile)
    except IOError:
        print("Error: Cannot open output file for spinning.")
        exit(1)


# spin the image counterclockwise and save
def spin_counterclockwise(image, infile, speed, spinfile):
    logo_spin()
    print("Spinning", infile, "counterclockwise with speed =", str(speed) + ".")
    resized = resize_image(image)
    ccwised = counterclockwise(resized)
    try:
        ccwised[0].save(spinfile, 'GIF', save_all=True, append_images=ccwised[1:], duration=speed,
                        loop=0,
                        optimize=True, quality=100)
        print("Spinning GIF created: ", spinfile)
    except IOError:
        print("Error: Cannot open output file for spinning.")
        exit(1)


# strobe the image clockwise and save
def strobe_spin_clockwise(image, infile, speed, spinfile, flash):
    resized = resize_image(image)
    clockwised = clockwise_strobe(resized, flash)
    logo_strobe()
    print("Spinning", infile, "clockwise with speed =", speed, "and strobing", flash + ".")
    try:
        clockwised[0].save(spinfile, 'GIF', save_all=True, append_images=clockwised[1:],
                           duration=speed,
                           loop=0,
                           optimize=True, quality=100)
        print("Spinning GIF created:", spinfile)
    except IOError:
        print("Error: Cannot open output file for strobing.")
        exit(1)


# strobe the image counterclockwise and save
def strobe_spin_counterclockwise(image, infile, speed, spinfile, flash):
    resized = resize_image(image)
    ccwised = counterclockwise_strobe(resized, flash)
    logo_strobe()
    print("Spinning", infile, "counterclockwise with speed =", speed, "and strobing", flash + ".")
    try:
        ccwised[0].save(spinfile, 'GIF', save_all=True, append_images=ccwised[1:], duration=speed,
                        loop=0,
                        optimize=True, quality=100)
        print("Spinning GIF created: ", spinfile)
    except IOError:
        print("Error: Cannot open output file for strobing.")
        exit(1)


# convert png to rgba image
def rem_trans(img, color_bg):
    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
        alpha = img.convert('RGBA').split()[-1]
        bg = Image.new("RGBA", img.size, color_bg + (255,))
        bg.paste(img, mask=alpha)
        return bg
    else:
        return img


# bounce the image and save
def bouncy(image, infile, speed, bouncefile):
    logo_bounce()
    print("Bouncing", infile, "with speed = ", str(speed) + ".")
    resized = resize_image(image)
    bounced = bounce(resized)
    try:
        bounced[0].save(bouncefile, 'GIF', save_all=True, append_images=bounced[1:],
                        duration=speed,
                        loop=0,
                        optimize=True, quality=100)
        print("Bouncing GIF created:", bouncefile)
    except IOError:
        print("Error: Cannot open output file for bouncing.")
        exit(1)


# just save the emote
def emote(image, emote, outfile):
    print("Creating an emote from", outfile)
    resized = resize_image(image)
    try:
        resized.save(emote, 'GIF', save_all=True, optimize=True, quality=100)
        print("Emote created:", emote)
    except IOError:
        print("Error: Cannot open output file for writing.")
        exit(1)


# rotate the image clockwise and apply the strobe color
def clockwise_strobe(c_image, color):
    images = []
    if color == "red":
        img = Image.new('RGB', (80, 80), (255, 0, 0))
    elif color == "yellow":
        img = Image.new('RGB', (80, 80), (255, 255, 0))
    elif color == "orange":
        img = Image.new('RGB', (80, 80), (255, 140, 0))
    else:
        print("You specified a weird or unsupported color. Try again.")
        exit(1)
    degrees = -1
    while degrees >= -360:
        trans_img = c_image.rotate(degrees)
        images.append(trans_img)
        if degrees == -81 or degrees == -181 or degrees == -281 or degrees == -341:
            images.append(img)
        degrees -= 20
    return images


# rotate the image counterclockwise and apply the strobe color
def counterclockwise_strobe(cc_image, color):
    images = []
    if color == "red":
        img = Image.new('RGB', (80, 80), (255, 0, 0))
    elif color == "yellow":
        img = Image.new('RGB', (80, 80), (255, 255, 0))
    elif color == "orange":
        img = Image.new('RGB', (80, 80), (255, 140, 0))
    else:
        print("You specified a weird or unsupported color. Try again.")
        exit(1)
    degrees = 1
    while degrees <= 360:
        trans_img = cc_image.rotate(degrees)
        images.append(trans_img)
        if degrees == 81 or degrees == 181 or degrees == 281 or degrees == 341:
            images.append(img)
        degrees += 20
    return images


def create_emote(image_file, emote_file):
    what = "emote"
    emote_image = open_file(image_file, what)
    emote(emote_image, emote_file, image_file)
    exit(1)


# main
def main():
    # get arguments
    (args) = check_args()

    # ensure all required options are provided
    # if all arguments not supplied, will save as
    # an 80x80 emote
    error_check(args.i, args.o, args.s, args.t, args.d)

    # get the action (spin, strobe, bounce, tile)
    manip_type = check_type(args.t)

    # open the file and get the image
    img = open_file(args.i, manip_type)

    # probably a better way to do this
    get_manip(img, manip_type, args)


if __name__ == '__main__':
    main()
