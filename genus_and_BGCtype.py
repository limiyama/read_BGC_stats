import shutil, zipfile, os, glob, argparse
import pandas as pd
from Bio import SeqIO

def classify_bgc(type):
    if 'NRPS' in type and 'KS' in type:
        return "NRPS-PKS"
    elif 'NRPS' in type:
        return "NRPS"
    elif 'KS' in type:
        return "PKS"
    elif 'RiPP' in type:
        return "RiPP"
    elif 'terpene' in type:
        return "Terpene"
    else:
        return "Other"

def process_bgcs_from_gbk(gbk_dir, results):
    data = []

    for gbk_file in glob.glob(os.path.join(gbk_dir, "*region*.gbk")):

        for record in SeqIO.parse(gbk_file, "genbank"):
            features = record.features

            for feature in features:
                # products - se é NRPS, PKS, terpeno, etc
                if feature.type == "region" and "product" in feature.qualifiers: 
                    products = feature.qualifiers["product"]
                    bgc_type = ", ".join(products)
                    bgc_class = classify_bgc(bgc_type)

            data.append({
                "Organism": record.annotations.get("organism", "Unknown"),
                "Type": bgc_type,
                "Class": bgc_class
            })

            df = pd.DataFrame(data)
            # salva em CSV
            df.to_csv(results, sep='\t', index=False)
