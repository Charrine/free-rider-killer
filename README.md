# free-rider-killer
贴吧删贴机

##运行环境设置
1. python2
2. beautiful soup 4: http://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/
3. 结巴分词：https://github.com/fxsjy/jieba

##使用方法
`python2 TiebaAutoTool.py username password`

##TODO
1. 各种成功测试，比如登录是否成功、删封是否成功，现在连是否删出了验证码都不知道？
2. 贴吧置顶是硬编码，增减置顶数量或者直播都会导致出错，还有百度强行置顶之类的。
3. 多线程，网络IO还是可以加多线程的。
4. 输出log，挂上服务器的话，log还是有必要的。
5. 更加细腻的删封判断。

##更新日志
这个怎么写
