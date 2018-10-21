-- DROP TABLE IF EXISTS car;

CREATE TABLE car(
  id int(11) NOT NULL AUTO_INCREMENT,
  brand varchar(255) NOT NULL COMMENT '品牌',
  unique_id varchar(255) NOT NULL COMMENT '车辆ID，必须唯一，防止重复爬取',
  version varchar(255) NOT NULL COMMENT '车型号',
  first_licence date NOT NULL COMMENT '首次上牌日期',
  mailage int(11) NOT NULL COMMENT '行驶里程数',
  new_price int(11) NOT NULL COMMENT '新车价格',
  current_price int(11) NOT NULL COMMENT '当前二手价格',
  source tinyint(4) DEFAULT '1' COMMENT '来源，车商为1，个人为0',
  area varchar(255) NOT NULL COMMENT '地区',
  color varchar(255) NOT NULL COMMENT '颜色',
  transfer_times int(11) NOT NULL COMMENT '过户次数',
  add_date date NOT NULL COMMENT '上架日期',
  sale_date date COMMENT '最终交易日期',
  fix_record text COMMENT '维修记录',
  url varchar(255) NOT NULL,
  PRIMARY KEY(id),
  UNIQUE KEY unique_id (unique_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

