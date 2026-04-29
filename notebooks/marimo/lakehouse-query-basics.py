# /// script
# dependencies = ["pandas", "trino"]
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
    # Querying the PSDI lakehouse with Trino

    This notebook is a hands-on tutorial for querying the PSDI lakehouse through Trino.

    It covers:

    - connecting to Trino with PSDI authentication,
    - discovering schemas and tables,
    - running simple SQL queries,
    - and working through examples using the parsed [OMol25](adf) dataset.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Install and import dependencies

    We will need the Trino Python client to fetch data and `pandas` to manage datasets.
    """)
    return


@app.cell
def _():
    # packages added via marimo's package management: trino pandas !pip install -q trino pandas
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now let's import the required components:
    """)
    return


@app.cell
def _():
    from pprint import pprint  # Used for clearer output in the tutorial

    import pandas as pd

    from trino.dbapi import connect
    from trino.auth import OAuth2Authentication

    return OAuth2Authentication, connect, pd, pprint


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Connect to Trino

    Run the cell below to open a connection. At the first run, you will be prompted to authenticate via the PSDI Authentification system in your browser.
    """)
    return


@app.cell
def _(OAuth2Authentication, connect):
    TRINO_HOST = "trino-dev.psdi.ac.uk"

    try:
        conn = connect(
            host=TRINO_HOST,
            port=443,
            http_scheme="https",
            auth=OAuth2Authentication(),
            catalog="lakekeeper",
            request_timeout=300,
        )
    
        cursor = conn.cursor()

        # Validate the connection
        cursor.execute("SHOW SCHEMAS FROM lakekeeper")
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

    - **catalog**: a data source for Trino (in our case, `lakekeeper`)
    - **schema**: corresponds to a *dataset* (e.g. `omol25`, `materials_project`)
    - **table**: a structured collection of records within a dataset (e.g. `alloy_pairs`)

    ---

    **Catalog**

    The catalog name in our case is `lakekeeper`. It is specified when establishing the connection (`catalog="lakekeeper"`), so it can usually be omitted in queries.

    ---

    **Schema**

    The proper way to refer to a schema is `<catalog_name>.<schema_name>`
    (or just `<schema_name>` if the catalog is already set).

    Examples of schema names:
    - `lakekeeper.omol25`
    - `lakekeeper.materials_project`

    ---

    **Table**

    The proper way to refer to a table is `<catalog_name>.<schema_name>.<table_name>`
    (or `<schema_name>.<table_name>` if the catalog is already set).

    Examples of table names:
    - `lakekeeper.omol25.omol25`
    - `lakekeeper.materials_project.absorption_flattened`
    - `lakekeeper.materials_project.alloys_flattened`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.2 General pattern for executing commands

    To execute SQL queries, you first need to create a **cursor object**, which represents an active SQL session. The recommended approach is to use a context manager:

    ```python
    with conn.cursor() as cursor:
        cursor.execute("<SQL coomand>")
        result = cursor.fetchall()
    ```

    Within the context manager:
    - `cursor.execute("<SQL command>")`: sends a SQL command to Trino for execution.
    - `cursor.fetchall()`: retrieves all results returned by Trino.
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.3 Listing available schemas

    The following code lists all available schemas (i.e. datasets), excluding system ones:
    """)
    return


@app.cell
def _(conn, pprint):
    with conn.cursor() as cursor_1:
        cursor_1.execute('SHOW SCHEMAS FROM lakekeeper')
        schemas = cursor_1.fetchall()
        exclude = {'information_schema', 'system'}
        datasets = [s[0] for s in schemas if s[0] not in exclude]  # Exclude system schemas
        pprint(datasets)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Note that we haven't inluded the catalog name, `lakekeeper`, in the query as it was specified when establishing the connection. However, you can optionally include it by using the command `SHOW SCHEMAS FROM lakekeeper`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ### 2.4 Listing available tables within a schema

    Now let's have a closer look at the tables inside a particular schema, for example `materials_project`.
    """)
    return


@app.cell
def _(conn, pprint):
    with conn.cursor() as cursor_2:
        cursor_2.execute('SHOW TABLES FROM lakekeeper.materials_project')
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
        cursor_3.execute('SHOW TABLES FROM lakekeeper.omol25')
        tables_1 = cursor_3.fetchall()
        pprint(tables_1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### 2.5 Explore columns from a specific table

    To inspect column names and types in the specific table, you can run the `DESCRIBE` command followed by `<schema_name>.<table_name>`, for example:
    """)
    return


@app.cell
def _(conn, pprint):
    with conn.cursor() as cursor_4:
        cursor_4.execute('DESCRIBE lakekeeper.omol25.omol25')
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
    ### 2.6 Previewing data from a table

    To inspect a table, it is often useful to display a small number of rows.
    This can be done using the `SELECT` statement together with `LIMIT`.

    For example, the following query returns a single row from the `omol25.omol25` table:
    """)
    return


@app.cell
def _(conn, pprint):
    with conn.cursor() as cursor_5:
        cursor_5.execute('SELECT * FROM lakekeeper.omol25.omol25 LIMIT 1')
        rows = cursor_5.fetchall()
        pprint(rows)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### 2.7 Counting rows in a table

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
        cursor_6.execute('SELECT COUNT(*) FROM lakekeeper.omol25.omol25')
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
    FROM lakekeeper.materials_project.alloy_pairs_flattened
    LIMIT 5
    ```
    ```sql
    SELECT column_name_a, column_name_b
    FROM lakekeeper.materials_project.alloy_pairs_flattened
    LIMIT 5
    ```

    **`COUNT(*)`**
    Counts the number of rows in a table or within a group.
    ```sql
    SELECT COUNT(*)
    FROM lakekeeper.materials_project.alloy_pairs_flattened
    ```

    **`GROUP BY`**
    Groups rows that share the same values in specified columns.
    Often used together with aggregation functions like `COUNT`, `AVG`, etc.

    Example: count how many entries exist for each element:
    ```sql
    SELECT column_name_a, COUNT(*)
    FROM lakekeeper.materials_project.alloy_pairs_flattened
    GROUP BY column_name_a
    ```

    **`ORDER BY`**
    Sorts the results of a query.
    ```sql
    SELECT column_name_a, COUNT(*) AS count
    FROM lakekeeper.materials_project.alloy_pairs_flattened
    GROUP BY column_name_a
    ORDER BY count DESC
    ```

    - ASC --> ascending order (default)
    - DESC --> descending order

    **Putting it all together**
    These commands are often combined to answer questions about the data.

    For example, to find the most common elements:
    ```sql
    SELECT column_name_a, COUNT(*) AS count
    FROM lakekeeper.materials_project.alloy_pairs_flattened
    GROUP BY column_name_a
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
    - `FROM`: Indicates the source table (`lakekeeper.omol25.omol25`).
    - `GROUP BY num_atoms`: Aggregates rows that have the same number of atoms.
    - `COUNT(*)`: Counts how many rows (molecules) are in each group.
    - `ORDER BY num_atoms`: Sorts the results in ascending order of the number of atoms.
    """)
    return


@app.cell
def _(conn):
    with conn.cursor() as cursor_7:
        cursor_7.execute('\n    SELECT num_atoms, COUNT(*)\n    FROM lakekeeper.omol25.omol25\n    GROUP BY num_atoms\n    ORDER BY num_atoms\n    ')
        for row in cursor_7.fetchall():
            print(row)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### 4.2 Charge distribution

    This query calculates the distribution of molecules by their formal charge.
    It groups molecules by the charge column and counts how many molecules fall into each charge category.

    - `SELECT`: Specifies the columns to return. Here, it selects the `charge` column and also calculates the number of occurrences using `COUNT(*)`.
    - `FROM`: Indicates the source table (`lakekeeper.omol25.omol25`).
    - `GROUP BY charge`: Collects all rows with the same charge value.
    - `COUNT(*)`: Computes how many molecules are in each charge group.
    - `ORDER BY charge`: Sorts results from lowest to highest charge.
    """)
    return


@app.cell
def _(conn):
    with conn.cursor() as cursor_8:
        cursor_8.execute('\n    SELECT charge, COUNT(*)\n    FROM lakekeeper.omol25.omol25\n    GROUP BY charge\n    ORDER BY charge\n    ')
        for row_1 in cursor_8.fetchall():
            print(row_1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### 4.3 Most common compositions

    The query retrieves the 20 most frequent values of the composition column from the `lakekeeper.omol25.omol25` table.

    It uses several standard SQL commands:

    - `SELECT`: Specifies the columns to return. Here, it selects `composition` and calculates the number of occurrences using `COUNT(*)`, aliased as `count`.
    - `FROM`: Indicates the source table (`lakekeeper.omol25.omol25`).
    - `GROUP BY`: Groups rows by composition so that the count can be computed for each unique value.
    - `ORDER BY`: Sorts the results in descending order based on the computed count. `DESC` means the results are ordered from highest to lowest.
    - `LIMIT 5`: Restricts the output to the top 5 results.
    """)
    return


@app.cell
def _(conn):
    with conn.cursor() as cursor_9:
        cursor_9.execute('\n    SELECT composition, COUNT(*) AS count\n    FROM lakekeeper.omol25.omol25\n    GROUP BY composition\n    ORDER BY count DESC\n    LIMIT 5\n    ')
        for row_2 in cursor_9.fetchall():
            print(row_2)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### 4.4 NL energy stats

    This query calculates basic statistics for the `nl_energy` column in the `lakekeeper.omol25.omol25` table. Specifically, it returns the minimum, maximum, and average values, excluding any missing (`NULL`) entries.

    1. `SELECT`: Specifies the values to return. Here, it computes aggregate statistics and returns them as aliases `(min_nl, max_nl, avg_nl)`:
        - `MIN(nl_energy)` --> the smallest value
        - `MAX(nl_energy)` --> the largest value
        - `AVG(nl_energy)` --> the average value
    2. `FROM`: Indicates the source table (`lakekeeper.omol25.omol25`).
    3. `WHERE`: Filters out rows where `nl_energy` is `NULL`, ensuring that only valid numeric values are used in the calculations.
    """)
    return


@app.cell
def _(conn):
    with conn.cursor() as cursor_10:
        cursor_10.execute('\n    SELECT\n        MIN(nl_energy) AS min_nl,\n        MAX(nl_energy) AS max_nl,\n        AVG(nl_energy) AS avg_nl\n    FROM lakekeeper.omol25.omol25\n    WHERE nl_energy IS NOT NULL\n    ')
        print('Min, max and average energies:')
        print(cursor_10.fetchone())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ### 4.5 Using pandas for post-processing of Trino query results

    When working with large datasets, it is inefficient to load all rows into memory. Instead, you should perform heavy computations (such as grouping and aggregation) in Trino, and use `pandas` only for lightweight post-processing of the reduced result set.

    The query below retrieves a small sample of rows (non-null `nl_energy` values) from the `lakekeeper.omol25.omol25` table. The result is then loaded into a pandas DataFrame for further analysis.
    """)
    return


@app.cell
def _(conn, pd):
    with conn.cursor() as cursor_11:
        cursor_11.execute('\n    SELECT composition, nl_energy\n    FROM lakekeeper.omol25.omol25\n    WHERE nl_energy IS NOT NULL\n    LIMIT 100\n    ')
        df = pd.DataFrame(cursor_11.fetchall(), columns=[col[0] for col in cursor_11.description])
    print(df.head())
    # Print top rows
    # Compute average nl_energy per composition (on the sampled data)
    print(df.groupby('composition')['nl_energy'].mean())  # Load results into a pandas DataFrame
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
                catalog="lakekeeper",
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
    TRINO_HOST_1 = 'trino-dev.psdi.ac.uk'
    with get_connection(TRINO_HOST_1) as conn_1:
        with conn_1.cursor() as cursor_12:
            cursor_12.execute('SHOW SCHEMAS FROM lakekeeper')
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
