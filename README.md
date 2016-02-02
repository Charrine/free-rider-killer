# free-rider-killer
贴吧删贴机

##运行环境设置
1. python2: https://www.python.org/download/releases/2.7.2/
2. beautiful soup 4: http://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/
3. html5lib: https://pypi.python.org/pypi/html5lib

----------


##使用方法
删贴机支持三种使用方法，您可以在参数中直接给出用户名，或者在一个 json 文件中给出（推荐），或者使用 cookie（推荐）。

您可以在运行时在命令行中直接提供用户名

`python2 TiebaAutoTool.py run -u username -p password`

您也可以配置 json 文件，它看起来应该像下面这样

    {
        "username" : "您的用户名",
        "password" : "您的密码"
    }

`python2 TiebaAutoTool.py config-user`

并使用它运行删贴机

`python2 TiebaAutoTool.py run -l json`

或者

`python2 TiebaAutoTool.py run -l json -c tieba.json`

您也可以配置 cookie 文件

`python2 TiebaAutoTool.py config-cookie`

并使用它运行删贴机

`python2 TiebaAutoTool.py run -l cookie`

或者

`python2 TiebaAutoTool.py run -l cookie -k cookie.txt`

您可以指定贴吧名字

`python2 TiebaAutoTool.py run -f c语言`

如果您不给出文件名参数

`python2 TiebaAutoTool.py run`

那么将使用 json 方法默认的配置文件名，即程序目录下的tieba.json


----------


更多信息，请使用-h参数来查看帮助
