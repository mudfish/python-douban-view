/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50726
 Source Host           : localhost:3306
 Source Schema         : db_douban

 Target Server Type    : MySQL
 Target Server Version : 50726
 File Encoding         : 65001

 Date: 28/04/2024 22:46:06
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for tb_movie
-- ----------------------------
DROP TABLE IF EXISTS `tb_movie`;
CREATE TABLE `tb_movie`  (
  `id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '标题',
  `year` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '年份',
  `directors` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '导演',
  `rating` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '评分',
  `cover` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '封面',
  `country` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '国家地区',
  `summary` varchar(2000) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '简介',
  `types` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '类型',
  `lang` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '语言',
  `time` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '时长',
  `casts` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '演员',
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '链接',
  `release_date` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '上映日期',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tb_movie
-- ----------------------------
INSERT INTO `tb_movie` VALUES ('35636423', '来自未来的访客', '2022', 'François Descraques', '5.5', 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2876899873.jpg', ' 法国', 'Alice is a young woman opposed to the construction of a power-plant, an idea of her own father who is a member of the parliament. But a weird Visitor from the Future takes her to 2555, a future destroyed by the explosion of that same power-plant. According to the Visiteur, the premature death of her father would prevent this future from happening. But they’ll have to be quick b...', '喜剧,科幻', ' 法语', '90分钟', 'Enya Baroux,Florent Dorin,Raphaël Descraques,Slimane-Baptiste Berhoun,阿尔诺·杜克雷,阿萨·西拉,Lénie Chérino,Mathieu Poggi', 'https://movie.douban.com/subject/35636423/', '2022-09-07');
INSERT INTO `tb_movie` VALUES ('36181096', '蠢货', '2023', '武克·伦古洛夫-克洛茨', '6.1', 'https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2886887688.jpg', ' 美国', '故事来自导演的亲身经历。跨性别者费南开展了变性后的新生活，一夜之间，那些在他变性期间缺席了的人，突然又回到他的生命。与直男前度过了浪漫又尴尬的春宵，令他以为旧情可以复炽；好久不见的父亲，难以适应女儿的新身份；离家出走的妹妹给他添了不少乱，同时揭开了他过去的伤疤⋯⋯', '剧情,同性', ' 英语 / 西班牙语', '87分钟', '利奥·梅希尔,科尔·杜曼,米米·莱德,亚历山德罗·高克,贾赛·蔡斯·欧文斯,贾里·琼斯,本·格罗,莎拉·赫尔曼,娜奥米·阿萨,德斯蒙德·康福伊,欧文·拉赫恩,丽兹贝斯·范·佐伦,查尔斯·法尔科维兹,塔尔雅·斯科尼克,加雷思·斯密特,罗杰·曼库斯,黛博拉·斯特格麦尔,丽莎·奈特利,杰克·赫尔曼-斯塔奇,威尔·因曼', 'https://movie.douban.com/subject/36181096/', '2023-01-23');
INSERT INTO `tb_movie` VALUES ('35863319', '去唱卡拉OK吧！', '2023', '山下敦弘', '7.9', 'https://img9.doubanio.com/view/photo/s_ratio_poster/public/p2900802556.jpg', ' 日本', '由于某种原因想要变得擅长唱歌的黑社会成员成田狂儿（绫野刚 饰）邀请担任合唱部部长的中学生冈聪实去卡拉OK指导他唱歌。聪实虽然讨厌狂儿，但还是进行了歌唱指导，在这过程中两人产生了奇妙的友情。合唱部部长冈聪实由试镜选拔而出的斋藤润饰演。', '剧情', ' 日语', '108分钟', '绫野刚,斋藤润,北村一辉,芳根京子,桥本润,矢部享佑,吉永秀平,大城文章,湘南乃风,冈部弘树,八木美树,后圣人 ', 'https://movie.douban.com/subject/35863319/', '2023-11-15');
INSERT INTO `tb_movie` VALUES ('35736400', '伸冤人3', '2023', '安东尼·福奎阿', '7.2', 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2897743122.jpg', ' 美国', '退休特工兼私人侦探罗伯特·麦考尔（丹泽尔·华盛顿 饰）大杀四方为复仇之路写下最后一章。他放弃了为政府担任杀手的生活，并一直在努力调解过去所做的可怕之事，在代表被压迫者伸张正义时，他的内心找到了一种奇怪的慰藉。在意大利南部，罗伯特发现他的新朋友被犯罪头目控制了，随着事件变得致命起来，罗伯特知道自己必须与黑手党交手，以保护朋友安全。', '动作,惊悚,犯罪', ' 英语', '109分钟', '丹泽尔·华盛顿,达科塔·范宁,欧吉尼奥·马斯特兰德雷亚,大卫·丹曼,盖亚·斯考达里奥,雷莫·吉罗内,安德烈·斯卡杜齐奥,安德烈埃·多德罗,丹尼尔·佩罗内,扎卡里亚·哈姆扎,索尼娅·阿马尔,尼可洛·森尼,布鲁诺·比洛塔,萨尔瓦多·罗科', 'https://movie.douban.com/subject/35736400/', '2023-08-31');
INSERT INTO `tb_movie` VALUES ('36312009', '这个男人来自地狱', '2023', '查克·康策尔曼,卡里·所罗门', '5.5', 'https://img2.doubanio.com/view/photo/s_ratio_poster/public/p2889242451.jpg', ' 美国', '在计划被处决的当天，一名被定罪的连环杀手接受了精神病评估。在评估期间，他声称自己是一个恶魔，并进一步声称，在评估时间结束之前，精神病学家自己将犯下三起谋杀案。Steve Deace所撰写的宗教题材畅销书A Nefarious Plot的前传电影。', '悬疑,惊悚,恐怖', ' 英语', '119分钟', '肖恩·派特里克·弗兰纳里,乔丹·贝尔菲,小詹姆斯·希利,埃里克·汉森,斯特里奥·萨万特,卡梅伦·阿内特,贾瑞特·勒马斯特,罗伯特·皮特斯,汤姆·欧默,萨拉·埃尔南德斯,蒂娜·托纳,莫拉·科西尼,马克·德亚历山德罗,森约·阿莫库,丹尼尔·马丁·伯基', 'https://movie.douban.com/subject/36312009/', '2023-04-14');
INSERT INTO `tb_movie` VALUES ('36645798', '一人之下·锈铁重现', '2024', '陈烨', '6.6', 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p2904308777.jpg', ' 中国大陆', '张楚岚和冯宝宝二人所在的哪都通公司派遣了一个特别任务﹣﹣护送昔日的宝刀\"蛭丸\"到边境，完成和瀛国石川家一个几十年的约定。张楚岚和冯宝宝将面对陌生的队友、冬日恶劣的北地天气和虎视眈眈的夺刀强敌。一场\"蛭丸\"保卫战在林海雪原打响。', '动画,奇幻', ' 汉语普通话', '70分钟', '曹云图,小连杀', 'https://movie.douban.com/subject/36645798/', '2024-02-15');

SET FOREIGN_KEY_CHECKS = 1;
