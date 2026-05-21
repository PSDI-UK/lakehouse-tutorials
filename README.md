# Tutorials for the PSDI Lakehouse

This repository provides a collection of tutorials demonstrating how to interact with the PSDI Lakehouse.

The tutorials are available in two formats:

- **Jupyter notebooks**: located in `notebooks/jupyter/`
- [**Marimo notebooks**](https://marimo.io/): located in `notebooks/marimo/`

## Available Tutorials

There are two 'branches' of tutorials. `notebooks/jupyter/sql` and `notebooks/marimo/sql` house tutorials
belong to the *SQL branch*, and involve interacting with the PSDI Lakehouse using
[SQL](https://en.wikipedia.org/wiki/SQL) queries. `notebooks/jupyter/ibis` and `notebooks/marimo/ibis`
house tutorials belonging to the *Ibis branch*, and involve interacting with the PSDI Lakehouse using
[Ibis](https://ibis-project.org/). The content covered by the SQL and Ibis branches is very similar;
the essential difference between the branches is the query language (i.e. SQL or Ibis). Hence,
depending on their interest in SQL or Ibis, a user may wish to undertake the tutorials in only one
of the branches. 

### SQL branch

The tutorials in the SQL branch are as follows. The numbers next to the tutorials indicate the order in
which we recommend the tutorials are undertaken.

#### 1. `lakehouse-query-basics`
An introduction to querying the PSDI Lakehouse using SQL. This tutorial covers:
- How to connect to the lakehouse
- Writing and executing basic SQL queries
- Example queries on the OMol25 dataset

#### 2. `lakehouse-materials-project-sql.ipynb`
Querying the Materials Project data in the PSDI Lakehouse using SQL. This tutorial covers:
- Exploring the structure of Materials Project tabular data in the lakehouse
- Querying the Materials Project tables using SQL. This includes filtering and combining data from different
  tables, and making plots.


### Ibis branch

The tutorials in the Ibis branch are as follows. The numbers next to the tutorials indicate the order in
which we recommend the tutorials are undertaken.

#### 1. `lakehouse-query-with-ibis`
A guide to querying the lakehouse using Ibis, a Python library that enables analytical queries through a pandas-like API without writing SQL directly. This tutorial includes:
- Connecting to the lakehouse with Ibis
- Constructing queries programmatically
- Translating analytical workflows from SQL to Python

#### 2. `lakehouse-materials-project-ibis.ipynb`
Querying the Materials Project data in the PSDI Lakehouse using Ibis. This tutorial covers:
- Exploring the structure of Materials Project tabular data in the lakehouse
- Querying the Materials Project tables using Ibis. This includes filtering and combining data from different
  tables, and making plots.

## Getting Started

To run the notebooks locally:
1. Clone this repository
2. Install the required dependencies (see environment/setup instructions if available)
3. Launch Jupyter or marimo and open the desired notebook
