import os
import ebooklib
from ebooklib import epub
from lxml import etree

# Step 1: Importing txt file
with open('地煞七十二变.txt', 'r') as file:
    text = file.read()

# Step 2: Txt is divided into chapters based on "\n\n".
chapters = text.split("\n\n")

# Step 3: Create a standard epub3 file, write metadata, and add a cover.
book = epub.EpubBook()

# set metadata
book.set_identifier('id123456')
book.set_title('地煞七十二变')
book.set_language('zh-CN')

book.add_author('祭酒')

# add cover image
book.set_cover("ds.jpeg", open('ds.jpeg', 'rb').read())

# Step 4: Create a stylesheet, with the first line of each chapter defined as a heading and the body text aligned justified.
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

# define an empty list of chapters
book_chapters = []
book_spine = ['nav']

# add chapters
for i, chapter in enumerate(chapters):
    lines = chapter.split('\n')
    title = lines[0] if len(lines) > 0 else 'Chapter {}'.format(i+1)
    content = '</p><p>'.join(lines[1:]) if len(lines) > 1 else ''
    c = epub.EpubHtml(title=title, file_name='chap_{}.xhtml'.format(i+1), lang='en')
    c.content=u'<h2>{}</h2><p>{}</p>'.format(title, content)
    c.add_item(default_css)
    book.add_item(c)
    book_chapters.append(c)
    book_spine.append(c)

# define Table Of Contents
book.toc = tuple(book_chapters)

# add navigation files
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# define spine
book.spine = book_spine

# compile epub file
epub.write_epub('output.epub', book, {})
