# biopythonwork
用到的包：OS Pandas Seaborn Matplotlib Scipy
## 1、introduction
生命活动依赖蛋白质表达，蛋白质由密码子编码的氨基酸构成。密码子的使用存在偏好性，不同物种或同物种内不同基因中，同一氨基酸的多个同义密码子使用频率不同，称为密码子使用偏好（CUB）。CUB反映了物种或基因的进化过程。研究表明，基因表达水平高的基因倾向于使用最优密码子，显示出较强的CUB。技术进步使得对更高等生物CUB的研究成为可能。本研究分析了9种模式生物的密码子偏好性，并与标准使用频率进行了比较，探讨了密码子使用频率的差异及其背后的生物学意义。
## 2、method

### 1.dataset

首先我们获取了9个物种的CDS序列，并生成了每种氨基酸对应密码子的使用频率，根据这个结果我们做了一个热图来表示不同物种对不同密码子的使用频率即密码子使用偏好性，并对其进行了聚类。
接下来我们对我们自己生成的密码子使用偏好性与标准表进行了对比，以折线图的方式对9个物种的对比结果进行了可视化。


compare
![scatter_plot.png](https://github.com/twihere/biopythonwork/blob/main/pythonProject/pictures/scatter_plot.png)

Comparison of Fraction - codon frequency Arabidopsis thaliana.csv
![codon frequency Arabidopsis thaliana.png](https://github.com/twihere/biopythonwork/blob/main/pythonProject/pictures/codon%20frequency%20Arabidopsis%20thaliana.png)

Comparison of Fraction - codon frequency Caenorhabditis elegans.csv
![codon frequency Caenorhabditis elegans.png](https://github.com/twihere/biopythonwork/blob/main/pythonProject/pictures/codon%20frequency%20Caenorhabditis%20elegans.png)

Comparison of Fraction - codon frequency Drosophila melanogaster.csv
![codon frequency Drosophila melanogaster.png](https://github.com/twihere/biopythonwork/blob/main/pythonProject/pictures/codon%20frequency%20Drosophila%20melanogaster.png)

Comparison of Fraction - codon frequency E.coli.csv
![codon frequency E.coli.png](https://github.com/twihere/biopythonwork/blob/main/pythonProject/pictures/codon%20frequency%20E.coli.png)

Comparison of Fraction - codon frequency Human.csv
![codon frequency Human.png](https://github.com/twihere/biopythonwork/blob/main/pythonProject/pictures/codon%20frequency%20Human.png)

Comparison of Fraction - codon frequency Mus musculus.csv
![codon frequency Mus musculus.png](https://github.com/twihere/biopythonwork/blob/main/pythonProject/pictures/codon%20frequency%20Mus%20musculus.png)

Comparison of Fraction - codon frequency Rat.csv
![codon frequency Rat.png](https://github.com/twihere/biopythonwork/blob/main/pythonProject/pictures/codon%20frequency%20Rat.png)

Comparison of Fraction - codon frequency Saccharomyces cerevisiae.csv
![codon frequency Saccharomyces cerevisiae.png](https://github.com/twihere/biopythonwork/blob/main/pythonProject/pictures/codon%20frequency%20Saccharomyces%20cerevisiae.png)

Comparison of Fraction - codon frequency Zea mays.csv
![codon frequency Zea mays.png](https://github.com/twihere/biopythonwork/blob/main/pythonProject/pictures/codon%20frequency%20Zea%20mays.png)

### 2.data clean


主要用于处理FASTA格式的遗传序列文件。FASTA是一种文本格式，常用于表示核苷酸序列或肽链序列，每个序列前都会有一个以">"开始的描述行。
首先，定义了一个read_fasta函数，它接受一个文件路径参数，读取该路径下的FASTA文件，并返回文件中所有序列的列表。如果一行以">"开始，表示序列的开始；如果不是，则将该行的内容（去除空白字符）累加到当前序列。
接着，定义了filter_cds_sequences函数，用于筛选和清理编码区（CDS）序列。该函数调用read_fasta函数获取序列列表，然后对每个序列进行一系列的检查：序列只包含A、T、C、G四种碱基，序列长度为3的倍数，序列以有效的起始密码子开始，以有效的终止密码子结束，序列长度大于等于300个碱基对，且序列不是重复序列。满足这些条件的序列将被添加到清理后的序列列表中。
然后，脚本定义了一个字典species_files，包含不同物种的FASTA文件路径。脚本遍历该字典，对每个物种的文件进行处理，调用filter_cds_sequences函数获取清理后的序列，然后将这些序列写入到新的文件中，保存在cleaned_sequences文件夹内。


### 3.frequency compute

这段代码用于分析遗传编码序列（CDS），计算特定密码子的使用概率、总计数以及每千个密码子中的出现次数。首先，它定义了一个密码子到氨基酸的映射字典codon_to_aa，其中包含了所有标准密码子及其对应的氨基酸。接着定义了				read_cds_sequences_from_file函数，用于从指定路径读取CDS序列，并移除每行末尾的换行符。
calculate_codon_probability_and_count函数计算给定密码子在序列中的出现概率和计数，以及与之同义的密码子的总出现次数。这个函数返回密码子的使用概率、计数和每千个密码子中的计数，都经过四舍五入处理。
然后，代码读取了一系列预先清理好的CDS序列文件路径，并对每个文件中的序列进行了密码子使用情况的分析。对于每个密码子，它计算了相关的统计数据，并将结果保存在一个数据框架中，其中包含密码子、对应的氨基酸、使用概率、每千个密码子中的计数和总计数，以及物种信息。这些数据最后被排序并保存到CSV文件中，用于进一步分析或报告。

### 4.clustering_heatmap

这段代码是使用Python中的Pandas、Seaborn和Matplotlib库来分析和可视化不同物种中密码子使用频率的热图。首先，它定义了包含多个CSV文件的文件夹路径，这些CSV文件包含了不同物种密码子使用频率的数据。代码通过遍历该文件夹，读取每个CSV文件，并将其存储为Pandas DataFrame对象的列表。
在处理每个物种的数据时，代码将物种名称添加为新列，并且创建了一个集合all_codons来追踪所有出现过的密码子。这样做是为了确保在后续步骤中，每个物种DataFrame都包含所有可能的密码子，即使某个密码子在该物种中没有出现（在这种情况下，其使用频率被设置为0.0）。
接下来，代码将所有物种的DataFrame合并成一个大的DataFrame，并将其重塑成一个透视表heatmap_data，行为密码子，列为物种，值为密码子的使用频率。
最后，使用Seaborn的clustermap函数绘制了一个聚类热图，该热图基于密码子使用频率的相似性对密码子和物种进行了聚类。热图使用了RdYlBu_r色谱，并设置了合适的图形大小以及颜色条属性。代码还调整了轴标签的角度、对齐方式和字体大小，以提高图形的可读性。最后，将生成的热图保存为PNG文件，并显示在屏幕上。

###   5.line_chart

这段代码主要用于比较和可视化自定义密码子使用频率数据与标准密码子使用频率数据之间的差异。首先，代码定义了两个文件夹路径，一个是存储自定义密码子使用频率数据的custom_folder，另一个是存储标准数据的standard_folder。然后，代码遍历custom_folder中的所有.csv文件。
对于每个自定义频率文件，代码构建了对应的标准频率文件的路径，然后分别读取这两个文件到Pandas的DataFrame中。使用pd.merge函数，代码根据密码子将两个DataFrame合并在一起，使得每个密码子的自定义频率和标准频率能够一一对应。
随后，代码遍历columns_to_compare列表中指定的列名（在这个例子中是Fraction），对于每个指定的列，它创建一个新的图形窗口，并绘制两个频率的折线图。这些图显示了每个密码子的自定义使用频率与标准使用频率之间的对比。X轴表示密码子，Y轴表示列名指定的度量（这里是频率分数），并且X轴的标签被旋转为垂直方向以便阅读。
最后，每个图形都被赋予了标题，标题中包含了当前正在比较的列名和文件名。此外，图例被添加以区分自定义频率与标准频率的折线，使得对比结果更加明显。每次循环结束时，使用plt.show()显示图形。

###   6.scatter plot

这段代码是用于比较不同数据集中密码子使用频率的统计分析和可视化工具。具体来说，它比较了自定义密码子使用频率数据集与标准数据集，并通过散点图显示它们之间的关系。这可以帮助研究人员理解特定物种的密码子使用模式与标准参考模式之间的差异。
代码首先定义了两个文件夹路径，一个用于存放自定义密码子频率的CSV文件，另一个用于存放标准密码子频率的CSV文件。然后，代码遍历自定义文件夹中的所有CSV文件，对于每个文件，它构建了文件的完整路径，然后加载了自定义和标准的密码子频率数据。
通过使用Pandas库中的merge函数，代码将自定义和标准的数据集根据密码子进行匹配合并。接着，它创建了一个3x3的子图网格，对每个密码子使用频率进行可视化对比，使用散点图来显示自定义数据集与标准数据集的密码子频率之间的关系。此外，它还在每个子图上绘制了一条红色虚线，表示完美相关的参考线（斜率为1的线），并计算了Pearson相关系数（r值）来量化两个数据集之间的相关性。
最后，代码调整了图形的布局，添加了一个总标题，并且使用Matplotlib显示了最终的图形。这样的可视化有助于直观地比较和理解不同数据集之间的相似性和差异性。


## 3、result

热点图
![cluster_heatmap.png](https://github.com/twihere/biopythonwork/blob/main/pythonProject/pictures/cluster_heatmap.png)
在这个热图中，每一行代表不同的密码子（DNA上的三个核苷酸序列），而每一列代表不同的物种。颜色的深浅表示密码子使用频率的高低，颜色越深（趋向蓝色）表示使用频率越低，颜色越浅（趋向黄色）表示使用频率越高。
图的左侧和顶部有树状图（聚类树），用来显示密码子使用频率模式的相似性。物种之间的树状图揭示了基因组密码子使用频率的相似性。例如，如果两个物种在树状图中彼此接近，这意味着它们在密码子使用频率上有更多的相似性。同样，密码子之间的树状图显示了哪些密码子在不同物种中有相似的使用模式。


通过我们自己获得的9个物种的密码子使用频率的分析，可以观察到一下现象。
首先，我们能明显观察密码子ATG、TGG的使用频率几乎是百分百，这与实际情况相一致。ATG在所有生物中扮演一个重要的角色，即唯一的起始密码子，编码甲硫氨酸，只不过在真核生物中起始氨基酸为甲硫氨酸（Met），而在原核生物中为甲酰甲硫氨酸（fMet）。而TGG所编码的氨基酸为色氨酸，这个密码子也是唯一能够编码色氨酸的密码子，所以这两个密码子的使用频率为1是合情合理的。
第二，我们观察到似乎热图中一部分的氨基酸似乎在所有9种生物中的使用频率普遍较低，而另一部分则普遍相对较高。我们认为可能存在一些因素能够影响所有生物，使其对于一些密码子的使用较为困难，而另一些密码子则更容易被利用。这可能与蛋白质结构、GC富集程度或基因突变频率、方式相关。
第三，我们观察到，在一些物种之间，密码子的使用频率存在显而易见的差异，这也是意料之中的。不同物种之间密码子使用偏好性不同的原因是复杂而多样的，这涉及到生物学、遗传学和演化等方面的因素。以下是一些我们了解的原因：

##### 1）基因组组成：不同物种的基因组组成可能有所不同。基因组中的密码子使用偏好性可能受到基因组结构和组织的影响。某些物种可能拥有特定的密码子使用模式，反映了它们的遗传特征。

##### 2）选择压力，物种在演化过程中可能受到自然选择的影响，使得特定密码子更有利于适应环境。不同的环境条件可能导致不同物种对某些密码子的使用频率有所偏好。

##### 3）突变，突变是遗传变异的一种方式，可能导致密码子的变化。不同物种之间的突变率和突变类型可能不同，进而影响密码子的使用。

##### 4）基因表达调控，不同物种可能对基因表达调控有不同的需求，从而影响密码子的选择。一些密码子可能在某些物种中更适合特定的调控机制。

##### 5）物种间的进化关系，进化关系可能影响密码子使用的相似性和差异性。密切相关的物种可能有更相似的密码子使用模式。总的来说，不同物种之间密码子使用偏好性不同的原因是一个复杂的交互过程，包含多种因素。

最后通过聚类结果我们可以看到，一些物种它们的密码子使用偏好性较为类似，一些则又一定差距，这与它们之间的遗传距离以及生物分类是相符的。比较典型的是小鼠和大鼠极为相似，它们与人又较为相似。（其他的我在图里看不太出来，后面聚类结果有了并且如果说得通的话可以再补充。不过感觉不说也行。）
通过将我们自己获得的9种物种的密码子使用偏好性与标准表对比，我们发现两者相比，结果基本一致，这也能对我们前面获得结果的正确性进行一个佐证。

## 4、discussion
密码子使用偏好性是基因组学和遗传学领域中一个比较重要的研究方向。我们的分析观察到了一些物种之间的密码子使用存在一些共性，但更多观察注意到了他们之间的差异，并且对这些差异产生的原因进行了简单的探讨，具体推理总结了一些因素：自然选择与环境适应、突变和遗传变异、基因表达调控、物种进化关系等。通过这次研究，我们更全面地理解了不同物种之间密码子使用偏好性地原因。并且我们认为，这有助于揭示生物多样性地基础，为未来基因组学和遗传学研究提供了新的方向和挑战。