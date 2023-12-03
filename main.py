import os
import ebooklib
from ebooklib import epub
from lxml import etree

def read_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    return text

def create_book(identifier, title, language, author, cover_image):
    book = epub.EpubBook()
    book.set_identifier(identifier)
    book.set_title(title)
    book.set_language(language)
    book.add_author(author)
    book.set_cover(cover_image, open(cover_image, 'rb').read())
    return book

def add_stylesheet(book):
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
    return default_css

def create_chapter(book, default_css, chapter_text, index):
    lines = chapter_text.split('\n')
    title = lines[0] if len(lines) > 0 else 'Chapter {}'.format(index+1)
    content = '</p><p>'.join(lines[1:]) if len(lines) > 1 else ''
    c = epub.EpubHtml(title=title, file_name='chap_{}.xhtml'.format(index+1), lang=book.language)
    c.content=u'<h2>{}</h2><p>{}</p>'.format(title, content)
    c.add_item(default_css)
    book.add_item(c)
    return c

def add_chapters_to_book(book, default_css, text):
    chapters = text.split("\n\n")
    book_chapters = []
    book_spine = ['nav']

    for i, chapter in enumerate(chapters):
        c = create_chapter(book, default_css, chapter, i)
        book_chapters.append(c)
        book_spine.append(c)

    book.toc = tuple(book_chapters)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = book_spine

def output_book(book, output_path):
    epub.write_epub(output_path, book, {})

def main():
    file_path = '地煞七十二变.txt'
    identifier = 'id123456'
    title = '地煞七十二变'
    language = 'zh-CN'
    author = '祭酒'
    cover_image = 'ds.jpeg'
    output_path = '地煞七十二变.epub'
    
    text = read_file(file_path)
    book = create_book(identifier, title, language, author, cover_image)
    default_css = add_stylesheet(book)
    add_chapters_to_book(book, default_css, text)
    output_book(book, output_path)

if __name__ == "__main__":
    main()
