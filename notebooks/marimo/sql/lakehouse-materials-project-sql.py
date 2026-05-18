# /// script
# dependencies = ["matplotlib", "pandas", "trino"]
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
    # Querying Materials Project data in the PSDI datalake using SQL
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In this notebook we use [SQL (Structured Query Language)](https://en.wikipedia.org/wiki/SQL) to query tables of [Materials Project](https://materialsproject.org) data housed in PSDI's data lakehouse.
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
    # packages added via marimo's package management: trino matplotlib pandas !pip install -q trino matplotlib pandas
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now import the required resources:
    """)
    return


@app.cell
def _():
    from trino.dbapi import connect
    from trino.auth import OAuth2Authentication

    import pandas as pd

    import matplotlib.pyplot as plt

    return OAuth2Authentication, connect, pd, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 1. Set up

    To query the data we use PSDI's [Trino](https://trino.io/) server to process our queries. This Trino server acts as a middleman between us and the data. Our SQL queries will be passed to Trino. Trino, which has direct access to the data (while we do not), will then process the query, compile the results, and pass the results back to us.

    First we must establish a connection with PSDI's Trino. Run the cell below to do this. Note that the first time you run the cell you will be prompted to authenticate via the PSDI Authentification system in your browser.
    """)
    return


@app.cell
def _(OAuth2Authentication, connect):
    TRINO_HOST = "trino-staging.psdi.ac.uk"

    try:
        conn = connect(
            host=TRINO_HOST,
            port=443,
            http_scheme="https",
            auth=OAuth2Authentication(),
            catalog="psdi",
            request_timeout=300,
        )
    
        cursor = conn.cursor()

        # Validate the connection
        cursor.execute("SHOW SCHEMAS FROM psdi")
        cursor.fetchone()
    
        print("\nConnected to Trino successfully!")

    except Exception as e:
        print("\nFailed to connect to Trino")
        raise
    return (conn,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 3. Exploring the data

    Here we use the Materials Project's [AWS Open Data](https://materialsproject-build.s3.amazonaws.com/index.html). To elaborate, PSDI has taken various 'collections' of the [build data](https://materialsproject-build.s3.amazonaws.com/index.html) (which is provided in JSONL format) and converted them in to tables. (See [here](https://materialsproject-build.s3.amazonaws.com/index.html#collections/) to see the list of collections). We will query those tables.

    Various 'catalogs' are available through PSDI's Trino. The tables pertinent to this notebook are located in the `materials_project` 'schema' (where 'schema' in this context means 'collection of tables') within the `psdi` catalog. Note that each table in the `materials_project` schema corresponds to a 'collection' in the [build data](https://materialsproject-build.s3.amazonaws.com/index.html); e.g. the `absorption_flattened` table corresponds to the `absorption` collection.

    The following code lists all the tables in the `materials_project` schema. Note that we pipe the results of the SQL query `SHOW TABLES FROM materials_project`, something returned by `cursor.fetchall()`, into a Pandas DataFrame for ease of viewing the results; `cursor.fetchall()` returns a list of lists which is cumbersome. We use DataFrames similarly throughout this notebook.
    """)
    return


@app.cell
def _(conn, pd):
    with conn.cursor() as cursor_1:
        cursor_1.execute('SHOW TABLES FROM materials_project')
        df = pd.DataFrame(cursor_1.fetchall(), columns=[col[0] for col in cursor_1.description])
        print(df)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### List columns in a table

    The structure of a table (i.e. its column names, data types and often other information about columns - something often referred to as its *schema*) can be determined using the `DESCRIBE` command. For a given table
    `DESCRIBE` always returns 4 fields describing each column:
    1. `Column`: the name of the column
    2. `Type`: its data type
    3. `Extra`: additional metadata, if available
    4. `Comment`: a comment, i.e. a description of the column, if provided

    The last two fields are often empty if no additional metadata or comments are defined.

    Below we use `DESCRIBE` to probe the structure of the `absorption_flattened` table.
    """)
    return


@app.cell
def _(conn, pd):
    with conn.cursor() as cursor_2:
        cursor_2.execute('DESCRIBE materials_project.absorption_flattened')
        df_1 = pd.DataFrame(cursor_2.fetchall(), columns=[col[0] for col in cursor_2.description])
        print(df_1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 4. Making graphs using data from the columns

    Assuming we know what columns we are interested in, we can combine columns, including columns from different tables, to make graphs showing correlations in materials properties. Note that the `material_id` column will be crucial to combining data from different tables, since this is a unique tag of a material in the Materials Projet.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Plotting data from a single table

    Below are code snippets which plot two columns from the `absorption_flattened` table. First we plot `bandgap` versus `density`.
    """)
    return


@app.cell
def _(conn, pd, plt):
    with conn.cursor() as cursor_3:
        cursor_3.execute('SELECT density,bandgap FROM materials_project.absorption_flattened')
        df_2 = pd.DataFrame(cursor_3.fetchall(), columns=[col[0] for col in cursor_3.description])
    plt.scatter(df_2['density'].tolist(), df_2['bandgap'].tolist(), color='blue', marker='o')
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
def _(conn, pd, plt):
    with conn.cursor() as cursor_4:
        cursor_4.execute('SELECT density,energy_max FROM materials_project.absorption_flattened')
        df_3 = pd.DataFrame(cursor_4.fetchall(), columns=[col[0] for col in cursor_4.description])
    plt.scatter(df_3['density'].tolist(), df_3['energy_max'].tolist(), color='blue', marker='o')
    plt.title('energy_max vs. density')
    plt.xlabel('density')
    plt.ylabel('energy_max')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Joining and plotting data from different tables

    Using a SQL [join](https://en.wikipedia.org/wiki/Join_(SQL)) operation over the `material_id` field we can combine data spread across many tables.

    Below we plot the `density` (renamed as `rho`) obtained from the `absorption_flattened` table versus the density from the `magnetism_flattened` table - for all structures which appear in both tables.
    """)
    return


@app.cell
def _(conn, pd, plt):
    with conn.cursor() as cursor_5:
        cursor_5.execute('\n    SELECT absorption.density AS absorption_rho, magnetism.density AS magnetism_rho\n    FROM materials_project.absorption_flattened AS absorption\n    INNER JOIN materials_project.magnetism_flattened AS magnetism ON absorption.material_id = magnetism.material_id\n    ')
        df_4 = pd.DataFrame(cursor_5.fetchall(), columns=[col[0] for col in cursor_5.description])
    plt.scatter(df_4['absorption_rho'].tolist(), df_4['magnetism_rho'].tolist(), color='blue', marker='o')
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
def _(conn, pd, plt):
    with conn.cursor() as cursor_6:
        cursor_6.execute('\n    SELECT absorption.density AS density, elasticity."bulk_modulus.voigt" AS bulk_modulus\n    FROM materials_project.absorption_flattened AS absorption\n    INNER JOIN materials_project.elasticity_flattened AS elasticity ON absorption.material_id = elasticity.material_id \n    WHERE elasticity."bulk_modulus.voigt" IS NOT NULL\n    ')
        df_5 = pd.DataFrame(cursor_6.fetchall(), columns=[col[0] for col in cursor_6.description])
    plt.scatter(df_5['density'].tolist(), df_5['bulk_modulus'].tolist(), color='blue', marker='o')
    plt.title('Young modulus vs. density')
    plt.xlabel('density')
    plt.ylabel('young_modulus')
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 5. SQL queries versus the Materials Project API

    Examples of how to perform queries using the Materials Project API are given at https://docs.materialsproject.org/downloading-data/using-the-api/examples.

    Below we perform SQL queries which reflect the aforementioned Materials Project API examples. Note that this is not a fair comparison since it is not like-for-like. For one thing the SQL queries are on tables in the PSDI lakehouse derived from the 'build' open Materials Project data, not the 'main' Materials Project data which requires an API key to access.
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

    Below is an analogous SQL query for the `dielectic_flattened` dataset. Note that I have exploited a regex to catch only the element symbol 'O' instead of using the glob pattern `%O%` which might match the element symbols 'Os' or 'Og'.
    """)
    return


@app.cell
def _(conn, pd):
    with conn.cursor() as cursor_7:
        cursor_7.execute("\n    SELECT formula_pretty, material_id\n    FROM materials_project.dielectric_flattened\n    WHERE formula_pretty LIKE '%Si%'\n    AND REGEXP_LIKE(formula_pretty,'.*O[0-9]+.*')\n    ")
        df_6 = pd.DataFrame(cursor_7.fetchall(), columns=[col[0] for col in cursor_7.description])
    print(df_6)
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

    Below is an analogous query for the `absorption_flattened` data set. Note that we are using regular expressions to find chemical formulae which match `Si` and `O` (but not `Os` or `Og`)
    """)
    return


@app.cell
def _(conn, pd):
    with conn.cursor() as cursor_8:
        cursor_8.execute("\n    SELECT formula_pretty, material_id, bandgap \n    FROM materials_project.absorption_flattened\n    WHERE regexp_like(formula_pretty,'Si') AND regexp_like(formula_pretty,'O[^sg]*')\n    ")
        df_7 = pd.DataFrame(cursor_8.fetchall(), columns=[col[0] for col in cursor_8.description])
    print(df_7)
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
    Below is an analogous SQL query.
    """)
    return


@app.cell
def _(conn, pd):
    with conn.cursor() as cursor_9:
        cursor_9.execute('SELECT material_id FROM materials_project.dielectric_flattened')
        df_8 = pd.DataFrame(cursor_9.fetchall(), columns=[col[0] for col in cursor_9.description])
    print(df_8)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
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
