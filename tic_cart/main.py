#!/usr/bin/env python3

import argparse
import enum
import struct

import PIL.Image as Image


Kind = enum.IntEnum('Kind', dict(
    TILES=1,
    SPRITES=2,
    MAP=4,
    CODE=5,
    COVER=3,
    SAMPLES=9,
    WAVEFORM=10,
    PALETTE=12,
    MUSIC=14,
    PATTERNS=15,
))


def parse_args():
    parser = argparse.ArgumentParser(description='Build tic80 cartridge.')
    parser.add_argument('--tiles', help='file with tiles data')
    parser.add_argument('--sprites', help='file with sprites data')
    parser.add_argument('--map', help='file with map data')
    parser.add_argument('--code', help='file with code')
    parser.add_argument('-o', '--output', required=True, help='output file')
    return parser.parse_args()


def write_chunk(fout, kind, data):
    size = len(data)
    fout.write(struct.pack('I', size << 8 | kind))
    fout.write(data)


def convert_image_to_bytes(filename, yshift):
    im = Image.open(filename)
    im = im.crop((0, yshift, 128, yshift+128))
    w, h = im.size
    imdata = im.getdata()
    data = []
    for j in range(h//8):
        for i in range(w//8):
            for y in range(8):
                for x in range(4):
                    ind = (j*8+y)*w + i*8+2*x
                    data.append(imdata[ind] | imdata[ind+1] << 4)
    return bytes(data)


def main():
    args = parse_args()
    with open(args.output, 'wb') as fout:
        if args.tiles:
            if args.tiles.endswith('.gif'):
                data = convert_image_to_bytes(args.tiles, 0)
            else:
                data = open(args.tiles, 'rb').read()
            write_chunk(fout, Kind.TILES, data)
        if args.sprites:
            if args.sprites.endswith('.gif'):
                data = convert_image_to_bytes(args.sprites, 128)
            else:
                data = open(args.sprites, 'rb').read()
            write_chunk(fout, Kind.SPRITES, data)
        for filename, kind in (
            (args.map, Kind.MAP),
            (args.code, Kind.CODE),
        ):
            if filename:
                data = open(filename, 'rb').read()
                write_chunk(fout, kind, data)


if __name__ == '__main__':
    exit(main())
