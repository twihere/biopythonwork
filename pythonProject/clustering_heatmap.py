import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 文件夹路径
folder_path = 'codon_frequency_csv'

# 获取文件路径列表
file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path)]

# 存储所有数据框的列表
dfs = []

# 读取所有文件并存储在 dfs 列表中
all_codons = set()  # 用于存储所有出现过的密码子

for file_path in file_paths:
    species_name = file_path.split('_')[-1].split('.')[0]
    df = pd.read_csv(file_path)
    df['Species'] = species_name
    dfs.append(df[['Species', 'Codon', 'Fraction']])

    # 将该物种出现过的密码子加入集合
    all_codons.update(df['Codon'])

# 确保所有物种都包含所有密码子
for i in range(len(dfs)):
    missing_codons = all_codons - set(dfs[i]['Codon'])
    if missing_codons:
        for codon in missing_codons:
            dfs[i] = dfs[i].append({'Species': dfs[i]['Species'].iloc[0], 'Codon': codon, 'Fraction': 0.0},
                                   ignore_index=True)

# 合并所有数据框
merged_df = pd.concat(dfs, ignore_index=True)

# 将数据重塑为透视表
heatmap_data = merged_df.pivot(index='Codon', columns='Species', values='Fraction')

# 绘制聚类热图
sns.set(font_scale=0.8)  # 调整字体大小

# 绘制热图
cluster_grid = sns.clustermap(heatmap_data, method='average', cmap='RdYlBu_r', figsize=(12, 18), annot=False,
                              cbar_kws={"shrink": 0.5})

# 调整x轴标签的角度和对齐方式
cluster_grid.ax_heatmap.set_xticklabels(cluster_grid.ax_heatmap.get_xticklabels(), rotation=45, ha='right')

# 增大物种和密码子名称的字体大小
cluster_grid.ax_heatmap.set_xticklabels(cluster_grid.ax_heatmap.get_xticklabels(), fontsize=12)  # 根据需要调整字体大小
cluster_grid.ax_heatmap.set_yticklabels(cluster_grid.ax_heatmap.get_yticklabels(), fontsize=12)  # 根据需要调整字体大小

# 保存图形
plt.savefig('cluster_heatmap.png', bbox_inches='tight')

# 显示图形
plt.show()