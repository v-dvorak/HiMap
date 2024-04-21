from pathlib import Path


class ZoomLevel:
    """
    Stores information about zoom level
    """
    def __init__(self, file_path: Path):
        self.zoom_data, self.min_index, self.max_index = self.load_zoom_file(file_path)

    @staticmethod
    def load_zoom_file(file_path: Path) -> (dict[int, float], int, int):
        """
        Loads zoom data from file

        :param file_path: path to zoom file
        :return: dictionary with zoom level information
        """
        total_min = 0
        total_max = 0
        data = {}
        with open(file_path, "r") as file:
            for line in file:
                temp = line.strip().split(":")
                zoom, value = int(temp[0]), float(temp[1])
                data[zoom] = value
                # update min and max value
                total_min = min(total_min, zoom)
                total_max = max(total_max, zoom)
        return data, total_min, total_max

    def _check_index(self, zoom: int) -> bool:
        """
        Checks if the zoom level is valid

        :param zoom: zoom level
        :return: True if valid, else False
        """
        if self.min_index <= zoom <= self.max_index:
            return True
        else:
            return False

    def get_zoom_ratio(self, zoom1: int, zoom2: int) -> float:
        """
        Calculates zoom ratio

        :param zoom1: first zoom level
        :param zoom2: second zoom level
        :return: ratio zoom1 / zoom2
        """
        if not self._check_index(zoom1) or not self._check_index(zoom2):
            print(f"Zoom level has to be between {self.min_index} and {self.max_index}.")
            raise IndexError
        return self.zoom_data[zoom1] / self.zoom_data[zoom2]

