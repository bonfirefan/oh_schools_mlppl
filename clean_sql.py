import sys

replacements = {' NOT NULL':''}

def clean_sql(fin, fout, csvfile):
    with open(fin) as infile, open(fout, 'w') as outfile:
        for line in infile:
            for src, target in replacements.items():
                line = line.replace(src, target)
            outfile.write(line)
        endline = "\COPY ohschools.ohcensus from '{0}' WITH CSV HEADER;".format(csvfile)
        outfile.write(endline)


if __name__ == "__main__":
    clean_sql(sys.argv[1], sys.argv[2], sys.argv[3])
