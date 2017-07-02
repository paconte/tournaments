#!/bin/sh
echo "Set django secret key for touchdb"
export DJANGO_TOUCHDB_SECRET_KEY="example_django_secret_key"
echo "Set postgres user"
export POSTGRES_USER="example_database_user"
echo "Set postgres password"
export POSTGRES_PASSWORD="example_datanase_password"
