import geopandas as gpd
import numpy as np

class ImportShapefile(object):
    """ Finalize docstring (TODO)
    Importing 'ESRI shapefile' polygons and prepare for plotting.

    Contains functions that extracts exterior of polygons, saved in columns
    'x' and 'y'. These functions are closely based on the following git-repo:

    References
        [1] https://automating-gis-processes.github.io/2016/
    """

    def _get_xy_coords(self, geometry, coord_type):
        """ Finalize docstring (TODO)
        Returns either x or y coordinates from  geometry
        coordinate sequence (Polygon).
        """
        if coord_type == 'x':
            return geometry.coords.xy[0]
        elif coord_type == 'y':
            return geometry.coords.xy[1]

    def _get_poly_coords(self, geometry, coord_type):
        """ Finalize docstring (TODO)
        Returns Coordinates of Polygon using the Exterior of the Polygon."""
        ext = geometry.exterior
        return self._get_xy_coords(ext, coord_type)

    def _multi_poly_handler(self, multi_geometry, coord_type):
        """ Finalize docstring (TODO)
        /1/
        """
        for i, part in enumerate(multi_geometry):
            # On the first part of the Multi-geometry initialize the coord_array (np.array)
            if i == 0:
                coord_arrays = np.append(self._get_poly_coords(part, coord_type), np.nan)
            else:
                coord_arrays = np.concatenate([coord_arrays,
                                              np.append(self._get_poly_coords(part, coord_type), np.nan)])

        # Return the coordinates
        return coord_arrays

    def _get_coords(self, row, geom_col, coord_type):
        """ Finalize docstring (TODO)
        Returns coordinates ('x' or 'y') of a geometry (Point, LineString or Polygon) as
        a list (if geometry is LineString or Polygon).
        Can handle also MultiGeometries.
        """
        # Get geometry
        geom = row[geom_col]
        # Check the geometry type
        gtype = geom.geom_type

        if gtype == "Polygon":
            return list(self._get_poly_coords(geom, coord_type) )
        elif gtype == "MultiPolygon":
            return list(self._multi_poly_handler(geom, coord_type))
        else:
            err_msg = "Geometry type (",gtype,") not suppert by function"
            raise TypeError(err_msg)

    def _add_coordinate_data(self, df, geom_col):
        """Add docstring (TODO)
        """
        coord_types = ['x', 'y']

        x = df.apply(self._get_coords,
                     geom_col=geom_col,
                     coord_type='x',
                     axis = 1)

        y = df.apply(self._get_coords,
                     geom_col=geom_col,
                     coord_type='y',
                     axis = 1)
        return x,y

    def get_df(self):
        return self.df

    def __init__(self, link, geom_col='geometry'):
        """Add docstring (TODO)

        Param:
        Link: Directory to shapefile
        """
        # Check for file format etc.?
        # TO BE WRITTEN

        self.df = gpd.read_file(link)
        (self.df['x'], self.df['y']) = self._add_coordinate_data(self.df, geom_col)

        """ TODO
        Consider adding parameter with list of dicts [{'continent': 'Africa'}]
        resulting in:

        mask = data_world['continent']=='Africa'
        self.df = data_world.loc[mask,:]

        """

        return None
