# 目录结构
## crawler 
### carpolicy.py
- 数据来源[汽车工业协会]，爬汽车政策

### chezhuzhijia.py
- 数据来源[车主之家]，爬汽车销量数据

### renrenche.py
- 数据来源[人人车]，爬二手车交易数据，更新出售时间（每天都要运行）

### yiche.py
- 数据来源[易车网]，爬汽车配置数据、以及在售汽车报价（每天都要运行）

### config.py
- 配置文件
- mysql连接配置
- redis连接配置
- 各个汽车网站的链接

### logs
- 存放日志的文件夹

## price_predict
### price_prediction.py
- 价格预测


## sql
- 各个数据的创表语句
注意：auto_project.sql就是整个数据库的数据！直接用导入mysql就行！
