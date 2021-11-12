#!/usr/bin/env python3

# python 3 script to manipulate an image for use in slack, etc.
# basically just makes a 80x80 emote from an image
# this can:
# spin the image clockwise or counterclockwise
# bounce the image
# just save as an emote
# create 4 80x80 tiles from the image
# Ken Mininger, kmininger@us.ibm.com
# October 2021
import PIL.Image
from PIL import Image, ImageOps
from sys import exit
import argparse


# check the arguments
def check_args():
    parser = argparse.ArgumentParser(
        description="Manipulates an image and saves as specified GIF file (or whatever).", prog="gif-manip",
        usage="%(prog)s "
              "[options]")
    parser.add_argument("-i", help="Input file - The file you want to work with.",
                        required=True)
    parser.add_argument("-o", help="Output file - If you don't add the .gif extension, I'll add it for you (except "
                                   "for the four tile thing where it'll be .jpgs).",
                        required=True)
    parser.add_argument("-s", help="Spin/bounce speed (50 is a good clean spin, 20 is turbo spin). Option not needed "
                                   "with 'e' argument and is ignored if supplied.", type=int)
    parser.add_argument("-d", help="Direction or task (c=clockwise spin, cc=counterclockwise spin, b=bounce, "
                                   "f=four tiles, p=flip, or e=just save as an emote).", required=True)
    args1 = parser.parse_args()
    return (args1)


# check that arguments are supplied
def error_check(infile, spinfile, speed, dir):
    if not infile:
        print("Input file not provided: use -i")
        exit(1)
    if not os.path.isfile(infile):
        print("Input file not found")
        exit(1)
    if not spinfile:
        print("Output file not provided: use -o")
        exit(1)
    if not speed and (dir == "c" or dir == "cc" or dir == "b"):
        print("Need some speed with this option: use -s")
        exit(1)
    if not dir:
        print("What do you want to do: use -d")
        exit(1)


# open image file and process
def open_file(option, what):
    ideal_width = 80
    ideal_height = 80
    try:
        if what == "b":
            doing = "bouncing."
        elif (what == "c") or (what == "cc"):
            doing = "spinning."
        elif what == "f":
            doing = "tile creation."
        elif what == "p":
            doing = "flipping."
        else:
            doing = "emote creating."
        image_open = Image.open(option, 'r')
        print("Opened", option, "for", doing)
        if (image_open.height < ideal_height) or (image_open.width < ideal_width):
            print("WARNING: Image smaller than", ideal_height, "x", ideal_width, ",", (doing[:-1]), "may look weird.")
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


# convert png to rgba image
def rem_trans(img, color_bg):
    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
        alpha = img.convert('RGBA').split()[-1]
        bg = Image.new("RGBA", img.size, color_bg + (255,))
        bg.paste(img, mask=alpha)
        return bg
    else:
        return img


# resize image
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


# flip the image
def flip_it(flip_image):
    images = []
    trans_img = flip_image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
    images.append(trans_img)
    trans_img = ImageOps.flip(trans_img)
    images.append(trans_img)
    trans_img = flip_image.transpose(PIL.Image.FLIP_TOP_BOTTOM)
    images.append(trans_img)
    # degrees = range(1, 360, 40)
    # degrees2 = range(360, 1, -40)
    # for deg in degrees:
    #    trans_img = b_image.rotate(deg)
    #    images.append(trans_img)
    # for deg2 in degrees2:
    #    trans_img = b_image.rotate(deg2)
    #    images.append(trans_img)
    return images


# create-four tiles
def create_four(f_image, tilefile):
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


# bounce the image and save
def bouncy(image, infile, speed, bouncefile):
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


# flip and save
def flippy(image, infile, speed, flipfile):
    print("Flipping", infile, "with speed = ", str(speed) + ".")
    resized = resize_image(image)
    flipped = flip_it(resized)
    try:
        flipped[0].save(flipfile, 'GIF', save_all=True, append_images=flipped[1:],
                        duration=speed,
                        loop=0,
                        optimize=True, quality=100)
        print("Flipping GIF created:", flipfile)
    except IOError:
        print("Error: Cannot open output file for flipping.")
        exit(1)


# just save the emote
def emote(image, outfile):
    print("Saving the file as an emote.")
    resized = resize_image(image)
    try:
        resized.save(outfile, 'GIF', save_all=True, optimize=True, quality=100)
        print("Emote created:", outfile)
    except IOError:
        print("Error: Cannot open output file for writing.")
        exit(1)


# create the emote
def create_emote(image_file, emote_file):
    emote(image_file, emote_file)
    exit(1)


# add .gif if not supplied on input
def gif_file(extension):
    if not extension.endswith('.gif'):
        filename_new = extension + ".gif"
        return filename_new
    else:
        return extension


# figure out what to do
def get_manip(picture, what_do, outfile, things):
    if what_do == "c":
        spin_clockwise(picture, (things.i), (things.s), (outfile))
    elif what_do == "cc":
        spin_counterclockwise(picture, (things.i), (things.s), (outfile))
    elif what_do == "f":
        create_four(picture, (outfile))
    elif what_do == "b":
        bouncy(picture, (things.i), (things.s), (outfile))
    elif what_do == "e":
        create_emote(picture, outfile)
    elif what_do == "p":
        flippy(picture, (things.i), (things.s), (outfile))
    else:
        print("I don't know what you're trying to do.")
        exit(1)


# main
def main():
    # get args
    (args) = check_args()

    # check args
    error_check(args.i, args.o, args.s, args.d)

    # check that .gif is appended to the -o argument
    new_output = gif_file(args.o)

    # open the file and get the image
    img = open_file(args.i, args.d)

    # manipulate it
    get_manip(img, args.d, new_output, args)


if __name__ == '__main__':
    main()
