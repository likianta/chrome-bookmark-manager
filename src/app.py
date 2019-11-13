from os.path import exists

from bs4.element import Tag
from lk_utils import read_and_write_basic
from lk_utils.char_converter import PunctuationConverter
from lk_utils.lk_logger import lk
from lk_utils.name_formatter import prettify_name
from lk_wrapper.bs4_wrapper import BeautifulSoup


def main():
    """
    IN: bookmark.html: 输入一个浏览器导出的书签文件 (html 格式). 注意不能直接用浏览器导出的
        书签文件, 因为该文件中存在大量未封口的 tag, 会导致 soup 解析失败. 为了解决此问题, 我
        们先用浏览器打开该 html 文件, 浏览器会帮我们处理好 tag 的封口. 按 f12 复制 outer
        html, 并保存到文件, 这个文件的路径才是本函数接受的输入.
    OT: bookmark.json
        bookmark_prettified.html
    
    REF: data/sample.mhtml
    """
    if exists('../data/bookmark.json'):
        data = read_and_write_basic.read_json('../data/bookmark.json')
    else:
        soup = BeautifulSoup('../data/bookmark.html')
        data = indexing(soup.dl.dt, {})
        read_and_write_basic.write_json(data, '../data/bookmark.json')
    
    # ------------------------------------------------
    
    html_builder = export_new_html(data, [])
    
    html_builder.insert(0, """<!DOCTYPE netscape-bookmark-file-1>
    <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
            <title>Bookmarks</title>
        </head>
        <body>
            <h1>Bookmarks</h1>
            <dl>""")
    html_builder.append("""
            </dl>
        </body>
    </html>""")
    
    read_and_write_basic.write_file(
        html_builder, '../output/bookmark_prettified.html'
    )


def indexing(element: Tag, holder: dict):
    """
    structure:
        1. dl > p, [dt]
        2. dt > h3, dl
        3. dt > a
    IN: bookmark.html
    OT: data: {folder: {link: (title, icon)}}
    """
    if element.h3:  # folder
        title = element.h3.text
        lk.loga(title)
        node = holder.setdefault(title, {})
        for dt in element.dl.find_all('dt', recursive=False):
            indexing(dt, node)
    else:  # item
        a = element.a
        try:
            link, title, icon = a['href'], a.text, a.get('icon', '')
            holder[link] = (title, icon)
        except KeyError:
            lk.logt('[E3036]', a)
            # -> <a add_date="1552352241">为知笔记剪藏</a>
    return holder


def export_new_html(data: dict, builder: list):
    """
    structure:
        1. dl > p, [dt]
        2. dt > h3, dl
        3. dt > a
        
    IN: data: {folder: {link: (title, icon)}}
        builder: [] (initial with empty list)
    OT: builder: [str]
    """
    for k, v in data.items():
        if isinstance(v, dict):
            builder.append(
                f"""<dt><h3>{k}</h3><dl>"""
            )
            export_new_html(v, builder)
            builder.append(
                """</dl></dt>"""
            )
        else:
            # k: link, v: (title, icon)
            link = k
            title = prettify_title(v[0])
            icon = v[1]
            if icon:
                builder.append(
                    f'<dt><a href="{link}" icon="{icon}">{title}</a></dt>'
                )
            else:
                builder.append(
                    f'<dt><a href="{link}">{title}</a></dt>'
                )
    return builder


converter = PunctuationConverter()


def prettify_title(title: str):
    title = converter.trans(title)
    for k, v in {
        '<': '&lt;',
        '>': '&gt;',
        '_': ' - ',
        '|': ' - ',
        '~': '',
    }.items():
        title = title.replace(k, v)
    
    title = prettify_name(title, lower=False, save_dot=True)
    
    return title


if __name__ == "__main__":
    main()
    lk.print_important_msg()
    lk.over()
    # lk.dump_log()
