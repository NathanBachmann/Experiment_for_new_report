#!/usr/local/bin/python
#Written by Nathan Bachmann (nathan_bachmann@hotmail.com) on the 23/07/26

import sys
import argparse
import re

parser = argparse.ArgumentParser(description='Get the top ASV from an exported feature table from QIIME2')
parser.add_argument('input', metavar='<table of ASVs>', type=str,
                    help='best_tax_merged_freq_tax.tsv')
parser.add_argument('--top', metavar='<number of top ASVs>', type=int, default=50,
                    help='Number of top ASVs to display (default: 50)')
args = parser.parse_args()

asv_table = args.input
top_n = args.top

with open(asv_table, 'r') as file:
    lines = file.readlines()

header = lines[0]
data = []

#main loop - calculates the total frequency for each ASV
for line in lines[2:]:
    line = line.strip('\n')
    elements = line.split('\t')
    freqs = '\t'.join(elements[4:])
    values = list(map(int, elements[4:]))
    total = sum(values)
    taxonomy = re.sub(r'\w__', '', elements[2]).replace(';', '\t')
    data.append((elements[0], taxonomy, freqs, total))

#store the total frequency values from largest to smallest
data.sort(reverse=True, key=lambda x: x[3])

for asv in data[:top_n]:
    print(f"{asv[0]}\t{asv[1]}\t{asv[2]}")


