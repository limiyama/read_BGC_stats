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

def move_files_to_directory(input_dir, temp_dir):
    # ver se existe mesmo o temp dir ou eh fake news 
    os.makedirs(temp_dir, exist_ok=True)
    found_any_files = False 

    # para os arquivos no input dir
    for file in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file)
        
        # se ele for .gbk sozinho vai copiar pro temp dir
        if file.lower().endswith('.gbk'):
            print(f".gbk file found: {file}")
            shutil.copyfile(file_path, os.path.join(temp_dir, file))
            found_any_files = True

        # se ele for .zip vai unzipar so os arquivos .gbk comprimidos e botar no temp dir
        elif zipfile.is_zipfile(file_path):
            print(f".zip file found: {file}")
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                for item in zip_ref.namelist():

                    # se for .gbk
                    if item.lower().endswith('.gbk'):
                        zip_ref.extract(item, temp_dir)
                        extracted_path = os.path.join(temp_dir, item)

                        # move pro temp dir de verdade e nao subpastas
                        if os.path.exists(extracted_path):
                            os.rename(extracted_path, os.path.join(temp_dir, os.path.basename(item)))
                            found_any_files = True
                        
                        print(f".gbk file extracted: {os.path.basename(item)}")

    if not found_any_files:
        print("No .gbk files found. Make sure that your input path is correct.")
    else:
        print("Extracted with success!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="BGCpri",
        description="BGCpri is an algorithm that prioritizes NRPS, PKS and hybrid NRPS-PKS BGCs from .gbk files obtained from antiSMASH analysis."
    )

    parser.add_argument('-i', '--input', help="input path", required="True")
    parser.add_argument('-o', '--output', help="output path", required="True")
    parser.add_argument('-v', '--version', action='version', version='BGCpri 1.0')
    args = parser.parse_args()

    input = args.input
    output = args.output

    print("Welcome to BGCpri - python version :)\nLLLL                      BBBB\nLLLL                      BBBB\nLLLL                      BBBB\nLLLL     AAAAAAAAAAAAAA   BBBBBBBBBBBBB\nLLLL    AAAAAAAAAAAAAAA   BBBBBBBBBBBBBB\nLLLL   AAAAA      AAAAA   BBBBB      BBBB\nLLLL   AAAA       AAAAA   BBBB       BBBB\nLLLL   AAAA       AAAAA   BBBB       BBBB\nLLLL   AAAAAA    AAAAAA   BBBBBB    BBBBB\nLLLL    AAAAAAAAAAAAAAA   BBBBBBBBBBBBBB                  LLLL\nLLLL      AAAAAAAA AAAA   BBB  BBBBBBB                    LLLL\n                                                          LLLL\n          AAAAAAAA AAAA   ZZZZZZZZZZZZ   UUUU      UUUUU  LLLL\n        AAAAAAAAAAAAAAA   ZZZZZZZZZZZZ   UUUU      UUUUU  LLLL\n       AAAAA     AAAAAA         ZZZZ     UUUU      UUUUU  LLLL\n       AAAA       AAAAA       ZZZZZ      UUUU      UUUUU  LLLL\n       AAAA       AAAAA      ZZZZZ       UUUU      UUUUU  LLLL\n       AAAAA      AAAAA     ZZZZ         UUUUU    UUUUUU  LLLL\nAAAA    AAAAAAAAAAAAAAA   ZZZZZZZZZZZZ    UUUUUUUUUUUUUU  LLLL\nAAAA      AAAAAAAAAAAAA   ZZZZZZZZZZZZ     UUUUUUVUUUUUU  LLLL\nThe BGC PRIORITIZATION ALGORITHM uses all .zip or .gbk files from antiSMASH results inside the same directory.\nIf your files are scattered across multiple directories or if you want to run only specific files, please make sure to make a copy of them in a specific directory before you run this program, in order to get the correct results.")

    output_file = os.path.join(output, "BGC_summary.tsv")

    # cria um diretório temporário para jogar a bagunça dos zips e gbks
    temp_dir = os.path.join(output, "dir_temp")
    print("Temp directory: ", temp_dir)

    # move os arquivos .zip e .gbk para o diretório temporário e utiliza apenas os .gbk
    move_files_to_directory(input, temp_dir)

    # processa os .gbk extraídos da função anterior
    process_bgcs_from_gbk(temp_dir, output_file)
    
    # ver como apagar o diretorio caso de qualquer erro
    #  apagar diretorio temporario no final
    shutil.rmtree(temp_dir)
    print("Done! Thank you for using BGCpri :)")