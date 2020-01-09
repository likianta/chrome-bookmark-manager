"""
对 json 格式的书签的处理.

步骤:
    1. 找到该文件: "C:/Users/<User>/AppData/Local/Google/Chrome/User Data
       /<User Profile>/Bookmarks", 这里的 <User Profile> 是你的用户名, 比如
       "Guest Profile", "Profile 1" 等.
    2. 复制该文件到本项目的 data 目录下, 并重命名为 "bookmarks.json"
    3. 运行本程序
    4. 生成文件: "output/bookmarks.json"
    5. 将文件重命名为 "Bookmarks", 粘贴回原位置并覆盖 (请预先将被覆盖的文件备份)
    6. 重新启动浏览器
    
REF:
    https://www.baidu.com/link?url=FwH1iorA6KLCB0YhmpeDA0qCEbAMVe74-Pw2XdjwRr6yl
    TJNQOtjuvRobB_MZUivUaXsM3S0NJgytCTKes4YTK&wd=&eqid=975a4e2e00007c37000000045
    e16d933
"""
import re

from lk_utils.toolbox import *


def main(ifile, ofile):
    """
    IN: data/bookmarks.json
            ifile copied from: "C:/Users/Likianta/AppData/Local/CentBrowser
            /User Data/Default/Bookmarks"
    OT: output/bookmarks.json
    """
    bookmarks = read_and_write.loads(ifile)
    """
    structure:
        {
            "checksum": str,
            "version": int,
            "roots": {
                "bookmark_bar": {
                    "date_added": <str abstime>,
                    "date_modified": <str abstime>,
                    "id": str,
                    "name": "书签栏",
                    "sync_transaction_version": str,
                    "type": "folder"
                    "children": [
                        {
                            "date_added": <str abstime>,
                            "date_modified": <str abstime>,
                            "id": str,
                            "name": str,
                            "sync_transaction_version": str,
                            "type": "folder",
                            "children": [
                                {
                                    "date_added": <str abstime>,
                                    "id": str,
                                    "name": str,
                                    "sync_transaction_version": str,
                                    "type": "url",
                                    "url": str,
                                    "meta_info": {
                                        "last_visited_desktop": <str abstime>,
                                    },
                                },
                                ...
                            ]
                        },
                        ...
                    ]
                }
            }
        }
    """
    walk(bookmarks['roots']['bookmark_bar'])
    read_and_write.dumps(bookmarks, ofile)
    return bookmarks


def export_excel(bookmarks: dict, ofile):
    """
    this is an optional method.
    """
    
    def _processing(node, parent_name):
        folder_name = '{}/{}'.format(
            parent_name, node['name']
        )
        for item in node['children']:
            if item['type'] == 'url':
                _writeln(folder_name, item['name'], item['url'])
            elif item['type'] == 'folder':
                _processing(item, folder_name)
            else:
                raise Exception(item['type'])
    
    def _writeln(*data):
        writer.writeln(*data, auto_index=True)
    
    # ------------------------------------------------
    
    writer = ExcelWriter(ofile)
    writer.writeln('index', 'folder_name', 'title', 'url')
    _processing(bookmarks['roots']['bookmark_bar'], 'root')
    writer.save()


def walk(node: dict):
    lk.logax('walking folder', node['name'])
    
    for item in node['children']:
        if item['type'] == 'url':
            process_url(item)
        elif item['type'] == 'folder':
            walk(item)
        else:
            raise Exception(item['type'])


def process_url(node: dict):
    node['name'] = beautify_title(node['name'])


reg1 = re.compile(r'[- ,.:?\w]+')
reg2 = re.compile(r'[,.:?\d\u4e00-\u9fa5]+|[- ,.:?a-z0-9]+')
reg3 = re.compile(r'\s+')
cn_to_en = {
    '，' : ', ', '。': '. ', '、': ', ',
    '“' : '"', '”': '"', '‘': '\'', '’': '\'',
    '：' : ': ', '；': '; ',
    '·' : ' ', '~': '~',
    '？' : '? ', '！': '! ',
    '（' : ' (', '）': ') ',
    '【' : '[', '】': ']',
    '《' : '"', '》': '"',
    '……': '...', '——': ' - ',
}


def beautify_title(title: str):
    for i, j in cn_to_en.items():
        title = title.replace(i, j)
    title = title.replace('|', '-').replace('_', ' - ').lower()
    title = ' '.join(reg1.findall(title))
    title = ' '.join(reg2.findall(title))
    title = re.sub(reg3, ' ', title).strip()
    return title


if __name__ == '__main__':
    resu = main(r'../data/bookmarks.json', '../output/bookmarks.json')
    export_excel(resu, '../output/bookmarks.xlsx')
    
    lk.print_important_msg()
    lk.over()
