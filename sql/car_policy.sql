DROP TABLE IF EXISTS car_policy;

CREATE TABLE car_policy(
  id char(32) NOT NULL COMMENT '中国汽车工业协会的政策Id',
  title varchar(255) NOT NULL COMMENT '政策标题',
  release_date date NOT NULL COMMENT '发布日期',
  release_department varchar(255) NOT NULL COMMENT '发布单位',
  begin_date date COMMENT '起始时间',
  end_date varchar(255) COMMENT '终止时间',
  url varchar(255) NOT NULL COMMENT '中国汽车协会政策url',
  type tinyint NOT NULL COMMENT '政策类型[1:全国政策, 2:地方政策]',
  content text NOT NULL COMMENT '政策内容',
  PRIMARY KEY(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;