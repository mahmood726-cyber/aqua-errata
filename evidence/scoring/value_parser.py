import json,pathlib,re,ast,operator,collections
from fractions import Fraction as F
num=r'(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?'
def parse(s):
 s=re.sub(r'^[A-E]\)\s*','',s).strip().replace('\u2212','-')
 m=re.fullmatch(r'([+\-\d., /()]+)\s*([A-Za-z.%]*)',s)
 if not m:return None
 a,unit=m.groups();a=a.strip().strip('()')
 if ',' in a:
  if not re.fullmatch(r'[+-]?\d{1,3}(?:,\d{3})+(?:\.\d+)?',a):return None
  a=a.replace(',','')
 mixed=re.fullmatch(r'([+-]?\d+)\s+(\d+)\s*/\s*(\d+)',a)
 try:
  if mixed:
   whole,num,den=map(int,mixed.groups());v=F(abs(whole))+F(num,den);v=v*(-1 if mixed[1].startswith('-') else 1)
  else:
   if re.search(r'\d\s+\d',a):return None
   v=F(re.sub(r'\s+','',a))
 except (ValueError,ZeroDivisionError):return None
 unit=unit.lower().rstrip('.')
 aliases={'secs':'sec','seconds':'sec','second':'sec','mins':'min','minutes':'min','minute':'min','hours':'hr','hour':'hr','hrs':'hr','metres':'m','meters':'m','meter':'m','metre':'m','kgs':'kg','days':'day','rupees':'rs'}
 unit=aliases.get(unit,unit)
 return v,unit
