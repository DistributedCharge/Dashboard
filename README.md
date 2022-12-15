
## Distributed Grid Dashboard

This dashboard visualizes meter data and metrics in real time.


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


## Run (host)

If you installed on your host machine, spin up the dashboard using the following command

```sh
(dc) python 
```
