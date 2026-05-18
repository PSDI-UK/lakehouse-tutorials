# /// script
# dependencies = ["ibis-framework", "matplotlib", "pandas", "trino"]
# ///

import marimo

__generated_with = "0.23.1"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Querying Materials Project data in the PSDI datalake using Ibis
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In this notebook we use [Ibis](https://ibis-project.org/) to query tables in PSDI's lakehouse containing data from the [Materials Project](https://materialsproject.org).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 1. Prerequisites

    The following command installs the packages required for this notebook via `pip`:
    """)
    return


@app.cell
def _():
    # packages added via marimo's package management: trino matplotlib pandas ibis-framework[trino] !pip install -q trino matplotlib pandas "ibis-framework[trino]"
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now import the required resources:
    """)
    return


@app.cell
def _():
    import ibis
    from ibis.backends.trino import Backend

    from trino.dbapi import connect
    from trino.auth import OAuth2Authentication

    import pandas as pd   # Used for clearer output in the tutorial
    from pprint import pprint  # Used for clearer output in the tutorial

    import matplotlib.pyplot as plt

    return Backend, OAuth2Authentication, connect, plt, pprint


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 2. Set up

    To query the data we use PSDI's [Trino](https://trino.io/) server to process our queries. This Trino server acts as a middleman between us and the data. Our Ibis queries will be passed to Trino. Trino, which has direct access to the data (while we do not), will then process the query, compile the results, and pass the results back to us.

    First we must establish a connection with PSDI's Trino. Then we must link Ibis to this connection. Run the cell below to do this.
    """)
    return


@app.cell
def _(Backend, OAuth2Authentication, connect):
    TRINO_HOST = "trino-staging.psdi.ac.uk"

    conn = connect(
        host=TRINO_HOST,
        port=443,
        http_scheme="https",
        auth=OAuth2Authentication(),
        catalog="psdi",
        request_timeout=300,
    )

    # Hand the live Trino connection to Ibis
    con = Backend.from_connection(conn)
    return con, conn


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Note that the first time you run a query through this connection you will be prompted to authenticate via the PSDI Authentification system in your browser.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To check the connection, let's try to list the available databases in the `psdi` catalog. As mentioned above, you may be prompted to authenticate.
    """)
    return


@app.cell
def _(con):
    con.list_databases(catalog="psdi")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 3. Exploring the data

    Here we use the Materials Project's [AWS Open Data](https://materialsproject-build.s3.amazonaws.com/index.html). To elaborate, PSDI has taken various 'collections' of the [build data](https://materialsproject-build.s3.amazonaws.com/index.html) (which is provided in JSONL format) and converted them in to tables. (See [here](https://materialsproject-build.s3.amazonaws.com/index.html#collections/) to see the list of collections). We will query those tables.

    Various 'catalogs' are available through PSDI's Trino. The tables pertinent to this notebook are located in the `materials_project` database (where 'database' in this context means 'collection of tables') within the `psdi` catalog. Note that each table in the `materials_project` database corresponds to a 'collection' in the [build data](https://materialsproject-build.s3.amazonaws.com/index.html); e.g. the `absorption_flattened` table corresponds to the `absorption` collection.

    The following code lists all the tables in the `materials_project` database.
    """)
    return


@app.cell
def _(con, pprint):
    tables = con.list_tables(database="materials_project")
    pprint(tables)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To create a variable linked to a table, `con.table(...)` can be used. E.g.
    """)
    return


@app.cell
def _(con):
    dielectric_table = con.table("dielectric_flattened", database="materials_project")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### List columns in a table

    The *schema* of a table, i.e. its column names and data types (and often other information about columns) can be determined using `.schema()`. Below we use this to retrieve the schema of the `absorption_flattened` table.
    """)
    return


@app.cell
def _(con):
    absorption_table = con.table("absorption_flattened", database="materials_project")
    print(absorption_table.schema())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 4. Making graphs using data from the columns

    Assuming we know what columns we are interested in, we can combine columns, including columns from different tables, to make graphs showing correlations in materials properties. Note that the `material_id` column will be crucial to combining data from different tables, since this is a unique tag of a material in the Materials Projet
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plotting data from a single table

    Below are code snippets which plot two columns from the `absorption_flattened` table. First we plot `bandgap` versus `density`.

    Note that we are using `select` to filter out only the pertinent columns of the table, and `to_pandas()` to export the result of the filter to a Pandas DataFrame. Data in the DataFrame is then plotted. We do this a lot in the rest of this notebook.
    """)
    return


@app.cell
def _(con, plt):
    absorption_table_1 = con.table('absorption_flattened', database='materials_project')
    result = absorption_table_1.select('density', 'bandgap')
    df = result.to_pandas()
    plt.scatter(df['density'].tolist(), df['bandgap'].tolist(), color='blue', marker='o')
    plt.title('bandgap vs. density')
    plt.xlabel('density')
    plt.ylabel('bandgap')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Below we instead plot `energy_max` versus `density`.
    """)
    return


@app.cell
def _(con, plt):
    absorption_table_2 = con.table('absorption_flattened', database='materials_project')
    result_1 = absorption_table_2.select('density', 'energy_max')
    df_1 = result_1.to_pandas()
    plt.scatter(df_1['density'].tolist(), df_1['energy_max'].tolist(), color='blue', marker='o')
    plt.title('energy_max vs. density')
    plt.xlabel('density')
    plt.ylabel('energy_max')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Joining and plotting data from different tables

    Using a [SQL join](https://en.wikipedia.org/wiki/Join_(SQL)) operation over the `material_id` field we can combine data spread across many tables.

    Below we plot the `density` (renamed as `rho`) obtained from the `absorption_flattened` table versus the density from the `magnetism_flattened` table - for all structures which appear in both tables.
    """)
    return


@app.cell
def _(con, plt):
    absorption = con.table('absorption_flattened', database='materials_project')
    magnetism = con.table('magnetism_flattened', database='materials_project')
    result_2 = absorption.join(magnetism, absorption.material_id == magnetism.material_id, how='inner').select(absorption.density.name('absorption_rho'), magnetism.density.name('magnetism_rho'))
    df_2 = result_2.to_pandas()
    plt.scatter(df_2['absorption_rho'].tolist(), df_2['magnetism_rho'].tolist(), color='blue', marker='o')
    plt.title('Comparing material densities in absorption and magnetism data sets')
    plt.xlabel('absorption.density')
    plt.ylabel('magnetism.density')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    It is interesting that the densities from the two tables are not the same for a given structure.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Below we similarly plot the `density` obtained from the `absorption_flattened` table against the `bulk_modulus.voigt` property (renamed as `bulk_modulus`) in the `elasticity_flattened` table.
    """)
    return


@app.cell
def _(con, plt):
    absorption_1 = con.table('absorption_flattened', database='materials_project')
    elasticity = con.table('elasticity_flattened', database='materials_project')
    result_3 = absorption_1.join(elasticity, absorption_1.material_id == elasticity.material_id, how='inner').filter(elasticity['bulk_modulus.voigt'].notnull()).select(absorption_1.density.name('density'), elasticity['bulk_modulus.voigt'].name('bulk_modulus'))
    df_3 = result_3.to_pandas()
    plt.scatter(df_3['density'].tolist(), df_3['bulk_modulus'].tolist(), color='blue', marker='o')
    plt.title('Young modulus vs. density')
    plt.xlabel('density')
    plt.ylabel('young_modulus')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 5. Ibis queries versus the Materials Project API

    Examples of how to perform queries using the Materials Project API are given at https://docs.materialsproject.org/downloading-data/using-the-api/examples.

    Below we perform Ibis queries which reflect the aforementioned Materials Project API examples. Note that this is not a fair comparison since it is not like-for-like. For one thing the queries are on tables in the PSDI lakehouse derived from the 'build' open Materials Project data, not the 'main' Materials Project data which requires an API key to access.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### List the chemical formulae for all materials containing at least Si and O

    This is the Materials Project API code for the 'summary' data set (which we do not consider here because it is too big for casual demonstrations):

    ```
    from mp_api.client import MPRester

    with MPRester("your_api_key_here") as mpr:
        docs = mpr.materials.summary.search(
            elements=["Si", "O"], fields=["material_id", "band_gap", "formula_pretty"]
        )
        mpid_formula_dict = {
            doc.material_id: doc.formula_pretty for doc in docs
        }
    ```

    Below is an analogous Ibis query for the `dielectic_flattened` dataset. Note that I have exploited a regex to catch only the element symbol 'O' instead of using the glob pattern `%O%` which might match the element symbol 'Os' or 'Og'.
    """)
    return


@app.cell
def _(con):
    dielectric = con.table('dielectric_flattened', database='materials_project')
    result_4 = dielectric.filter(dielectric.formula_pretty.like('%Si%') & dielectric.formula_pretty.re_search('.*O[0-9]+.*')).select(dielectric.formula_pretty, dielectric.material_id)
    df_4 = result_4.to_pandas()
    print(df_4)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### List the band gaps for all materials containing only Si and O

    This is the Materials Project API code:

    ```
    from mp_api.client import MPRester

    with MPRester("your_api_key_here") as mpr:
        docs = mpr.materials.summary.search(
            chemsys="Si-O", fields=["material_id", "band_gap"]
        )
        mpid_bgap_dict = {doc.material_id: doc.band_gap for doc in docs}
    ```

    Below is an analogous query for the `absorption_flattened` data set. Note that we are using regular expression searches to find chemical formulae which contain`Si` and `O` (but not `Os` or `Og`).
    """)
    return


@app.cell
def _(con):
    absorption_2 = con.table('absorption_flattened', database='materials_project')
    result_5 = absorption_2.filter(absorption_2.formula_pretty.re_search('Si') & absorption_2.formula_pretty.re_search('O[^sg]*')).select(absorption_2.formula_pretty, absorption_2.material_id, absorption_2.bandgap)
    df_5 = result_5.to_pandas()
    print(df_5)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Find all Materials Project IDs for entries with dielectric data

    This is the Materials Project API code given in the documentation:
    ```
    from mp_api.client import MPRester
    from emmet.core.summary import HasProps

    with MPRester("your_api_key_here") as mpr:
        docs = mpr.materials.summary.search(
            has_props = [HasProps.dielectric], fields=["material_id"]
        )
        mpids = [doc.material_id for doc in docs]
    ```
    Below is an analogous query.
    """)
    return


@app.cell
def _(con):
    dielectric_1 = con.table('dielectric_flattened', database='materials_project')
    result_6 = dielectric_1.select(dielectric_1.material_id)
    df_6 = result_6.to_pandas()
    print(df_6)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Close connection to Trino

    It is good practice to close your connection to Trino when it is not not longer needed, as each open connection holds server-side resources. You can do this by running:
    """)
    return


@app.cell
def _(conn):
    conn.close()
    return


if __name__ == "__main__":
    app.run()
