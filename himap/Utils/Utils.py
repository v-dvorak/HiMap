import requests
from PIL import Image
from io import BytesIO
from pathlib import Path
from geopy import distance

from ..Towns.Prague import Prague


def get_growth_ratio_to_Prague(start: tuple[float, float]) -> float:
    """
    :param start: GPS coordinates of the start point
    :return: ratio of growth in regard to Prague
    """
    prg = Prague()
    return _get_growth_ratio((prg.x, prg.y), start)


def _get_growth_ratio(coord1: tuple[float, float], coord2: tuple[float, float], offset: float = 0.01) -> float:
    """
    :param coord1: GPS coordinates of a point
    :param coord2: GPS coordinates of a point
    :param offset: distance measured for ratio estimation
    :return: growth ratio estimation
    """
    dis1 = distance.distance(coord1, (coord1[0], coord1[1] + offset))
    dis2 = distance.distance(coord2, (coord2[0], coord2[1] + offset))
    return dis1.meters / dis2.meters


def get_static_style(styles: dict) -> str:
    """
    :param styles: dictionary with static styles loaded from a JSON
    :return: static style as a string
    """
    # heavily inspired by this SO answer https://stackoverflow.com/a/19117380
    result = []
    for record in styles:
        style = ''
        if 'stylers' in record:  # only if there is a styler object
            if len(record['stylers']) > 0:  # needs to have a style rule to be valid.
                style += ('feature:' + record['featureType'] if 'featureType' in record else 'feature:all') + '|'
                style += ('element:' + record['elementType'] if 'elementType' in record else 'element:all') + '|'
                for val in record['stylers']:
                    property_name = list(val.keys())[0]
                    property_val = str(val[property_name]).replace('#', '0x')
                    style += property_name + ':' + property_val + '|'
        result.append('style=' + style)
    return '&'.join(result)


def _gps_coord_to_str(lat: float, lon: float) -> str:
    """
    :param lat: GPS latitude
    :param lon: GPS longitude
    :return: string representation of GPS coordinates for Google API call
    """
    return f"{lat},{lon}"


def _size_to_str(size: tuple[int, int]) -> str:
    """
    :param size: image size `width x height` in pixels
    :return: string representation of image size for Google API call
    """
    return f"{size[0]}x{size[1]}"


def get_static_request(api_key: str,
                       center: tuple[float, float] | str,
                       zoom: int | str,
                       size: tuple[int, int] | str,
                       style_parameters: str) -> str:
    # check params
    if isinstance(center, tuple):
        center = _gps_coord_to_str(*center)
    if isinstance(size, tuple):
        size = _size_to_str(size)

    # construct the URL
    base = "https://maps.googleapis.com/maps/api/staticmap?"
    return f"{base}center={center}&zoom={zoom}&size={size}&{style_parameters}&key={api_key}"


def download_static_map(url: str, file_path: Path, verbose: bool = False) -> None:
    """
    :param url: url to download
    :param file_path: path to store static map
    :param verbose: verbose mode
    """
    response = requests.get(url)
    # check if the request was successful
    if response.status_code == 200:
        # save image
        with open(file_path, 'wb') as f:
            f.write(response.content)
        if verbose:
            print(f"Image saved to {file_path}")
    else:
        pass
        print(f"Error: Unable to download image. Status code: {response.status_code}")


def load_image_from_url(url: str) -> Image:
    """
    :param url: url to download
    :return: loaded Image
    """
    # Fetch image content from the URL
    response = requests.get(url)
    # Check if request was successful
    if response.status_code == 200:
        # Open the image using PIL
        image = Image.open(BytesIO(response.content))
        return image
    else:
        print("Error: Unable to fetch image from URL.")
        return None


def generate_matrix_image(image_paths, size: tuple[int, int],
                          output_path=None, resize=False) -> None:
    """
    :param image_paths: list of image paths
    :param size: matrix size `width x height` in images
    :param output_path: path to save image
    :param resize: resize image
    """
    rows, columns = size
    reference = Image.open(image_paths[0]).crop((0, 0, 640, 614))
    # dimensions of the final image
    image_width, image_height = reference.size
    final_width = image_width * columns
    final_height = image_height * rows

    # new blank image
    final_image = Image.new('RGBA', (final_width, final_height), color='white')

    # process image
    for i, image_path in enumerate(image_paths):
        if resize:
            image = Image.open(image_path).crop((0, 0, 640, 614))
        else:
            image = Image.open(image_path)
        row = i // columns
        col = i % columns
        x_offset = col * image_width
        y_offset = row * image_height

        final_image.paste(image, (x_offset, y_offset))

    # final_image.show()
    final_image.save(output_path)
    # imshow(final_image)
