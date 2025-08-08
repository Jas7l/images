FROM ghcr.io/osgeo/gdal:alpine-small-latest AS gdal-base

FROM python:3.12-slim

COPY --from=gdal-base /usr/local/ /usr/local/

WORKDIR /app
RUN apt update && \
    apt install -y \
        locales \
        gcc \
        g++ \
        python3-dev \
        build-essential \
        libgdal-dev \
        gdal-bin \
    && locale-gen ru_RU && \
    locale-gen ru_RU.UTF-8 && \
    update-locale

ENV CPLUS_INCLUDE_PATH=/usr/local/include/gdal
ENV C_INCLUDE_PATH=/usr/local/include/gdal
ENV PROJ_LIB=/usr/local/share/proj
ENV GDAL_DATA=/usr/local/share/gdal
ENV LANG=ru_RU.UTF-8

ENV LD_LIBRARY_PATH=/usr/local/lib

COPY requirements.txt /app/
RUN python -m pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir GDAL==$(gdal-config --version)


COPY uwsgi.ini /app/

COPY . .
WORKDIR /app/src

CMD ["uwsgi", "--ini", "../uwsgi.ini"]