import os
import re
import argparse
from ebooklib import epub

# 正则表达式匹配中文章节标题
# CHAPTER_REGEX = r'^(.*第[\u4e00-\u9fa5零一二三四五六七八九十百千万0-9]+章.*)$'
CHAPTER_REGEX = r'(第[\u4e00-\u9fa5零一二三四五六七八九十百千万0-9]+章)'

def read_file(file_path):
    """读取文本文件并返回其内容。"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.readlines()
    except IOError as e:
        print(f'无法打开文件 {file_path}: {e}')
        return None

def clean_lines(lines):
    """去除行前空白和空白行并返回文本。"""
    return [line.lstrip() for line in lines if line.strip()]

def process_text(lines):
    """处理文本，将章节标题分隔并返回处理后的文本。"""
    text = ''.join(lines)
    text = re.sub(f'(?m){CHAPTER_REGEX}', r'\n\1', text)
    return text

def create_book(identifier, title, language, author, cover_image):
    """创建EPUB书籍对象，并设置基本信息和封面。"""
    try:
        with open(cover_image, 'rb') as img_file:
            cover_data = img_file.read()
    except IOError as e:
        print(f'无法打开封面图片 {cover_image}: {e}')
        return None

    book = epub.EpubBook()
    book.set_identifier(identifier)
    book.set_title(title)
    book.set_language(language)
    book.add_author(author)
    book.set_cover(file_name="cover.jpg", content=cover_data)
    
    return book

def create_chapter(title, content, language, chapter_number, stylesheet):
    """创建并返回一个EPUB章节。"""
    chapter_file_name = f'chap_{chapter_number}.xhtml'
    chapter_title = title if title else f'Chapter {chapter_number}'

    c = epub.EpubHtml(title=chapter_title, file_name=chapter_file_name, lang=language)
    c.content = f'<h2>{chapter_title}</h2><p>{content}</p>'
    c.add_item(stylesheet)
    
    return c

def build_book_structure(book, chapters):
    """构建EPUB书籍的结构，包括目录、章节和导航信息。"""
    book.toc = tuple(chapters)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    spine = ['nav'] + chapters
    book.spine = spine

def export_book(book, output_path):
    """导出EPUB书籍到指定的文件路径。"""
    try:
        epub.write_epub(output_path, book, {})
    except Exception as e:
        print(f'无法导出EPUB书籍: {e}')

def main():
    """程序主入口函数。处理命令行参数，导入文本，创建EPUB书籍，并导出。"""
    parser = argparse.ArgumentParser(description='TXT小说转换为EPUB格式书籍')
    parser.add_argument('-i', '--input', type=str, required=True, help='输入TXT小说文本路径')
    parser.add_argument('-c', '--cover_image', type=str, required=True, help='封面图片文件路径')
    
    args = parser.parse_args()
    
    if not args.input.endswith('.txt'):
        print('错误：输入文件必须是txt格式')
        return

    lines = read_file(args.input)
    if lines is None:
        return

    lines = clean_lines(lines)
    text = process_text(lines)

    title = os.path.splitext(os.path.basename(args.input))[0]
    output_path = os.path.join(os.path.dirname(args.input), title + '.epub')
    
    identifier = input('请输入书籍ID(例如：id123456): ') or 'id123456'
    language = input('请输入书籍语言(例如：zh-CN): ') or 'zh-CN'
    author = input('请输入作者名字(例如：无名): ') or '无名'
    
    book = create_book(identifier, title, language, author, args.cover_image)
    if book is None:
        return

    # 定义CSS样式
    style = '''
    @namespace epub "http://www.idpf.org/2007/ops";
    body {
        text-align: justify;
    }
    h2 {
        text-align: left;
        text-transform: uppercase;
        font-weight: 200;
    }
    '''
    default_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(default_css)

    # 处理章节并添加到书中
    chapters = text.split("\n\n")
    book_chapters = []
    for i, chapter_text in enumerate(chapters):
        lines = chapter_text.split('\n')
        title = lines[0] if lines else ''
        content = '</p><p>'.join(lines[1:]) if len(lines) > 1 else ''
        chapter = create_chapter(title, content, language, i + 1, default_css)
        book.add_item(chapter)
        book_chapters.append(chapter)

    build_book_structure(book, book_chapters)
    export_book(book, output_path)
    print(f'书籍已导出：{output_path}')

if __name__ == "__main__":
    main()