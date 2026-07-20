# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "ibis-framework[duckdb,trino]",
#     "marimo",
#     "trino",
# ]
# ///

import marimo

__generated_with = "0.23.6"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Querying the PSDI Lakehouse with Ibis

    [Ibis](https://ibis-project.org/) is a Python library that lets you write analytical queries using a pandas-like API, which are then executed efficiently on SQL-based backends such as Trino.

    This notebook is a practical introduction to using **Ibis** to query the PSDI lakehouse.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Why use Ibis?

    Common reasons to use Ibis include:

    - **One Python API across many backends**: Trino, DuckDB, PostgreSQL, BigQuery, and others.
    - **Less data movement**: the backend does the heavy lifting.
    - **Readable code**: it often looks more like working with dataframes than writing raw SQL.
    - **Easy interoperability**: results can be turned into pandas DataFrames when needed.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Install dependencies

    In this notebook we will use:
    - `ibis` for the query API
    - `trino` for the underlying Trino connection

    If you are using `uv`, those dependencies can be installed automatically via inline script metadata.

    Either way, the cell below will attempt to import them and install if missing.
    """)
    return


@app.cell
def _():
    packages = ["ibis-framework[trino]", "trino"]

    try:
        import ibis
        from ibis.backends.trino import Backend
        from trino.dbapi import connect
        from trino.auth import OAuth2Authentication
    except ImportError:
        import shutil
        import subprocess
        import sys
        try:
            subprocess.run(["uv", "pip", "install", "--python", sys.executable, *packages], check=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            subprocess.run([sys.executable, "-m", "pip", "install", "--user", *packages], check=True)
    return Backend, OAuth2Authentication, connect


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's also import `pprint` for clearer output in the tutorial.
    """)
    return


@app.cell
def _():
    from pprint import pprint

    return (pprint,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Connect to Trino and hand the connection to Ibis

    Ibis can work on top of an existing Trino connection. After creating the Trino connection, we pass it to the Ibis backend.
    """)
    return


@app.cell
def _(Backend, OAuth2Authentication, connect):
    TRINO_HOST = "trino.psdi.ac.uk"

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
    Note that authentication is only triggered when you first execute a query through this connection.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. First checks

    Before exploring the data, it is useful to confirm that the connection works and that Ibis can access the catalog. To do this, let us list the available databases in the `psdi` catalog.

    When you execute this query for the first time, you will be prompted to authenticate via the PSDI authentication system. You can use your institutional credentials for this. A browser window will open automatically for the authentication step.
    """)
    return


@app.cell
def _(con):
    con.list_databases(catalog="psdi")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Understanding the hierarchy

    The lakehouse is organized as:

    **catalog → schema → table**

    In Ibis terminology, the hierarchy is usually described as:

    **catalog → database → table**

    As you can see, the Trino *schema* corresponds to what Ibis calls a *database*.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. List databases in a catalog
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This can be done using `list_databases()`. As we specified `catalog="psdi"` when establishing the connection, the catalog name can be omitted from subsequent queries:
    """)
    return


@app.cell
def _(con, pprint):
    databases = con.list_databases()
    pprint(databases)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. List tables in a database
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
    Note that some databases contain only one table, for example `omol25`:
    """)
    return


@app.cell
def _(con, pprint):
    tables_1 = con.list_tables(database='omol25')
    pprint(tables_1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Load a table as an Ibis expression

    `con.table(...)` returns an Ibis table expression.

    At this point nothing has been loaded into pandas yet. You now have a lazy query object that you can inspect, transform, and execute.
    """)
    return


@app.cell
def _(con):
    dielectric_table = con.table("dielectric", database="materials_project")
    return (dielectric_table,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9. Inspect column names and schema

    `.schema()` returns the Ibis schema:
    """)
    return


@app.cell
def _(dielectric_table):
    table_schema = dielectric_table.schema()
    print(table_schema)
    return (table_schema,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The column names can be listed as
    """)
    return


@app.cell
def _(table_schema):
    column_names = list(table_schema.fields.keys())
    print(column_names)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 10. Preview rows

    A quick preview is often the fastest way to understand a table.

    Use `head()` to request only the first two rows, then call `to_pandas()` or `execute()` to materialize the result.
    """)
    return


@app.cell
def _(dielectric_table):
    preview = dielectric_table.head(2).to_pandas()
    print(preview)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    Alternatively, you can use `limit()` in combination with `execute()`:
    """)
    return


@app.cell
def _(dielectric_table):
    preview_1 = dielectric_table.limit(2).execute()
    print(preview_1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 11. Count rows in a table

    Because Ibis expressions are lazy, the count is only computed when you execute the expression.
    """)
    return


@app.cell
def _(dielectric_table):
    dielectric_table.count().execute()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 12. A few common Ibis patterns

    Once you can discover and preview tables, the next step is usually to write real queries.

    Typical patterns include:

    - **selecting columns** with `table[[...]]` or `table.select(...)`,
    - **filtering rows** with `table.filter(...)`,
    - **aggregating** with `group_by(...).agg(...)`,
    - **sorting** with `order_by(...)`,
    - and **limiting** with `head(...)` or `limit(...)`.

    Example shape:

    ```python
    t = con.table("my_table", database=("psdi", "my_database"))

    result = (
        t
        .filter(t.some_column.is_not_null())
        .select("some_column", "another_column")
        .head(10)
    )

    df = result.to_pandas()
    ```

    Note that all expressions that end with `.execute()` or `.to_pandas()` return a pandas DataFrame. Without one of these calls, the result is a lazy ibis expression - the query is built but not yet run against the database.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 13. OMol25 example

    Below are some example analytical queries for the OMol25 dataset.

    First let's load the `omol25` table as an Ibis expression:
    """)
    return


@app.cell
def _(con):
    omol25_table = con.table("omol25", database="omol25")
    return (omol25_table,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 13.1 Selecting columns

    Select only a subset of columns:
    """)
    return


@app.cell
def _(omol25_table):
    omol25_table.select("composition", "num_atoms").limit(2).execute()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 13.2 Filtering rows

    Get molecules with a defined (non-null) energy:
    """)
    return


@app.cell
def _(omol25_table):
    omol25_table.filter(omol25_table.nl_energy.notnull()).limit(2).execute()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    You can also combine conditions and use `select()` to specify the columns you want to keep:
    """)
    return


@app.cell
def _(omol25_table):
    omol25_table.filter(
        (omol25_table.nl_energy.notnull()) & (omol25_table.num_atoms > 10)
    ).select("composition", "num_atoms", "nl_energy").limit(2).execute()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 13.3 Aggregation (group by)

    Get molecules with a defined (non-null) energy:
    """)
    return


@app.cell
def _(omol25_table):
    (
        omol25_table
        .group_by(omol25_table.num_atoms)
        .agg(count=omol25_table.count())
        .order_by(omol25_table.num_atoms)
        .limit(3)
        .execute()
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ### 13.4 Sorting results

    Find molecules with the highest energy:
    """)
    return


@app.cell
def _(omol25_table):
    (
        omol25_table
        .filter(omol25_table.nl_energy.notnull())
        .select("composition", "nl_energy")
        .order_by(omol25_table.nl_energy.desc())
        .limit(3)
        .execute()
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ### 13.5 Most common compositions
    """)
    return


@app.cell
def _(omol25_table):
    (
        omol25_table
        .group_by(omol25_table.composition)
        .agg(count=omol25_table.count())
        .order_by(lambda x: x["count"].desc())
        .limit(4)
        .execute()
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ### 13.6 Basic statistics

    Compute min, max, and average energy:
    """)
    return


@app.cell
def _(omol25_table):
    (
        omol25_table
        .filter(omol25_table.nl_energy.notnull())
        .aggregate(
            min_nl=omol25_table.nl_energy.min(),
            max_nl=omol25_table.nl_energy.max(),
            avg_nl=omol25_table.nl_energy.mean(),
        )
        .execute()
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 14. Notes for users (important)

    Analytical queries may take time on large lakehouse tables.

    To improve performance:

    - select only necessary columns
    - use `limit()`
    - apply filters where possible
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 15. Close the connection

    It is good practice to close your connection to Trino when it is not not longer needed, as each open connection holds server-side resources. You can do this by running:
    """)
    return


@app.cell
def _(conn):
    conn.close()
    return


if __name__ == "__main__":
    app.run()
