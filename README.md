# Search Candidates

提供在51job网页根据关键词搜索候选人简历信息，并导出所有候选人成excel表格，方便本地查看和过滤。

## 功能简介：
1. 支持51job无忧简历库搜索，支持关键词搜索
1. 支持候选人基础信息（ID，年龄，学历 等）和详细信息（工作经历，项目经历 等）的抓取和解析
1. 支持导出候选人信息成excel表格（会自动翻页，包括所有页数的候选人）
1. 支持批量任务，每个任务可以设置单独的关键词和要保存的excel文件名
1. 支持Windows, Linux 和Mac OS

## 环境准备：
1. Python3.x，官网[下载路径](https://www.python.org/downloads/)
1. Firefox，官网[下载路径](https://www.firefox.com.cn/)
1. Python 插件，请使用命令行终端，进入本仓库，输入如下命令安装 `pip3 install -r requirement.txt`
1. Firefox driver，请拷贝本仓库下firefox_driver中对应的OS版本，到python安装目录或者system32目录，是其在终端下可以被调用

## 命令行参数
```
usage: search_candidates.py [-h] -j JSON [-d] [-v VERBOSE]

Search and dump candidates information from website

optional arguments:
  -h, --help            show this help message and exit
  -j JSON, --json JSON  Specify the input arguments to search resumes, see
                        'input.json' as an example
  -d, --details         Parse and save more experience details into output
                        excel.
  -v VERBOSE, --verbose VERBOSE
                        verbose log mode, 'debug', 'fatal', 'error',
                        'warning', 'info'
```
## json job参数配置
```
{
  "webMain": "https://ehire.51job.com",
  "loginMember": "<登陆名称>",
  "loginUser": "<账户名称>",
  "loginPassword": "<账户密码>--可选",
  "searchConditions": [
    {
      "profileName": "<搜索任务1的名称>",
      "keyWords": "<搜索框输入的关键词>"
    },
    {
      "profileName": "<搜索任务2的名称>",
      "keyWords": "<搜索框输入的关键词>"
    }
  ]
}
```
可参考本仓库下的input.json示例。

## 使用示例
1. 搜索关键词"上海 and 嵌入式 and SDK and MCU"的候选人 
    1. 配置好"searchConditions"json<br>
         ```
         {
         "profileName": "上海MCU候选人",
         "keyWords": "上海 and 嵌入式 or MCU"
         }       
         ```
    1. 调用脚本命令如下，如需要导出详细的工作经历等信息，再加参数`-d` <br>
         ```
         python .\search_candidates.py -j .\input.json
         ```
    1. Firefox浏览器会自动启动并且开始填充账户等信息，需要用户手动完成登陆检测。<br>
       ![login_web](doc/login_web.png)
    1. 确保进入到搜索主页面，如果之前有异常没有正常退出，请点击"强制下线".
       ![main_page](doc/main_page.png)
       ![force_to_logout](doc/force_to_logout.png)
    1. 在命令行终端输入'y'确认，然后就可以放置后台自动搜索和导出后续人.<br>
         ```
         INFO:sr:Please login the website by manual because of AI checking in the website!
         Do you login successfully and jump to the main page? (y/n)y
         ```
