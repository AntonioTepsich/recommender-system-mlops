from setuptools import find_packages, setup
import os
DAGSTER_VERSION=os.getenv('DAGSTER_VERSION', '1.5.7')
DAGSTER_LIBS_VERSION=os.getenv('DAGSTER_LIBS_VERSION', '0.21.6')
MLFLOW_VERSION=os.getenv('MLFLOW_VERSION', '2.8.0')
TENSORFRLOW_VERSION=os.getenv('TENSORFRLOW_VERSION', '2.14.0')

setup(
    name="movies_dagster",
    packages=find_packages(exclude=["movies_dagster_tests"]),
    install_requires=[
        "dagster",
        "dagster_airbyte",
        "dagster_dbt",
        "dbt-postgres",
        "psycopg2",
        "dagster_postgres",
        f"dagster-mlflow=={DAGSTER_LIBS_VERSION}",
        f"mlflow=={MLFLOW_VERSION}",
        f"tensorflow=={TENSORFRLOW_VERSION}",
    ],
    extras_require={"dev": ["dagster-webserver", "pytest", "jupyter"]},
)