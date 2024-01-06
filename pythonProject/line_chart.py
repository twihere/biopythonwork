import os
import pandas as pd
import matplotlib.pyplot as plt

# 定义文件夹路径
custom_folder = 'codon_frequency_csv'
standard_folder = 'norm_codon_frequency_csv'
output_figure_folder = 'line_chart_figures'  # 新增的输出图表目录

# 创建输出图表目录
os.makedirs(output_figure_folder, exist_ok=True)

# 获取文件夹中的所有文件名
custom_files = os.listdir(custom_folder)

# 提取需要对比的列，例如 Fraction、Count per Thousand 等
columns_to_compare = ['Fraction']

# 遍历自定义密码子使用频率文件夹中的文件
for file in custom_files:
    if file.endswith('.csv'):
        # 构建完整的文件路径
        custom_file_path = os.path.join(custom_folder, file)
        standard_file_path = os.path.join(standard_folder, f"norm_{file}")

        # 读取自定义密码子使用频率文件和对应的标准密码子使用频率文件
        custom_df = pd.read_csv(custom_file_path)
        standard_df = pd.read_csv(standard_file_path)

        # 根据密码子进行匹配
        merged_df = pd.merge(custom_df, standard_df, on='Codon', suffixes=('_custom', '_standard'))

        # 对比并绘制可视化图形
        for column in columns_to_compare:
            plt.figure(figsize=(12, 6))  # 设置图表宽度为12，高度为6
            plt.plot(merged_df['Codon'], merged_df[column + '_custom'], label='Custom Frequency')
            plt.plot(merged_df['Codon'], merged_df[column + '_standard'], label='Standard Frequency')
            plt.xlabel('Codon')
            plt.ylabel(column)
            plt.title(f'Comparison of {column} - {file}')
            plt.xticks(rotation=90)  # 旋转 X 轴标签为垂直方向
            plt.legend()

            # 生成文件名并保存图表到输出图表目录
            output_file_name = f'{column}_comparison_{file.replace(".csv", ".png")}'
            output_file_path = os.path.join(output_figure_folder, output_file_name)
            plt.savefig(output_file_path)

            # 显示图表
            plt.show()

print(f'All comparison figures saved to {output_figure_folder}')
