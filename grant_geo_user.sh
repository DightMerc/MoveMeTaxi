set -e

POSTGRES="docker-compose exec -T db psql move_me"

echo "Setting permissions to database role: geo"

$POSTGRES <<-EOSQL
; GRANT ALL PRIVELEGES ON DATABASE move_me TO geo;
EOSQL

