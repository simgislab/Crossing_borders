
FROM registry.nextgis.com/toolbox-workers/base:0.0.11-ubuntu2004-gdal
RUN apt-get update --yes && apt-get upgrade --yes
RUN apt install --yes img2pdf
RUN pip3 install filetype

COPY . /opt/avral_crossing_borders
RUN pip3 install --no-cache-dir /opt/avral_crossing_borders
