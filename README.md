# SwissR0

Quick and dirty study to assess municipality based differences in R0 arising from population density differences between municipalities in Switzerland.

The assessment if based on a contact network approach, modeling the population as a random graph with distance based connection probabilities between individuals.
Individuals are distributed homogeneously over the municipal area (certainly inaccurate in rural and mountain regions).


## Useful links

Swiss demographic (and much more) data can be found here:

https://www.bfs.admin.ch/bfs/en/home/services/recherche/stat-tab-online-data-search.html

For example permanent and non-permanent resident population by institutional units:

https://www.pxweb.bfs.admin.ch/pxweb/en/px-x-0102010000_101/-/px-x-0102010000_101.px/?rxid=39d782e9-2546-4c2e-ad39-e42526612e91


## Features

Using a network model allows to incorporate:

	- population densities (on the municipality level).
	- age distribution (on the municipality level) with the possibility to introduce age specific pathogenic parameters and contact rates.

## Limitations

Neighbouring countries are missing.
This leads to a general reduction of the R0 in the boundary regions and does not allow to model the impact of incidences in neighbouring regions.

The data used here stems from population counts which are not carried out frequently.
In the current state the count from 2000 were the most recent ones.
The better approach would be to use resident population data from the link provided above.
