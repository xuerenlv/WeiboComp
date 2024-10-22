#coding:utf8
'''
Created on 2016年7月24日

@author: Xuehj
'''

if __name__ == '__main__':
    province = [(1, u'北京'), (2, u'上海'), (3, u'香港'), (4, u'台湾'),(5, u'重庆'), (6, u'澳门'), (7, u'天津'), (8, u'江苏'), (9, u'浙江'), (10, u'四川'), (11, u'江西'), (12, u'福建'), (13, u'青海'), (14, u'吉林'), (15, u'贵州'),
 (16, u'陕西'), (17, u'山西'), (18, u'河北'), (19, u'湖北'), (20, u'辽宁'), (21, u'湖南'), (22, u'山东'), (23, u'云南'), (24, u'河南'), (25, u'广东'), (26, u'安徽'),
 (27, u'甘肃'), (29, u'黑龙江'), (30, u'内蒙古'), (31, u'新疆'), (32, u'广西'), (33, u'宁夏'), (34, u'西藏')]
    
    CITY = {8: ((1, u'常州'),(2, u'连云港'),
     (3, u'泰州'),
     (4, u'南京'),
     (5, u'扬州'),
     (6, u'镇江'),
     (7, u'宿迁'),
     (8, u'盐城'),
     (9, u'徐州'),
     (10, u'南通'),
     (11, u'淮安'),
     (12, u'无锡'),
     (13, u'苏州')),
 9: ((14, u'湖州'),
     (15, u'杭州'),
     (16, u'舟山'),
     (17, u'嘉兴'),
     (18, u'衢州'),
     (19, u'金华'),
     (20, u'宁波'),
     (21, u'台州'),

     (24, u'绍兴')),
 10: ((25, u'广元'),
      (26, u'凉山彝族自治州'),
      (27, u'绵阳'),
      (28, u'资阳'),
      (29, u'巴中'),
      (30, u'德阳'),
      (31, u'眉山'),
      (32, u'甘孜藏族自治州'),
      (33, u'成都'),
      (34, u'乐山'),
      (35, u'阿坝藏族羌族自治州'),
      (36, u'内江'),
      (37, u'自贡'),
      (38, u'攀枝花'),
      (39, u'达州'),
      (40, u'宜宾'),
      (41, u'泸州'),
      (42, u'遂宁'),
      (43, u'雅安'),
      (44, u'南充'),
      (45, u'广安')),
 11: ((46, u'赣州'),
      (47, u'上饶'),
      (48, u'宜春'),
      (49, u'抚州'),
      (50, u'新余'),
      (51, u'吉安'),
      (52, u'南昌'),
      (53, u'鹰潭'),
      (54, u'景德镇'),
      (55, u'九江'),
      (56, u'萍乡')),
 12: ((57, u'宁德'),
      (58, u'三明'),
      (59, u'福州'),
      (60, u'南平'),
      (61, u'龙岩'),
      (62, u'莆田'),
      (63, u'泉州'),
      (64, u'漳州')),
 13: ((65, u'西宁'),
      (66, u'果洛藏族自治州'),
      (67, u'海东地区'),
      (68, u'黄南藏族自治州'),
      (69, u'海南藏族自治州'),
      (70, u'海北藏族自治州'),
      (71, u'玉树藏族自治州'),
      (72, u'海西蒙古族藏族自治州')),
 14: ((73, u'辽源'),
      (74, u'延边朝鲜族自治州'),
      (75, u'白城'),
      (76, u'四平'),
      (77, u'长春'),
      (78, u'通化'),
      (79, u'吉林'),
      (80, u'白山'),
      (81, u'松原')),
 15: ((82, u'黔南布依族苗族自治州'),
      (83, u'六盘水'),
      (84, u'贵阳'),
      (85, u'遵义'),
      (86, u'铜仁地区'),
      (87, u'毕节地区'),
      (88, u'安顺'),
      (89, u'黔东南苗族侗族自治州'),
      (90, u'黔西南布依族苗族自治州')),
 16: ((91, u'西安'),
      (92, u'延安'),
      (93, u'汉中'),
      (94, u'宝鸡'),
      (95, u'榆林'),
      (96, u'渭南'),
      (97, u'咸阳'),
      (98, u'安康'),
      (99, u'铜川'),
      (100, u'商洛')),
 17: ((101, u'晋城'),
      (102, u'晋中'),
      (103, u'阳泉'),
      (104, u'忻州'),
      (105, u'朔州'),
      (106, u'大同'),
      (107, u'运城'),
      (108, u'太原'),
      (109, u'吕梁'),
      (110, u'临汾'),
      (111, u'长治')),
 18: ((112, u'廊坊'),
      (113, u'衡水'),
      (114, u'邢台'),
      (115, u'石家庄'),
      (116, u'沧州'),
      (117, u'保定'),
      (118, u'邯郸'),
      (119, u'张家口'),
      (120, u'承德'),
      (121, u'唐山'),
      (122, u'秦皇岛')),
 19: ((123, u'荆门'),
      (124, u'十堰'),
      (125, u'荆州'),
      (126, u'恩施土家族苗族自治州'),
      (127, u'随州'),
      (128, u'黄冈'),
      (129, u'咸宁'),
      (130, u'宜昌'),
      (131, u'襄樊'),
      (132, u'孝感'),
      (133, u'黄石')),
 20: ((134, u'营口'),
      (135, u'沈阳'),
      (136, u'辽阳'),
      (137, u'大连'),
      (138, u'朝阳'),
      (139, u'抚顺'),
      (140, u'本溪'),
      (141, u'鞍山'),
      (142, u'葫芦岛'),
      (143, u'盘锦'),
      (144, u'丹东'),
      (145, u'锦州'),
      (146, u'阜新'),
      (147, u'铁岭')),
 21: ((148, u'怀化'),
      (149, u'长沙'),
      (150, u'常德'),
      (151, u'岳阳'),
      (152, u'株洲'),
      (153, u'湘西土家族苗族自治州'),
      (154, u'张家界'),
      (155, u'湘潭'),
      (156, u'益阳'),
      (157, u'娄底'),
      (158, u'衡阳'),
      (159, u'郴州'),
      (160, u'永州'),
      (161, u'邵阳')),
 22: ((162, u'枣庄'),
      (163, u'德州'),
      (164, u'济南'),
      (165, u'济宁'),
      (166, u'菏泽'),
      (167, u'滨州'),
      (168, u'烟台'),
      (169, u'潍坊'),
      (170, u'聊城'),
      (171, u'日照'),
      (172, u'泰安'),
      (173, u'东营'),
      (174, u'临沂'),
      (175, u'青岛'),
      (176, u'威海'),
      (177, u'淄博')),
 23: ((178, u'玉溪'),
      (179, u'曲靖'),
      (180, u'西双版纳傣族自治州'),
      (181, u'文山壮族苗族自治州'),
      (182, u'德宏傣族景颇族自治州'),
      (183, u'保山'),
      (184, u'昭通'),
      (185, u'迪庆藏族自治州'),
      (186, u'普洱'),
      (187, u'昆明'),
      (188, u'丽江'),
      (189, u'楚雄彝族自治州'),
      (190, u'红河哈尼族彝族自治州'),
      (191, u'临沧'),
      (192, u'怒江傈僳族自治州'),
      (193, u'大理白族自治州')),
 24: ((194, u'新乡'),
      (195, u'驻马店'),
      (196, u'南阳'),
      (197, u'漯河'),
      (198, u'安阳'),
      (199, u'平顶山'),
      (200, u'商丘'),
      (201, u'开封'),
      (202, u'郑州'),
      (203, u'濮阳'),
      (204, u'三门峡'),
      (205, u'周口'),
      (206, u'焦作'),
      (207, u'信阳'),
      (208, u'许昌'),
      (209, u'洛阳')),
 25: ((210, u'广州'),
      (211, u'湛江'),
      (212, u'汕尾'),
      (213, u'汕头'),
      (214, u'梅州'),
      (215, u'云浮'),
      (216, u'阳江'),
      (217, u'清远'),
      (218, u'茂名'),
      (219, u'揭阳'),
      (220, u'惠州'),
      (221, u'潮州'),
      (222, u'河源'),
      (223, u'韶关'),
      (224, u'肇庆'),
      (225, u'江门')),
 26: ((226, u'六安'),
      (227, u'淮南'),
      (228, u'铜陵'),
      (229, u'宣城'),
      (230, u'阜阳'),
      (231, u'宿州'),
      (232, u'滁州'),
      (233, u'黄山'),
      (234, u'蚌埠'),
      (235, u'淮北'),
      (236, u'安庆'),
      (237, u'亳州'),
      (238, u'马鞍山'),
      (239, u'巢湖'),
      (240, u'芜湖'),
      (241, u'池州'),
      (242, u'合肥')),
 27: ((243, u'临夏回族自治州'),
      (244, u'白银'),
      (245, u'陇南'),
      (246, u'金昌'),
      (247, u'兰州'),
      (248, u'武威'),
      (249, u'定西'),
      (250, u'酒泉'),
      (251, u'甘南藏族自治州'),
      (252, u'庆阳'),
      (253, u'天水'),
      (254, u'张掖'),
      (255, u'平凉')),
 29: ((256, u'齐齐哈尔'),
      (257, u'大兴安岭地区'),
      (258, u'鸡西'),
      (259, u'黑河'),
      (260, u'佳木斯'),
      (261, u'哈尔滨'),
      (262, u'牡丹江'),
      (263, u'双鸭山'),
      (264, u'七台河'),
      (265, u'大庆'),
      (266, u'绥化'),
      (267, u'伊春'),
      (268, u'鹤岗')),
 30: ((269, u'兴安盟'),
      (270, u'呼伦贝尔'),
      (271, u'乌兰察布'),
      (272, u'巴彦淖尔'),
      (273, u'锡林郭勒盟'),
      (274, u'鄂尔多斯'),
      (275, u'通辽'),
      (276, u'赤峰'),
      (277, u'呼和浩特'),
      (278, u'阿拉善盟'),
      (279, u'包头')),
 31: ((280, u'伊犁哈萨克自治州'),
      (281, u'博尔塔拉蒙古自治州'),
      (282, u'巴音郭楞蒙古自治州'),
      (283, u'乌鲁木齐'),
      (284, u'和田地区'),
      (285, u'喀什地区'),
      (286, u'哈密地区'),
      (287, u'阿勒泰地区'),
      (288, u'克孜勒苏柯尔克孜自治州'),
      (289, u'昌吉回族自治州'),
      (290, u'阿克苏地区'),
      (291, u'吐鲁番地区'),
      (292, u'塔城地区')),
 32: ((293, u'贵港'),
      (294, u'河池'),
      (295, u'贺州'),
      (296, u'柳州'),
      (297, u'北海'),
      (298, u'玉林'),
      (299, u'桂林'),
      (300, u'百色'),
      (301, u'钦州'),
      (302, u'梧州'),
      (303, u'来宾'),
      (304, u'崇左'),
      (305, u'南宁'),
      (306, u'防城港')),
 33: ((307, u'石嘴山'),
      (308, u'中卫'),
      (309, u'吴忠'),
      (310, u'固原'),
      (311, u'银川')),
 34: ((312, u'那曲地区'),
      (313, u'昌都地区'),
      (314, u'拉萨'),
      (315, u'山南地区'),
      (316, u'林芝地区'),
      (317, u'日喀则地区'),
      (318, u'阿里地区'))
}
    code_map_pro = {}
    for code,pro in province:
        code_map_pro[code] = pro
#     print code_map_pro
    
    
    for code in CITY:
        one_line = '[u\''+ code_map_pro[code]+'\','
        for inde,cit in CITY[code]:
            one_line+='u\''+cit+'\','
        print one_line[:-1]+']'
 
    
    pass#