from tqdm import tqdm
from pathlib import Path
from PIL import Image

from ..Utils import Utils


def make_map(start: tuple[float, float], width: int, height: int, x_growth: float, y_growth: float,
             api_key: str, output_path: Path, zoom: int = 16, size: tuple[int, int] = (640, 640), style: str = "",
             verbose: bool = False, save_images: bool = False):
    """
    Takes in basic information about the map, downloads it and saves in a PNG format.

    :param start: start coordinates
    :param width: width of the map
    :param height: height of the map
    :param zoom: zoom of the map
    :param x_growth: growth factor of the map along the X coordinate
    :param y_growth: growth factor of the map along the Y coordinate
    :param api_key: api key
    :param output_path: output path
    :param zoom: zoom of the map
    :param style: style of the map
    :param verbose: verbose mode
    :param save_images: save images when generating the final map
    """

    home = output_path / ".."
    x, y = start
    y_base = y

    if save_images:
        for i in tqdm(range(height)):
            y = y_base
            for j in range(width):
                file_path = Path(home / (str(i * width + j) + ".png"))
                url = Utils.get_static_request(api_key, (x, y), zoom, size, style)
                if verbose:
                    print(url)
                Utils.download_static_map(url, file_path, verbose=verbose)
                y += y_growth
            x -= x_growth

        Utils.generate_matrix_image([home / (str(i) + ".png") for i in range(height * width)],
                                    (height, width), output_path=output_path, resize=True)
    else:
        rows, columns = height, width
        # dimensions of the final image
        image_width, image_height = 640, 614
        final_width = image_width * columns
        final_height = image_height * rows

        # new blank image
        final_image = Image.new('RGBA', (final_width, final_height), color='white')

        final_image.save(output_path)
        im_num = 0
        for i in tqdm(range(height)):
            y = y_base
            for j in range(width):
                url = Utils.get_static_request(api_key, (x, y), zoom, size, style)
                image = Utils.load_image_from_url(url).crop((0, 0, 640, 614))

                row = im_num // columns
                col = im_num % columns
                x_offset = col * image_width
                y_offset = row * image_height

                final_image.paste(image, (x_offset, y_offset))

                if verbose:
                    print(url)

                im_num += 1
                y += y_growth
            x -= x_growth

        final_image.save(output_path)

