#!/usr/bin/env python3
"""Build a daily opportunity feed from Google News RSS searches.
Search results are discovery leads, not official verification. Original source links are retained.
"""
import json, re, time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from urllib.parse import quote
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data.json'
QUERIES = [
 ('Government Jobs', '(graduate recruitment OR graduate vacancy OR government jobs) India official notification'),
 ('Government Jobs', '(UPSSSC OR UPPSC OR UP government recruitment) vacancy notification'),
 ('Government Jobs', '(SSC OR Railway OR bank recruitment) graduate vacancy notification India'),
 ('BHU Jobs', 'site:bhu.ac.in recruitment vacancy project staff non teaching'),
 ('BHU Jobs', 'Banaras Hindu University recruitment project fellow vacancy'),
 ('MBA & Admissions', '(CAT OR XAT OR CMAT OR SNAP OR NMAT OR MAT) 2027 registration admission'),
 ('MBA & Admissions', 'MBA admission 2027 application form last date India college'),
 ('Scholarships', '(OBC scholarship OR post matric scholarship) 2026 2027 India official'),
 ('Scholarships', '(fellowship OR scholarship) postgraduate India application deadline 2026'),
 ('Science & Environment', '(Zoology OR life science OR environmental science) project assistant research jobs India'),
 ('Science & Environment', '(wildlife OR biodiversity OR ecology) project recruitment India'),
 ('Internships', 'paid internship graduate India government research 2026'),
 ('Results & Exams', '(exam result OR admit card OR exam date) graduate recruitment India 2026'),
]

def clean(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s or '')).strip()

def get_text(node, name):
    x = node.find(name)
    return clean(x.text if x is not None and x.text else '')

def fetch(category, query):
    url = 'https://news.google.com/rss/search?q=' + quote(query) + '&hl=en-IN&gl=IN&ceid=IN:en'
    req = Request(url, headers={'User-Agent':'Mozilla/5.0 (compatible; PersonalOpportunityDesk/1.0)'})
    try:
        with urlopen(req, timeout=20) as response:
            raw = response.read()
        root = ET.fromstring(raw)
    except Exception as exc:
        print('Feed error:', query, exc)
        return []
    results=[]
    for item in root.findall('.//item'):
        title=get_text(item,'title'); link=get_text(item,'link'); source=get_text(item,'source') or 'News feed'
        desc=get_text(item,'description')
        date=get_text(item,'pubDate')
        try: published=parsedate_to_datetime(date).astimezone(timezone.utc).isoformat()
        except Exception: published=''
        if not title or not link: continue
        results.append({'title':title,'link':link,'source':source,'published':published,'summary':desc[:320],'category':category,'query':query})
    return results

def main():
    all_items=[]
    for category, query in QUERIES:
        all_items.extend(fetch(category, query)); time.sleep(0.4)
    # De-duplicate by normalized title and link; keep newest item when possible.
    seen=set(); unique=[]
    for x in sorted(all_items, key=lambda a:a.get('published',''), reverse=True):
        key=re.sub(r'[^a-z0-9]+',' ',x['title'].lower()).strip()
        if key in seen: continue
        seen.add(key); unique.append(x)
    data={'updated_at':datetime.now(timezone.utc).isoformat(),'items':unique[:250],
          'notice':'Items are discovered through news RSS. Verify details at the official recruiting/admissions website before acting.'}
    OUT.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'Wrote {len(data["items"])} items to {OUT}')

if __name__ == '__main__': main()
