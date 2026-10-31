#!/usr/bin/env python3
"""GitHub GraphQL -> real commit tracker SVG. Uses stdlib only; never fabricates data."""
from pathlib import Path
from datetime import datetime,date,timedelta,timezone
import json, os, math, html, urllib.request, urllib.error, sys
from xml.etree import ElementTree as ET
ROOT=Path(__file__).resolve().parent.parent
API='https://api.github.com/graphql'
Q='query ($login: String!, $from: DateTime!, $to: DateTime!) {\n user(login: $login) {\n  login\n  contributionsCollection(from:$from,to:$to) {\n   totalCommitContributions\n   contributionCalendar {\n    totalContributions\n    weeks { contributionDays { date contributionCount } }\n   }\n  }\n }\n}'

def load_stats():
    login=os.environ.get('GITHUB_USERNAME','roshan-1205')
    token=os.environ.get('GITHUB_TOKEN')
    if not token:raise RuntimeError('GITHUB_TOKEN is missing')
    now=datetime.now(timezone.utc)
    frm=now-timedelta(days=364)
    payload=json.dumps({'query':Q,'variables':{'login':login,'from':frm.isoformat(),'to':now.isoformat()}}).encode()
    req=urllib.request.Request(API,data=payload,headers={
      'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json',
      'User-Agent':'roshan-akatsuki-readme-tracker','Content-Type':'application/json'})
    with urllib.request.urlopen(req,timeout=30) as response: result=json.load(response)
    if result.get('errors'):raise RuntimeError('GitHub GraphQL '+str(result['errors'])[:700])
    user=(result.get('data') or {}).get('user')
    if not user:raise RuntimeError('No user returned by GitHub GraphQL')
    collection=user['contributionsCollection']; calendar=collection['contributionCalendar']
    days={date.fromisoformat(d['date']):int(d['contributionCount']) for week in calendar['weeks'] for d in week['contributionDays']}
    if not days:raise RuntimeError('No calendar results')
    days={d:c for d,c in days.items() if d<=now.date()}
    active=sum(c>0 for c in days.values())
    current=now.date() if days.get(now.date(),0)>0 else now.date()-timedelta(days=1)
    streak=0
    while days.get(current,0)>0:
      streak+=1
      current-=timedelta(days=1)
    return {
      'login':user['login'],
      'commits':int(collection['totalCommitContributions']),
      'contrib':int(calendar['totalContributions']),
      'active':active,'streak':streak,
      'days':days,'timestamp':now.strftime('%Y-%m-%d %H:%M UTC'),
      'today':now.date(),
    }

def text(x,y,value,size=18,color='#FFF4ED',weight=600,anchor=None):
    a=' text-anchor="'+anchor+'"' if anchor else ''
    return f'<text x="{x}" y="{y}" font-family="Arial,Helvetica,sans-serif" font-size="{size}" font-weight="{weight}" fill="{color}"{a}>{html.escape(str(value))}</text>'

def make_svg(st):
    template=(ROOT/'assets/activity-template.svg').read_text(encoding='utf-8')
    if '<!--DYNAMIC_SLOT-->' not in template:raise RuntimeError('Missing tracker template slot')
    out=[]
    for i,val in enumerate([st['commits'],st['contrib'],st['active'],st['streak']]):
      out.append(text(88+i*295,285,f'{val:,}',39,weight=800))
    # calendar left 88..1005. 53 weeks * 17.0 = 901px
    start=min(st['days']); last=st['today']
    start=start-timedelta(days=(start.weekday()+1)%7)  # Sunday
    total_weeks=math.ceil((last-start).days/7)+1
    if total_weeks>54:total_weeks=54
    x0,y0,dx,dy=90,458,17.1,17.8
    month_last=None
    for w in range(total_weeks):
      first=start+timedelta(days=w*7)
      if w>0 and first.day<=7 and first.month!=month_last and w<total_weeks-2:
        out.append(text(round(x0+w*dx,1),440,first.strftime('%b').upper(),11,'#BFAFBB',600))
        month_last=first.month
      for day_of_week in range(7):
        d=first+timedelta(days=day_of_week)
        if d not in st['days'] or d>last:continue
        count=st['days'][d]
        color=('#2A202A' if count==0 else '#53223A' if count<=2 else '#8E3150' if count<=5 else '#C93C60' if count<=10 else '#FF647E')
        x=round(x0+w*dx,2); y=round(y0+day_of_week*dy,2)
        out.append(f'<rect x="{x}" y="{y}" width="13.5" height="13.5" rx="3" fill="{color}" class="pulse" style="animation-delay:{w*.03:.2f}s"><title>{d.isoformat()}: {count} contributions</title></rect>')
    out.append(text(1038,451,'LAST 7 DAYS',12,'#FF9AAC',700))
    last7=sum(st['days'].get(st['today']-timedelta(days=i),0) for i in range(7))
    out.append(text(1038,493,f'{last7:,}',36,'#FFF4ED',800))
    out.append(text(1038,514,'contributions',12,'#BFAFBB'))
    out.append(text(1038,558,'SYNCED',11,'#FF9AAC',700))
    out.append(text(1038,579,st['timestamp'][:16],10,'#BFAFBB',500))
    svg=template.replace('<!--DYNAMIC_SLOT-->',''.join(out))
    ET.fromstring(svg)
    return svg

def main():
    stats=load_stats()
    svg=make_svg(stats)
    dest=ROOT/'activity-tracker.svg'
    dest.write_text(svg,encoding='utf-8')
    print('Updated activity tracker: '+str(stats['commits'])+' commits; '+str(stats['contrib'])+' contributions; '+str(stats['streak'])+' streak')
if __name__=='__main__':
    try:main()
    except Exception as e:
      print('Tracker update failed; previous art preserved: '+str(e),file=sys.stderr)
      sys.exit(1)
