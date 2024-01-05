import os
import pandas as pd

codon_to_aa = {
    'AAA': 'K', 'AAC': 'N', 'AAG': 'K', 'AAT': 'N',
    'ACA': 'T', 'ACC': 'T', 'ACG': 'T', 'ACT': 'T',
    'AGA': 'R', 'AGC': 'S', 'AGG': 'R', 'AGT': 'S',
    'ATA': 'I', 'ATC': 'I', 'ATG': 'M', 'ATT': 'I',
    'CAA': 'Q', 'CAC': 'H', 'CAG': 'Q', 'CAT': 'H',
    'CCA': 'P', 'CCC': 'P', 'CCG': 'P', 'CCT': 'P',
    'CGA': 'R', 'CGC': 'R', 'CGG': 'R', 'CGT': 'R',
    'CTA': 'L', 'CTC': 'L', 'CTG': 'L', 'CTT': 'L',
    'GAA': 'E', 'GAC': 'D', 'GAG': 'E', 'GAT': 'D',
    'GCA': 'A', 'GCC': 'A', 'GCG': 'A', 'GCT': 'A',
    'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGT': 'G',
    'GTA': 'V', 'GTC': 'V', 'GTG': 'V', 'GTT': 'V',
    'TAC': 'Y', 'TAT': 'Y', 'TCA': 'S', 'TCC': 'S',
    'TCG': 'S', 'TCT': 'S', 'TGC': 'C', 'TGG': 'W',
    'TGT': 'C', 'TTA': 'L', 'TTC': 'F', 'TTG': 'L',
    'TTT': 'F', 'TAA': '*', 'TAG': '*', 'TGA': '*'
}

def read_cds_sequences_from_file(file_path):
    with open(file_path, 'r') as file:
        cds_sequences = file.readlines()
    # Remove trailing newline characters from each line
    cds_sequences = [sequence.strip() for sequence in cds_sequences]
    return cds_sequences

def calculate_codon_probability_and_count(cds_sequences, codon):
    codon_count = sum(sequence.count(codon) for sequence in cds_sequences)
    total_codons_count = sum(sequence.count(c) for sequence in cds_sequences for c in codon_to_aa.keys())
    synonymous_codons = [syn_codon for syn_codon, aa in codon_to_aa.items() if aa == codon_to_aa[codon]]
    total_synonymous_codons = sum(sequence.count(syn_codon) for sequence in cds_sequences for syn_codon in synonymous_codons)
    
    codon_probability = codon_count / total_synonymous_codons if total_synonymous_codons != 0 else 0
    codon_count_per_thousand = (codon_count / total_codons_count) * 1000
    
    return round(codon_probability, 2), codon_count, round(codon_count_per_thousand, 2)

# Read CDS sequence file
file_paths = [
    'cleaned_sequences/Arabidopsis_thaliana_cleaned.fa',
    'cleaned_sequences/Drosophila_melanogaster_cleaned.fa',
    'cleaned_sequences/Human_cleaned.fa',
    'cleaned_sequences/Mus_musculus_cleaned.fa',
    'cleaned_sequences/Rat_cleaned.fa',
    'cleaned_sequences/Zea_mays_cleaned.fa',
    'cleaned_sequences/Saccharomyces_cerevisiae_cleaned.fa',
    'cleaned_sequences/Caenorhabditis_elegans_cleaned.fa',
    'cleaned_sequences/e.coli_cleaned.fa'
]  # Add your file paths, can be multiple

for file_path in file_paths:
    cds_sequences = read_cds_sequences_from_file(file_path)
    
    # Calculate the proportion, count, and occurrences per thousand for each codon in the encoding amino acid's codons
    codon_fractions = {}
    for codon, aa in codon_to_aa.items():
        codon_fraction = calculate_codon_probability_and_count(cds_sequences, codon)
        codon_fractions[codon] = codon_fraction

    # Build DataFrame
    data = []
    for codon, codon_fraction in codon_fractions.items():
        aa = codon_to_aa[codon]
        probability, count, count_per_thousand = codon_fraction
        species_name = ' '.join(file_path.split('_')[:-1]).split('/')[-1]  # Extract species information from the file name
        data.append([codon, aa, probability, count_per_thousand, count, species_name])

    df = pd.DataFrame(data, columns=['Codon', 'Amino Acid', 'Probability', 'Count per Thousand', 'Count', 'Species'])

    # Sort DataFrame by 'Amino Acid' column
    df_sorted = df.sort_values(by='Amino Acid')

    # Create a new folder
    output_dir = 'codon_frequency_csv'
    os.makedirs(output_dir, exist_ok=True)

    # Output the sorted table to a CSV file
    output_filename = os.path.join(output_dir, f'codon_frequency_{species_name}.csv')
    df_sorted.to_csv(output_filename, index=False)
