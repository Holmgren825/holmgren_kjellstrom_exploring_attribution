# Extreme event attribution project template
>Work in progress.

This repository holds a collection of Jupyter notebooks, working as a template for how to do an extreme event attribution study using the attribution python package.

Start by taking a look at the introduction in `notebooks/0_introduction.ipynb`.

Use `config.yml` to save the configuration for the project such as paths to the data, which variable to use, which timespan to investigate and coordinates for the region of interest.

## Usage
Clone this repository when starting the analysis of a new event. Run through the notebooks and adapt `config.yml`. It is also possible to write your own custom scripts.
Using functions from `attribution` from any of the subfolders will be able to read `config.yml`.
