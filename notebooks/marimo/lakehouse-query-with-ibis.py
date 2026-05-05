# /// script
# dependencies = ["ibis-framework", "pandas", "trino"]
# ///

import marimo

__generated_with = "0.23.4"
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

    - `ibis` for the query API,
    - `trino` for the underlying Trino connection,
    - and `pandas` for displaying tabular results nicely.

    You can install them via `pip`:
    """)
    return


@app.cell
def _():
    # packages added via marimo's package management: ibis-framework[trino] trino pandas !pip install -q "ibis-framework[trino]" trino pandas
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now let's import the required components:
    """)
    return


@app.cell
def _():
    import pandas as pd
    from pprint import pprint  # Used for clearer output in the tutorial

    import ibis
    from ibis.backends.trino import Backend

    from trino.dbapi import connect
    from trino.auth import OAuth2Authentication

    return Backend, OAuth2Authentication, connect, pprint


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Connect to Trino and hand the connection to Ibis

    Ibis can work on top of an existing Trino connection. After creating the Trino connection, we pass it to the Ibis backend.
    """)
    return


@app.cell
def _(Backend, OAuth2Authentication, connect):
    TRINO_HOST = "trino-dev.psdi.ac.uk"

    conn = connect(
        host=TRINO_HOST,
        port=443,
        http_scheme="https",
        auth=OAuth2Authentication(),
        catalog="lakekeeper",
        request_timeout=300,
    )

    # Hand the live Trino connection to Ibis
    con = Backend.from_connection(conn)

    print("\nConnected to the lakehouse successfully!")
    return con, conn


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. First checks

    Before exploring the data, it is useful to confirm that the connection works and that Ibis can access the catalog. To do this, let us list the available databases in the lakekeeper catalog:
    """)
    return


@app.cell
def _(con):
    con.list_databases(catalog="lakekeeper")
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

    So in this notebook:

    - Trino `catalog` = Ibis catalog = `lakekeeper`
    - Trino `schema` = Ibis `database`
    - Trino `table` = Ibis `table`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. List databases (schemas) in a catalog
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As we specified `catalog="lakekeeper"` when establishing the connection, it can be omitted in in subsequent queries.
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
    Note that some schemas contain only one table, for example `omol25`:
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
    ## 7. Load a table as an Ibis expression

    `con.table(...)` returns an Ibis table expression.

    At this point nothing has been loaded into pandas yet. You now have a lazy query object that you can inspect, transform, and execute.
    """)
    return


@app.cell
def _(con):
    table = con.table("absorption_flattened", database="materials_project")
    return (table,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Inspect column names and schema

    `table.schema()` returns the Ibis schema:
    """)
    return


@app.cell
def _(table):
    table_schema = table.schema()
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
    ## 9. Preview rows

    A quick preview is often the fastest way to understand a table.

    Use `head()` to request only the first few rows, then call `to_pandas()` or `execute()` to materialize the result.
    """)
    return


@app.cell
def _(table):
    preview = table.head(5).to_pandas()
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
def _(table):
    preview_1 = table.limit(2).execute()
    print(preview_1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 10. Count rows in a table

    Because Ibis expressions are lazy, the count is only computed when you execute the expression.
    """)
    return


@app.cell
def _(table):
    table.count().execute()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 11. A few common Ibis patterns

    Once you can discover and preview tables, the next step is usually to write real queries.

    Typical patterns include:

    - **selecting columns** with `table[[...]]` or `table.select(...)`,
    - **filtering rows** with `table.filter(...)`,
    - **aggregating** with `group_by(...).agg(...)`,
    - **sorting** with `order_by(...)`,
    - and **limiting** with `head(...)` or `limit(...)`.

    Example shape:

    ```python
    t = con.table("my_table", database=("lakekeeper", "my_database"))

    result = (
        t
        .filter(t.some_column.is_not_null())
        .select("some_column", "another_column")
        .head(10)
    )

    df = result.to_pandas()
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 12. OMol25 example

    Below are some example analytical queries for the OMol25 dataset.

    First let's load the `omol25` table as an Ibis expression:
    """)
    return


@app.cell
def _(con):
    table_1 = con.table('omol25', database='omol25')
    return (table_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 12.1 Selecting columns

    Select only a subset of columns:
    """)
    return


@app.cell
def _(table_1):
    table_1.select('composition', 'num_atoms').limit(2).execute()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 12.2 Filtering rows

    Get molecules with a defined (non-null) energy:
    """)
    return


@app.cell
def _(table_1):
    table_1.filter(table_1.nl_energy.notnull()).limit(2).execute()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    You can also combine conditions and use `select()` to specify the columns you want to keep:
    """)
    return


@app.cell
def _(table_1):
    table_1.filter(table_1.nl_energy.notnull() & (table_1.num_atoms > 10)).select('composition', 'num_atoms', 'nl_energy').limit(2).execute()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 12.3 Aggregation (group by)

    Get molecules with a defined (non-null) energy:
    """)
    return


@app.cell
def _(table_1):
    table_1.group_by(table_1.num_atoms).agg(count=table_1.count()).order_by(table_1.num_atoms).limit(3).execute()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ### 12.4 Sorting results

    Find molecules with the highest energy:
    """)
    return


@app.cell
def _(table_1):
    table_1.filter(table_1.nl_energy.notnull()).select('composition', 'nl_energy').order_by(table_1.nl_energy.desc()).limit(3).execute()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ### 12.5 Most common compositions
    """)
    return


@app.cell
def _(table_1):
    table_1.group_by(table_1.composition).agg(count=table_1.count()).order_by(lambda x: x['count'].desc()).limit(5).execute()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ### 12.6 Basic statistics

    Compute min, max, and average energy:
    """)
    return


@app.cell
def _(table_1):
    table_1.filter(table_1.nl_energy.notnull()).aggregate(min_nl=table_1.nl_energy.min(), max_nl=table_1.nl_energy.max(), avg_nl=table_1.nl_energy.mean()).execute()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 13. Notes for users (important)

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
    ## 14. Close the connection

    It is good practice to close your connection to Trino when it is not not longer needed, as each open connection holds server-side resources. You can do this by running:
    """)
    return


@app.cell
def _(conn):
    conn.close()
    return


if __name__ == "__main__":
    app.run()
