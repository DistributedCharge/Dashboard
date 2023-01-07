
## Distributed Grid Dashboard

This dashboard visualizes meter data and metrics in real time.


## Setup (docker)

Run the production version with

```console
docker compose up
```

Run the dev version with

```console
docker compose -f docker-compose-dev.yml up dashboard simulator
```

That runs the dashboard in debug mode along with the simulator. See below for setting up data paths.



## Setup (conda)

This project may be set up with a miniconda environment, which is a stripped-down version of anaconda.

Download the miniconda package manager here https://docs.conda.io/en/latest/miniconda.html#latest-miniconda-installer-links

Once installed, you can spin up a new conda environment for this project:

```sh
conda create -n dc python=3.7
conda activate dc # activates distributed charge environment
(dc) conda install jupyter
(dc) pip install -r requirements.txt
```

### Core requirements

* pandas
* numpy
* plotly
* dash (from plotly) https://dash.plotly.com/introduction
* psidash (from psi/Asher) https://github.com/predsci/psidash

These are installed automatically by installing this project in editable mode

```sh
(dc) pip install -e . # from base of this repo
```

### Docs requirements

These packages are necessary for generating the documentation site.

* mkdocs `pip install mkdocs`
* markdown-include - for embedding files outside the docs path `pip install markdown-include`
* codehighlight - rendering code blocks `pip install pygments`
* mkautodoc - docstrings `pip install mkautodoc`
* mdxmath - mathematics rendering `pip install python-markdown-math`
* material theme - `pip install mkdocs-material`
* jupytext - executable markdown as jupyter notebook `pip install jupytext`

### Environment variables

The dashboard reads data files generated by the [DistributedCharge](https://github.com/DistributedCharge/DistributedCharge) hardware.

These variables are needed by the dashboard container

ENV VARIABLE | container default | description
-------------|-------------------|------------
DASH_DEBUG | False | dashboard debug mode (to see live stack traces)
DATA_PATH | /dashboard/data_files | `/full/path/where` data files will be read from
DATA_LOG | DataLog.txt | the name of the file to read the primary data log
DISCRETE_DATA_LOG | DiscreteDataLog.txt | data log of **discrete** load
VARIABLE_DATA_LOG | VariableDataLog.txt | data log of **variable** load


The simulator reads data and writes them to the same location as the above files.
The following variables are needed by the simulator container:

ENV VARIABLE | container default | description
-------------|-------------------|------------
READ_DATA_PATH | /dashboard/data_files | `/full/path/where` data files will be **read** from
DATA_PATH | /dashboard/data_files | `/full/path/where` data files will be written to
READ_DATA_LOG| read from host env | the name of the file to **read** the primary data log from
DATA_LOG | DataLog.txt | the name of the file to **write** the primary data log to



## Run (host)

If you installed on your host machine, spin up the dashboard using the following command

```sh
(dc) python dcharge/dashboard/dashboard.py
```
