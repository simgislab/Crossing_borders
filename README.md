# Crossing borders

This script receives polygonal and point layers as input,
and counts the intersections of the layer's geometries with
the polygons of the regional borders.

## Installation

To run `crossing_borders_shapely` version install this dependencies

```bash
pip install fiona
pip install shapely
```

For `crossing_borders_osgeo` version use the ready to run container from this 
[Dockerfile](https://github.com/GroveBow/Crossing_borders/blob/master/Dockerfile)

## Usage

Run the file `crossing_borders.py` with two arguments.
The first argument is the path to the folder with borders.
The second argument is the path to the folder with `.shp` files.

```bash
- `-b` the path to the folder with borders.
- `-i` the path to the folder with .shp files
```

```bash
python crossing_borders.py -b ./regions -i ./objects
```

## Docker

### Development

```bash
cd avral_crossing_borders
docker build -t avral_crossing_borders:latest .
docker run --rm -t -i -v ${PWD}:/opt/avral_crossing_borders avral_crossing_borders:latest /bin/bash
cd /opt/avral_crossing_borders
avral-exec --debug crossing_borders /opt/avral_crossing_borders/tests/borders.zip /opt/avral_crossing_borders/tests/objects.zip 
```

With docker-compose

```bash
docker-compose build
docker-compose up
```

### Publish

```bash
docker build -t avral_crossing_borders:latest .
docker tag avral_crossing_borders:latest registry.nextgis.com/toolbox-workers/crossing_borders:prod
docker image push registry.nextgis.com/toolbox-workers/crossing_borders:prod
```

#### IO

```bash
Inputs:
[["borders", {"__type__": "FileType"}], ["objects", {"__type__": "FileType"}]]
Outputs:
[["output", {"__type__": "FileType"}]]
```
