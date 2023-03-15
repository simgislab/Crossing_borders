
FROM registry.nextgis.com/toolbox-workers/base:0.0.11-ubuntu2004-gdal
RUN apt-get update --yes && apt-get upgrade --yes
RUN apt-get --yes install python3-gdal gdal-data gdal-bin
RUN apt-get install --yes img2pdf
RUN pip install filetype

COPY . /opt/avral_crossing_borders
RUN pip install --no-cache-dir /opt/avral_crossing_borders
