import pandas as pd

df = pd.read_csv('BGC_summary_all.tsv', sep='\t')

# count NRPS, PKS or NRPS-PKS
column_bgc_class = df['BGC_Class'].astype(str) 

nrps = column_bgc_class.str.count('NRPS').sum() - column_bgc_class.str.count('NRPS-PKS').sum()
pks = column_bgc_class.str.count('PKS').sum() - column_bgc_class.str.count('NRPS-PKS').sum()
nrps_pks = column_bgc_class.str.count('NRPS-PKS').sum()

print("NRPS: ", nrps, "\nPKS: ", pks, "\nNRPS-PKS: ", nrps_pks)

# count how many BGCs scored higher than jamaicamides, hectochlorin, etc
jamaicamides = (df["Score"]>91.5).sum()
hectochlorin = (df["Score"]>55).sum()
cryptomaldamide = (df["Score"]>42).sum()

print("Number of BGCs that scored higher than jamaicamides: ", jamaicamides)
print("Number of BGCs that scored higher than hectochlorin: ", hectochlorin)
print("Number of BGCs that scored higher than cryptomaldamide: ", cryptomaldamide)
