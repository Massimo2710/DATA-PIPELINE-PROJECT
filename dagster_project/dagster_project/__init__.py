from dagster import Definitions, asset, AssetExecutionContext
from dagster_dbt import DbtCliResource
import subprocess
import os

# Chemins
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DBT_PROJECT_DIR = os.path.join(PROJECT_DIR, "dbt_project")
INGESTION_SCRIPT = os.path.join(PROJECT_DIR, "ingestion", "generate_data.py")

# Configure dbt
dbt_resource = DbtCliResource(project_dir=DBT_PROJECT_DIR)

# Asset 1 : Ingestion des données
@asset(group_name="ingestion")
def raw_data(context: AssetExecutionContext):
    """Génère les données brutes avec Python/Faker"""
    context.log.info("🚀 Exécution du script d'ingestion...")
    result = subprocess.run(
        ["python", INGESTION_SCRIPT],
        capture_output=True,
        text=True
    )
    context.log.info(result.stdout)
    if result.returncode != 0:
        context.log.error(result.stderr)
        raise Exception("Échec de l'ingestion")
    context.log.info("✅ Données chargées dans DuckDB")

# Asset 2 : Tous les modèles dbt
@asset(
    group_name="dbt",
    deps=["raw_data"]
)
def dbt_staging_and_analytics(context: AssetExecutionContext):
    """Execute tous les modèles dbt"""
    context.log.info("🚀 Exécution de dbt...")
    result = subprocess.run(
        ["dbt", "build", "--project-dir", DBT_PROJECT_DIR],
        capture_output=True,
        text=True
    )
    context.log.info(result.stdout)
    if result.returncode != 0:
        context.log.error(result.stderr)
        raise Exception("Échec de dbt")
    context.log.info("✅ Modèles dbt créés")

# Définitions Dagster
defs = Definitions(
    assets=[raw_data, dbt_staging_and_analytics],
    resources={"dbt": dbt_resource}
)