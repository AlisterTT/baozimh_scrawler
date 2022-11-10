import requests,os,time,shutil
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

def merge(final_list,directory_name):#下载图片后合并为pdf
    output_dir = ['PDF', directory_name]
    for i in range(len(output_dir)):
        if not os.path.exists(output_dir[i]):
            os.mkdir(output_dir[i])
    for i in range (len(final_list)):
        file_url = final_list[i]
        file_path = f'{directory_name}/{directory_name}_{i}.jpg'
        down_load(file_url, file_path)
        time.sleep(0.1)#设置延迟
    folder = f'./{directory_name}/'
    pdfFile = f'./PDF/{directory_name}.pdf'
    combine_imgs_pdf(folder, pdfFile)
    shutil.rmtree(folder) #完成后删除图片文件夹
    print(f'\n{directory_name}Complate\n')


def region2list(rg_str):#格式化章节序列号为列表
    lst = []
    rg_str_lst = rg_str.strip().split(',')
    for i in rg_str_lst:
        if '-' in i:
            st, ed = i.split('-')
            lst.extend(list(range(int(st), int(ed)+1)))
        else:
            lst.append(int(i))
    return lst