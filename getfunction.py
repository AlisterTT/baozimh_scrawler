import requests,re,os
from contextlib import closing
from PIL import Image

def down_load(file_url, file_path): #下载用
    with closing(requests.get(file_url, stream=True)) as response:
        chunk_size = 1024  # 单次请求最大值
        if 'Content-Length' in response.headers:
            content_size = int(response.headers['content-length'])  # 内容体总大小
        else:
#            print("Warning: missing key 'Content-Length' in request headers; taking default length of 100 for progress bar.")
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

def getlist(origin):
    origin_str = requests.get(origin).content.decode()
    capter_str = re.findall('items\"(.*?)\/button',origin_str, re.S)
    capter_list = re.findall('comics-chapters(.*?)<\/a>',capter_str[0], re.S)
    #print('\n'.join(capter_list))
    capter_final = []
    for i in range (len(capter_list)):
        capter_slot = re.findall('r_slot=(.*?)\"',capter_list[i], re.S)
        capter_name = re.findall('<span.*?>(.+?)</span>',capter_list[i], re.S)
#        capter_total = [{f'{capter_slot[0]}':capter_name[0]}]
        capter_total = [[capter_slot[0],capter_name[0]]]
        for u in range(len(capter_total)):
            capter_final.append(capter_total[u])
    return(capter_final)