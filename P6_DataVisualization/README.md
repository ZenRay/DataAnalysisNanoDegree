# Data Visualization
Data Visualization and D3.js About Udacity Project

## 项目说明
本次数据可视化项目使用数据为 [Prosper](https://s3.amazonaws.com/udacity-hosted-downloads/ud651/prosperLoanData.csv) ，可视化主要依据了在[ EDA 项目](https://github.com/ZenRay/DataAnalysisAndSummary)中的分析结果，并且利用 D3.js 为主要工具来展示在项目中分析结果以及基于从投资价值的角度分析的展示。

1. 基于在 EDA 项目中的分析，Prosper是美国一家不同于传统借贷的 P2P 借贷服务的公司，服务内容是借款人通过平台选择借款，投资人出借资金给借款人获取投资收益，而公司收益是从贷方和借方收取服务费。
2. 分析在 2013 年 10 月至 2014 年 03 月期间，交易情况可以知道在 2013 年出现了较大的波动——针对该项进行细节展示
3. 同时通过 D3 来展示各年度中借款额度与借款人所在州进行展示

### 其他说明
因为项目中使用了 ES6 的语法，需要使用支持 ES6 的浏览器运行文件

### 项目设计
因为项目的目的是希望能够通过可视化，传达出不同年份中贷款额度的变化，并且能够在交互过程中表现出各州是否有发生贷款；在各年份中，表现出各月份中贷款变化趋势，各月份贷款额度以及各州是否发生贷款。

在设计交互过程中，考虑信息传达的真实性，以及项目中使用的数据是数值类型的。因此项目使用点位置，条形图的高度来表现数据大小的量；因为需要表现出数据整体变化趋势，使用折线图来表现出不同年份的数据动态变化趋势；为了增强读者交互性，使用了颜色变化来的可视化编码；另一方面，为了传达出图形的数据内容，使用了文本内容直接表现出数据的内容。

## 项目文件结构
* getdata.py

	>用于选择需要可视化的变量名称以便于缩小原始数据
* index.html

	>用于展示可视化成果的 Web 文件
* data 文件夹

	>存放用于可视化的数据文件
	>> 使用了两个数据集，dataset.csv 包含了需要分析借款情况的数据集， statetopo.js 文件是用于制作美国各州地图的数据集
* js 文件夹

	>使用到的 JavaScript 文件如下：
	
	>>工具集包括 D3 的版本为 version 4.X ，bootstrap 使用的版本是 V3.3.7，jQuery 使用版本为 V3.2.1，以及 topojson
	
	>><font color=red> project.js 和 interactive.js 是项目中用于可视化 JavaScript 文件</font>

* css 文件夹
	>使用到的 CSS 文件如下：
	>>包括 bootstrap 支持的 CSS 文件
	
	>>style.css 文件为个人定义的 CSS 文件

## 反馈
1. javascript 改进建议：最初的 js 是依照课程方式来书写的，在项目进行中逐渐暴露出，代码混乱，模块化不足以及不是一个函数方式不足。后期根据朋友建议进行了相应的修改
2. 页面分布问题，在利用 bootstrap 进行页面布局中，存在因分辨率问题不能够很好展现可视化结果。通过更改 CSS 文件和利用 bootstrap 的栅栏格式进行了相应的修改
3. 得到的另一条反馈是，总体能够反映所提出的问题，但是细节还需要优化

## 参考
1. [优秀可视化参考](http://www.perceptualedge.com/blog/?p=1374)
2. [D3.js - Data-Driven Documents](https://d3js.org/)
3. [ D3 v3和 D3 v4 差异 Remark](https://iros.github.io/d3-v4-whats-new/#1)
4. [ D3 v4 Line Chart - bl.ocks.org](https://bl.ocks.org/mbostock/3883245)
5. [ Geo 图形转换](https://github.com/d3/d3-geo/blob/master/README.md#transforms)
6. [ Geom 图形转换示例 ]([geoTransform Example - bl.ocks.org](https://bl.ocks.org/Andrew-Reid/496078bd5e37fd22a9b43fd6be84b36b))
7. [ Javascript 刷新頁面的幾種方法](http://hugo.qov.tw/?p=1185&i=1)
8. [按日期排序 JavaScript 对象数组](https://codeday.me/bug/20170326/6296.html)
9. [Ordinal Axis - bl.ocks.org](https://bl.ocks.org/mbostock/3259783)
10. [Simple bar graph in v4 - bl.ocks.org](https://bl.ocks.org/d3noob/bdf28027e0ce70bd132edc64f1dd7ea4)
11. [动态交互柱状图 - bl.ocks.org](https://bl.ocks.org/hhhuangqiong/ffa47c3f432f2f4cd750e421b075beca)
12. [Simple bar graph in v4 - bl.ocks.org](https://bl.ocks.org/d3noob/bdf28027e0ce70bd132edc64f1dd7ea4)
13. [Bootstrap 文档](http://v3.bootcss.com/)
14. [jQuery API Documentation](http://api.jquery.com/)
15. [更改bootstrap导航栏折叠](http://dovov.com/bootstrapless.html)
