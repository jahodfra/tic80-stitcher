#!/usr/bin/python3

import argparse
import enum
import struct


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


def write_chunk(fout, kind, input_filename):
    data = open(input_filename, 'rb').read()
    size = len(data)
    fout.write(struct.pack('I', size << 8 | kind))
    fout.write(data)
    

args = parse_args()
with open(args.output, 'wb') as fout:
    for filename, kind in (
        (args.tiles, Kind.TILES),
        (args.sprites, Kind.SPRITES),
        (args.map, Kind.MAP),
        (args.code, Kind.CODE),
    ):
        if filename:
            write_chunk(fout, kind, filename)

