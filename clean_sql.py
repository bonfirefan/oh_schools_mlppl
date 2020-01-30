import sys

replacements = {' NOT NULL':''}

def clean_sql(fin, fout, csvfile):
    with open(f) as infile, open(fout, 'w') as outfile:
        for line in infile:
            for src, target in replacements.iteritems():
                line = line.replace(src, target)
            outfile.write(line)
        endline = "'\COPY ohschools.ohcensus from '{0}' WITH CSV HEADER;'".format(csvfile)
        outfile.write(endline)
def main():
    # print command line arguments
    for arg in :
        print arg

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
