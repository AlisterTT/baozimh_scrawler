import requests,re,getfunction

class baozimh():  #https://cn.baozimh.com/
    def output_list(importurl,import_list,choose):
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
        return final_list,directory_name