"""Validate source notes and generate static pages. Python standard library only."""
from pathlib import Path
from string import Template
from datetime import date
from urllib.parse import urlparse
import json, html, re, shutil

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs'
FIELDS={'slug','title','category','summary','minutes','order','updated','goals','concept','steps','example','pitfalls','checks','sources'}
def text(value):
    return isinstance(value,str) and bool(value.strip())
def load_notes():
    notes=[]
    for path in sorted((ROOT/'content').glob('*.json')):
        n=json.loads(path.read_text(encoding='utf-8'))
        assert isinstance(n,dict) and set(n)==FIELDS, f'{path.name}: fields'
        assert re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*',n['slug']) and n['slug']==path.stem, 'slug'
        assert text(n['title']) and len(n['title'])<=30, 'title'
        assert text(n['summary']) and len(n['summary'])<=100, 'summary'
        assert n['category'] in ['AI 概念','學習方法'], 'category'
        assert type(n['minutes']) is int and 1<=n['minutes']<=60, 'minutes'
        assert type(n['order']) is int and n['order']>0, 'order'
        assert date.fromisoformat(n['updated']).isoformat()==n['updated'], 'updated'
        for k,minimum in [('goals',2),('concept',1),('steps',3),('pitfalls',1)]:
            assert isinstance(n[k],list) and len(n[k])>=minimum and all(text(v) for v in n[k]),k
        assert text(n['example']), 'example'
        assert isinstance(n['checks'],list) and len(n['checks'])>=2, 'checks'
        for check in n['checks']:
            assert set(check)=={'question','answer'} and all(text(v) for v in check.values()),'check structure'
        assert isinstance(n['sources'],list) and len(n['sources'])>=1, 'sources'
        for source in n['sources']:
            assert set(source)=={'label','url','note'} and all(text(v) for v in source.values()),'source structure'
            u=urlparse(source['url']);assert u.scheme=='https' and u.netloc and not u.username,'source URL'
        notes.append(n)
    assert notes,'No notes'
    assert len({n['order'] for n in notes})==len(notes),'Duplicate order'
    return sorted(notes,key=lambda n:n['order'])
def e(v):return html.escape(str(v),quote=True)
def lis(items):return ''.join('<li>'+e(v)+'</li>' for v in items)
def build():
    notes=load_notes() # validate everything before writing
    (OUT/'notes').mkdir(parents=True,exist_ok=True)
    shutil.copytree(ROOT/'assets',OUT/'assets',dirs_exist_ok=True)
    template=Template((ROOT/'templates/page.html').read_text(encoding='utf-8'))
    def page(path,title,description,content,root):
        path.write_text(template.substitute(title=e(title),description=e(description),content=content,root=root),encoding='utf-8')
    cards=''.join(f'<article class="card" data-group="{e(n["category"])}"><div class="meta"><span>{e(n["category"])}</span><span>約 {n["minutes"]} 分鐘</span></div><h3><a href="notes/{n["slug"]}.html">{e(n["title"])}</a></h3><p>{e(n["summary"])}</p><a class="read" href="notes/{n["slug"]}.html">開始閱讀 →</a></article>' for n in notes)
    content=f'''<section class="hero wrap"><div><div class="eyebrow">SMALL NOTES. CLEAR NEXT STEPS.</div><h1>每次學一點，<br><span>下次用得上。</span></h1><p class="lead">把 AI 概念與課業整理方法，寫成有例子、能檢核的學習筆記。讀完一篇，帶走一個可以實際使用的方法。</p><a href="#library">從一篇筆記開始 ↓</a></div><aside class="hero-note"><span class="accent">THE NOTE METHOD</span><h2>不只收藏，也要理解。</h2><ol><li>先掌握一個核心概念</li><li>用具體例子連起來</li><li>最後問問自己：懂了嗎？</li></ol></aside></section><section id="library" class="wrap"><div class="section-head"><h2>挑一篇，開始學習</h2><span id="count" class="count" aria-live="polite">{len(notes)} 篇筆記</span></div><div class="tools"><div class="filters" aria-label="分類篩選"><button data-category="全部" aria-pressed="true">全部筆記</button><button data-category="AI 概念" aria-pressed="false">AI 概念</button><button data-category="學習方法" aria-pressed="false">學習方法</button></div><div class="search"><label for="search">搜尋標題與摘要</label><input id="search" type="search" placeholder="試試：報告、AI、閱讀"></div></div><div class="grid">{cards}</div><p id="empty" class="empty" hidden>沒有找到符合的筆記，試著換個關鍵字或分類。</p><div class="rule-banner"><div><h3>每篇不同主題，同一套清楚的閱讀順序。</h3><p>從概念、步驟、例子，到提醒、檢核與來源，依照共用規則持續新增。</p></div><a href="https://github.com/Xiangyu911117/study-notes-lab/blob/main/AGENTS.md">閱讀 AGENTS.md ↗</a></div></section>'''
    page(OUT/'index.html','首頁','AI 概念與學習方法，依一致規則持續累積的筆記站。',content,'.')
    sections=[('concept','核心概念'),('steps','操作步驟'),('example','具體例子'),('pitfalls','易錯提醒'),('checks','自我檢核'),('sources','參考來源')]
    for i,n in enumerate(notes):
        toc=''.join(f'<a href="#{k}">{label}</a>' for k,label in sections)
        checks=''.join(f'<div class="check"><label><input type="checkbox" data-check="{e(ch["question"])}">{e(ch["question"])}</label><details><summary>展開參考答案</summary><p>{e(ch["answer"])}</p></details></div>' for ch in n['checks'])
        sources=''.join(f'<li><a href="{e(s["url"])}">{e(s["label"])}</a><br>{e(s["note"])}</li>' for s in n['sources'])
        prev=f'<a href="{notes[i-1]["slug"]}.html">← {e(notes[i-1]["title"])}</a>' if i else '<a href="../index.html">← 全部筆記</a>'
        nxt=f'<a href="{notes[i+1]["slug"]}.html">{e(notes[i+1]["title"])} →</a>' if i+1<len(notes) else '<a href="../index.html">回到筆記列表 →</a>'
        content=f'''<div class="note-head"><a class="back" href="../index.html">← 回到筆記列表</a><div class="meta"><span>{e(n['category'])}</span><span>預估閱讀 {n['minutes']} 分鐘</span><span>更新 {n['updated']}</span></div><h1>{e(n['title'])}</h1><p class="lead">{e(n['summary'])}</p></div><div class="article-grid wrap"><aside class="toc"><strong>這篇的閱讀路線</strong>{toc}</aside><article data-slug="{n['slug']}"><div class="goals"><strong>讀完後，你應該能夠</strong><ul>{lis(n['goals'])}</ul></div><h2 id="concept">核心概念</h2>{''.join('<p>'+e(v)+'</p>' for v in n['concept'])}<h2 id="steps">操作步驟</h2><ol>{lis(n['steps'])}</ol><h2 id="example">具體例子</h2><div class="example">{e(n['example'])}</div><h2 id="pitfalls">易錯提醒</h2><ul>{lis(n['pitfalls'])}</ul><h2 id="checks">自我檢核</h2><p>先想答案，再展開對照；能說明原因後再勾選。</p><p id="check-status" class="status" aria-live="polite"></p>{checks}<h2 id="sources">參考來源</h2><ul class="sources">{sources}</ul><div class="pager">{prev}{nxt}</div></article></div>'''
        page(OUT/'notes'/f'{n["slug"]}.html',n['title'],n['summary'],content,'..')
    (OUT/'.nojekyll').write_text('',encoding='utf-8')
    print(f'Built {len(notes)} notes + index')
if __name__=='__main__':build()
