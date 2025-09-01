# count NRPS, PKS or NRPS-PKS
import pandas as pd

df = pd.read_csv('BGC_summary_all.tsv', sep='\t')
column_data = df['BGC_Class'].astype(str) 

nrps = column_data.str.count('NRPS').sum() - column_data.str.count('NRPS-PKS').sum()
pks = column_data.str.count('PKS').sum() - column_data.str.count('NRPS-PKS').sum()
nrps_pks = column_data.str.count('NRPS-PKS').sum()

print("NRPS: ", nrps, "\nPKS: ", pks, "\nNRPS-PKS: ", nrps_pks)


# count how many BGCs scored higher than the jamaicamides