import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# 定义文件夹路径
custom_folder = 'codon_frequency_csv'
standard_folder = 'norm_codon_frequency_csv'
output_figure_folder = 'scatter_plot_figures'  # 新增的输出图表目录

# 创建输出图表目录
os.makedirs(output_figure_folder, exist_ok=True)

# 获取文件夹中的所有文件名
custom_files = os.listdir(custom_folder)

# 提取需要对比的列，例如 Fraction、Count per Thousand 等
columns_to_compare = ['Fraction']

# 创建一个3x3的子图网格
fig, axes = plt.subplots(3, 3, figsize=(12, 12))

# 遍历前9个自定义密码子使用频率文件夹中的文件
for i, file in enumerate(custom_files[:9]):
    print(f'Processing file: {file}')
    if file.endswith('.csv'):
        # 提取标题部分
        title = file.replace('codon_frequency_', '').replace('.csv', '')

        # 构建完整的文件路径
        custom_file_path = os.path.join(custom_folder, file)
        standard_file_path = os.path.join(standard_folder, f"norm_{file}")

        # 读取自定义密码子使用频率文件和对应的标准密码子使用频率文件
        custom_df = pd.read_csv(custom_file_path)
        standard_df = pd.read_csv(standard_file_path)

        # 根据密码子进行匹配
        merged_df = pd.merge(custom_df, standard_df, on='Codon', suffixes=('_custom', '_standard'))

        # 对比并绘制散点图
        for j, column in enumerate(columns_to_compare):
            ax = axes[i // 3, i % 3]  # 获取当前子图的坐标轴
            ax.scatter(merged_df[column + '_custom'], merged_df[column + '_standard'])
            ax.plot([0, 1], [0, 1], color='red', linestyle='--')  # 绘制斜率为1的红色虚线
            ax.set_xlabel('Custom Frequency')
            ax.set_ylabel('Standard Frequency')
            ax.set_title(f'{title}')

            # 计算相关系数（r 值）
            r, _ = pearsonr(merged_df[column + '_custom'], merged_df[column + '_standard'])
            ax.text(0.05, 0.9, f'r = {r:.2f}', transform=ax.transAxes)

# 调整图形的比例
plt.subplots_adjust(wspace=0.4, hspace=0.4)

# 添加大标题
plt.suptitle('Comparison', fontsize=16, fontweight='bold')

# 保存整个图形到 "scatter_plot_figures" 目录中
output_file_path = os.path.join(output_figure_folder, 'scatter_plots.png')
plt.savefig(output_file_path)

# 显示图表
plt.show()

print(f'Scatter plot saved to {output_file_path}')
