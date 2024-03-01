from dagster import OpExecutionContext, Output, with_resources , asset
from dagster_airbyte import AirbyteResource, build_airbyte_assets
from dagster_dbt import get_asset_key_for_model
import pandas as pd


from dagster_dbt import dbt_assets, DbtCliResource
import psycopg2
from ...utils.constants import AIRBYTE_CONFIG, AIRBYTE_MOVIES_CONNECTION_ID, AIRBYTE_SCORES_CONNECTION_ID, AIRBYTE_USERS_CONNECTION_ID, dbt_manifest_path



# --------------------Airbyte Assets--------------------

airbyte_instance = AirbyteResource(**AIRBYTE_CONFIG)

movies_assets = with_resources(
    build_airbyte_assets(
        connection_id=AIRBYTE_MOVIES_CONNECTION_ID,
        asset_key_prefix=["recommender_system_raw"],
        destination_tables=["movies"],
    ),
    {"airbyte": airbyte_instance},
)

scores_assets = with_resources(
    build_airbyte_assets(
        connection_id=AIRBYTE_SCORES_CONNECTION_ID,
        asset_key_prefix=["recommender_system_raw"],
        destination_tables=["scores"],
    ),
    {"airbyte": airbyte_instance},
)

users_assets = with_resources(
    build_airbyte_assets(
        connection_id=AIRBYTE_USERS_CONNECTION_ID,
        asset_key_prefix=["recommender_system_raw"],
        destination_tables=["users"],
    ),
    {"airbyte": airbyte_instance},
)

airbyte_combine = movies_assets + scores_assets + users_assets






# --------------------DBT Assets--------------------

@dbt_assets(manifest=dbt_manifest_path)
def dbt_project_dbt_assets(context: OpExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()


# --------------------Postgres Assets--------------------

@asset(
    compute_kind="python",
    deps=[get_asset_key_for_model([dbt_project_dbt_assets], "scores_movies_users")],
    )
def training_data(context):
    # Database connection parameters
    user="postgres"
    password="mysecretpassword"
    host="localhost"
    database="mlops_movie"

    schema_name = "target"
    table_name = "scores_movies_users"

    # Establish the database connection
    conn = psycopg2.connect(
        dbname=database,
        user=user,
        password=password,
        host=host,
    )

    # SQL query to select all data from the specified table
    sql_query = f"SELECT * FROM {schema_name}.{table_name};"
    df = pd.read_sql_query(sql_query, conn)

    # Fetch all the rows
    rows = len(df)

    # Log the number of rows fetched
    context.log.info(f"Fetched {rows} rows from {schema_name}.{table_name}")

    # Yield the fetched data as an output
    yield Output(df, output_name="result", metadata={"row_count": rows})

    # Close the cursor and the connection
    conn.close()