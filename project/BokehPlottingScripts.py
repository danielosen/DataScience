from bokeh.plotting import figure, save
from bokeh.models import ColumnDataSource, HoverTool, LogColorMapper
from bokeh.palettes import RdYlGn10 as palette
#import geopandas as gpd
import numpy as np

#from bokeh.palettes import YlOrRd as palette  #Spectral6 as palette

from bokeh.io import output_notebook, show
output_notebook()


def bokeh_plot_test(df, data='area', title="Map with no title"):
    """ Finalize docstring (TODO)
    Simple function for plotting map contours

    Input:
    df - dataframe including columns
        'name': Country name
        'x' and 'y' that cointain exterior coordinates of the contries contours.
        One column with values used for colouring (see 'data')

    data: String containing name of column in 'df' to fill contours
    """
    color_mapper = LogColorMapper(palette=palette)

    TOOLS = "pan,wheel_zoom,reset,save"

    bokeh_cds = ColumnDataSource(df)

    p = figure(title=title, tools=TOOLS)

    contour = p.patches('x', 'y', source=bokeh_cds,
                        fill_color={'field': data, 'transform': color_mapper},
                        fill_alpha=1.0, line_color="black", line_width=0.05)


    hover = HoverTool(renderers=[contour])
    hover.tooltips=[("Country", "@name"),
                    (data, "@"+data)]

    p.add_tools(hover)
    show(p)

    return p
