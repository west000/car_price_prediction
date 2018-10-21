DROP TABLE IF EXISTS car_sales_record;

CREATE TABLE car_sales_record(
  id int(11) NOT NULL AUTO_INCREMENT,
  brand varchar(255) NOT NULL COMMENT '品牌',
  subbrand varchar(255) NOT NULL COMMENT '子品牌',
  serie varchar(255) NOT NULL COMMENT '系列',
  serieId int(11) NOT NULL COMMENT '车主之家的系列ID',
  sale_month date NOT NULL COMMENT '日期',
  sales_volume int(11) COMMENT '销量',
  PRIMARY KEY(id)
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;