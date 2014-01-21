import os
import sys
import codecs
import markdown
import json

def read_file(filename):
    content = ""
    try:
        f = codecs.open(filename, 'r', "utf-8")
    except IOError:
        print "File", filename, "does not exist!"
        return [-1, content]
    content = f.read()
    f.close()
    return [0, content]

def write_file(filename, text):
    f = codecs.open(filename, 'w', 'utf-8')
    f.write(text)
    f.close()

def extract(str, sep):
    h, s, t = str.partition(sep)
    h = h.strip()
    t = t.strip()
    return [h, t]

def parse_meta(raw_meta):
    lines = raw_meta.splitlines()
    meta = {'author':'',
            'category':'',
            'tag':'',
            'date':'',
            'filename':'',
            'title':''
            }
    for line in lines:
        name, value = extract(line, ':')
        meta[name] = value
    
    meta['filename'] = meta['filename'].replace('_posts/', '')
    meta['category'], sep, name = meta['filename'].rpartition('/')
    meta['title'], fmt = extract(name, '.')
    if meta['tag']:
        meta['tag'] = [s.strip() for s in meta['tag'].split(',')]
    else:
        meta['tag'] = []
    return meta

def output_article(path, title, text):
    directory = path.replace('_posts/', '', 1)

    if not directory.endswith('/'):
        directory += '/'

    directory += title + "/"

    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = directory + 'index.html'
    write_file(filename, text)
    
def load_meta_store():
    global meta_store
    try:
        f = open("./.meta_store.json", 'r')
        meta_store = json.load(f)
        f.close()
    except IOError:
        meta_store = []

def save_meta_store():
    f = open("./.meta_store.json", 'w')
    json.dump(meta_store, f)
    f.close()

def update_meta_store(meta):
    global meta_store
    found = False
    for idx in range(0, len(meta_store)):
        if meta_store[idx]['filename'] == meta['filename']:
            meta_store[idx] = meta
            found = True
            break
    if not found:
        meta_store.insert(0, meta)

def generate_article(filename):
    path, sep, title = filename.rpartition('/')
    title, sep, fmt = title.rpartition('.')
    output = head.replace("{{title}}", title)
    ret, content = read_file(filename)
    if ret < 0:
        return
    raw_meta, content = extract(content, "--begin--")
    raw_meta += "\n filename: " + filename
    meta = parse_meta(raw_meta)
    update_meta_store(meta)
    output += markdown.markdown(content)
    output += foot
    output_article(path, title, output)

def generate_index(meta_store):
    meta_store = sorted(meta_store, key = lambda meta: meta['date'], reverse = True)
    output = head.replace("{{title}}", "Kai's notes")
    cnt = 0
    fmt = '<p><span>%s</span>: <a href="/%s/%s">%s</a></p>\n'
    for meta in meta_store:
        output += fmt % (meta['date'], meta['category'], meta['title'], meta['title'])
        cnt += 1
        if cnt == 5:
            break
    output += foot
    write_file('index.html', output)

def generate_tag(meta_store):
    meta_store = sorted(meta_store, key = lambda meta: meta['date'], reverse = True)
    tags = {}
    for meta in meta_store:
        for tag in meta['tag']:
            if tags.has_key(tag):
                tags[tag].append(meta)
            else:
                tags[tag] = [meta]

    output = head.replace("{{title}}", "Kai's notes | Tag")
    fmt = '<p><span>%s</span>: <a href="/%s/%s">%s</a></p>\n'
    for tag in sorted(tags.iterkeys()):
        output += "<t2>%s</t2>\n" % tag
        for i in tags[tag]:
            output += fmt % (i['date'], i['category'], i['title'], i['title'])
    output += foot
    write_file('tag.html', output)

def generate_category(meta_store):
    meta_store = sorted(meta_store, key = lambda meta: meta['date'], reverse = True)
    categories = {}
    for meta in meta_store:
        if categories.has_key(meta['category']):
            categories[meta['category']].append(meta)
        else:
            categories[meta['category']] = [meta]

    output = head.replace("{{title}}", "Kai's notes | Category")
    fmt = '<p><span>%s</span>: <a href="/%s/%s">%s</a></p>\n'
    for cate in sorted(categories.iterkeys()):
        output += "<t2>%s</t2>\n" % cate
        for i in categories[cate]:
            output += fmt % (i['date'], i['category'], i['title'], i['title'])
    output += foot
    write_file('category.html', output)

def generate_archive(meta_store):
    meta_store = sorted(meta_store, key = lambda meta: meta['date'], reverse = True)
    output = head.replace("{{title}}", "Kai's notes | Archive")
    fmt = '<p><span>%s</span>: <a href="/%s/%s">%s</a></p>\n'
    cur = "0000-00-00"
    for meta in meta_store:
        date = meta['date']
        if not date.startswith(cur):
            cur = date[0:7]
            output += "<h2>%s</h2>\n" % cur
        output += fmt % (meta['date'], meta['category'], meta['title'], meta['title'])   
    output += foot
    write_file('archive.html', output)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        files = sys.argv[1:]

    global head, foot
    ret, head = read_file("./_includes/head.html")
    ret, foot = read_file("./_includes/foot.html")
    load_meta_store()
    for f in files:
        generate_article(f)
    generate_index(meta_store)
    generate_tag(meta_store)
    generate_category(meta_store)
    generate_archive(meta_store)
    save_meta_store()
