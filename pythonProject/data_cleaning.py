import os


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
    'e.coli': 'Escherichia_coli_str_k_12_substr_mg1655_gca_000005845.ASM584v2.cds.all.fa'
    #'human': 'Homo_sapiens.GRCh38.cds.all.fa',
    #'mouse': 'Mus_musculus.GRCm39.cds.all.fa',
    # 添加其他物种的文件路径
}

for species, file_path in species_files.items():
    print(f'Processing {species}...')
    cleaned_sequences = filter_cds_sequences(file_path)

    # 保存清理后的序列到文件
    output_dir = 'cleaned_sequences'
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f'{species}_cleaned.fa')

    with open(output_file, 'w') as output:
        for sequence in cleaned_sequences:
            output.write(f'>{species}\n{sequence}\n')

    print(f'Cleaned sequences for {species} saved to {output_file}')