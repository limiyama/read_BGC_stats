with open("Moorea_summary.tsv", "r") as f1, open("CIFARP_summary.tsv", "a") as f2 :
    line = f1.readline() #remove header
    line = f1.readline()
    while line != "" :
        f2.write(line)
        line = f1.readline()