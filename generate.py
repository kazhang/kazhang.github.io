import os
import sys
import codecs
import markdown

from datetime import datetime

def read_file(filename):
    content = ""
    try:
        f = codecs.open(filename, 'r', "utf-8")
    except IOError:
        print "File", filename, "does not exist!"
        return [-1, content]
    content = f.read()
    return [0, content]

def output_article(date, title, text):
    date = datetime.strptime(date, "%Y-%m-%d")
    directory = "./"
    directory += date.strftime("%Y/%m/%d") + '/'
    directory += title + '/'

    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = directory + 'index.html'
    f = open(filename, 'w')
    f.write(text)

def extract(str, sep):
    h, s, t = str.partition(sep)
    h = h.strip()
    t = t.strip()
    return [h, s, t]

def generate(filename):
    path, sep, title = filename.rpartition('/')
    title, sep, fmt = title.rpartition('.')
    output = head.replace("{{title}}", title)
    ret, content = read_file(filename)
    if ret < 0:
        return
    meta, sep, content = extract(content, "--begin--")
    output += markdown.markdown(content)
    output += foot
    output_article("2014-01-02", title, output)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        files = sys.argv[1:]

    global head, foot
    ret, head = read_file("./_includes/head.html")
    ret, foot = read_file("./_includes/foot.html")
    for f in files:
        generate(f)
