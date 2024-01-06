import os

# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 目标目录（主目录下的 cleaned 目录）
output_dir = os.path.join(current_dir, 'cleaned_sequences')
# 目标目录
cds_sequences_dir = os.path.join(current_dir, 'cds_sequences')

# 更改当前工作目录到cds_sequences目录下
os.chdir(cds_sequences_dir)

# 读取FASTA文件
def read_fasta(file_path):
    sequences = []
    with open(file_path, 'r') as file:
        sequence = ''
        for line in file:
            if line.startswith('>'):
                if sequence:
                    sequences.append(sequence)
                    sequence = ''
            else:
                sequence += line.strip()
        if sequence:
            sequences.append(sequence)
    return sequences
    
# 筛选并清理CDS序列
def filter_cds_sequences(file_path):
    sequences = read_fasta(file_path)
    cleaned_sequences = []

    for sequence in sequences:
        # 检查序列是否由A、T、C、G四种碱基组成
        if set(sequence.upper()).issubset({'A', 'T', 'C', 'G'}):
            # 检查序列碱基数是否是3的倍数
            if len(sequence) % 3 == 0:
                # 检查起始和终止密码子
                start_codon = sequence[:3]
                stop_codon = sequence[-3:]
                if start_codon in {'ATG', 'GTG', 'TTG'} and stop_codon in {'TAA', 'TAG', 'TGA'}:
                    # 检查序列长度是否大于300 bp
                    if len(sequence) >= 300:
                        # 检查是否为重复序列
                        if sequence not in cleaned_sequences:
                            cleaned_sequences.append(sequence)

    return cleaned_sequences
    
# 处理多个物种的CDS序列
species_files = {
    'E.coli': 'Escherichia_coli_str_k_12_substr_mg1655_gca_000005845.ASM584v2.cds.all.fa',
    'Human': 'Homo_sapiens.GRCh38.cds.all.fa',
    'Mus_musculus': 'Mus_musculus.GRCm39.cds.all.fa',
    'Arabidopsis_thaliana': 'Arabidopsis_thaliana.TAIR10.cds.all.fa',
    'Caenorhabditis_elegans': 'Caenorhabditis_elegans.WBcel235.cds.all.fa',
    'Drosophila_melanogaster': 'Drosophila_melanogaster.BDGP6.46.cds.all.fa',
    'Rat': 'Rattus_norvegicus.mRatBN7.2.cds.all.fa',
    'Saccharomyces_cerevisiae': 'Saccharomyces_cerevisiae.R64-1-1.cds.all.fa',
    'Zea_mays': 'Zea_mays.Zm-B73-REFERENCE-NAM-5.0.cds.all.fa'
}

for species, file_path in species_files.items():
    print(f'Processing {species}...')
    cleaned_sequences = filter_cds_sequences(file_path)

    # 保存清理后的序列到文件
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f'{species}_cleaned.fa')

    with open(output_file, 'w') as output:
        for sequence in cleaned_sequences:
            output.write(f'>{species}\n{sequence}\n')

    print(f'Cleaned sequences for {species} saved to {output_file}')
