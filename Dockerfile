
FROM registry.nextgis.com/toolbox-workers/base:0.0.11-ubuntu2004-gdal

RUN apt update --yes && apt upgrade --yes
RUN apt install --yes img2pdf

RUN pip install filetype

COPY . /opt/avral_crossing_borders
RUN pip install --no-cache-dir /opt/avral_crossing_borders
