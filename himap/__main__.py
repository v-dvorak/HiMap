from pathlib import Path
import json
import argparse
import math

from .Utils import Utils
from .ImageGenerator import MapGenerator
from .Utils import ApiKeyUtil
from .Utils.Zoom import ZoomLevel
from .Towns.Prague import Prague

parser = argparse.ArgumentParser(
    prog="HiMap",
    description="",
    epilog=""
)

prg = Prague()

# Required positional argument: output file name
parser.add_argument("output", help="Path to store the final image at.")

# request params
parser.add_argument("--start", nargs="+", help="Top left coordinates", default=None)
parser.add_argument("--end", nargs="+", help="Bottom right coordinates", default=None)
parser.add_argument("--width", help="Width in parts", default=None, type=int)
parser.add_argument("--height", help="Height in parts", default=None, type=int)
parser.add_argument("--xgrowth", help="Growth x", default=prg.x_growth, type=float)
parser.add_argument("--ygrowth", help="Growth y", default=prg.y_growth, type=float)
parser.add_argument("-z", "--zoom", help="Zoom level", default=16, type=int)
parser.add_argument("--style", help="Map style", default=None)

# generation params
parser.add_argument("--save", action="store_true", help="Save partial maps into PNGs", default=False)

# api key params
parser.add_argument("--key", help="API key", default=None)
parser.add_argument("--store", action="store_true", help="Store API key", default=False)

parser.add_argument("-v", "--verbose", action="store_true", help="Make script verbose")

args = parser.parse_args()

# gc
prg = None

# CHECK COORDINATES
if args.start is None:
    print("Please provide start coordinates.")
    quit()
if args.end is None and (args.width is None or args.height is None):
    print("Please provide end coordinates or width and height.")
    quit()

# convert coordinates
try:
    start = [float(x) for x in args.start]
    if len(start) != 2:
        print("Please provide exactly two start coordinates.")
        quit()
    start = (start[0], start[1])
except ValueError:
    print("Please provide start coordinates as two floats.")
    quit()

end = None
if args.end is not None:
    try:
        end = [float(x) for x in args.end]
        if len(end) != 2:
            print("Please provide exactly two end coordinates.")
            quit()
        end = (end[0], end[1])
    except ValueError:
        print("Please provide end coordinates as two floats.")
        quit()

# PARAM SETUP
# basic
zoom = int(args.zoom)
x, y = start

# setup zoom
zoom_level = ZoomLevel(Path("./himap/Utils/zoom_levels.txt"))
ratio = zoom_level.get_zoom_ratio(zoom, 16)

if args.verbose:
    print("Zoom level:", zoom)

# growth
x_growth = float(args.xgrowth)

if args.verbose:
    print(f"Default x growth: {x_growth}")

x_growth = float(x_growth) * ratio / Utils.get_growth_ratio_to_Prague(start)
y_growth = float(args.ygrowth) * ratio
if args.verbose:
    print(f"X growth after adjustments: {x_growth}")
    print(f"Y growth: {y_growth}")

# size
if ((args.width is not None and args.end is not None)
        or (args.height is not None and args.end is not None)):
    print("Provide either width and height as two uints or end as two floats.")
    quit()

if args.width is not None and args.height is not None:
    width = int(args.width)
    height = int(args.height)
else:
    height = max(int(math.ceil(abs(start[0] - end[0]) / x_growth * 640 / 616)), 1)
    width = max(int(math.ceil(abs((start[1] - end[1]) / y_growth))), 1)

# API KEY
api_key = None  # default, (for correct highlighting)
if args.key is None:
    try:
        api_key = ApiKeyUtil.load_api_key()
        if args.verbose:
            print("API key loaded successfully:", api_key)
    except FileNotFoundError:
        print("API key file not found or invalid. Please provide a valid API key.")
else:
    api_key = args.key
    if args.store:
        ApiKeyUtil.save_api_key(api_key)

# LOAD STYLE
if args.style is not None:
    with open(args.style, 'r') as f:
        style = json.load(f)
    style = Utils.get_static_style(style)
else:
    style = ""

MapGenerator.make_map(start, width, height, x_growth, y_growth, api_key,
                      Path(args.output),
                      zoom=zoom, style=style,
                      save_images=args.save, verbose=args.verbose)

print(f"Map generation finished. Image saved at: {Path(args.output).absolute().resolve()}")
