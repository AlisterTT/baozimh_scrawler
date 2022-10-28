import requests,re,time,os,ast
from contextlib import closing
from PIL import Image

def down_load(file_url, file_path): #下载用
    with closing(requests.get(file_url, stream=True)) as response:
        chunk_size = 1024  # 单次请求最大值
        if 'Content-Length' in response.headers:
            content_size = int(response.headers['content-length'])  # 内容体总大小
        else:
            print("Warning: missing key 'Content-Length' in request headers; taking default length of 100 for progress bar.")
            content_size = 100
        data_count = 0
        with open(file_path, "wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                data_count = data_count + len(data)
                now_jd = (data_count / content_size) * 100
                print("\r 文件下载进度：%d%%(%d/%d) - %s"
                      % (now_jd, data_count, content_size, file_path), end=" ")

def combine_imgs_pdf(folder_path, pdf_file_path):  #合成pdf
    files = os.listdir(folder_path)
    png_files = []
    sources = []
    for file in files:
        if 'png' in file or 'jpg' in file:
            png_files.append(folder_path + file)
    png_files.sort(key=lambda x: os.stat(x).st_ctime_ns)
    output = Image.open(png_files[0])
    png_files.pop(0)
    for file in png_files:
        png_file = Image.open(file)
        if png_file.mode == "RGB":
            png_file = png_file.convert("RGB")
        sources.append(png_file)
    output.save(pdf_file_path, "pdf", save_all=True, append_images=sources)

with open('comic_list.txt', 'r',encoding='UTF-8') as f:
    import_list = ast.literal_eval(f.read())
for i in range(len(import_list)):
    a = str(import_list[i]['name'])
    choose_list = str(i+1) + '. ' + a
    print(choose_list)
choose = int(input('选择漫画序号：'))
comic_capter = input('输入章节：')
comic_capter_format = comic_capter + '_'
baseurl = import_list[choose-1]['url']+'0_'+comic_capter_format
directory_name = import_list[choose-1]['name']+comic_capter

comic_url = []
temlist = []
for i in range(1,21):
    comic_url.append(baseurl+str(i)+'.html')
for i in range(len(comic_url)):
    html_str = requests.get(comic_url[i]).content.decode()
    img_list = re.findall('img src="(.*?)" alt',html_str, re.S)
    for u in range(len(img_list)):
        temlist.append(img_list[u])
final_list = sorted(set(temlist),key=temlist.index)

if not os.path.exists(directory_name):
    work_directory = os.mkdir(directory_name)

for i in range (len(final_list)):
    file_url = final_list[i]
    file_path = f'{directory_name}/{directory_name}_{i}.jpg'
    down_load(file_url, file_path)
    time.sleep(0.5)

folder = f'./{directory_name}/'
pdfFile = f'./{directory_name}/{directory_name}_final.pdf'
combine_imgs_pdf(folder, pdfFile)