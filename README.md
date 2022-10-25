# Introduction

See [BEST-PRACTICES.md](BEST-PRACTICES.md) for repository layout and coding best practices. Particularly, this repository has been setup to use [Poetry](https://python-poetry.org/) for Python dependency management and [renv](https://rstudio.github.io/renv/) for R dependency management. Things will be easier for you if you also try using those. The commands you are most likely looking for are `poetry install` (in the shell) and `renv::restore()` (in R), but if those don't work off the bat look to the documentation of the two tools to sort things out. 

For quick-start introductions on how to use the data in practice from code, look at [`src/example_user/example_analysis.Rmd`](src/example_user/example_analysis.md) and[`src/example_user/example_analysis.ipynb`](src/example_user/example_analysis.ipynb). 

