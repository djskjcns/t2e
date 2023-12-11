import os
import re
import ebooklib
from ebooklib import epub
from lxml import etree

def import_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = [line.lstrip() for line in file.readlines()]
        text = ''.join(lines)

    chapter_regex = r'(.{0,10}第.*章.{0,30})'
    
    first_line = lines[0] if lines else ""
    if re.match(chapter_regex, first_line):
        text = re.sub(f'(?m){chapter_regex}', r'\n\1', text)
        text = re.sub(r'\n+(.{0,10}第.*章.{0,30})', r'\1', text, count=1)
    else:
        text = re.sub(f'(?m){chapter_regex}', r'\n\1', text)

    return text

def create_book(identifier, title, language, author, cover_image):
    book = epub.EpubBook()
    book.set_identifier(identifier)
    book.set_title(title)
    book.set_language(language)
    book.add_author(author)
    book.set_cover(cover_image, open(cover_image, 'rb').read())
    return book

def process_chapters(book, text):
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
    
    chapters = text.split("\n\n")
    book_chapters = []
    book_spine = ['nav']

    for i, chapter_text in enumerate(chapters):
        lines = chapter_text.split('\n')
        title = lines[0] if lines else 'Chapter {}'.format(i + 1)
        content = '</p><p>'.join(lines[1:]) if len(lines) > 1 else ''
        c = epub.EpubHtml(title=title, file_name='chap_{}.xhtml'.format(i + 1), lang=book.language)
        c.content = u'<h2>{}</h2><p>{}</p>'.format(title, content)
        c.add_item(default_css)
        book.add_item(c)
        book_chapters.append(c)
        book_spine.append(c)

    book.toc = tuple(book_chapters)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = book_spine

    return book

def export_book(book, output_path):
    epub.write_epub(output_path, book, {})

def main():
    file_path = '我的病娇仙子模拟器.txt'
    identifier = 'id123456'
    title = '我的病娇仙子模拟器'
    language = 'zh-CN'
    author = '憨八龟爱上大大怪'
    cover_image = 'wd.png'
    output_path = '我的病娇仙子模拟器.epub'
    
    text = import_file(file_path)
    book = create_book(identifier, title, language, author, cover_image)
    book = process_chapters(book, text)
    export_book(book, output_path)

if __name__ == "__main__":
    main()