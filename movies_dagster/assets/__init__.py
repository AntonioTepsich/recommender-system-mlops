from dagster import load_assets_from_package_module
from . import extract
from . import recommender


core_assets = load_assets_from_package_module(
    package_module=extract, group_name='extract',
    
)
recommender_assets = load_assets_from_package_module(
    package_module=recommender, group_name='recommender'
)