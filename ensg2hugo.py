import sys
import fileinput
import re
import pandas as pd
import numpy as np
import csv

Lookup_gene={}
for each_line_of_text in list(fileinput.FileInput('Homo_sapiens.GRCh37.75.gtf')):
    Ensembl_name = re.findall(r'ENSG+[0-9]{11}',each_line_of_text)
    HUGO_name = re.findall(r'gene_name\s"(.*?)"',each_line_of_text)
    
    if(len(Ensembl_name) is not 0 or len(HUGO_name) is not 0):
        Lookup_gene.setdefault(Ensembl_name[0], HUGO_name[0])
fileinput.close()

index = 0
if (len(sys.argv) > 2):
    df = pd.read_csv(sys.argv[2])
    column_num = int(sys.argv[1][2:])-1
else:
    df = pd.read_csv(sys.argv[1])
    column_num = 0

for line in list(df.iloc[:,1]):
    Ensembl = re.findall(r'ENSG+[0-9]{11}',line)
    if(len(Ensembl) is not 0):
        try:
            hugo_name = Lookup_gene[Ensembl[0]]
            df.replace(df.iloc[index,column_num],hugo_name, inplace=True)
        except KeyError as e:
            df.replace(df.iloc[index,column_num],'unknown', inplace=True)
        index += 1
fileinput.close()
print(df.to_csv(quoting=csv.QUOTE_NONNUMERIC,index=False, line_terminator='\n'))
