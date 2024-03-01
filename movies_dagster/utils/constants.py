from dagster._utils import file_relative_path
from dagster_dbt import DbtCliResource
from pathlib import Path
import os

# Airbyte connection IDs
AIRBYTE_MOVIES_CONNECTION_ID = "68f41ff3-6b5f-488c-959b-be8ae7f5fd19"
AIRBYTE_SCORES_CONNECTION_ID = "efab560d-023a-4a9c-9874-ba83c1cd7a83"
AIRBYTE_USERS_CONNECTION_ID = "15f0a078-2251-49b6-b338-1197158a8edd"

# Airbyte configuration
AIRBYTE_CONFIG = {
    "host": "localhost",
    "port": "8000",
    "username": "airbyte",
    "password": "password"
}

# DBT project and profile paths
dbt_project_dir = Path(file_relative_path(__file__, "../../db_postgres"))
DBT_PROFILE_PATH = Path(file_relative_path(__file__, "../../db_postgres/config"))
DBT_CONFIG = {"project_dir": dbt_project_dir, "profiles_dir": DBT_PROFILE_PATH}

# Initialize DbtCliResource with project_dir
dbt = DbtCliResource(project_dir=os.fspath(dbt_project_dir))

# Determine dbt manifest path based on environment variable
if os.getenv("DAGSTER_DBT_PARSE_PROJECT_ON_LOAD"):
    dbt_manifest_path = (
        dbt.cli(
            ["--quiet", "parse"],
            target_path=Path("target"),
        )
        .wait()
        .target_path.joinpath("manifest.json")
    )
    if not dbt_manifest_path.exists():
        raise FileNotFoundError(f"DBT manifest not found at {dbt_manifest_path}")
else:
    dbt_manifest_path = dbt_project_dir.joinpath("target", "manifest.json")
    if not dbt_manifest_path.exists():
        raise FileNotFoundError(f"DBT manifest not found at {dbt_manifest_path}")

