
#head -n 1000 test.csv | tr [:upper:] [:lower:] | tr ' ' '_' | sed 's/#/num/' | csvsql -i postgresql --db-schema postgres --tables ohcensus
psql -f setup_sql.sql -U postgres
