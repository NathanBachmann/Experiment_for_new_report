#!/usr/local/bin/python
#Written by Nathan Bachmann (nathan_bachmann@hotmail.com) on the 23/07/26

import sys
import argparse

parser = argparse.ArgumentParser(description='Get the top ASV from an exported feature table from QIIME2')
parser.add_argument('input', metavar='<Logfile>', type=str,
                    help='best_tax_merged_freq_tax.tsv')
args = parser.parse_args()

asv_table = args.input

