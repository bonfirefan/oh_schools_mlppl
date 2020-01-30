import sys
import subprocess


replacements = {' NOT NULL':''}

# Command with shell expansion
def gen_table(csvfile, sch_name, tb_name, sql_file):
    return("head -n 1000 '{0}' | tr [:upper:] [:lower:] | tr ' ' '_' | sed 's/#/num/' | csvsql -i postgresql --db-schema {1} --tables {2} > {3}".format(csvfile, sch_name, tb_name, sql_file))

def gen_schema(sch_name, tb_name):
    return('''CREATE SCHEMA IF NOT EXISTS {0};
    DROP TABLE IF EXISTS {0}.{1};'''.format(sch_name, tb_name))

def clean_sql(fin, fout, csvfile, sch_name, tb_name):
    sch_sql = gen_schema(sch_name, tb_name)
    with open(fin) as infile, open(fout, 'w') as outfile:
        outfile.write(sch_sql)
        for line in infile:
            for src, target in replacements.items():
                line = line.replace(src, target)
            outfile.write(line)
        endline = "\COPY ohschools.ohcensus from '{0}' WITH CSV HEADER;".format(csvfile)
        outfile.write(endline)


if __name__ == "__main__":
    # 1 : sql script name
    # 1 : sql script name
    shell1 = gen_table(sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[1])
    subprocess.call(shell1, shell=True)
    clean_sql(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    subprocess.call('psql -f {0}'.format(sys.argv[2]), shell=True)
