# biopythonwork

## 1、introduction

## 2、method
### 1.data clean


主要用于处理FASTA格式的遗传序列文件。FASTA是一种文本格式，常用于表示核苷酸序列或肽链序列，每个序列前都会有一个以">"开始的描述行。
首先，定义了一个read_fasta函数，它接受一个文件路径参数，读取该路径下的FASTA文件，并返回文件中所有序列的列表。如果一行以">"开始，表示序列的开始；如果不是，则将该行的内容（去除空白字符）累加到当前序列。
接着，定义了filter_cds_sequences函数，用于筛选和清理编码区（CDS）序列。该函数调用read_fasta函数获取序列列表，然后对每个序列进行一系列的检查：序列只包含A、T、C、G四种碱基，序列长度为3的倍数，序列以有效的起始密码子开始，以有效的终止密码子结束，序列长度大于等于300个碱基对，且序列不是重复序列。满足这些条件的序列将被添加到清理后的序列列表中。
然后，脚本定义了一个字典species_files，包含不同物种的FASTA文件路径。脚本遍历该字典，对每个物种的文件进行处理，调用filter_cds_sequences函数获取清理后的序列，然后将这些序列写入到新的文件中，保存在cleaned_sequences文件夹内。


### 2.frequency compute

这段代码用于分析遗传编码序列（CDS），计算特定密码子的使用概率、总计数以及每千个密码子中的出现次数。首先，它定义了一个密码子到氨基酸的映射字典codon_to_aa，其中包含了所有标准密码子及其对应的氨基酸。接着定义了				read_cds_sequences_from_file函数，用于从指定路径读取CDS序列，并移除每行末尾的换行符。
calculate_codon_probability_and_count函数计算给定密码子在序列中的出现概率和计数，以及与之同义的密码子的总出现次数。这个函数返回密码子的使用概率、计数和每千个密码子中的计数，都经过四舍五入处理。
然后，代码读取了一系列预先清理好的CDS序列文件路径，并对每个文件中的序列进行了密码子使用情况的分析。对于每个密码子，它计算了相关的统计数据，并将结果保存在一个数据框架中，其中包含密码子、对应的氨基酸、使用概率、每千个密码子中的计数和总计数，以及物种信息。这些数据最后被排序并保存到CSV文件中，用于进一步分析或报告。

### 3.clustering_heatmap

这段代码是使用Python中的Pandas、Seaborn和Matplotlib库来分析和可视化不同物种中密码子使用频率的热图。首先，它定义了包含多个CSV文件的文件夹路径，这些CSV文件包含了不同物种密码子使用频率的数据。代码通过遍历该文件夹，读取每个CSV文件，并将其存储为Pandas DataFrame对象的列表。
在处理每个物种的数据时，代码将物种名称添加为新列，并且创建了一个集合all_codons来追踪所有出现过的密码子。这样做是为了确保在后续步骤中，每个物种DataFrame都包含所有可能的密码子，即使某个密码子在该物种中没有出现（在这种情况下，其使用频率被设置为0.0）。
接下来，代码将所有物种的DataFrame合并成一个大的DataFrame，并将其重塑成一个透视表heatmap_data，行为密码子，列为物种，值为密码子的使用频率。
最后，使用Seaborn的clustermap函数绘制了一个聚类热图，该热图基于密码子使用频率的相似性对密码子和物种进行了聚类。热图使用了RdYlBu_r色谱，并设置了合适的图形大小以及颜色条属性。代码还调整了轴标签的角度、对齐方式和字体大小，以提高图形的可读性。最后，将生成的热图保存为PNG文件，并显示在屏幕上。

###   4.line_chart

这段代码主要用于比较和可视化自定义密码子使用频率数据与标准密码子使用频率数据之间的差异。首先，代码定义了两个文件夹路径，一个是存储自定义密码子使用频率数据的custom_folder，另一个是存储标准数据的standard_folder。然后，代码遍历custom_folder中的所有.csv文件。
对于每个自定义频率文件，代码构建了对应的标准频率文件的路径，然后分别读取这两个文件到Pandas的DataFrame中。使用pd.merge函数，代码根据密码子将两个DataFrame合并在一起，使得每个密码子的自定义频率和标准频率能够一一对应。
随后，代码遍历columns_to_compare列表中指定的列名（在这个例子中是Fraction），对于每个指定的列，它创建一个新的图形窗口，并绘制两个频率的折线图。这些图显示了每个密码子的自定义使用频率与标准使用频率之间的对比。X轴表示密码子，Y轴表示列名指定的度量（这里是频率分数），并且X轴的标签被旋转为垂直方向以便阅读。
最后，每个图形都被赋予了标题，标题中包含了当前正在比较的列名和文件名。此外，图例被添加以区分自定义频率与标准频率的折线，使得对比结果更加明显。每次循环结束时，使用plt.show()显示图形。

###   5.scatter plot

这段代码是用于比较不同数据集中密码子使用频率的统计分析和可视化工具。具体来说，它比较了自定义密码子使用频率数据集与标准数据集，并通过散点图显示它们之间的关系。这可以帮助研究人员理解特定物种的密码子使用模式与标准参考模式之间的差异。
代码首先定义了两个文件夹路径，一个用于存放自定义密码子频率的CSV文件，另一个用于存放标准密码子频率的CSV文件。然后，代码遍历自定义文件夹中的所有CSV文件，对于每个文件，它构建了文件的完整路径，然后加载了自定义和标准的密码子频率数据。
通过使用Pandas库中的merge函数，代码将自定义和标准的数据集根据密码子进行匹配合并。接着，它创建了一个3x3的子图网格，对每个密码子使用频率进行可视化对比，使用散点图来显示自定义数据集与标准数据集的密码子频率之间的关系。此外，它还在每个子图上绘制了一条红色虚线，表示完美相关的参考线（斜率为1的线），并计算了Pearson相关系数（r值）来量化两个数据集之间的相关性。
最后，代码调整了图形的布局，添加了一个总标题，并且使用Matplotlib显示了最终的图形。这样的可视化有助于直观地比较和理解不同数据集之间的相似性和差异性。


## 3、result

热点图
![cluster_heatmap.png](..%2F..%2Ffinalbio%2FpythonProject%2Fcluster_heatmap.png)

