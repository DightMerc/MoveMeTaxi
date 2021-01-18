set -e

DOCKER="docker-compose up -d --build"
POSTGRES="docker-compose exec -T db psql move_me"

echo "Docker initialization"
$DOCKER

echo "Creating database roles: GEO && FINDER"
$POSTGRES <<-EOSQL
CREATE USER geo WITH PASSWORD 'q1w2e3r4T';
GRANT ALL ON DATABASE move_me TO geo;
GRANT ALL ON ALL TABLES IN SCHEMA public to geo;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public to geo;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public to geo;

CREATE USER finder WITH PASSWORD 'q1w2e3r4T';
GRANT ALL ON DATABASE move_me TO finder;
GRANT ALL ON ALL TABLES IN SCHEMA public to finder;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public to finder;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public to finder;

EOSQL

