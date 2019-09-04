from io import StringIO

from django.http import HttpResponse

depts_list = [
    {'no': 10, 'name': '财务部', 'location': '北京'},
    {'no': 20, 'name': '研发部', 'location': '成都'},
    {'no': 30, 'name': '销售部', 'location': '上海'},
]


def index(request):
    output = StringIO()
    output.write('<html>\n')
    output.write('<head>\n')
    output.write('\t<meta charset="utf-8">\n')
    output.write('\t<title>首页</title>')
    output.write('</head>\n')
    output.write('<body>\n')
    output.write('\t<h1>部门信息</h1>\n')
    output.write('\t<hr>\n')
    output.write('\t<table>\n')
    output.write('\t\t<tr>\n')
    output.write('\t\t\t<th width=120>部门编号</th>\n')
    output.write('\t\t\t<th width=180>部门名称</th>\n')
    output.write('\t\t\t<th width=180>所在地</th>\n')
    output.write('\t\t</tr>\n')
    for dept in depts_list:
        output.write('\t\t<tr>\n')
        output.write('\t\t\t<td align=center>%s</td>\n' % dept["no"])
        output.write('\t\t\t<td align=center>%s</td>\n' % dept["name"])
        output.write('\t\t\t<td align=center>%s</td>\n' % dept["location"])
        # output.write(f'\t\t\t<td align=center>{dept["no"]}</td>\n')
        # output.write(f'\t\t\t<td align=center>{dept["name"]}</td>\n')
        # output.write(f'\t\t\t<td align=center>{dept["location"]}</td>\n')
        output.write('\t\t</tr>\n')
    output.write('</html>\n')
    return HttpResponse(output.getvalue())