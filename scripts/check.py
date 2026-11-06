from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from build import load_notes, OUT

class Page(HTMLParser):
    def __init__(self):super().__init__();self.ids=set();self.links=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        if tag in ('a','script','link'):
            v=a.get('href') or a.get('src')
            if v:self.links.append(v)

notes=load_notes(); pages={}
for f in OUT.rglob('*.html'):
    p=Page();p.feed(f.read_text(encoding='utf-8'));pages[f.resolve()]=p
assert len(pages)==len(notes)+1,'Unexpected generated page count'
for f,p in pages.items():
    for link in p.links:
        u=urlsplit(link)
        if u.scheme or u.netloc:
            assert u.scheme=='https',f'Unsafe URL: {link}';continue
        target=(f.parent/unquote(u.path)).resolve() if u.path else f
        assert target.is_relative_to(OUT.resolve()),'Path escapes docs'
        assert target.is_file(),f'Missing file: {link}'
        if u.fragment:assert target in pages and u.fragment in pages[target].ids,f'Missing anchor: {link}'
for n in notes:
    p=pages[(OUT/'notes'/f'{n["slug"]}.html').resolve()]
    assert {'concept','steps','example','pitfalls','checks','sources'}<=p.ids,'Missing section'
print(f'PASS: {len(notes)} source notes, {len(pages)} pages, internal links, anchors, six sections, HTTPS sources')
