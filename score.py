import requests
import getpass
import os
import io, sys
from decaptcha import decaptcha

from bs4 import BeautifulSoup
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
print('\n********** 欢迎使用东北大学研究生成绩查询系统 **********')
s = requests.Session()
url_home = "http://219.216.96.73/pyxx/login.aspx"
req = s.get(url_home)
soup = BeautifulSoup(req.text, "html.parser")
VIEWSTATE = soup.select("#__VIEWSTATE")[0]['value']
VIEWSTATEGENERATOR = soup.select('#__VIEWSTATEGENERATOR')[0]['value']
while 1:
    username = input('请输入学号：')
    if username:
        break
while 1:
    password = getpass.getpass('请输入密码：')
    if password:
        break
# username = ""
# password = ""
count = 0
while 1:
    ir = s.get('http://219.216.96.73/pyxx/PageTemplate/NsoftPage/yzm/createyzm.aspx')
    if ir.status_code == 200:
        open('code.jpg', 'wb').write(ir.content)
    # 调用pytesseract识别验证码
    code = decaptcha('code.jpg')
    print("识别验证码:" + code)
    # os.system('code.jpg')
    # while 1:
    #     code = input('请输入验证码：')
    #     if code:
    #         break

    headers = {
        'Origin': 'http://219.216.96.73',
        'Referer': 'http://219.216.96.73/pyxx/login.aspx',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    }
    data = {
        '__VIEWSTATE': VIEWSTATE,
        '__VIEWSTATEGENERATOR': VIEWSTATEGENERATOR,
        'ctl00$txtusername': username,
        'ctl00$txtpassword': password,
        'ctl00$txtyzm': code,
        'ctl00$ImageButton1.x': 0,
        'ctl00$ImageButton1.y': 0
    }
    req = s.post('http://219.216.96.73/pyxx/login.aspx', data=data, headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    if(req.text.find("用户名不存在") != -1):
        print("用户名不存在")
        exit(0)
    if(req.text.find("密码错误") != -1):
        print("密码错误")
        exit(0)
    f = soup.select('frameset')
    if len(f) > 0:
        print('登录成功！')
        break
    else:
        print('验证码错误，重新识别验证码')
    if(count > 10):
        print("识别系统故障")
        exit(0)
    count += 1

req = s.get('http://219.216.96.73/pyxx/grgl/xskccjcx.aspx?xh=%s' % username)
soup = BeautifulSoup(req.text, 'html.parser')

bx_scores = soup.select('#MainWork_dgData tr')[1:]
print('\n共找到%d条必修课成绩' % len(bx_scores))
for score in bx_scores:
    soup1 = BeautifulSoup(str(score), 'html.parser')
    name = soup1.select('td')[0].text.replace(u'\xa0', u' ')
    value = soup1.select('td')[2].text.replace(u'\xa0', u' ')
    print(name, value)

xx_scores = soup.select('#MainWork_Datagrid1 tr')[1:]
print('\n共找到%d条选修课成绩' % len(xx_scores))
for score in xx_scores:
    soup2 = BeautifulSoup(str(score), 'html.parser')    
    name = soup2.select('td')[0].text.replace(u'\xa0', u' ') 
    value = soup2.select('td')[2].text.replace(u'\xa0', u' ')
    print(name, value)

input('\n按Enter键退出...')