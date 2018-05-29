[toc]

# Project: EnronMachineLearning
Udacity project 5 about machine learning

# 项目概述
安然曾是 2000 年美国最大的公司之一。2002 年，由于其存在大量的企业欺诈行为，这个昔日的大集团土崩瓦解。 在随后联邦进行的调查过程中，大量有代表性的保密信息进入了公众的视线，包括成千上万涉及高管的邮件和详细的财务数据。

你将在此项目中扮演侦探，运用你的新技能，根据安然丑闻中公开的财务和邮件数据来构建相关人士识别符。 为了协助你进行侦查工作，我们已将数据与手动整理出来的欺诈案涉案人员列表进行了合并， 这意味着被起诉的人员要么达成和解，要么向政府签署认罪协议，再或者出庭作证以获得免受起诉的豁免权。

在此项目中，最终运用机器学习技能构建一个算法，通过公开的安然财务和邮件数据集，找出有欺诈嫌疑的安然雇员。

# 项目目的
* 处理现实当中不完美的数据集
* 使用测试数据验证机器学习的结果
* 使用定量指标评估机器学习的结果
* 创建、选择和转换特征
* 比较机器学习算法的性能
* 为获得最大性能调整机器学习算法
* 清楚表述你的机器学习算法

# 项目流程
我们将给予你可读入数据的初始代码，将你选择的特征放入 numpy 数组中，该数组是大多数 sklearn 函数假定的输入表单。 你要做的就是设计特征，选择并调整算法，用以测试和评估识别符。 我们在设计数个迷你项目之初就想到了这个最终的项目，因此请记得借助你已完成的工作成果。

在预处理此项目时，我们已将安然邮件和财务数据与字典结合在一起，字典中的每对键值对应一个人。 字典键是人名，值是另一个字典（包含此人的所有特征名和对应的值）。 数据中的特征分为三大类，即财务特征、邮件特征和 POI 标签。

财务特征: ['salary', 'deferral\_payments', 'total\_payments', 'loan\_advances', 'bonus', 'restricted\_stock\_deferred', 'deferred\_income', 'total\_stock\_value', 'expenses', 'exercised\_stock\_options', 'other', 'long\_term\_incentive', 'restricted\_stock', 'director\_fees'] (单位均是美元）

邮件特征: ['to\_messages', 'email\_address', 'from\_poi\_to\_this\_person', 'from\_messages', 'from\_this\_person\_to\_poi', 'shared\_receipt\_with\_poi'] (单位通常是电子邮件的数量，明显的例外是 ‘email\_address’，这是一个字符串）

POI 标签: [‘poi’] \(boolean，整数)

我们鼓励你在启动器功能中制作，转换或重新调整新功能。如果这样做，你应该把新功能存储到my_dataset，如果你想在最终算法中使用新功能，你还应该将功能名称添加到 my_feature_list，以便于你的评估者可以在测试期间访问它。关于如何在数据集中添加具体的新要素的例子，可以参考“特征选择”这一课。

此外，我们还建议你可以在完成项目过程中做一些记号。你可以写出系列问题的答案（在下一页），将这个作为提交的项目的一部分，以便于评估者了解到你对于不同方面分析的方法。你的思维过程在很大程度上比你的最终项目更重要，我们将通过你在这些问题的解答中了解你的思维过程。

# 项目文件说明
| File | Description|
|------|------------|
|README.md|项目启动说明，关于项目的基本描述|
|Report.ipynb|项目运行代码文件，使用 jupyter notebook 文件形式保存|
|report|项目报告文件夹|
|report/report.md|项目报告文件，以 markdown 形式保存|
|final\_project|在项目运行中使用到的一些模块文件夹|
|final\_project/feature\_format.py|在该模块中调用了featureFormat 和 targetFeatureSplit 两个函数|
|tools|在项目中验证和评估中需要使用到的模块文件夹|
|tools/tester.py|在该模块中调用了 dump\_classifier\_and\_data 和 test\_classifier 两个函数|
|my\_dataset.pkl| 运行 Report.ipynb 之后，生成的数据集文件|
|my\_classifier.pkl| 运行 Report.ipynb 之后，生成的模型文件|
|my\_feature\_list.pkl| 运行 Report.ipynb 之后，生成的特征列表文件|
