DROP TABLE IF EXISTS car_price;

CREATE TABLE car_dealer(
  id char(32) NOT NULL COMMENT '易车的经销商id',
  province varchar(255) NOT NULL COMMENT '北京市、天津市、上海市、重庆市为直辖市，city和province的值相同',
  city varchar(255) NOT NULL COMMENT '',
  area varchar(255) COMMENT '有些经销商没有具体到区',
  name varchar(255) NOT NULL COMMENT '经销商名称',
  full_name varchar(255) COMMENT '经销商全名',
  type tinyint(4) NOT NULL COMMENT '综合店[0]、4S店[1]、特许店[2]',
  address varchar(255) NOT NULL COMMENT '经销商地址',
  official_webstie varchar(255) COMMENT '经销商官网',
  sale_phone_number varchar(255) COMMENT '销售电话',
  contact_number varchar(255) COMMENT '联系电话，以|分隔开',
  PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE car_price(
  id int(11) NOT NULL AUTO_INCREMENT,
  carid char(32) NOT NULL COMMENT '车辆ID',
  dealer_id char(32) NOT NULL COMMENT '经销商id',
  sales_price int(11) NOT NULL COMMENT '销售价格',
  is_promotion boolean NOT NULL COMMENT '是否为促销价格',
  publish_date date NOT NULL COMMENT '如果is_promotion=TRUE，则表示促销价格发布日期，否则表示爬取的日期',
  end_date date COMMENT '促销价格的截止日期，有些店可能没有促销',
--   price_url varchar(255) NOT NULL COMMENT '报价的来源',  # 这个url没什么必要了，因为都是 'http://dealer.bitauto.com/%s/price_detail/%s.html' % (dealer_id, carid)的形式，用的时候拼接一下即可
  PRIMARY KEY (id),
  FOREIGN KEY (carid) REFERENCES car_base_info(unique_id),
  FOREIGN KEY (dealer_id) REFERENCES car_dealer(id)
)ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


