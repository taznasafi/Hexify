import os.path
import pandas as pd
import geopandas as gp
import h3
from shapely.geometry import Polygon
from hexify import GPK_OUTPUT
import os



class CSVProcessor:
    def __init__(self, input_path):
        self.input_path = input_path
        self.df = None
        self.gdf = None
        self.gpkg_output_path = None
        self.output_layer_name = os.path.basename(self.input_path).replace(".csv", "")

    def load_csv(self):
        self.df = pd.read_csv(self.input_path)

    def polygonize(self, hex_id):
        coords = h3.h3_to_geo_boundary(hex_id)
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
            self.gpkg_output_path = os.path.join(GPK_OUTPUT, f"{output_layer_name}.gpkg")
            try:
                self.gdf.to_file(self.gpkg_output_path, layer_name=output_layer_name)
            except:
                self.gdf.to_file(self.gpkg_output_path, layer=output_layer_name)
        else:
            raise ValueError("No data to save.")
