#! /usr/bin/env bash

# Let the DB start
python /app/app/backend_pre_start.py

env

# Create initial data in DB
# python /app/app/initial_data.py

if [ "$REFRESH_SCHEMA" = "YES" ]
then
    psql -v ON_ERROR_STOP=1 postgresql://postgres:postgres@db:5432/app -f scripts/sql/public_schema_export.sql
    echo "REFRESH SCHEMA Completed. Dropped and recreated the tables from public_schema_export.sql"
fi

if [ ! -z "$SEED_DATA" ]
then
    echo "You have chosen to load data from $SEED_DATA !. This might take few minutes."
    echo "Loading demo data....."
    psql -v ON_ERROR_STOP=1 postgresql://postgres:postgres@db:5432/app -f scripts/sql/app_data_export.sql
    echo "Demo data loaded successfully"
fi

# Run migrations
alembic upgrade head

# Run data changes
psql -v ON_ERROR_STOP=1 postgresql://postgres:postgres@db:5432/app -f scripts/sql/ticket_data_changes_1.sql
