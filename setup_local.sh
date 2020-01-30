
head -n 1000 'assignment1/test.csv' | tr [:upper:] [:lower:] | tr ' ' '_' | sed 's/#/num/' | csvsql -i postgresql --db-schema ohschools --tables ohcensus > 'table_script.sql'
psql -f setup_sql.sql
python clean_sql.py 'table_script.sql' 'table_script_cleaned.sql' 'assignment1/test.csv'
psql -f table_script_cleaned.sql
