# HiMap

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

HiMap is a console application that allows you to download Google Maps with custom styling, with any supported zoom and at any size. The program is written in Python and relies on the Google Maps Static API, through which it sequentially requests parts of the map and then uses the PIL library to assemble them into one large image.

![](/docs/cover.png)

## Features

The user specifies the map coordinates (or one coordinate and the total size), zoom level, map style, and enters their API key. The result is a map matching the requirements stored in PNG.

You can use [Snazzy Maps](https://snazzymaps.com/) to style the map and then download the style as a `JavaScript Style Array` directly from the SM editor.

<figure>
    <img src="/docs/snazzy_showcase.png" alt="" />
    <figcaption>showcase of popular styles from <a href="https://snazzymaps.com/">Snazzy Maps</a></figcaption>
</figure>

The resulting map has size of `width*640 x height*614` px.

## Limitations

Unfortunately, the Earth is not flat, so we have to accept that linear approximations do not work in extreme cases. This approach breaks around the poles, for example, but works perfectly for countries in Europe.

## Installation and use

The script is controlled from the command line. You need to have Python `3.11` or higher installed. After cloning the repository from GitHub, we first create a virtual environment and install the necessary packages using commands:

```bash
# creating venv:
python -m venv .venv

# venv activation:
# linux
source .venv/bin/activate
# windows cmd
.venv/Scripts/activate.bat
# windows PS
.venv/Scripts/Activate.ps1

# installing requirements:
pip install -r requirements.txt

# run the script
python3 -m himap output_path optional_params
```

- `output_path`
  - the result will be stored here
- `--start X Y`
  - where `X` and `Y` are the latitude and longitude in degrees of the upper left corner of the map
  - `X` and `Y` are `float`
- `--end X Y`
  - where X and Y are the latitude and longitude in degrees of the bottom right corner of the map
  - `X` and `Y` are `float`
- `--width X`
  - map width as the number of squares that make up the final map
  - `X` is `uint`
- `--height X`
  - map height as the number of squares that make up the final map
  - `X` is `uint`
  - these parameters can be used for debugging (for example, to check the alignment of map pieces: `--width 2 --height 2`)
- `-z X, --zoom X`
  - Google Maps zoom level, determines the zoom of the map
  - `X` is `unint`, `0 <= X <= 19`
- `--style path_to_style`
  - path to `JSON` with styling to be used on the map
- `--save`
  - if this flag is set, all parts of the map that the script pulls from the Google server during runtime are saved in the same directory as the final map
- `--key api_key`
  - the API key is needed to communicate with the Google server, each user has their own
- `--store`
  - saves the specified API key for further use
  - there is no need to enter the key when the script is run again, it reads it itself from the created `TXT` file

Since it is significantly easier to crop the map than to struggle with shifting coordinates because of a few pixels, a padding is added around the specified coordinates, from 320 to around 640 px.

## :warning: Disclaimer

Downloading, caching and similar usage of Google Maps violates the TOS, therefore I disclaim any liability arising from the use of this program. More at [Google Maps TOS](https://cloud.google.com/maps-platform/terms?_gl=1*1x7oou1*_ga*MjgzMTU4Njg3LjE3MTI5MjQ3ODQ.*_ga_NRWSTWS78N*MTcxMzUxMjEyOS40LjEuMTcxMzUxMjEzNS4wLjAuMA..#3.-license.), to be more specific: paragraph `3.2.3 a)`.

The stored API key is not encrypted in any way, it is saved as plain text in the directory from which the script is run. It is therefore visible to everyone who has access to the folder.