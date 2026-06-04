import os.path

import geopandas as gp
import pandas as pd

gp.options.io_engine = "pyogrio"
import h3
from shapely.geometry import Polygon
from hexify import GPK_OUTPUT
import os
import re
import charset_normalizer


def name_fixer(value):
    return re.sub(r"\W", "_", value)

def detect_csv_encoding(file_path: str) -> str:
    """
    Detects the character encoding of a CSV file.
    Falls back to 'utf-8' if detection fails.
    """
    try:
        # Read the file in binary mode
        with open(file_path, 'rb') as f:
            # Analyze a sample (first 50,000 bytes) to save memory
            sample = f.read(50000)
            # Perform detection
        result = charset_normalizer.from_bytes(sample).best()
        # Return detected encoding name, or fallback
        return result.encoding if result else 'utf-8'
    except Exception:
        return 'utf-8'


class CSVProcessor:
    def __init__(self, input_path, gpkg_output_path=GPK_OUTPUT):
        self.input_path = input_path
        self.df = None
        self.gdf = None
        self.gpkg_output_path = gpkg_output_path
        self.output_layer_name = name_fixer(os.path.basename(self.input_path))
        self.input_encoding = detect_csv_encoding(self.input_path)

    def set_output_path(self, output_path):
        self.gpkg_output_path = output_path

    def load_csv(self):
        self.df = pd.read_csv(self.input_path, encoding=self.input_encoding)

    def polygonize(self, hex_id):
        coords = h3.cell_to_boundary(hex_id)
        flipped = tuple(coord[::-1] for coord in coords)
        return Polygon(flipped)

    def create_gis_file(self, hex_id_col_name):
        if self.df is None:
            raise ValueError("CSV not loaded.")

        if hex_id_col_name not in self.df.columns:
            raise ValueError(f"cannot find '{hex_id_col_name}' name in the dataframe columns.")

        self.df['geometry'] = self.df[f"{hex_id_col_name}"].apply(self.polygonize)

        self.gdf = gp.GeoDataFrame(self.df, geometry='geometry', crs=4326)

    def save_gdf(self, output_layer_name):
        if self.gdf is not None:
            self.gpkg_output_path = os.path.join(self.gpkg_output_path, f"{output_layer_name}.gpkg")
            try:
                self.gdf.to_file(self.gpkg_output_path, layer=output_layer_name)
            except Exception as e:
                raise ValueError(e)
        else:
            raise ValueError("No data to save.")
