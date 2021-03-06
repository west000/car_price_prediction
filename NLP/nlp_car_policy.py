#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'West'

import jieba
import jieba.analyse


s1 = '''各省、自治区、直辖市、计划单列市财政厅（局）、国家税务局、地方税务局，新疆生产建设兵团财务局：
　　为了进一步支持小型微利企业发展，经国务院批准，现就小型微利企业所得税政策通知如下：
　　一、自2014年1月1日至2016年12月31日，对年应纳税所得额低于10万元（含10万元）的小型微利企业，其所得减按50％计入应纳税所得额，按20%的税率缴纳企业所得税。
　　二、本通知所称小型微利企业，是指符合《中华人民共和国企业所得税法》及其实施条例以及相关税收政策规定的小型微利企业。
　　请遵照执行。
'''

s2 = '''
各省、自治区、直辖市、计划单列市财政厅（局）、国家税务局，新疆生产建设兵团财务局：
　　为了引导合理消费，促进节能减排，经国务院批准，对超豪华小汽车加征消费税。现将有关事项通知如下：
　　一、“小汽车”税目下增设“超豪华小汽车”子税目。征收范围为每辆零售价格130万元（不含增值税）及以上的乘用车和中轻型商用客车，即乘用车和中轻型商用客车子税目中的超豪华小汽车。对超豪华小汽车，在生产（进口）环节按现行税率征收消费税基础上，在零售环节加征消费税，税率为10%。
　　二、将超豪华小汽车销售给消费者的单位和个人为超豪华小汽车零售环节纳税人。
　　三、超豪华小汽车零售环节消费税应纳税额计算公式：
　　应纳税额=零售环节销售额（不含增值税，下同）×零售环节税率
　　国内汽车生产企业直接销售给消费者的超豪华小汽车，消费税税率按照生产环节税率和零售环节税率加总计算。消费税应纳税额计算公式:
　　应纳税额=销售额×(生产环节税率+零售环节税率)
　　四、上述规定自2016年12月1日起执行。对于11月30日（含）之前已签订汽车销售合同，但未交付实物的超豪华小汽车，自12月1日（含）起5个工作日内，纳税人持已签订的汽车销售合同，向其主管税务机关备案。对按规定备案的不征收零售环节消费税，未备案以及未按规定期限备案的，征收零售环节消费税。
'''

s3 = '''
根据《财政部、国家经贸委关于发布〈老旧汽车报废更新补贴资金管理暂行办法〉的通知》（财建〔2002〕742号）等有关规定，现将2012年度老旧汽车报废更新补贴车辆范围、补贴标准及申领程序公告如下：
　　一、补贴车辆范围及补贴标准
　　（一）农村客运车辆
　　2012年1月1日—12月31日期间交售给报废汽车回收企业的，使用6年以上（含6年）且不到15年，车长大于4.8米（含4.8米）、小于7.5米，并于当年更新的农村客运车辆，补贴标准为每辆车11000元人民币。
　　（二）城市公交车辆
　　2012年1月1日—12月31日期间交售给报废汽车回收企业的，使用8年以上（含8年）且不到15年，车长大于6米（含6米）或乘坐人数大于20人（含20人），并于当年更新的城市公交车，补贴标准为每辆车18000元人民币；车长小于6米且乘坐人数为10-19人，并于当年更新的城市公交车，补贴标准为每辆车11000元人民币。
　　（三）重型载货车辆
　　2012年1月1日—12月31日期间交售给报废汽车回收企业的，使用10年以上（含10年）且不到15年的半挂牵引车和总质量大于12000千克（含12000千克）的重型载货汽车（含普通货车、厢式货车、仓栅式货车、封闭货车、罐式货车、平板货车、集装箱车、自卸货车、特殊结构货车等车型，不含全挂车和半挂车），补贴标准为每辆车18000元人民币。
　　二、补贴资金申领时间
　　2012年11月13日至2013年1月31日。
　　三、补贴资金申领程序
　　（一）符合上述补贴范围的老旧汽车车主，可在补贴资金申领时间内，向车辆报废所在的报废汽车回收拆解企业提交以下材料：
　　1、《2012年老旧汽车报废更新补贴资金申请表》（一式三份），下载网址：http://bfqc.scjss.mofcom.gov.cn/（老旧汽车报废更新信息管理系统“文件下载”栏目）；
　　2、《报废汽车回收证明》第三联原件；
　　3、《机动车注销证明》原件及复印件（原件查验退回，复印件留存）；
　　4、更新车辆购车发票原件及复印件（申请重型载货车辆报废补贴的不需提供）（原件查验退回，复印件留存）；
　　5、有效身份证明原件及复印件（原件查验退回，复印件留存）；
　　6、与车主同名的个人建设银行活期储蓄账户存折（储蓄卡）或单位账户开户许可证复印件；
　　7、申请农村客运车辆报废更新补贴的车主，需提供中华人民共和国道路运输证、运输管理部门出具的意见。
　　（二）报废汽车回收拆解企业负责收集车主提交的申请材料，通过“老旧汽车报废更新信息管理系统”录入并核对有关信息，将符合条件的申请材料报北京市商务委员会。
　　（三）北京市商务委员会审核车辆信息无误后，报北京市财政局审核。
　　（四）北京市财政局审核是否未享受本市老旧机动车淘汰更新补贴，向未享受本市老旧机动车淘汰更新补贴的车主发放资金补贴。
　　四、领取补贴资金相关要求
　　在2012年期间，对同时符合北京市《关于进一步促进本市老旧机动车淘汰更新方案》及本公告补贴车辆范围的车主（单位），可选择其中一项政策享受政策补贴资金。
　　特此公告。
　　北京市商务委员会
　　联系人：王喜艳、赵洁，联系电话：87211852/87211833
　　中国建设银行北京阜成路支行（海淀区阜成路十九号）
　　联系人：曲薇薇，联系电话：68419156
'''

'''
各市、自治州人民政府，兰州新区管委会，省政府有关部门：
　　《甘肃省淘汰尾气排放不达标黄标车和老旧报废机动车工作实施办法》已经省政府同意，现印发给你们，请认真组织实施。
'''


s4 = '''
各有关省、直辖市、计划单列市财政厅（局）、科技厅（科委、局）、工业和信息化主管部门、发展改革委：
　　2009年，财政部、科技部、工业和信息化部、发展改革委等四部门在25个城市开展了节能与新能源汽车示范推广试点，并在6个城市开展了私人购买新能源汽车补贴试点。根据《财政部 科技部关于开展节能与新能源汽车示范推广试点工作的通知》（财建[2009]6号）等相关文件要求，为贯彻落实国务院关于发展新能源汽车战略性新兴产业的战略部署，进一步促进新能源汽车产业发展，财政部、科技部、工业和信息化部、发展改革委决定组织开展节能与新能源汽车示范推广试点验收工作。现将有关事宜通知如下：
　　一、验收内容和形式
　　主要针对实施方案中提出的各项目标，逐一考核评估实施效果。采取实地核查与会议集中评议相结合的方式：四部委将于12月中下旬组成验收组分赴试点城市进行实地考核。验收组由四部委和相关专家组成。
　　二、验收依据
　　(一) 财政部、科技部、工业和信息化部、国家发展改革委批复的各试点城市节能与新能源汽车示范推广试点实施方案；
　　(二) 《财政部 科技部关于开展节能与新能源汽车示范推广试点工作的通知》（财建[2009]6号）；
　　(三) 《财政部 科技部 工业和信息化部 国家发展改革委关于扩大公共服务领域节能与新能源汽车示范推广有关工作的通知》（财建[2010]227号）；
　　(四) 《财政部 科技部 工业和信息化部 国家发展改革委关于增加公共服务领域节能与新能源汽车示范推广试点城市的通知》（财建[2010]434号）；
　　(五) 《财政部 科技部 工业和信息化部 国家发展改革委关于开展私人购买新能源汽车补贴试点的通知》（财建[2010]230号）；
　　(六) 《关于加强节能与新能源汽车示范推广安全管理工作的函》（国科办函高[2011]322号）；
　　(七) 《关于进一步做好节能与新能源汽车示范推广试点工作的通知》（财办建[2011]149号）。
　　三、材料准备
    请按照批复的“节能与新能源汽车示范推广实施方案”和试点城市验收总结报告编写提纲（附件），编写试点城市验收总结报告，并于2012年12月10日前将验收总结报告一式十二份及电子版一份（WORD版光盘）寄送至科技部电动汽车重大项目管理办公室。
　　四、验收时间
　　拟于2012年12月中下旬开展实地核查方式验收。具体时间另行通知。
'''

def getKeywords(sentence):
    for x, w in jieba.analyse.extract_tags(sentence=sentence, withWeight=True):
        print('%s %s' % (x, w))

print('-'*100)
getKeywords(s1)
print('-'*100)
getKeywords(s2)
print('-'*100)
getKeywords(s3)
print('-'*100)
getKeywords(s4)


quit()
titleList = []
for line in open('data/local_policy.txt', encoding='utf-8'):
    titleList.append(line)

print(len(titleList))
quit()
jieba.add_word('交通运输部')
jieba.add_word('中置轴')
jieba.add_word('智能网联汽车')
jieba.add_word('工业和信息化部')
jieba.add_word('环境保护税')
jieba.add_word('多证合一')
jieba.add_word('国家发展改革委')
jieba.add_word('')

wordCountMap = {}
for title in titleList:
    result = jieba.lcut(sentence=title)
    for word in result:
        num = wordCountMap.get(word, 0) + 1
        wordCountMap[word] = num
    print('/'.join(result))

wordCountList = sorted(wordCountMap.items(), key=lambda d:d[1])
for word, num in wordCountList:
    print(word, '-', num)

'对原产于美国的部分进口商品加征关税', '购置税', '减征', '交强险', '车船税', '补助',
'轿车', '越野车', '小汽车', '黄标车', '旧车', '蓄电池', '电池', '电动汽车', '充电', '节能汽车', '自驾车', '旅居车'

'服务车', '农用', '收割机', '手扶拖拉机', '煤油', '航空', '军用', '自行车', '偷漏税', '专用汽车', '三轮', '拆解', '助力车', '警车', '农用车', '货运车',
'小型微利企业', ''
# https://baike.baidu.com/item/%E9%BB%84%E6%A0%87%E8%BD%A6/261015?fr=aladdin

quit()
policy = '''
为控制机动车排气污染，改善空气质量，保障人民群众身体健康，根据国家环境保护部《关于实施国家第四阶段轻型汽油车、两用燃料车和单一气体燃料车污染物排放标准的公告》（公告2011年第49号）、《关于实施国家第四阶段车用压燃式发动机与汽车污染物排放标准的公告》（公告2011年第92号）、《关于实施国家第四阶段重型车用汽油发动机与汽车排放标准的公告》（公告2012年第46号），以及《关于印发汕头市大气污染防治工作实施方案（2014—2017年）的通知》（汕府〔2014〕92号）等规定，汕头市将于2014年12月1日起执行国家第四阶段（国ⅳ）机动车大气污染物排放标准。现将有关事项通告如下：
    一、执行机动车国ⅳ标准地区范围
    汕头市全市范围。
    二、执行机动车国ⅳ标准时间
    自2014年12月1日起，在本市范围内生产、进口、销售和注册登记的机动车均执行国ⅳ排放标准，不符合标准的，公安部门不予办理注册登记、外地转入本市的变更登记和转移登记手续。
    三、机动车国ⅳ标准的定义
    本通告所称机动车国ⅳ标准是指按《轻型汽车污染物排放限值及测量方法（中国ⅲ、ⅳ阶段）》（gb18352.3-2005）和《车用压燃式、气体燃料点燃式发动机与汽车排放污染物排放限值及测量方法（中国ⅲ、ⅳ、ⅴ阶段）》（gb17691-2005）中的第四阶段排放控制要求。达到国ⅳ标准的车型目录可登陆国家环境保护部（www.zhb.gov.cn）、广东环境保护公众网（www.gdepb.gov.cn）查询。
    四、机动车办理注册登记、外市转入本市的变更登记和转移登记手续时，公安部门应根据环境保护部核定的机动车达标车型公告作出是否受理的决定。
    对未列入达标车型公告的机动车，一律不予办理相关登记手续。环保部门在机动车排气定期检验、环保检验合格标志核发等工作中，要严格执行排放标准规定。对不符合标准要求的车辆，不予核发环保检验合格标志，并配合公安部门停止其在本市办理注册登记、外市转入本市的变更登记和转移登记手续。对生产、进口、销售超标车辆的，环保部门将会同相关部门严格依法查处。
'''

s = '    自2014年12月1日起，在本市范围内生产、进口、销售和注册登记的机动车均执行国ⅳ排放标准，不符合标准的，公安部门不予办理注册登记、外地转入本市的变更登记和转移登记手续。'
for x, w in jieba.analyse.extract_tags(s, withWeight=True):
    print('%s %s' % (x, w))

jieba.add_word('国ⅳ标准', freq=200000, tag='ns')
# jieba.suggest_freq('国ⅳ', True)
result = jieba.cut(sentence=policy)
print('/'.join(result))


