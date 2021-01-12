set -e

POSTGRES="docker-compose exec -T db psql move_me"

echo "Creating database role: geo"

$POSTGRES <<-EOSQL
CREATE USER geo WITH PASSWORD 'q1w2e3r4T';
GRANT ALL ON DATABASE move_me TO geo;
GRANT ALL ON ALL TABLES IN SCHEMA public to geo;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public to geo;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public to geo;
EOSQL

