# free-rider-killer
贴吧删贴机

##运行环境设置
1. python2: https://www.python.org/download/releases/2.7.2/
2. beautiful soup 4: http://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/
3. html5lib: https://pypi.python.org/pypi/html5lib

----------


##使用方法
删贴机支持两种使用方法，您可以在参数中直接给出用户名，或者在一个json文件中给出（推荐）
您可以在运行时在命令行中直接提供用户名

 - `-u username`
 - `-p password`

`python2 TiebaAutoTool.py run -u username -p password`

您还可以使用一个json格式的配置文件来保存你的用户名和密码，例如配置文件为tieba.json，那么它看起来应该想下面这样

	{
		"username" : "您的用户名",
		"password" : "您的密码"
	}
然后，你可以使用下面的方法来启动删贴机

	python2 TiebaAutoTool.py run -c tieba.json

如果您不给出文件名参数

	python2 TiebaAutoTool.py run

那么将使用默认的配置文件名，即程序目录下的tieba.json


----------


更多信息，请使用-h参数来查看帮助
