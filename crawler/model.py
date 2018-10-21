#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'West'

from utility import Utility

# 基本信息
class CarBaseInfo(dict):
    __slots__ = ('unique_id', 'brand', 'subbrand', 'series', 'version', 'guide_price', 'mark_date', 'model_level', 'model_type',
                 'power_type', 'engine','max_speed', 'max_power_torque', 'transmission_type', 'fuel_consumption', 'acceleration_time',
                 'envir_standards', 'warranty_policy','exterior_color', 'exterior_color_code', 'stop_selling', 'source_url',
                 'img_url', 'real_shot_img_link')
    __attrname__ = {
        '厂商指导价':'guide_price', '上市日期':'mark_date', '车型级别':'model_level', '车身型式':'model_type', '动力类型':'power_type',
        '发动机':'engine', '最大功率/最大扭矩':'max_power_torque', '变速箱类型':'transmission_type','混合工况油耗':'fuel_consumption',
        '最高车速':'max_speed', '0-100km/h加速时间':'acceleration_time', '环保标准':'envir_standards', '保修政策':'warranty_policy',
    }

    __defaultvalue__ = {
        'model_level':'-', 'model_type':'-', 'power_type':'-', 'engine':'-', 'max_power_torque':'-','transmission_type': '-',
        'fuel_consumption':'-', 'envir_standards':'-', 'warranty_policy':'-', 'exterior_color':'-', 'exterior_color_code':'-',
        'stop_selling':False,
        'max_speed': None, 'acceleration_time': None, 'img_url': None, 'real_shot_img_link': None
    }

    def __setattr__(self, key, value):
        if value is None:
            if key in self.__class__.__defaultvalue__:
                value = self.__class__.__defaultvalue__[key]
        elif key == 'guide_price':
            value = int(Utility.getFloatFromStr(value) * 10000)
        elif key == 'acceleration_time':
            value = Utility.getFloatFromStr(value)
        elif key == 'max_speed':
            value = Utility.getIntFromStr(value)
        self[key] = value

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            if key in self.__class__.__defaultvalue__:
                return self.__class__.__defaultvalue__[key]
            return None

# 车身尺寸
class CarBodyInfo(dict):
    __slots__ = ('unique_id', 'length', 'width', 'height', 'wheelbase', 'quality', 'seats',
                 'luggage_volume', 'fuel_tank_volume', 'front_tire', 'rear_tire', 'spare_tire')
    __attrname__ = {
        '长':'length', '宽':'width', '高':'height', '轴距':'wheelbase', '整备质量':'quality',
        '座位数':'seats', '行李厢容积':'luggage_volume', '油箱容积':'fuel_tank_volume','前轮胎规格':'front_tire',
        '后轮胎规格':'rear_tire', '备胎':'spare_tire'
    }

    __defaultvalue__ = {
        'luggage_volume':None,
        'front_tire':'-', 'rear_tire':'-', 'spare_tire':'-'
    }

    def __setattr__(self, key, value):
        if value is None:
            if key in self.__class__.__defaultvalue__:
                value = self.__class__.__defaultvalue__[key]
        elif key in ('length', 'width', 'height', 'wheelbase', 'quality', 'seats', 'luggage_volume', 'fuel_tank_volume'):
            value = Utility.getIntFromStr(value)
        self[key] = value

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            if key in self.__class__.__defaultvalue__:
                return self.__class__.__defaultvalue__[key]
            return None

# 动力系统
class CarPowerSystem(dict):
    __slots__ = ('unique_id', 'displacement', 'max_power', 'max_horsepower', 'max_power_speed', 'max_torque', 'max_torque_speed',
                 'cylinder_num', 'cylinder_form', 'air_intake_form', 'oil_supply_method', 'fuel_marking', 'transmission_type',
                 'gears_number', 'engine_start_stop', 'compression_ratio')
    __attrname__ = {
        '排气量':'displacement', '最大功率':'max_power', '最大马力':'max_horsepower', '最大功率转速':'max_power_speed', '最大扭矩':'max_torque',
        '最大扭矩转速':'max_torque_speed', '气缸数':'cylinder_num', '缸体形式':'cylinder_form','进气形式':'air_intake_form','供油方式':'oil_supply_method',
        '燃油标号':'fuel_marking','变速箱类型':'transmission_type', '挡位个数':'gears_number', '发动机启停':'engine_start_stop','压缩比':'compression_ratio',
    }

    __defaultvalue__ = {
        'max_torque_speed':'-', 'cylinder_form':'-', 'air_intake_form':'-', 'oil_supply_method':'-', 'fuel_marking':'-', 'transmission_type':'-',
        'engine_start_stop':False,
        'gears_number':None, 'compression_ratio':None
    }

    def __setattr__(self, key, value):
        if value is None:
            if key in self.__class__.__defaultvalue__:
                value = self.__class__.__defaultvalue__[key]
        elif key in ('displacement', 'max_power', 'max_horsepower', 'max_power_speed', 'max_torque', 'cylinder_num', 'gears_number'):
            value = Utility.getIntFromStr(value)
        elif key == 'engine_start_stop':
            value = True if value == '●' else False
        self[key] = value

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            if key in self.__class__.__defaultvalue__:
                return self.__class__.__defaultvalue__[key]
            return None

# 底盘制动
class CarChassisBrake(dict):
    __slots__ = ('unique_id', 'driving_method', 'front_suspension_type', 'rear_suspension_type', 'front_brake_type', 'rear_brake_type',
                 'parking_brake_type', 'body_structure', 'limited_slip_differential', 'adjustable_suspension', 'approach_angle', 'departure_angle')

    __attrname__ = {
        '驱动方式':'driving_method', '前悬架类型':'front_suspension_type', '后悬架类型':'rear_suspension_type', '前轮制动器类型':'front_brake_type',
        '后轮制动器类型':'rear_brake_type', '驻车制动类型':'parking_brake_type', '车体结构':'body_structure', '限滑差速器/差速锁':'limited_slip_differential',
        '可调悬架':'adjustable_suspension','接近角':'approach_angle', '离去角':'departure_angle',
    }

    __defaultvalue__ = {
        'approach_angle':None, 'departure_angle':None,
        'body_structure':'-', 'driving_method':'-', 'front_suspension_type':'-', 'rear_suspension_type':'-',
        'front_brake_type':'-', 'rear_brake_type':'-', 'parking_brake_type':'-', 'limited_slip_differential':'-',
        'adjustable_suspension':False
    }

    def __setattr__(self, key, value):
        if value is None:
            if key in self.__class__.__defaultvalue__:
                value = self.__class__.__defaultvalue__[key]
        elif key in ('approach_angle', 'departure_angle'):
            value = Utility.getFloatFromStr(value)
        elif key in ('limited_slip_differential', 'adjustable_suspension'):
            value = True if value == '●' else False
        self[key] = value

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            if key in self.__class__.__defaultvalue__:
                return self.__class__.__defaultvalue__[key]
            return None

# 安全配置
class CarSecurityConfiguration(dict):
    __slots__ = ('unique_id', 'anti_lock_brake', 'braking_force_distribution', 'brake_assist', 'traction_control', 'body_stability_control',
                 'main_driving_airbag', 'first_officer_airbag', 'front_airbag', 'rear_airbag', 'side_curtain', 'knee_balloon', 'seat_belts',
                 'rear_center_airbag', 'tire_pressure_monitoring', 'zero_continuous_tire', 'rear_child_seat_interface')

    __attrname__ = {
        '防抱死制动(ABS)':'anti_lock_brake', '制动力分配(EBD/CBC等)':'braking_force_distribution', '制动辅助(BA/EBA等)':'brake_assist', '牵引力控制(ARS/TCS等)':'traction_control',
        '车身稳定控制(ESP/DSC等)':'body_stability_control', '主驾驶安全气囊':'main_driving_airbag', '副驾驶安全气囊':'first_officer_airbag', '前侧气囊':'front_airbag',
        '后侧气囊':'rear_airbag','侧安全气帘':'side_curtain', '膝部气囊':'knee_balloon', '安全带气囊':'seat_belts', '后排中央气囊':'rear_center_airbag',
        '胎压监测': 'tire_pressure_monitoring', '零胎压续行轮胎': 'zero_continuous_tire', '后排儿童座椅接口': 'rear_child_seat_interface',
    }

    __defaultvalue__ = {
        'anti_lock_brake':False, 'braking_force_distribution':False, 'brake_assist':False, 'traction_control':False, 'body_stability_control':False,
        'main_driving_airbag':False, 'first_officer_airbag':False, 'front_airbag':False, 'rear_airbag':False, 'side_curtain':False, 'knee_balloon':False,
        'seat_belts': False, 'rear_center_airbag':False, 'tire_pressure_monitoring':False, 'zero_continuous_tire':False, 'rear_child_seat_interface':False
    }

    def __setattr__(self, key, value):
        if value is None:
            if key in self.__class__.__defaultvalue__:
                value = self.__class__.__defaultvalue__[key]
        elif key in ('anti_lock_brake', 'braking_force_distribution', 'brake_assist', 'traction_control', 'body_stability_control',
                 'main_driving_airbag', 'first_officer_airbag', 'front_airbag', 'rear_airbag', 'side_curtain', 'knee_balloon', 'seat_belts',
                 'rear_center_airbag', 'tire_pressure_monitoring', 'zero_continuous_tire', 'rear_child_seat_interface'):
            value = True if value == '●' else False
        self[key] = value

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            if key in self.__class__.__defaultvalue__:
                return self.__class__.__defaultvalue__[key]
            return None

# 驾驶辅助
class CarDriveAssistance(dict):
    __slots__ = ('unique_id', 'cruise_control', 'lane_keep', 'concurrent_aux', 'collision_alarm', 'fatigue_remind',
                 'auto_parking', 'remote_parking', 'auto_driving_aux', 'auto_hold', 'uphill_assist', 'steep_slope_descend',
                 'night_vision_system', 'var_tooth_ratio_steer', 'front_parking_sensor', 'rear_parking_sensor', 'reverse_image',
                 'driving_model_select',)

    __attrname__ = {
        '定速巡航':'cruise_control', '车道保持':'lane_keep', '并线辅助':'concurrent_aux', '碰撞报警/主动刹车':'collision_alarm',
        '疲劳提醒':'fatigue_remind', '自动泊车':'auto_parking', '遥控泊车':'remote_parking', '自动驾驶辅助':'auto_driving_aux',
        '自动驻车':'auto_hold','上坡辅助':'uphill_assist', '陡坡缓降':'steep_slope_descend', '夜视系统':'night_vision_system',
        '可变齿比转向': 'var_tooth_ratio_steer', '前倒车雷达': 'front_parking_sensor', '后倒车雷达': 'rear_parking_sensor',
        '倒车影像': 'reverse_image', '驾驶模式选择': 'driving_model_select'
    }

    __defaultvalue__ = {
        'cruise_control':'-', 'reverse_image':'-',
        'lane_keep':False, 'concurrent_aux':False, 'collision_alarm':False, 'fatigue_remind':False, 'auto_parking':False,
        'remote_parking': False, 'auto_driving_aux': False, 'auto_hold': False, 'uphill_assist': False, 'steep_slope_descend': False,
        'night_vision_system': False, 'var_tooth_ratio_steer': False, 'front_parking_sensor': False, 'rear_parking_sensor': False,
        'driving_model_select': False,
    }

    def __setattr__(self, key, value):
        if value is None:
            if key in self.__class__.__defaultvalue__:
                value = self.__class__.__defaultvalue__[key]
        elif key in ('lane_keep', 'concurrent_aux', 'collision_alarm', 'fatigue_remind', 'auto_parking', 'remote_parking',
                     'auto_driving_aux', 'auto_hold', 'uphill_assist', 'steep_slope_descend', 'night_vision_system',
                     'var_tooth_ratio_steer', 'front_parking_sensor', 'rear_parking_sensor', 'driving_model_select'):
            value = True if value == '●' else False
        self[key] = value

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            if key in self.__class__.__defaultvalue__:
                return self.__class__.__defaultvalue__[key]
            return None

# 外部配置
class CarExternalConfiguration(dict):
    __slots__ = ('unique_id', 'headlight', 'led_daytime_light', 'auto_headlight', 'front_fog_light', 'headlight_function',
                 'skylight_type', 'front_window', 'rear_window', 'exterior_mirror_electric_adjustment', 'inner_rearview_mirror',
                 'streaming_mirrors', 'outer_rearview_mirror', 'privacy_glass', 'rear_side_sunshade', 'read_sun_blinds',
                 'front_wiper', 'rear_wiper', 'electric_suction_door', 'electric_sliding_door', 'electric_luggage_compartment',
                 'roof_rack', 'central_locking', 'smart_key', 'remote_control', 'tail_spoiler', 'sport_appearance_kit')

    __attrname__ = {
        '前大灯': 'headlight', 'LED日间行车灯': 'led_daytime_light', '自动大灯': 'auto_headlight', '前雾灯': 'front_fog_light',
        '大灯功能': 'headlight_function', '天窗类型': 'skylight_type', '前电动车窗': 'front_window', '后电动车窗': 'rear_window',
        '外后视镜电动调节': 'exterior_mirror_electric_adjustment', '内后视镜自动防眩目': 'inner_rearview_mirror', '流媒体后视镜': 'streaming_mirrors',
        '外后视镜自动防眩目': 'outer_rearview_mirror', '隐私玻璃': 'privacy_glass', '后排侧遮阳帘': 'rear_side_sunshade', '后遮阳帘': 'read_sun_blinds',
        '前雨刷器': 'front_wiper', '后雨刷器': 'rear_wiper', '电吸门': 'electric_suction_door', '电动侧滑门': 'electric_sliding_door',
        '电动行李厢': 'electric_luggage_compartment', '车顶行李架': 'roof_rack', '中控锁': 'central_locking', '智能钥匙': 'smart_key',
        '远程遥控功能': 'remote_control', '尾翼/扰流板': 'tail_spoiler', '运动外观套件': 'sport_appearance_kit'
    }

    __defaultvalue__ = {
        'headlight': '-', 'auto_headlight': '-', 'headlight_function': '-', 'skylight_type': '-',
        'exterior_mirror_electric_adjustment': '-', 'front_wiper': '-', 'rear_wiper': '-',
        'electric_luggage_compartment': '-', 'central_locking': '-', 'smart_key': '-', 'remote_control': '-',
        'tail_spoiler': '-', 'sport_appearance_kit': '-',
        'led_daytime_light': False, 'front_fog_light': False, 'front_window': False, 'rear_window': False,'inner_rearview_mirror': False,
        'streaming_mirrors': False, 'outer_rearview_mirror': False, 'rear_side_sunshade': False, 'read_sun_blinds': False,
        'electric_suction_door': False, 'electric_sliding_door': False, 'roof_rack': False, 'privacy_glass': False
    }

    def __setattr__(self, key, value):
        if value is None:
            if key in self.__class__.__defaultvalue__:
                value = self.__class__.__defaultvalue__[key]
        elif key in ('led_daytime_light', 'front_fog_light', 'front_window', 'rear_window', 'inner_rearview_mirror', 'streaming_mirrors', 'privacy_glass',
                    'outer_rearview_mirror', 'rear_side_sunshade', 'read_sun_blinds', 'electric_suction_door', 'electric_sliding_door','roof_rack'):
            value = True if value == '●' else False
        self[key] = value

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            if key in self.__class__.__defaultvalue__:
                return self.__class__.__defaultvalue__[key]
            return None

# 内部配置
class CarInternalConfiguration(dict):
    __slots__ = ('unique_id', 'inter_material', 'inter_atmosphere_light', 'visor_mirror', 'steering_wheel_material', 'multifunction_steering_wheel',
                 'steering_wheel_adjust', 'steering_wheel_heat', 'steering_wheel_shift', 'front_air_conditioning', 'rear_air_conditioning',
                 'fragrance_system', 'air_purification', 'car_refrigerator', 'active_noise_reduction')

    __attrname__ = {
        '内饰材质': 'inter_material', '车内氛围灯': 'inter_atmosphere_light', '遮阳板化妆镜': 'visor_mirror', '方向盘材质': 'steering_wheel_material',
        '多功能方向盘': 'multifunction_steering_wheel', '方向盘调节': 'steering_wheel_adjust', '方向盘加热': 'steering_wheel_heat',
        '方向盘换挡': 'steering_wheel_shift', '前排空调': 'front_air_conditioning', '后排空调': 'rear_air_conditioning', '香氛系统': 'fragrance_system',
        '空气净化': 'air_purification', '车载冰箱': 'car_refrigerator', '主动降噪': 'active_noise_reduction'
    }

    __defaultvalue__ = {
        'inter_material': '-', 'steering_wheel_material': '-', 'steering_wheel_adjust': '-', 'front_air_conditioning': '-', 'rear_air_conditioning': '-',
        'inter_atmosphere_light': False, 'visor_mirror': False, 'multifunction_steering_wheel': False, 'steering_wheel_heat': False, 'steering_wheel_shift': False,
        'fragrance_system': False, 'air_purification': False, 'car_refrigerator': False, 'active_noise_reduction': False
    }

    def __setattr__(self, key, value):
        if value is None:
            if key in self.__class__.__defaultvalue__:
                value = self.__class__.__defaultvalue__[key]
        elif key in ('inter_atmosphere_light', 'visor_mirror', 'multifunction_steering_wheel', 'steering_wheel_heat',
                   'steering_wheel_shift', 'fragrance_system', 'air_purification', 'car_refrigerator',
                   'active_noise_reduction'):
            value = True if value == '●' else False
        self[key] = value

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            if key in self.__class__.__defaultvalue__:
                return self.__class__.__defaultvalue__[key]
            return None

# 座椅配置
class CarSeatConfiguration(dict):
    __slots__ = ('unique_id', 'seat_material', 'sports_seat', 'main_seat_electric_adjust', 'deputy_seat_electric_adjust', 'main_seat_adjust_method',
                 'sub_seat_adjust_method', 'second_row_electric_adjust', 'second_row_seat_adjust', 'front_seat_function', 'rear_seat_function',
                 'front_center_armrest', 'rear_center_armrest', 'thrid_row_seat', 'seat_down_mode', 'rear_cup_holder', 'rear_folding_table')

    __attrname__ = {
        '座椅材质': 'seat_material', '运动风格座椅': 'sports_seat', '主座椅电动调节': 'main_seat_electric_adjust', '副座椅电动调节': 'deputy_seat_electric_adjust',
        '主座椅调节方式': 'main_seat_adjust_method', '副座椅调节方式': 'sub_seat_adjust_method', '第二排座椅电动调节': 'second_row_electric_adjust',
        '第二排座椅调节方式': 'second_row_seat_adjust', '前排座椅功能': 'front_seat_function', '后排座椅功能': 'rear_seat_function', '前排中央扶手': 'front_center_armrest',
        '后排中央扶手': 'rear_center_armrest', '第三排座椅': 'thrid_row_seat', '座椅放倒方式': 'seat_down_mode', '后排杯架': 'rear_cup_holder', '后排折叠桌板': 'rear_folding_table'
    }

    __defaultvalue__ = {
        'seat_material': '-', 'main_seat_electric_adjust': '-', 'deputy_seat_electric_adjust': '-', 'main_seat_adjust_method': '-', 'sub_seat_adjust_method': '-',
        'second_row_electric_adjust': '-', 'second_row_seat_adjust': '-', 'front_seat_function': '-', 'rear_seat_function': '-', 'seat_down_mode': '-',
        'sports_seat': False, 'front_center_armrest': False, 'rear_center_armrest': False, 'thrid_row_seat': False, 'rear_cup_holder': False,
        'rear_folding_table': False
    }

    def __setattr__(self, key, value):
        if value is None:
            if key in self.__class__.__defaultvalue__:
                value = self.__class__.__defaultvalue__[key]
        elif key in ('sports_seat', 'front_center_armrest', 'rear_center_armrest', 'thrid_row_seat', 'rear_cup_holder', 'rear_folding_table'):
            value = True if value == '●' else False
        self[key] = value

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            if key in self.__class__.__defaultvalue__:
                return self.__class__.__defaultvalue__[key]
            return None

# 信息娱乐
class CarInfotainment(dict):
    __slots__ = ('unique_id', 'central_lcd_screen', 'full_lcd_dashboard', 'driving_computer_display', 'hud_display', 'gps_navigation',
                 'smart_positioning', 'voice_control', 'mobile_internet', 'mobile_wireless_charging', 'gesture_control_system','cd_dvd',
                 'bluetooth_wifi', 'external_interface', 'car_driving_recorder', 'car_tv', 'audio_brand', 'speakers_number', 'rear_lcd', 'car_power_supply')

    __attrname__ = {
        '中控彩色液晶屏': 'central_lcd_screen', '全液晶仪表盘': 'full_lcd_dashboard', '行车电脑显示屏': 'driving_computer_display', 'HUD平视显示': 'hud_display',
        'GPS导航': 'gps_navigation', '智能互联定位': 'smart_positioning', '语音控制': 'voice_control',
        '手机互联(Carplay&Android)': 'mobile_internet', '手机无线充电': 'mobile_wireless_charging', '手势控制系统': 'gesture_control_system', 'CD/DVD': 'cd_dvd',
        '蓝牙/WIFI连接': 'bluetooth_wifi', '外接接口': 'external_interface', '车载行车记录仪': 'car_driving_recorder', '车载电视': 'car_tv', '音响品牌': 'audio_brand',
        '扬声器数量': 'speakers_number', '后排液晶屏/娱乐系统': 'rear_lcd', '车载220V电源': 'car_power_supply'
    }

    __defaultvalue__ = {
        'central_lcd_screen': '-', 'mobile_internet': '-', 'cd_dvd': '-', 'bluetooth_wifi': '-', 'external_interface': '-',
        'audio_brand': '-', 'speakers_number': '-', 'rear_lcd': '-',
        'full_lcd_dashboard': False, 'driving_computer_display': False, 'hud_display': False, 'gps_navigation': False, 'smart_positioning': False,
        'voice_control': False, 'mobile_wireless_charging': False, 'gesture_control_system': False, 'car_driving_recorder': False, 'car_tv': False, 'car_power_supply': False
    }

    def __setattr__(self, key, value):
        if value is None:
            if key in self.__class__.__defaultvalue__:
                value = self.__class__.__defaultvalue__[key]
        elif key in ('full_lcd_dashboard', 'driving_computer_display', 'hud_display', 'gps_navigation', 'smart_positioning',
                   'voice_control', 'mobile_wireless_charging', 'gesture_control_system', 'car_driving_recorder', 'car_tv', 'car_power_supply'):
            value = True if value == '●' else False
        self[key] = value

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            if key in self.__class__.__defaultvalue__:
                return self.__class__.__defaultvalue__[key]
            return None

class CarPrice(object):
    def __init__(self, carId, dealer_id, sales_price, is_promotion, publish_date, end_date, price_url):
        self.carid = carId
        self.dealer_id = dealer_id
        self.sales_price = sales_price
        self.is_promotion = is_promotion
        self.publish_date = publish_date
        self.end_date = end_date
        self.price_url = price_url

    def generateCarPriceKeyValue(self):
        key = None
        if self.is_promotion is False:
            key = '%s|%s|%s|%s|%s|%s' % (self.carid, self.dealer_id, self.sales_price, self.is_promotion, '', '')
        else:
            key = '%s|%s|%s|%s|%s|%s' % (self.carid, self.dealer_id, self.sales_price, self.is_promotion, self.publish_date, self.end_date)
        value = self.price_url
        return (key, value)

    def parseCarPriceKeyValue(self, key, value):
        carId, dealer_id, sales_price, is_promotion, publish_date, end_date = key.split('|')
        if publish_date == '':
            publish_date = None
        if end_date == '':
            end_date = None
        price_url = value
        return CarPrice()

    def toTuple(self):
        return (self.carid, self.dealer_id, self.sales_price, self.is_promotion, self.publish_date, self.end_date)

class CarDealer(object):
    def __init__(self, id, province, city, area, name, full_name, type, address, official_website, sale_phone_number, contact_number):
        self.id = id
        self.province = province
        self.city = city
        self.area = area
        self.name = name
        self.full_name = full_name
        self.type = type
        self.address = address
        self.official_website = official_website
        self.sale_phone_number = sale_phone_number
        self.contact_number = contact_number

    def toTuple(self):
        return (self.id, self.province, self.city, self.area, self.name, self.full_name,
                self.type, self.address, self.official_website, self.sale_phone_number, self.contact_number)