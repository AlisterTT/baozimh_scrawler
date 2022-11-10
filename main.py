import requests,ast,comic_site

with open('comic_list.txt', 'r',encoding='UTF-8') as f:
    import_list = ast.literal_eval(f.read())
for i in range(len(import_list)):
    a = str(import_list[i]['name'])
    choose_list = str(i+1) + '. ' + a
    print(choose_list)
choose = int(input('选择漫画序号：'))
import_tmp = import_list[choose-1]['url']
importurl = requests.get(import_tmp).url

if 'baozimh' in import_tmp:
    comic_site.baozimh.output(importurl,import_list,choose)
else:
    print('你添加的网站不在支持列表内')
    exit()