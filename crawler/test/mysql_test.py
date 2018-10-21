import sys, pymysql

class Car:
    def __init__(self):
        self.brand = ''             # 品牌
        self.unique_id = ''         # 车子ID
        self.version = ''           # 车型
        self.first_licence = ''     # 首次上牌日期
        self.separator = 0          # 里程数
        self.new_price = 0          # 新车价格
        self.current_price = 0      # 当前二手车价格
        self.source = 0             # 车源，0代表个人，1代表车商
        self.transfer_times = 0     # 过户次数
        self.area = ''              # 所属地区
        self.color = ''             # 车身颜色
        self.add_date = ''          # 发布日期/上架日期
        self.fix_record = ''        # 维修记录
        self.url = ''               # 源信息url

    def getCarInfo(self):
        return self.__dict__

    def showCar(self):
        print(self.__dict__)

    def toTuple(self):
        '''car(brand, unique_id, version, first_licence, mailage, new_price, current_price, source, area, color, transfer_times, add_date, fix_record, url)'''
        return (self.brand, self.unique_id, self.version, self.first_licence, self.separator, self.new_price, self.current_price,
                self.source, self.area, self.color, self.transfer_times, self.add_date, self.fix_record, self.url)

MySQLConnection = None
def mysqlConnectionInit():
    global MySQLConnection
    MySQLConnection = pymysql.connect(host='192.168.56.102', port=3306, user='root', password='123',
                                      db='graduation_project', charset='utf8', cursorclass=pymysql.cursors.DictCursor)

def mysqlConnectionRelease():
    global MySQLConnection
    MySQLConnection.close()

def insertCarListIntoDB(carList):
    global MySQLConnection
    cursor = MySQLConnection.cursor()
    try:
        sql = 'INSERT INTO car(brand, unique_id, version, first_licence, mailage, new_price, current_price, source, area, color, transfer_times, add_date, fix_record, url) ' \
              'VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        data = [('五菱汽车', 'c8b7eda0c3746269', '五菱汽车-五菱荣光 2011款 1.2L基本型', '2014-03-01', 66300, 43400, 31000, 0, '鞍山', '银色', 0, '2018-03-25', '发动机舱盖表面：喷漆修复|右后车门：钣金修复|左后翼子板：钣金修复|前保险杠：覆盖件更换|右后翼子板：喷漆修复', 'https://renrenche.com/as/car/c8b7eda0c3746269'), ('五菱汽车', '644715f8a6bb17ff', '五菱汽车-五菱宏光 2015款 1.5L S基本型', '2015-11-01', 26800, 47800, 37000, 0, '鞍山', '白色', 0, '2018-03-25', '前保险杠：喷漆修复', 'https://renrenche.com/as/car/644715f8a6bb17ff'), ('奇瑞', '14408a04d661aebe', '奇瑞-A3 2009款 两厢 1.6L 手动标准型', '2009-06-01', 38000, 78000, 20000, 0, '鞍山', '红色', 1, '2018-03-24', '后保险杠：喷漆修复|左后翼子板：喷漆修复|前保险杠：覆盖件更换|右前翼子板：钣金修复|左前翼子板：覆盖件更换', 'https://renrenche.com/as/car/14408a04d661aebe')]
        for car in data:
            cursor.execute(sql, car)
        MySQLConnection.commit()
    finally:
        cursor.close()

if __name__ == '__main__':
    mysqlConnectionInit()
    insertCarListIntoDB([])
    mysqlConnectionRelease()