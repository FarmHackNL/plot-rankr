from shapely.geometry import asShape, mapping
from json import load, dump
from rasterstats import zonal_stats
import numpy as np
import rasterio
import subprocess

def shrink():
    """Remove pixel bordering effect by shrinking plots through a negative buffer."""

    with open('data/percelen-sat.geojson') as f:
        data = load(f)['features']

    output = {"type": "FeatureCollection", "features": []}

    for feature in data:
        geom = asShape(feature['geometry'])

        shrink = geom.buffer(-21.0)

        if shrink.is_empty == False:
            output['features'].append({
                "type": "Feature",
                "geometry": mapping(shrink),
                "properties": {"perceel": feature['properties']['NAME']}
            })

    with open('data/1-percelen-shrunk.geojson', 'w') as f:
        dump(output, f)

def calc_ndvi():
    """Calculate NDVI from a Sentinel-2 image."""

    with rasterio.open('data/images/2-sentinel2-2016-04-01_demo.tif') as src:
        bands = src.read()
        red = bands[3]
        nir = bands[7]
        profile = src.profile

    ndvi = np.zeros(red.shape)
    for index in range(0, len(red)):
        ndvi[index] = (nir[index] - red[index])/(nir[index] + red[index])

    profile.update(dtype=rasterio.float32, count=1, compress='lzw')

    with rasterio.open('data/ndvi.tif', 'w', **profile) as dst:
        dst.write(ndvi.astype(rasterio.float32), 1)

def histogram(x):
    """Calculate the histogram of an NDVI map."""

    hist = np.histogram(x, bins=5,range=(x.min(), x.max()))

    return {'count': list(hist[0]), 'bins': list(hist[1])}

def stats():
    """Calculate the zonal statistics of each field."""

    stats = zonal_stats('data/1-percelen-shrunk.geojson',
        'data/images/2-sentinel2-2016-04-01_demo.tif',
        geojson_out=True,
        add_stats={'histogram':histogram}
    )

    print 'min:', stats[1]['properties']['min']
    print 'max:', stats[1]['properties']['max']
    print 'mean:', stats[1]['properties']['mean']
    print stats[1]['properties']['histogram']

    out = {'type': 'FeatureCollection', 'features': stats}

    with open('results/stats.geojson', 'w') as f_out:
        dump(out, f_out)

if __name__ == '__main__':
    """ Calculates the min, max and mean values, and the histogram of a plot's NDVI map"""

    shrink()
    calc_ndvi()
    stats()