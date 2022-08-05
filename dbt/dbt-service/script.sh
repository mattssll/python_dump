#!/bin/sh
# install deps (external table creation)
# dbt deps -- doing this in Dockerfile so not needed to do it here in runtime
# recreate external table
dbt run-operation stage_external_sources  --profiles-dir . --vars "ext_full_refresh: true"
# run our models (staging and dwh)
dbt run --profiles-dir .