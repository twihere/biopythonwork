import os
import pandas as pd

# 定义密码子到氨基酸的映射关系
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

# 从文件中读取CDS序列
def read_cds_sequences_from_file(file_path):
    with open(file_path, 'r') as file:
        cds_sequences = file.readlines()
    # 去除每行末尾的换行符
    cds_sequences = [sequence.strip() for sequence in cds_sequences]
    return cds_sequences

# 计算给定密码子的分数、计数和千分之一的出现次数
def calculate_codon_Fraction_and_count(cds_sequences, codon):
    codon_count = sum(sequence.count(codon) for sequence in cds_sequences)
    total_codons_count = sum(sequence.count(c) for sequence in cds_sequences for c in codon_to_aa.keys())
    synonymous_codons = [syn_codon for syn_codon, aa in codon_to_aa.items() if aa == codon_to_aa[codon]]
    total_synonymous_codons = sum(sequence.count(syn_codon) for sequence in cds_sequences for syn_codon in synonymous_codons)
    
    codon_fraction = codon_count / total_synonymous_codons if total_synonymous_codons != 0 else 0
    codon_count_per_thousand = (codon_count / total_codons_count) * 1000
    
    return round(codon_fraction, 2), codon_count, round(codon_count_per_thousand, 2)

# 主目录
base_dir = os.getcwd()

# 读取CDS序列文件
input_dir = 'cleaned_sequences'
output_dir = 'codon_frequency_csv'
os.makedirs(output_dir, exist_ok=True)

# 获取目录下所有文件
file_paths = [f for f in os.listdir(input_dir) if f.endswith('_cleaned.fa')]

for file_path in file_paths:
    cds_sequences = read_cds_sequences_from_file(os.path.join(input_dir, file_path))
    
    # 计算每个氨基酸编码的密码子的比例、计数和千分之一的出现次数
    codon_Fractions = {}
    for codon, aa in codon_to_aa.items():
        codon_Fraction = calculate_codon_Fraction_and_count(cds_sequences, codon)
        codon_Fractions[codon] = codon_Fraction

    # 构建DataFrame
    data = []
    for codon, codon_Fraction in codon_Fractions.items():
        aa = codon_to_aa[codon]
        Fraction, count, count_per_thousand = codon_Fraction
        species_name = file_path.split('_cleaned.fa')[0].replace('_', ' ')  # 从文件名提取物种信息
        data.append([codon, aa, Fraction, count_per_thousand, count, species_name])

    df = pd.DataFrame(data, columns=['Codon', 'Amino Acid', 'Fraction', 'Count per Thousand', 'Count', 'Species'])

    # 根据 'Amino Acid' 列对 DataFrame 进行排序
    df_sorted = df.sort_values(by='Amino Acid')

    # 将排序后的表格输出到 CSV 文件
    output_filename = os.path.join(output_dir, f'codon_frequency_{species_name}.csv')
    df_sorted.to_csv(output_filename, index=False)

print("Processing completed.")
