# biopythonwork
used package：OS、Pandas、Seaborn、Matplotlib、Scipy

## 代码结构如下：

![code-stucture.png](https://github.com/twihere/biopythonwork/blob/main/pythonProject/pictures/code-structure.png)
## 1、introduction
生命活动依赖蛋白质表达，蛋白质由密码子编码的氨基酸构成。密码子的使用存在偏好性，不同物种或同物种内不同基因中，同一氨基酸的多个同义密码子使用频率不同，称为密码子使用偏好（CUB）。CUB反映了物种或基因的进化过程。研究表明，基因表达水平高的基因倾向于使用最优密码子，显示出较强的CUB。技术进步使得对更高等生物CUB的研究成为可能。本研究分析了9种模式生物的密码子偏好性，并与标准使用频率进行了比较，探讨了密码子使用频率的差异及其背后的生物学意义。
## 2、dataset and method

### 1.dataset

我们获取了9个物种的CDS序列(物种为Arabidopsis thaliana、Caenorhabditis elegans、Drosophila melanogaster
E.coli、Human、Mus musculus、Rat、Saccharomyces cerevisiae、Zea mays)。


### 2.data_cleaning

data_cleaning.py是一个用来获得符合要求的CDS序列程序。


序列要求如下:(1)序列必须由A、T、C、G 四种碱基组成;(2)序列碱基数是3的倍数;(3)具有正确的起始和终止密码子;(4)移除其中的重复基因序列以及序列长度≥300 bp。
### 3.condon_frequence

condon_frequence.py是一个用来分析cds的程序并且还能生成各个物种的Codon、	Amino Acid	、Fraction、Count per Thousand、Count	、Species。
### 4.scatter_plot

scatter_plot.py可以生成不同物种密码子使用频率的scatter_plot图。

### 5.line_chart

line_chart.py
用来比较不同物种的密码子使用频率和标准的使用频率。
### 6.cluster_heatmap

cluster_heatmap.py用来生成不同物种的密码子使用频率的cluster_heatmap图。

## 3、result


折线图保存在image文件夹中，只展示第一张图



Comparison of Fraction - codon frequency Arabidopsis thaliana.csv
![codon frequency Arabidopsis thaliana.png](https://github.com/twihere/biopythonwork/blob/main/pythonProject/pictures/codon%20frequency%20Arabidopsis%20thaliana.png)




compare
![scatter_plot.png](https://github.com/twihere/biopythonwork/blob/main/pythonProject/pictures/scatter_plots.png)




cluster_heatmap图
![cluster_heatmap.png](https://github.com/twihere/biopythonwork/blob/main/pythonProject/pictures/cluster_heatmap.png)
在这个图中，每一行代表不同的密码子（DNA上的三个核苷酸序列），而每一列代表不同的物种。颜色的深浅表示密码子使用频率的高低，颜色越深（趋向蓝色）表示使用频率越低，颜色越浅（趋向黄色）表示使用频率越高。
图的左侧和顶部有树状图（聚类树），用来显示密码子使用频率模式的相似性。物种之间的树状图揭示了基因组密码子使用频率的相似性。例如，如果两个物种在树状图中彼此接近，这意味着它们在密码子使用频率上有更多的相似性。同样，密码子之间的树状图显示了哪些密码子在不同物种中有相似的使用模式。


