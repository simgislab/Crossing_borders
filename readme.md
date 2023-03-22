# Crossing borders
This script receives polygonal and point layers as input,
and counts the intersections of the layer's geometries with
the polygons of the regional borders.

## Installation

```bash
pip install fiona  
pip install argparse  
pip install fiona  
```

## Usage

Run the file main.py with two arguments.
The first argument is the path to the folder with borders.
The second argument is the path to the folder with .shp files.
```
bash

- `-r` the path to the folder with borders.
- `-o` the path to the folder with .shp files.

```bash
python main.py -r ./regions -o ./objects
```
```

## Docker

### development

```bash
```bash
cd avral_crossing_borders
docker build -t avral_crossing_borders:latest .
docker run --rm -t -i -v ${PWD}:/opt/avral_crossing_borders avral_crossing_borders:latest /bin/bash
cd /opt/avral_crossing_borders
avral-exec --debug crossing_borders 
```
With docker-compose
```bash
docker-compose build
docker-compose up
```