# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "marimo",
#     "matplotlib",
#     "pandas",
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
    # Querying the PSDI lakehouse with Trino

    This notebook is a hands-on tutorial for querying the PSDI lakehouse through Trino.

    It covers:

    - connecting to Trino with PSDI authentication,
    - discovering schemas and tables,
    - running simple [SQL](https://en.wikipedia.org/wiki/SQL) queries,
    - and working through examples using the parsed [OMol25](https://arxiv.org/abs/2505.08762) dataset.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Install and import dependencies

    We will need the Trino Python client to fetch data, `pandas` to manage datasets and 'matplotlib' for plotting graphs.

    If you are using `uv`, those dependencies can be installed automatically via inline script metadata.

    Either way, the cell below will attempt to import them and install if missing.
    """)
    return


@app.cell
def _():
    packages = ["trino", "pandas", "matplotlib"]

    try:
        import matplotlib.pyplot as plt
        import pandas as pd
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
    return OAuth2Authentication, connect, pd, plt


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
    ## 1. Connect to Trino

    Run the cell below to open a connection. At the first run, you will be prompted to authenticate via the PSDI Authentication System in your browser.
    """)
    return


@app.cell
def _(OAuth2Authentication, connect):
    TRINO_HOST = "trino.psdi.ac.uk"

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
    return TRINO_HOST, conn


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Discover what is available in the lakehouse

    ### 2.1 Terminology

    In the lakehouse, data is organised in the following hierarchy:

    **catalog** --> **schema** --> **table**

    - **catalog**: a data source for Trino (in our case, `psdi`)
    - **schema**: corresponds to a *dataset* (e.g. `omol25`, `materials_project`)
    - **table**: a structured collection of records within a dataset (e.g. `alloy_pairs`)

    ---

    **Catalog**

    The catalog name in our case is `psdi`. It is specified when establishing the connection (`catalog="psdi"`), so it can optionally be omitted in queries.

    ---

    **Schema**

    The proper way to refer to a schema is `<catalog_name>.<schema_name>`
    (or just `<schema_name>` if the catalog is already set).

    Examples of schema names:
    - `psdi.omol25`
    - `psdi.materials_project`

    ---

    **Table**

    The proper way to refer to a table is `<catalog_name>.<schema_name>.<table_name>`
    (or `<schema_name>.<table_name>` if the catalog is already set).

    Examples of table names:
    - `psdi.omol25.omol25`
    - `psdi.materials_project.absorption`
    - `psdi.materials_project.alloys`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ### 2.2 What is SQL?

    [SQL (Structured Query Language)](https://en.wikipedia.org/wiki/SQL) is commonly used to query and analyze structured data stored in databases and lakehouses. It provides a standard way to retrieve, filter, aggregate, and organize data using declarative queries.

    In SQL, keywords such as `SELECT`, `FROM`, `WHERE`, and `GROUP BY` are conventionally written in uppercase to improve readability. Table names, column names, and other identifiers are commonly written in lowercase. SQL queries are typically written across multiple lines to make them easier to read and understand.

    For example:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```SQL
    SELECT formula_pretty, bandgap
    FROM psdi.materials_project.materials
    WHERE bandgap > 1.0
    LIMIT 5
    ```
    This query:

    - selects the columns `formula_pretty` and `bandgap`
    - reads data from the materials table
    - filters rows where the band gap is larger than 1.0
    - returns only the first 5 matching rows
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ### 2.3 General pattern for executing commands

    To execute SQL queries, you first need to create a **cursor object**, which represents an active SQL session. The recommended approach is to use a context manager:

    ```python
    with conn.cursor() as cursor:
        # Send SQL command to Trino for execution
        cursor.execute("<SQL coomand>")

        # Retrieve all results returned by Trino
        result = cursor.fetchall()
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ### 2.4 Listing available schemas

    This can be done using the SQL query `"SHOW SCHEMAS FROM psdi"`. Here is an example:
    """)
    return


@app.cell
def _(conn, pprint):
    with conn.cursor() as cursor_1:
        cursor_1.execute('SHOW SCHEMAS FROM psdi')
        schemas = cursor_1.fetchall()
        datasets = [schema[0] for schema in schemas]
        pprint(datasets)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Note that `information_schema` and `system` are system-level schemas and do not contain meaningful user data.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ### 2.5 Listing available tables within a schema

    Now let's have a closer look at the tables inside a particular schema, for example `materials_project`.
    """)
    return


@app.cell
def _(conn, pprint):
    with conn.cursor() as cursor_2:
        cursor_2.execute('SHOW TABLES FROM psdi.materials_project')
        tables = cursor_2.fetchall()
        pprint(tables)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Note that some schemas contain only one table, for example `omol25`:
    """)
    return


@app.cell
def _(conn, pprint):
    with conn.cursor() as cursor_3:
        cursor_3.execute('SHOW TABLES FROM psdi.omol25')
        tables_1 = cursor_3.fetchall()
        pprint(tables_1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### 2.6 Explore columns from a specific table

    To inspect column names and types in the specific table, you can run the `DESCRIBE` command followed by `<schema_name>.<table_name>`, for example:
    """)
    return


@app.cell
def _(conn, pprint):
    with conn.cursor() as cursor_4:
        cursor_4.execute('DESCRIBE psdi.omol25.omol25')
        columns = cursor_4.fetchall()
        pprint(columns)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `DESCRIBE` always returns 4 fields:
    - name (column name)
    - type (data type)
    - extra (additional metadata, if available)
    - comment (description of the column, if provided)

    The last two fields are often empty if no additional metadata or comments are defined.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### 2.7 Previewing data from a table

    To inspect a table, it is often useful to display a small number of rows.
    This can be done using the `SELECT` statement together with `LIMIT`.

    In SQL, the * symbol after `SELECT` means "select all columns" from the table.

    For example, the following query returns a single row from the `psdi.omol25.omol25` table, including all available columns:
    """)
    return


@app.cell
def _(conn, pprint):
    with conn.cursor() as cursor_5:
        cursor_5.execute('SELECT * FROM psdi.omol25.omol25 LIMIT 1')
        rows = cursor_5.fetchall()
        pprint(rows)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here:
    - `SELECT *` returns all columns
    - `FROM psdi.omol25.omol25` specifies the table
    - `LIMIT 1` restricts the output to one row only
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### 2.8 Counting rows in a table

    To count rows, you can use the following command
    ```python
    SELECT COUNT(*) FROM <catalog>.<schema>.<table>
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For example:
    """)
    return


@app.cell
def _(conn):
    with conn.cursor() as cursor_6:
        cursor_6.execute('SELECT COUNT(*) FROM psdi.omol25.omol25')
        rows_1 = cursor_6.fetchone()  # fetchone() returns a single tuple like (1234,)
        print('Row count:', rows_1[0])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Basic SQL patterns

    Here is a good general recipe for exploring any lakehouse table:

    1. List all available schemas using `SHOW SCHEMAS FROM <catalog>`.
    2. List all available tables in a given schema using `SHOW TABLES FROM <catalog>.<schema>`.
    3. Inspect the columns of a table using `DESCRIBE <catalog>.<schema>.<table>`.
    4. Count rows in the table using `SELECT COUNT(*) FROM <catalog>.<schema>.<table>`.
    5. Preview data from the table using `SELECT * FROM <catalog>.<schema>.<table> LIMIT 1`.
    6. Then write analytical queries of your interest. The most commonly used SQL commands include `SELECT`, `COUNT(*)`, `GROUP BY`, and `ORDER BY`.

    ---

    ### Understanding common SQL patterns

    **`SELECT`**
    Used to retrieve data from a table. You can select all columns or only specific ones. In the following examples, we retrieve 5 rows.

    ```sql
    SELECT *
    FROM psdi.materials_project.absorption
    LIMIT 5
    ```
    ```sql
    SELECT nsites, formula_pretty
    FROM psdi.materials_project.absorption
    LIMIT 5
    ```

    **`COUNT(*)`**
    Counts the number of rows in a table or within a group.
    ```sql
    SELECT COUNT(*)
    FROM psdi.materials_project.absorption
    ```

    **`GROUP BY`**
    Groups rows that share the same values in specified columns.
    Often used together with aggregation functions like `COUNT`, `AVG`, etc.

    Example: count how many entries exist for each element:
    ```sql
    SELECT nsites, COUNT(*)
    FROM psdi.materials_project.absorption
    GROUP BY nsites
    ```

    **`ORDER BY`**
    Sorts the results of a query.
    ```sql
    SELECT nsites, COUNT(*) AS count
    FROM psdi.materials_project.absorption
    GROUP BY nsites
    ORDER BY count DESC
    ```

    - ASC --> ascending order (default)
    - DESC --> descending order

    **Putting it all together**

    These commands are often combined to answer questions about the data.

    For example, to find the most common elements:
    ```sql
    SELECT formula_pretty, COUNT(*) AS count
    FROM psdi.materials_project.absorption
    GROUP BY formula_pretty
    ORDER BY count DESC
    LIMIT 10
    ```

    This query:
    1. selects a column (`SELECT`)
    2. counts occurrences (`COUNT(*)`)
    3. groups results (`GROUP BY`)
    4. sorts them (`ORDER BY`)
    5. limits the output (`LIMIT`)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. OMol25 example

    [OMol25](https://arxiv.org/abs/2505.08762) is a large-scale molecular dataset containing computational data for organic molecules.

    Below are some example analytical queries for the OMol25 dataset.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4.1 Distribution of number of atoms

    This query computes the distribution of molecules by their number of atoms.
    It groups rows by the `num_atoms` column and counts how many molecules fall into each group.

    - `SELECT`: Specifies the columns to return. Here, it also calculates the number of occurrences using `COUNT(*)`.
    - `FROM`: Indicates the source table (`psdi.omol25.omol25`).
    - `GROUP BY num_atoms`: Aggregates rows that have the same number of atoms.
    - `COUNT(*)`: Counts how many rows (molecules) are in each group.
    - `ORDER BY num_atoms`: Sorts the results in ascending order of the number of atoms.
    """)
    return


@app.cell
def _(conn):
    with conn.cursor() as cursor_7:
        cursor_7.execute("""
        SELECT num_atoms, COUNT(*)
        FROM psdi.omol25.omol25
        GROUP BY num_atoms
        ORDER BY num_atoms
        """)

        data = cursor_7.fetchall()
        print('Data fetched successfully.')
    return (data,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now, let's plot the data using `matplotlib`.
    """)
    return


@app.cell
def _(data, plt):
    # Unzip the tuples into two separate lists: (num_atoms, counts)
    num_atoms, counts = zip(*data)

    plt.figure(figsize=(6, 4))
    plt.bar(num_atoms, counts, color="teal")
    plt.xlabel("Number of Atoms")
    plt.ylabel("Count")
    plt.title("Atom Distribution")
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### 4.2 Charge distribution

    This query calculates the distribution of molecules by their formal charge.
    It groups molecules by the charge column and counts how many molecules fall into each charge category.

    - `SELECT`: Specifies the columns to return. Here, it selects the `charge` column and also calculates the number of occurrences using `COUNT(*)`.
    - `FROM`: Indicates the source table (`psdi.omol25.omol25`).
    - `GROUP BY charge`: Collects all rows with the same charge value.
    - `COUNT(*)`: Computes how many molecules are in each charge group.
    - `ORDER BY charge`: Sorts results from lowest to highest charge.
    """)
    return


@app.cell
def _(conn):
    with conn.cursor() as cursor_8:
        cursor_8.execute("""
        SELECT charge, COUNT(*)
        FROM psdi.omol25.omol25
        GROUP BY charge
        ORDER BY charge
        """)

        for row in cursor_8.fetchall():
            print(row)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### 4.3 Most common compositions

    The query retrieves the 20 most frequent values of the composition column from the `psdi.omol25.omol25` table.

    It uses several standard SQL commands:

    - `SELECT`: Specifies the columns to return. Here, it selects `composition` and calculates the number of occurrences using `COUNT(*)`, aliased as `count`.
    - `FROM`: Indicates the source table (`psdi.omol25.omol25`).
    - `GROUP BY`: Groups rows by composition so that the count can be computed for each unique value.
    - `ORDER BY`: Sorts the results in descending order based on the computed count. `DESC` means the results are ordered from highest to lowest.
    - `LIMIT 5`: Restricts the output to the top 5 results.
    """)
    return


@app.cell
def _(conn):
    with conn.cursor() as cursor_9:
        cursor_9.execute("""
        SELECT composition, COUNT(*) AS count
        FROM psdi.omol25.omol25
        GROUP BY composition
        ORDER BY count DESC
        LIMIT 5
        """)

        for row_1 in cursor_9.fetchall():
            print(row_1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### 4.4 Non-local correlation energy statistics

    This query calculates basic statistics for the non-local correlation energy column, `nl_energy`, in the `psdi.omol25.omol25` table. Specifically, it returns the minimum, maximum, and average values, excluding any missing (`NULL`) entries.

    1. `SELECT`: Specifies the values to return. Here, it computes aggregate statistics and returns them as aliases `(min_nl, max_nl, avg_nl)`:
        - `MIN(nl_energy)` --> the smallest value
        - `MAX(nl_energy)` --> the largest value
        - `AVG(nl_energy)` --> the average value
    2. `FROM`: Indicates the source table (`psdi.omol25.omol25`).
    3. `WHERE`: Filters out rows where `nl_energy` is `NULL`, ensuring that only valid numeric values are used in the calculations.
    """)
    return


@app.cell
def _(conn):
    with conn.cursor() as cursor_10:
        cursor_10.execute("""
        SELECT
            MIN(nl_energy) AS min_nl,
            MAX(nl_energy) AS max_nl,
            AVG(nl_energy) AS avg_nl
        FROM psdi.omol25.omol25
        WHERE nl_energy IS NOT NULL
        """)

        print('Min, max and average energies:')
        print(cursor_10.fetchone())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### 4.5 Using pandas for post-processing of Trino query results

    When working with large datasets, it is inefficient to load all rows into memory. Instead, you should perform heavy computations (such as grouping and aggregation) in Trino, and use `pandas` only for lightweight post-processing of the reduced result set.

    The query below retrieves a small sample of rows (non-null `nl_energy` values) from the `psdi.omol25.omol25` table. The result is then loaded into a pandas DataFrame for further analysis.
    """)
    return


@app.cell
def _(conn, pd):
    with conn.cursor() as cursor_11:
        cursor_11.execute("""
        SELECT composition, nl_energy
        FROM psdi.omol25.omol25
        WHERE nl_energy IS NOT NULL
        LIMIT 100
        """)

        # Load results into a pandas DataFrame
        df = pd.DataFrame(cursor_11.fetchall(), columns=[col[0] for col in cursor_11.description])

    # Print top rows
    print(df.head())
    # Compute average nl_energy per composition (on the sampled data)
    print(df.groupby('composition')['nl_energy'].mean())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Close connection to Trino
    It is good practice to close your connection to Trino when it is not not longer needed, as each open connection holds server-side resources. You can do this by running:
    """)
    return


@app.cell
def _(conn):
    conn.close()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    An alternative approach is using context manager, which will automatically close the connection. To do that, you can use the following auxiliary function:
    """)
    return


@app.cell
def _(OAuth2Authentication, TRINO_HOST, connect):
    def get_connection(host: str):
        try:
            conn = connect(
                host=TRINO_HOST,
                port=443,
                http_scheme="https",
                auth=OAuth2Authentication(),
                catalog="psdi",
                request_timeout=300,
            )

            # Validate the connection
            with conn.cursor() as cursor:
                cursor.execute("SHOW SCHEMAS")
                cursor.fetchone()

            print("\nConnected to Trino successfully!")
            return conn
        except Exception as e:
            print("\nFailed to connect to Trino")
            raise

    return (get_connection,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Then you can use the following pattern for quering the lakehouse:
    """)
    return


@app.cell
def _(get_connection):
    TRINO_HOST_1 = 'trino.psdi.ac.uk'
    with get_connection(TRINO_HOST_1) as conn_1:
        with conn_1.cursor() as cursor_12:
            cursor_12.execute('SHOW SCHEMAS FROM psdi')
            schemas_1 = cursor_12.fetchall()
            print(schemas_1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Troubleshooting

    If something fails:

    - confirm the Keycloak login completed successfully,
    - run `SHOW SCHEMAS FROM <catalog>` to list all available shemas(datasets),
    - run `SHOW TABLES FROM <catalog>.<schema>` to check the actual table name,
    - and then inspect columns by running `DESCRIBE <catalog>.<schema_name>.<table_name>`.
    """)
    return


if __name__ == "__main__":
    app.run()
