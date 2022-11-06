import requests,re,time,os,ast,getfunction

with open('comic_list.txt', 'r',encoding='UTF-8') as f:
    import_list = ast.literal_eval(f.read())
for i in range(len(import_list)):
    a = str(import_list[i]['name'])
    choose_list = str(i+1) + '. ' + a
    print(choose_list)
choose = int(input('选择漫画序号：'))
importurl = import_list[choose-1]['url']
n = re.search(r'comic\/(.*?)$',importurl)
comic_name = n.group(1)
m = getfunction.getlist(importurl)
for i in range(len(m)):
    print (f'{i+1}. {m[i][1]}')
comic_capter = int(input('输入章节序号：'))
print('请稍等...')
comic_capter = comic_capter - 1
baseurl = f'https://cn.webmota.com/comic/chapter/{comic_name}/0_{m[comic_capter][0]}_'
directory_name = import_list[choose-1]['name']+'-'+m[comic_capter][1]

comic_url = []
temlist = []
for i in range(1,10):
    comic_url.append(baseurl+str(i)+'.html')
for i in range(len(comic_url)):
    html_str = requests.get(comic_url[i]).content.decode()
    img_list = re.findall('img src="(.*?)" alt',html_str, re.S)
    for u in range(len(img_list)):
        temlist.append(img_list[u])
final_list = sorted(set(temlist),key=temlist.index)

output_dir = ['PDF', directory_name]
for i in range(len(output_dir)):
    if not os.path.exists(output_dir[i]):
        os.mkdir(output_dir[i])

for i in range (len(final_list)):
    file_url = final_list[i]
    file_path = f'{directory_name}/{directory_name}_{i}.jpg'
    getfunction.down_load(file_url, file_path)
    time.sleep(0.1)

folder = f'./{directory_name}/'
#pdfFile = f'./{directory_name}/{directory_name}_final.pdf'
pdfFile = f'./PDF/{directory_name}.pdf'
getfunction.combine_imgs_pdf(folder, pdfFile)
print('\nComplate')