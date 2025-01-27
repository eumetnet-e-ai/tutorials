set -e

apt-get update && apt-get install -y \
    wget \
    python3 \
    gcc g++ gfortran \
    libc-dev \
    python3-dev python3-venv \
    git \
    cmake \
    make \
    libaec-dev \
    perl \
    bzip2 \
 && rm -rf /var/lib/apt/lists/*

wget -q https://confluence.ecmwf.int/download/attachments/45757960/eccodes-2.33.0-Source.tar.gz

tar xzf eccodes-2.33.0-Source.tar.gz
rm eccodes-2.33.0-Source.tar.gz
cd eccodes-2.33.0-Source && mkdir build
cd build && cmake .. -DCMAKE_INSTALL_MESSAGE=NEVER
make -j$(grep processor /proc/cpuinfo | wc -l)
make install VERBOSE=0
cd ../../ && rm -rf eccodes-2.33.0-Source

# clean up packages that were used only for this build process
apt-get remove -y \
    gcc g++ gfortran \
    libc-dev
apt autoremove -y
rm -rf /var/lib/apt/lists/*


# Optional: Use local definition files
# cd /usr/local/share/eccodes/
# wget -q http://opendata.dwd.de/weather/lib/grib/eccodes_definitions.edzw-2.32.0-1.tar.bz2
# tar xf eccodes_definitions.edzw-2.32.0-1.tar.bz2
# rm eccodes_definitions.edzw-2.32.0-1.tar.bz2
#
# To use these, add the following line to the Dockerfile
# ENV ECCODES_DEFINITION_PATH="/usr/local/share/eccodes/definitions.edzw-2.32.0-1/:/usr/local/share/eccodes/definitions/"
