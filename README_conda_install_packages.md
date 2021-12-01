Install AOS-related Python Packages with conda
==============================================

Download the miniconda bash file
 * macOS `wget https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh`
 * Linux `wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh`
 * Windows: https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh

Run the miniconda bash file, e.g. macOS

    bash Miniconda3-latest-MacOSX-x86_64.sh

Add the conda-forge channel to the .condarc file

    conda config --add channels conda-forge

Update conda

    conda update conda

Install AOS-related python packages

    conda install numpy scipy matplotlib ipython jupyter \
        xarray dask bottleneck netcdf4 cftime nc-time-axis basemap pandas numba \
        scikit-learn  seaborn eofs windspharm cartopy \
        joblib geopandas shapely rasterio hvplot \
        requests beautifulsoup4 wget nco cdo ffmpeg ncview \
        cdsapi salem regionmask jupyterlab jupyter_contrib_nbextensions xesmf

Other interesting packages:

    conda install gcc twine sphinx sphinx_rtd_theme spyder

Can also use `pip` to install packages:
    
    pip install cdsapi # now available from conda; for downloading ERA5 data: https://cds.climate.copernicus.eu/api-how-to#install-the-cds-api-client

    pip install salem # now available from conda

    pip install regionmask # now available from conda

    pip install jupyter_contrib_nbextensions
    jupyter contrib nbextension install --user


Clean the installation

    conda clean -all
