# SwissR0

This rather old project (2014) is a quick and dirty study to assess differences in R0 arising from differences in population densities across municipalities in Switzerland.

The assessment if based on a contact network approach, modeling the population as a random graph with distance based connection probabilities between individuals.
Individuals are distributed homogeneously over the municipal area (certainly inaccurate in rural and mountain regions).

A HTML-based presentation of the basic results is available [here](presentation/presentations/jgm_26_11_14/pres.html).
_Note: The presentation relies on various javascripts that are provided directly with the repository. You run these files at your own risk._

![relative representation of R0](presentation/presentations/jgm_26_11_14/plots/r0_2000_averaged_0_01.svg)


## Useful links

Swiss demographic (and much more) data can be found here:

https://www.bfs.admin.ch/bfs/en/home/services/recherche/stat-tab-online-data-search.html

For example permanent and non-permanent resident population by institutional units:

https://www.pxweb.bfs.admin.ch/pxweb/en/px-x-0102010000_101/-/px-x-0102010000_101.px/?rxid=39d782e9-2546-4c2e-ad39-e42526612e91


## Features

Using a network model allows to incorporate:

  - population densities (on the municipality level).
  - age distribution (on the municipality level) with the possibility to introduce age specific pathogenic and contact parameters.

## Limitations

Neighbouring countries are missing.
This leads to a general reduction of the R0 in the boundary regions and does not allow to model the impact of incidences in neighbouring regions.
Without the inclusion of the demographics in neighbouring countires (at least the boarder regions) this model is unlikely to provide meaningful predictions inside Switzerland.

The data used here stems from population counts which are not carried out frequently.
In the current state the count from 2000 were the most recent ones.
The better approach would be to use resident population data from the link provided above.


## Presentation

An HTML-based presentation of some basic results is available [here](presentation/presentations/jgm_26_11_14/pres.html).
Simply clone the repo and then run the file in your favourite browser, but note that several javascripts are required and provided in the repo to display the presentation correctly. _Also note that this was my first attempt to do a presentation in HTML, so please don't be offended by the looks..._
