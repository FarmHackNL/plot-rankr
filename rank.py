from shapely.geometry import asShape, mapping
from json import loads, dumps
import numpy as np
import rasterio
import subprocess


def shrink():
    with open('data/percelen-sat.geojson') as f:
        data = loads(f.read())['features']

    output = {"type": "FeatureCollection", "features": []}

    for feature in data:
        geom = asShape(feature['geometry'])

        shrink = geom.buffer(-21.0)

        if shrink.is_empty != True:
            output['features'].append({"type": "Feature", "geometry": mapping(shrink)})

    with open('data/1-percelen-shrunk.geojson', 'w') as f:
        f.write(dumps(output))

def calc_ndvi():
    with rasterio.open('data/images/2-sentinel2-2016-04-01_demo.tif') as src:
        bands = src.read()
        red = bands[3]
        nir = bands[7]

        ndvi = np.zeros(red.shape)
        for index in range(0, len(red)):
            ndvi[index] = (nir[index] - red[index])/(nir[index] + red[index])

        profile = src.profile
        profile.update(dtype=rasterio.float32, count=1, compress='lzw')

        with rasterio.open('data/ndvi.tif', 'w', **profile) as dst:
            dst.write(ndvi.astype(rasterio.float32), 1)

def calc_stats():
    subprocess.Popen('cat data/1-percelen-shrunk.geojson | rio zonalstats --stats "mean std" -r data/ndvi.tif > results/stats.geojson', shell=True)

if __name__ == '__main__':
    shrink()
    calc_ndvi()
    calc_stats()