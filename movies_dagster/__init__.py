from dagster import (
    AssetSelection,
    Definitions,
    ScheduleDefinition,
    define_asset_job,
)

from dagster_dbt import DbtCliResource

from .utils.constants import dbt_project_dir
import os


from .assets import (
    core_assets,
    recommender_assets,
)

all_assets = [*core_assets, *recommender_assets]

get_data_job = define_asset_job(
    name='get_data',
    selection=[*core_assets],
    # config=job_data_config
)

mlflow_tracking_config = {
    'experiment_name': 'recommender_system_itba',
}

defs = Definitions(
    assets=all_assets,
    resources={
        "dbt": DbtCliResource(project_dir=os.fspath(dbt_project_dir)),
        # "mlflow": mlflow_tracking.configured(mlflow_tracking_config),  # Configuración de MLflow aquí
    },

    jobs=[
        get_data_job,
        define_asset_job("full_process"),
        define_asset_job(
            "only_training",
            selection=AssetSelection.groups('recommender'),
        ),
    ],
    schedules=[
        # update all assets once a day
        ScheduleDefinition(
            job = get_data_job,
            cron_schedule="@daily"
        ),
    ],
)