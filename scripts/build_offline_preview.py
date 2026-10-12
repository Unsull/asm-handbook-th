#!/usr/bin/env python3
"""Optional independent no-Node preview generator.

Install separately (only for this auxiliary preview):
    python -m pip install markdown-it-py beautifulsoup4
This is NOT the VitePress deployment build; VitePress remains the source of truth.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path
from markdown_it import MarkdownIt
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
OUT = ROOT.parent / 'asm-handbook-th-preview'
OUT.mkdir(exist_ok=True, parents=True)
(OUT/'assets').mkdir(exist_ok=True)
manifest = json.loads((ROOT/'scripts'/'chapter_manifest.json').read_text(encoding='utf-8'))
quizzes = json.loads((DOCS/'.vitepress'/'quizzes.json').read_text(encoding='utf-8'))
md = MarkdownIt('default', {'html': True, 'typographer': True})


def clean_vitepress(text):
    if text.startswith('---\n'):
        _, _, text = text.partition('\n---\n')
    text = re.sub(r'<KnowledgeQuiz\s+:chapter="(\d+)"\s*/>', lambda m: f'<div class="quiz-widget" data-chapter="{m.group(1)}"></div>', text)
    # math display fallback; VitePress renders TeX via math plugin, offline preview shows a readable code block.
    text = re.sub(r'\\\[\s*(.*?)\s*\\\]', lambda m: '<pre class="math-equation">'+html.escape(m.group(1).strip())+'</pre>', text, flags=re.S)
    text = re.sub(r'(?m)^::: (tip|info|warning|danger)\s*\n(.*?)\n:::', lambda m: f'\n<aside class="callout {m.group(1)}">{md.render(m.group(2))}</aside>\n', text, flags=re.S)
    return text


def html_output_path(src:Path):
    rel = src.relative_to(DOCS)
    return OUT / rel.with_suffix('.html')


def relative_href(href: str, target: Path) -> str:
    if not href.startswith('/'):
        return href
    if href.startswith('/asm-handbook-th/'):
        href = href[len('/asm-handbook-th/'):]
    else:
        href = href.lstrip('/')
    url, sep, anchor = href.partition('#')
    if url.endswith('/'):
        url += 'index.html'
    elif not Path(url).suffix:
        url += '.html'
    source = OUT/url
    import os
    relative = os.path.relpath(source, start=target.parent).replace('\\','/')
    return relative + (('#'+anchor) if sep else '')


css = r'''
:root{--bg:#f6f8f8;--panel:#ffffff;--card:#f0f6f5;--text:#15312f;--muted:#59736e;--border:#d7e5e1;--brand:#087e73;--accent:#0d9f92;--code:#eff4f4;--shadow:0 16px 60px rgba(12,71,63,.06);color-scheme:light}
:root.dark{--bg:#101b1d;--panel:#162527;--card:#1c3234;--text:#e6f4f0;--muted:#a9c1bd;--border:#325052;--brand:#67d7c9;--accent:#73e5d7;--code:#1d3537;--shadow:none;color-scheme:dark}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{font-family:'Noto Sans Thai','Sarabun','Segoe UI',system-ui,sans-serif;color:var(--text);background:var(--bg);margin:0;font-size:15px;line-height:1.85}
a{color:var(--brand)}.topbar{position:sticky;top:0;z-index:30;background:var(--panel);border-bottom:1px solid var(--border);height:64px;display:flex;align-items:center;padding:0 28px;gap:24px}.brand{font-weight:900;color:var(--text);font-size:19px;white-space:nowrap;text-decoration:none;letter-spacing:-.02em}.logo{display:inline-block;border-radius:9px;background:#0d867b;color:white;font-weight:900;padding:0px 8px;margin-right:9px}.topnav{display:flex;gap:24px}.topnav a{text-decoration:none;color:var(--muted);font-size:13px;font-weight:700}.topnav a:hover{color:var(--brand)}.grow{flex:1}.search-wrap{position:relative;width:255px}.search-wrap input{font-family:inherit;width:100%;font-size:13px;padding:9px 12px;border:1px solid var(--border);background:var(--card);border-radius:11px;color:var(--text)}.search-panel{position:absolute;top:42px;left:0;width:420px;max-width:90vw;max-height:420px;overflow:auto;background:var(--panel);border:1px solid var(--border);border-radius:12px;box-shadow:var(--shadow);display:none;z-index:50}.search-panel a{display:block;text-decoration:none;color:var(--text);padding:12px 15px;border-bottom:1px solid var(--border);font-size:13px}.search-panel a:hover{background:var(--card)}.search-panel small{display:block;color:var(--muted);font-size:11px}.theme-toggle,.menu-toggle{font:inherit;cursor:pointer;border:1px solid var(--border);background:var(--card);color:var(--text);border-radius:9px;padding:6px 11px}.menu-toggle{display:none}
.layout{display:grid;grid-template-columns:265px minmax(0,1fr) 220px;max-width:1660px;margin:auto;min-height:calc(100vh - 64px)}.sidebar{position:sticky;top:64px;align-self:start;height:calc(100vh - 64px);overflow:auto;padding:26px 14px 40px 20px;border-right:1px solid var(--border)}.sidebar .side-label{font-size:11px;letter-spacing:.12em;text-transform:uppercase;font-weight:800;color:var(--muted);margin:0 8px 16px}.sidebar details{margin:7px 0}.sidebar summary{cursor:pointer;padding:8px 12px;font-size:13px;font-weight:700;line-height:1.45;border-radius:8px}.sidebar summary:hover{background:var(--card)}.sidebar .sublinks a{display:block;padding:5px 12px 5px 27px;text-decoration:none;font-size:12px;color:var(--muted);border-radius:7px}.sidebar .sublinks a.active{color:var(--brand);background:var(--card);font-weight:800}.sidebar .sublinks a:hover{color:var(--brand)}.content{min-width:0;padding:37px clamp(24px,4.7vw,78px) 100px;max-width:1000px;width:100%;margin:auto}.toc{position:sticky;top:64px;align-self:start;height:calc(100vh - 64px);overflow:auto;padding:27px 25px 30px 10px;border-left:1px solid var(--border);font-size:12px;color:var(--muted)}.toc .label{font-weight:800;font-size:11px;letter-spacing:.08em;margin-bottom:14px}.toc a{display:block;text-decoration:none;padding:4px 0;color:var(--muted);line-height:1.5}.toc a:hover{color:var(--brand)}.toc a.sub{padding-left:12px}
h1{font-size:clamp(28px,3.2vw,38px);letter-spacing:-.028em;line-height:1.4;margin:8px 0 22px}h2{font-size:24px;margin:42px 0 14px;padding-top:16px;border-top:1px solid var(--border)}h3{font-size:19px;margin:30px 0 10px}p{margin:14px 0}hr{border:none;border-top:1px solid var(--border);margin:30px 0}blockquote{margin:20px 0;background:var(--card);border-left:4px solid var(--brand);padding:9px 17px;border-radius:0 9px 9px 0;color:var(--text)}table{border-collapse:collapse;width:100%;font-size:13px;margin:20px 0;display:block;overflow-x:auto}td,th{border:1px solid var(--border);padding:9px 13px;text-align:left;vertical-align:top;min-width:110px}th{background:var(--card)}ul,ol{padding-left:24px}li{margin:5px 0}code{font-family:Consolas,monospace;background:var(--code);padding:2px 5px;border-radius:5px;font-size:12px;overflow-wrap:anywhere}pre{position:relative;background:var(--code);border:1px solid var(--border);border-radius:12px;padding:18px 18px;overflow:auto;font-size:13px;line-height:1.6}pre code{padding:0;background:transparent;font-size:12px}.callout{border:1px solid var(--border);background:var(--card);border-left:4px solid var(--brand);border-radius:10px;margin:18px 0;padding:12px 16px}.callout.warning{border-left-color:#d3a74f}.chapter-links{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px}.chapter-links a{display:block;border:1px solid var(--border);background:var(--card);padding:17px;border-radius:12px;font-weight:800;text-decoration:none;color:var(--text)}.chapter-links a:hover{border-color:var(--brand)}.chapter-links small{display:block;font-weight:400;color:var(--muted);font-size:12px;margin-top:4px}.pagebar{display:flex;justify-content:space-between;gap:12px;border-top:1px solid var(--border);padding-top:26px;margin-top:46px}.pagebar a{text-decoration:none;font-size:13px;font-weight:700}.eyebrow{font-size:11px;font-weight:900;color:var(--brand);letter-spacing:.15em}.hero{padding:48px 0}.hero h1{font-size:clamp(39px,4.5vw,57px);max-width:830px;line-height:1.22;margin:12px 0 22px}.hero h1 em{font-style:normal;color:var(--brand)}.hero .tagline{color:var(--muted);font-size:19px;max-width:810px}.hero .buttons{display:flex;gap:12px;margin:26px 0}.btn{background:var(--brand);color:var(--bg);text-decoration:none;border-radius:11px;padding:11px 18px;font-weight:800}.btn.ghost{background:var(--card);border:1px solid var(--border);color:var(--text)}.featuregrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:13px}.feature{background:var(--panel);border:1px solid var(--border);border-radius:15px;padding:22px;box-shadow:var(--shadow)}.feature span{font-size:25px}.feature h3{font-size:16px;margin:8px 0}.feature p{font-size:13px;color:var(--muted);margin:0}.quiz{border:1px solid var(--border);border-radius:16px;padding:24px;background:var(--card);margin:24px 0}.quiz-q{background:var(--panel);padding:17px;border:1px solid var(--border);border-radius:12px;margin:14px 0}.quiz-q legend{font-weight:800}.quiz-q fieldset{border:0}.quiz-opt{display:flex;gap:10px;align-items:center;padding:7px 4px;cursor:pointer;font-size:13px}.quiz-opt input{accent-color:var(--brand)}.quiz-results{padding:10px 14px;background:var(--card);border-radius:8px;margin:10px 0;font-size:13px}.quiz-actions{display:flex;gap:10px;margin-top:16px}.quiz-actions button{font:inherit;border-radius:9px;padding:8px 15px;cursor:pointer;border:1px solid var(--border);background:var(--panel);color:var(--text)}.quiz-actions button.primary{background:var(--brand);color:var(--bg)}.quiz-actions button:disabled{opacity:.35;cursor:not-allowed}.quiz-score{font-size:24px;font-weight:900;color:var(--brand);padding:12px 0}.copycode{position:absolute;right:9px;top:8px;border:1px solid var(--border);background:var(--panel);color:var(--muted);border-radius:6px;cursor:pointer;font-size:11px;padding:4px 8px}
@media(max-width:1250px){.layout{grid-template-columns:265px minmax(0,1fr)}.toc{display:none}.topnav{gap:12px}}
@media(max-width:780px){.layout{display:block}.sidebar{position:fixed;left:0;top:64px;width:min(86vw,320px);height:calc(100vh - 64px);z-index:29;background:var(--panel);transform:translateX(-103%);transition:transform .2s;box-shadow:var(--shadow)}body.showmenu .sidebar{transform:translateX(0)}.menu-toggle{display:block}.topnav{display:none}.topbar{gap:9px;padding:0 12px}.brand{font-size:15px}.search-wrap{width:auto;max-width:40vw}.search-panel{right:0;left:auto}.content{padding:24px 18px 70px}.hero{padding:24px 0}.hero .buttons{flex-wrap:wrap}}
'''
(OUT/'assets'/'style.css').write_text(css,encoding='utf-8')

js = r'''
(function(){
  const body = document.body;
  const prefix = body.dataset.root || '';
  const root = document.documentElement;
  document.querySelector('#toggle-theme')?.addEventListener('click',()=>{
    root.classList.toggle('dark');
    try{localStorage.setItem('asm-theme',root.classList.contains('dark')?'dark':'light')}catch(e){}
  });
  try{if(localStorage.getItem('asm-theme')==='dark')root.classList.add('dark')}catch(e){}
  document.querySelector('#toggle-menu')?.addEventListener('click',()=>body.classList.toggle('showmenu'));
  document.querySelectorAll('.sidebar a').forEach(a=>a.addEventListener('click',()=>body.classList.remove('showmenu')));
  document.querySelectorAll('pre').forEach(pre=>{
    if(pre.classList.contains('math-equation'))return;
    const button=document.createElement('button');button.className='copycode';button.textContent='Copy';
    button.addEventListener('click', async ()=>{try{await navigator.clipboard.writeText(pre.innerText.replace(/^Copy\n/,''));button.textContent='Copied'}catch(e){button.textContent='Select code to copy'}});
    pre.appendChild(button);
  });
  const input=document.querySelector('#global-search'), result=document.querySelector('#search-results');
  function safe(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
  if(input&&result){
    input.addEventListener('input',()=>{
      const q=input.value.toLocaleLowerCase().trim();
      if(q.length<2){result.style.display='none';result.innerHTML='';return}
      const matches=(window.__ASM_SEARCH||[]).filter(r=>(r.title+' '+r.text).toLocaleLowerCase().includes(q)).slice(0,8);
      result.innerHTML=matches.map(m=>`<a href="${prefix}${safe(m.url)}">${safe(m.title)}<small>${safe(m.excerpt)}</small></a>`).join('')||'<div style="padding:15px">ไม่พบผลลัพธ์</div>';
      result.style.display='block';
    });
    document.addEventListener('click',ev=>{if(!ev.target.closest('.search-wrap'))result.style.display='none'});
  }
  document.querySelectorAll('.quiz-widget').forEach(mount=>{
    const bank=(window.__ASM_QUIZZES||{})[String(mount.dataset.chapter)]||[];
    let selection={};let graded=false;
    const render=()=>{
      mount.innerHTML='<div class="quiz"><strong>Knowledge Check · '+bank.length+' Questions</strong>'+bank.map((q,i)=>{
        const options=q.options.map((v,j)=>`<label class="quiz-opt"><input type="radio" name="q${i}" data-q="${i}" value="${j}" ${selection[i]===j?'checked':''}/><span>${String.fromCharCode(65+j)}. ${safe(v)}</span></label>`).join('');
        const feedback=graded?`<div class="quiz-results"><strong>${selection[i]===q.answer?'✓ ถูกต้อง':'เฉลย: '+String.fromCharCode(65+q.answer)}</strong> · ${safe(q.why)}</div>`:'';
        return `<div class="quiz-q"><fieldset><legend>${i+1}. ${safe(q.prompt)}</legend>${options}</fieldset>${feedback}</div>`
      }).join('')+`<div class="quiz-actions"><button class="primary" data-action="grade" ${Object.keys(selection).length!==bank.length?'disabled':''}>ตรวจคำตอบ</button><button data-action="reset">เริ่มใหม่</button></div>${graded?'<div class="quiz-score">'+bank.filter((q,i)=>selection[i]===q.answer).length+' / '+bank.length+'</div>':''}</div>`;
      mount.querySelectorAll('input[type=radio]').forEach(input=>input.addEventListener('change',e=>{selection[Number(e.target.dataset.q)]=Number(e.target.value);graded=false;render()}));
      mount.querySelector('[data-action=grade]')?.addEventListener('click',()=>{graded=true;render()});
      mount.querySelector('[data-action=reset]')?.addEventListener('click',()=>{selection={};graded=false;render()});
    };
    render();
  });
})();
'''
(OUT/'assets'/'app.js').write_text(js,encoding='utf-8')
(OUT/'assets'/'quizzes.js').write_text('window.__ASM_QUIZZES = '+json.dumps(quizzes,ensure_ascii=False)+';\n',encoding='utf-8')

allpages = list(DOCS.rglob('*.md'))
pageinfo=[]
for source in allpages:
    if '.vitepress' in source.parts:continue
    content=clean_vitepress(source.read_text(encoding='utf-8'))
    if source == DOCS/'index.md':
        front=source.read_text(encoding='utf-8').split('---',2)[1]
        content='''<div class="hero"><div class="eyebrow">INDEPENDENT THAI-EDUCATION HANDBOOK</div><h1>เข้าใจ <em>Attack Surface Management</em> ตั้งแต่พื้นฐานถึงการปฏิบัติ</h1><p class="tagline">11 บทภาษาไทย พร้อมตัวอย่างร้านค้าออนไลน์และระบบทั่วไป Workshop ที่ปลอดภัย แบบทดสอบโต้ตอบ และอภิธานศัพท์ครบเล่ม</p><div class="buttons"><a class="btn" href="/chapters/01-foundations/">เริ่มอ่านบทที่ 1 →</a><a class="btn ghost" href="/learning-path">ดูสารบัญทั้งหมด</a></div></div><div class="featuregrid">'''+''.join(f'<div class="feature"><span>{icon}</span><h3>{name}</h3><p>{desc}</p></div>' for icon,name,desc in [('📘','ทฤษฎีเชิงลึก','เข้าใจคำศัพท์ กลไก และข้อจำกัดของการประเมิน'),('🧩','11 Chapters','แยก Concepts / Examples / Workshop / Quiz'),('🛠️','Hands-on Labs','Python, Docker, API Security และ Monitoring'),('✅','Quiz โต้ตอบ','เฉลยพร้อมเหตุผล ใช้งานได้โดยไม่ต้อง Login'),('🔎','ค้นหาและอภิธานศัพท์','ค้นข้อความทั้งคู่มือและศัพท์ Technical English'),('🌿','ปรับปรุงต่อได้','เนื้อหาต้นฉบับใหม่ เขียนด้วย Markdown')])+'</div><p class="source-note" style="margin-top:25px">คู่มือนี้เป็นเนื้อหาการศึกษาอิสระ ไม่ใช่คำแปลอย่างเป็นทางการของหนังสือ O’Reilly</p>'
    else:
        content = md.render(content)
    dst=html_output_path(source)
    dst.parent.mkdir(parents=True,exist_ok=True)
    soup=BeautifulSoup(content,'html.parser')
    headings=[]
    for h in soup.select('h2,h3'):
        name=h.get_text(' ',strip=True)
        hid=re.sub(r'[^\w\-]+','-',name.lower(),flags=re.U).strip('-')
        if not hid:hid='section-'+str(len(headings)+1)
        if soup.find(id=hid) is not None:hid+=str(len(headings))
        h['id']=hid
        headings.append((h.name,name,hid))
    for link in soup.select('a[href]'):
        link['href']=relative_href(link['href'],dst)
        if link['href'].startswith('https://'):
            link['target']='_blank'
            link['rel']='noopener noreferrer'
    title=soup.find('h1').get_text(' ',strip=True) if soup.find('h1') else 'ASM Handbook TH'
    rel=source.relative_to(DOCS).with_suffix('.html').as_posix()
    excerpt=soup.get_text(' ',strip=True)[:150]
    searchtext=soup.get_text(' ',strip=True)[:14000]
    pageinfo.append({'url':rel,'title':title,'excerpt':excerpt,'text':searchtext})
    prefix='../'*len(source.relative_to(DOCS).parts[:-1])
    groups=[]
    for ch in manifest:
        base=f'chapters/{ch["slug"]}/'
        active=rel.startswith(base)
        sublinks=''.join(f'<a href="{prefix+base+file}.html" class="{"active" if rel==base+file+".html" else ""}">{label}</a>' for file,label in [('index','ภาพรวม'),('concepts','ทฤษฎี'),('examples','กรณีศึกษา'),('workshop','Workshop'),('quiz','Quiz')])
        groups.append(f'<details {"open" if active else ""}><summary>บทที่ {ch["id"]:02d} · {html.escape(ch["thai"])}</summary><div class="sublinks">{sublinks}</div></details>')
    sidebar='\n'.join(groups)
    aside='<div class="label">ON THIS PAGE</div>'+''.join(f'<a href="#{hid}" class="{"sub" if tag=="h3" else ""}">{html.escape(name)}</a>' for tag,name,hid in headings[:30])
    if not headings:aside=''
    # prev-next navigation for chapter pages
    chapter_pages=[]
    for ch in manifest:
        for page in ('index','concepts','examples','workshop','quiz'):
            chapter_pages.append(f'chapters/{ch["slug"]}/{page}.html')
    pager=''
    if rel in chapter_pages:
        idx=chapter_pages.index(rel)
        prv=chapter_pages[idx-1] if idx>0 else None
        nxt=chapter_pages[idx+1] if idx<len(chapter_pages)-1 else None
        pager=f'<nav class="pagebar"><span>{f"<a href={chr(34)}{prefix+prv}{chr(34)}>← ก่อนหน้า</a>" if prv else ""}</span><span>{f"<a href={chr(34)}{prefix+nxt}{chr(34)}>ถัดไป →</a>" if nxt else ""}</span></nav>'
    output=f'''<!doctype html><html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light dark"><title>{html.escape(title)} | ASM Handbook TH</title><meta name="description" content="{html.escape(excerpt[:155],quote=True)}"><link rel="stylesheet" href="{prefix}assets/style.css"></head><body data-root="{prefix}"><header class="topbar"><button class="menu-toggle" id="toggle-menu" aria-label="เปิดสารบัญ">☰</button><a class="brand" href="{prefix}index.html"><span class="logo">AS</span> ASM Handbook TH</a><nav class="topnav"><a href="{prefix}learning-path.html">สารบัญ</a><a href="{prefix}case-study/index.html">กรณีศึกษา</a><a href="{prefix}glossary/index.html">อภิธานศัพท์</a><a href="{prefix}references/index.html">อ้างอิง</a></nav><div class="grow"></div><div class="search-wrap"><input id="global-search" type="search" placeholder="ค้นหาทั้งคู่มือ..." aria-label="ค้นหา"><div class="search-panel" id="search-results"></div></div><button class="theme-toggle" id="toggle-theme" aria-label="สลับธีม">◐</button></header><div class="layout"><aside class="sidebar"><div class="side-label">CHAPTERS · 01–11</div>{sidebar}</aside><main class="content">{str(soup)}{pager}</main><aside class="toc">{aside}</aside></div><script src="{prefix}assets/quizzes.js"></script><script src="{prefix}assets/search.js"></script><script src="{prefix}assets/app.js"></script></body></html>'''
    dst.write_text(output,encoding='utf-8')

(OUT/'assets'/'search.js').write_text('window.__ASM_SEARCH = '+json.dumps(pageinfo,ensure_ascii=False)+';\n',encoding='utf-8')
print(f'Created {len(pageinfo)} static offline preview HTML pages in {OUT}')
