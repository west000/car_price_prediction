--  DROP TABLE IF EXISTS car_body_info, car_power_system, car_chassis_brake, car_security_configuration,
--      car_drive_assistance, car_external_configuration, car_internal_configuration, car_seat_configuration, car_infotainment;
--  DROP TABLE IF EXISTS car_base_info;

CREATE TABLE car_base_info (
  id int(11) NOT NULL AUTO_INCREMENT,
--   基本信息
  unique_id char(32) NOT NULL COMMENT '车辆ID, 易车的汽车id',
  brand varchar(255) NOT NULL COMMENT '品牌',
  subbrand varchar(255) NOT NULL COMMENT '子品牌',
  series varchar(255) NOT NULL COMMENT '系列',
  version varchar(255) NOT NULL COMMENT '版本',
  guide_price int(11) COMMENT '厂商指导价',
  mark_date date COMMENT '上市日期',
  model_level varchar(255) NOT NULL COMMENT '车型级别',
  model_type varchar(255) NOT NULL COMMENT '车身型式',
  power_type varchar(255) NOT NULL COMMENT '动力类型',
  engine varchar(255) NOT NULL COMMENT '发动机',
  max_power_torque varchar(255) NOT NULL COMMENT '最大功率/最大扭矩',
  transmission_type varchar(255)NOT NULL COMMENT '变速箱类型',
  fuel_consumption varchar(255)NOT NULL COMMENT '混合工况油耗[L/100km]',
  max_speed int(11) COMMENT '最高车速[km/h]',
  acceleration_time decimal(10,1) COMMENT '0-100km/h加速时间[s]',
  envir_standards varchar(255) NOT NULL COMMENT '环保标准',
  warranty_policy varchar(255) NOT NULL COMMENT '保修政策',
  exterior_color text NOT NULL COMMENT '外观颜色，以|分割',
  exterior_color_code text NOT NULL COMMENT '外观颜色代码，以|分割',
  stop_selling boolean NOT NULL COMMENT '是否停售',
  source_url varchar(255) NOT NULL COMMENT '数据来源',
  img_url varchar(255) COMMENT '图片链接',
  real_shot_img_link varchar(255) COMMENT '实拍图片链接',
  PRIMARY KEY(id),
  UNIQUE KEY unique_id (unique_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE car_body_info(
  unique_id char(32) NOT NULL,
--   车身尺寸
  length int(11) COMMENT '长[mm]',
  width int(11) COMMENT '宽',
  height int(11) COMMENT '高',
  wheelbase int(11) COMMENT '轴距[mm]',
  quality int(11) COMMENT '整备质量[kg]',
  seats int(11) COMMENT '座位数[个]',
  luggage_volume int(11) COMMENT '行李厢容积[L]',
  fuel_tank_volume int(11) COMMENT '油箱容积[L]',
  front_tire varchar(255) NOT NULL COMMENT '前轮胎规格',
  rear_tire varchar(255) NOT NULL COMMENT '后轮胎规格',
  spare_tire varchar(255) NOT NULL COMMENT '备胎',
  PRIMARY KEY (unique_id),
  FOREIGN KEY (unique_id) REFERENCES car_base_info(unique_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE car_power_system(
  unique_id char(32) NOT NULL,
--   动力系统
  displacement int(11) COMMENT '排气量(mL)',
  max_power int(11) COMMENT '最大功率[kW]',
  max_horsepower int(11) COMMENT '最大马力[Ps]',
  max_power_speed int(11) COMMENT '最大功率转速[rpm]',
  max_torque int(11) COMMENT '最大扭矩[N.m]',
  max_torque_speed varchar(255) NOT NULL COMMENT '最大扭矩转速[rpm]',
  cylinder_num tinyint(4) COMMENT '气缸数',
  cylinder_form varchar(255) NOT NULL COMMENT '缸体形式[直列、V型、W型、水平对置、转子]',
  air_intake_form varchar(255) NOT NULL COMMENT '进气形式[自然吸气、涡轮增压、机械增压、双增压]',
  oil_supply_method varchar(255) NOT NULL COMMENT '供油方式[多点电喷、直喷、单点电喷、化油器、混合喷射]',
  fuel_marking varchar(255) NOT NULL COMMENT '燃油标号',
  transmission_type varchar(255) NOT NULL COMMENT '变速箱类型',
  gears_number tinyint(4) COMMENT '挡位个数',
  engine_start_stop boolean COMMENT '发动机启停',
  compression_ratio varchar(255) COMMENT '压缩比，可为空',
  PRIMARY KEY (unique_id),
  FOREIGN KEY (unique_id) REFERENCES car_base_info(unique_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE car_chassis_brake(
  unique_id char(32) NOT NULL,
--   底盘制动
  driving_method varchar(255) NOT NULL COMMENT '驱动方式[前轮驱动、后轮驱动、全时四驱、分时四驱、适时四驱]',
  front_suspension_type varchar(255) NOT NULL COMMENT '前悬架类型[双叉臂式独立悬架、多连杆式独立悬架、麦弗逊独立悬架]',
  rear_suspension_type varchar(255) NOT NULL COMMENT '后悬架类型[扭力梁式非独立悬架、拖拽臂式半独立悬架、双叉臂式独立悬架、多连杆式独立悬架、整体桥式非独立悬架]',
  front_brake_type varchar(255) NOT NULL COMMENT '前轮制动器类型[鼓式、盘式、通风盘、碳纤维陶瓷]',
  rear_brake_type varchar(255) NOT NULL COMMENT '后轮制动器类型[鼓式、盘式、通风盘、碳纤维陶瓷]',
  parking_brake_type varchar(255) NOT NULL COMMENT '驻车制动类型[手拉式、脚踩式、电子式]',
  limited_slip_differential varchar(255) NOT NULL COMMENT '限滑差速器/差速锁[前桥、后桥、中央]',
  adjustable_suspension boolean NOT NULL COMMENT '可调悬架',
  body_structure varchar(255) NOT NULL COMMENT '车体结构[非承载式、承载式]',
  approach_angle decimal(10,1) COMMENT '接近角',
  departure_angle decimal(10,1) COMMENT '离去角',
  PRIMARY KEY (unique_id),
  FOREIGN KEY (unique_id) REFERENCES car_base_info(unique_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE car_security_configuration(
  unique_id char(32) NOT NULL,
--   安全配置
  anti_lock_brake boolean NOT NULL COMMENT '防抱死制动(ABS)',
  braking_force_distribution boolean NOT NULL COMMENT '制动力分配(EBD/CBC等)',
  brake_assist boolean NOT NULL COMMENT '制动辅助(BA/EBA等)',
  traction_control boolean NOT NULL COMMENT '牵引力控制(ARS/TCS等)',
  body_stability_control boolean NOT NULL COMMENT '车身稳定控制(ESP/DSC等)	',
  main_driving_airbag boolean NOT NULL COMMENT '主驾驶安全气囊	',
  first_officer_airbag boolean NOT NULL COMMENT '副驾驶安全气囊',
  front_airbag boolean NOT NULL COMMENT '前侧气囊',
  rear_airbag boolean NOT NULL COMMENT '后侧气囊',
  side_curtain boolean NOT NULL COMMENT '侧安全气帘',
  knee_balloon boolean NOT NULL COMMENT '膝部气囊',
  seat_belts boolean NOT NULL COMMENT '安全带气囊',
  rear_center_airbag boolean NOT NULL COMMENT '后排中央气囊',
  tire_pressure_monitoring boolean NOT NULL COMMENT '胎压监测',
  zero_continuous_tire boolean NOT NULL COMMENT '零胎压续行轮胎',
  rear_child_seat_interface boolean NOT NULL COMMENT '后排儿童座椅接口',
  PRIMARY KEY (unique_id),
  FOREIGN KEY (unique_id) REFERENCES car_base_info(unique_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE car_drive_assistance(
  unique_id char(32) NOT NULL,
--   驾驶辅助
  cruise_control varchar(255) NOT NULL COMMENT '定速巡航',
  lane_keep boolean NOT NULL COMMENT '车道保持',
  concurrent_aux boolean NOT NULL COMMENT '并线辅助',
  collision_alarm boolean NOT NULL COMMENT '碰撞报警/主动刹车',
  fatigue_remind boolean NOT NULL COMMENT '疲劳提醒',
  auto_parking boolean NOT NULL COMMENT '自动泊车',
  remote_parking boolean NOT NULL COMMENT '遥控泊车',
  auto_driving_aux boolean NOT NULL COMMENT '自动驾驶辅助',
  auto_hold boolean NOT NULL COMMENT '自动驻车',
  uphill_assist boolean NOT NULL COMMENT '上坡辅助',
  steep_slope_descend boolean NOT NULL COMMENT '陡坡缓降',
  night_vision_system boolean NOT NULL COMMENT '夜视系统',
  var_tooth_ratio_steer boolean NOT NULL COMMENT '可变齿比转向',
  front_parking_sensor boolean NOT NULL COMMENT '前倒车雷达',
  rear_parking_sensor boolean NOT NULL COMMENT '后倒车雷达',
  reverse_image varchar(255) NOT NULL COMMENT '倒车影像',
  driving_model_select boolean NOT NULL COMMENT '驾驶模式选择',
  PRIMARY KEY (unique_id),
  FOREIGN KEY (unique_id) REFERENCES car_base_info(unique_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE car_external_configuration(
  unique_id char(32) NOT NULL,
--   外部配置
  headlight varchar(255) NOT NULL COMMENT '前大灯[卤素、氙灯、LED、激光]',
  led_daytime_light boolean NOT NULL COMMENT 'LED日间行车灯',
  auto_headlight varchar(255) NOT NULL COMMENT '自动大灯[自动开闭、自动远近光、自动转向、 转向辅助灯]',
  front_fog_light boolean NOT NULL COMMENT '前雾灯',
  headlight_function varchar(255) NOT NULL COMMENT '大灯功能',
  skylight_type varchar(255) NOT NULL COMMENT '天窗类型[单天窗、双天窗、全景天窗]',
  front_window boolean NOT NULL COMMENT '前电动车窗',
  rear_window boolean NOT NULL COMMENT '后电动车窗',
  exterior_mirror_electric_adjustment varchar(255) NOT NULL COMMENT '外后视镜电动调节',
  inner_rearview_mirror boolean NOT NULL COMMENT '内后视镜自动防眩目',
  streaming_mirrors boolean NOT NULL COMMENT '流媒体后视镜',
  outer_rearview_mirror boolean NOT NULL COMMENT '外后视镜自动防眩目',
  privacy_glass boolean NOT NULL COMMENT '隐私玻璃',
  rear_side_sunshade boolean NOT NULL COMMENT '后排侧遮阳帘',
  read_sun_blinds boolean NOT NULL COMMENT '后遮阳帘',
  front_wiper varchar(255) NOT NULL COMMENT '前雨刷器',
  rear_wiper varchar(255) NOT NULL COMMENT '后雨刷器',
  electric_suction_door boolean NOT NULL COMMENT '电吸门',
  electric_sliding_door boolean NOT NULL COMMENT '电动侧滑门',
  electric_luggage_compartment varchar(255) NOT NULL COMMENT '电动行李厢[电动开合、自动感应]',
  roof_rack boolean NOT NULL COMMENT '车顶行李架',
  central_locking varchar(255) NOT NULL COMMENT '中控锁',
  smart_key varchar(255) NOT NULL COMMENT '智能钥匙[智能进入、无钥匙启动]',
  remote_control varchar(255) NOT NULL COMMENT '远程遥控功能[远程解锁、远程通风、远程启动]',
  tail_spoiler varchar(255) NOT NULL COMMENT '尾翼/扰流板',
  sport_appearance_kit varchar(255) NOT NULL COMMENT '运动外观套件',
  PRIMARY KEY (unique_id),
  FOREIGN KEY (unique_id) REFERENCES car_base_info(unique_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE car_internal_configuration(
  unique_id char(32) NOT NULL,
--   内部配置
  inter_material varchar(255) NOT NULL COMMENT '内饰材质[塑料、皮质、木制、金属、碳纤维]',
  inter_atmosphere_light boolean NOT NULL COMMENT '车内氛围灯',
  visor_mirror boolean NOT NULL COMMENT '遮阳板化妆镜',
  steering_wheel_material varchar(255) NOT NULL COMMENT '方向盘材质',
  multifunction_steering_wheel boolean NOT NULL COMMENT '多功能方向盘',
  steering_wheel_adjust varchar(255) NOT NULL COMMENT '方向盘调节',
  steering_wheel_heat boolean NOT NULL COMMENT '方向盘加热',
  steering_wheel_shift boolean NOT NULL COMMENT '方向盘换挡',
  front_air_conditioning varchar(255) NOT NULL COMMENT '前排空调[手动空调、自动空调、双温区自动空调]',
  rear_air_conditioning varchar(255) NOT NULL COMMENT '后排空调[手动空调、自动空调、双温区自动空调]',
  fragrance_system boolean NOT NULL COMMENT '香氛系统',
  air_purification boolean NOT NULL COMMENT '空气净化',
  car_refrigerator boolean NOT NULL COMMENT '车载冰箱',
  active_noise_reduction boolean NOT NULL COMMENT '主动降噪',
  PRIMARY KEY (unique_id),
  FOREIGN KEY (unique_id) REFERENCES car_base_info(unique_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE car_seat_configuration(
  unique_id char(32) NOT NULL,
--   座椅配置
  seat_material varchar(255) NOT NULL COMMENT '座椅材质[织物、皮质、织物皮质混合]',
  sports_seat boolean NOT NULL COMMENT '运动风格座椅',
  main_seat_electric_adjust varchar(255) NOT NULL COMMENT '主座椅电动调节[电动调节、靠背调节、高低调节、腰部调节、肩部调节、腿托调节]',
  deputy_seat_electric_adjust varchar(255) NOT NULL COMMENT '副座椅电动调节[电动调节、靠背调节、高低调节、腰部调节、肩部调节、腿托调节]',
  main_seat_adjust_method varchar(255) NOT NULL COMMENT '主座椅调节方式',
  sub_seat_adjust_method varchar(255) NOT NULL COMMENT '副座椅调节方式',
  second_row_electric_adjust varchar(255) NOT NULL COMMENT '第二排座椅电动调节',
  second_row_seat_adjust varchar(255) NOT NULL COMMENT '第二排座椅调节方式',
  front_seat_function varchar(255) NOT NULL COMMENT '前排座椅功能[加热、通风、按摩]',
  rear_seat_function varchar(255) NOT NULL COMMENT '后排座椅功能[加热、通风、按摩]',
  front_center_armrest boolean NOT NULL COMMENT '前排中央扶手',
  rear_center_armrest boolean NOT NULL COMMENT '后排中央扶手',
  thrid_row_seat boolean NOT NULL COMMENT '第三排座椅',
  seat_down_mode varchar(255) NOT NULL COMMENT '座椅放倒方式[全部放倒、按比例放倒]',
  rear_cup_holder boolean NOT NULL COMMENT '后排杯架',
  rear_folding_table boolean NOT NULL COMMENT '后排折叠桌板',
  PRIMARY KEY (unique_id),
  FOREIGN KEY (unique_id) REFERENCES car_base_info(unique_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE  car_infotainment(
  unique_id char(32) NOT NULL,
-- 信息娱乐
  central_lcd_screen varchar(255) NOT NULL COMMENT '中控彩色液晶屏',
  full_lcd_dashboard boolean NOT NULL COMMENT '全液晶仪表盘',
  driving_computer_display boolean NOT NULL COMMENT '行车电脑显示屏',
  hud_display boolean NOT NULL COMMENT 'HUD平视显示',
  gps_navigation boolean NOT NULL COMMENT 'GPS导航',
  smart_positioning boolean NOT NULL COMMENT '智能互联定位',
  voice_control boolean NOT NULL COMMENT '语音控制',
  mobile_internet varchar(255) NOT NULL COMMENT '手机互联(Carplay&Android)',
  mobile_wireless_charging boolean NOT NULL COMMENT '手机无线充电',
  gesture_control_system boolean NOT NULL COMMENT '手势控制系统',
  cd_dvd varchar(255) NOT NULL COMMENT 'CD/DVD',
  bluetooth_wifi varchar(255) NOT NULL COMMENT '蓝牙/WIFI连接',
  external_interface varchar(255) NOT NULL COMMENT '外接接口',
  car_driving_recorder boolean NOT NULL COMMENT '车载行车记录仪',
  car_tv boolean NOT NULL COMMENT '车载电视',
  audio_brand varchar(255) NOT NULL COMMENT '音响品牌',
  speakers_number varchar(255) NOT NULL COMMENT '扬声器数量[个]',
  rear_lcd varchar(255) NOT NULL COMMENT '后排液晶屏/娱乐系统',
  car_power_supply boolean NOT NULL COMMENT '车载220V电源',
  PRIMARY KEY (unique_id),
  FOREIGN KEY (unique_id) REFERENCES car_base_info(unique_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
