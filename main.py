import requests,time,os,ast,shutil,getfunction,comic_site

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
    n = comic_site.baozimh.output_list(importurl,import_list,choose)
else:
    print('你添加的网站不在支持列表内')
    exit()

final_list = n[0]
directory_name = n[1]
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
pdfFile = f'./PDF/{directory_name}.pdf'
getfunction.combine_imgs_pdf(folder, pdfFile)
shutil.rmtree(folder) #完成后删除图片文件夹
print('\nComplate')