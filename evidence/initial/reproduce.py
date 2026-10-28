import ast,json,pathlib,re,hashlib,collections,math
from fractions import Fraction as F
from question_rules import rules,parseopt
ROOT=pathlib.Path(__file__).resolve().parent

def arithmetic(s):
 assert re.fullmatch(r'[\d+*()\s-]+',s),s
 def node(n):
  if isinstance(n,ast.Expression):return node(n.body)
  if isinstance(n,ast.Constant) and type(n.value)==int:return F(n.value)
  if isinstance(n,ast.UnaryOp) and isinstance(n.op,(ast.UAdd,ast.USub)):return node(n.operand)*(1 if isinstance(n.op,ast.UAdd) else -1)
  if isinstance(n,ast.BinOp):
   a,b=node(n.left),node(n.right)
   if isinstance(n.op,ast.Add):return a+b
   if isinstance(n.op,ast.Sub):return a-b
   if isinstance(n.op,ast.Mult):return a*b
  raise ValueError('Unsupported arithmetic')
 return node(ast.parse(s,mode='eval'))

def custom(e):
 q=e['example']['question'];line=e['line']
 if line in (5781,42168):
  area=int(re.search(r'area .*? is (\d+)',q).group(1));side=math.isqrt(area//2);assert 2*side*side==area;return F(4*side)
 if line==20947:return F(math.factorial(int(re.search(r'(\d+) people',q).group(1))-1))
 if line==22589:
  assert 'four people' in q and 'five married couples' in q
  return F(math.comb(5,4)*2**4)
 if line==31066:
  nums=[F(n) for n in re.findall(r'\d+',q)];assert nums==[50,2,60]
  return nums[0]*nums[1]/(nums[2]-nums[0]) # minutes
 if line in (43898,45130):return F(sum(math.floor(F(n)) for n in re.findall(r'\[(-?\d+(?:\.\d+)?)\]',q)))
 if line==48454:
  m=re.search(r'there are (\d+).*?Each question has (\d+)',q);return F(int(m[2])**int(m[1])-1)
 if line==52361:
  values=[int(n) for n in re.findall(r'\d+',re.search(r'\{([^}]+)\}',q)[1])];assert values==[1,2,3,4,5]
  total=2**len(values);good=0
  for mask in range(total):
   subset=[n for i,n in enumerate(values) if mask>>i&1]
   good+=bool(subset and max(subset) in (3,4))
  return F(good,total)
 if line==52974:
  lo,hi=map(int,re.search(r'between (\d+) and (\d+)',q).groups());div=int(re.search(r'divisible by (\d+)',q)[1]);return F(sum(n*(n+1)%div==0 for n in range(lo,hi+1)),hi-lo+1)
 raise ValueError('Unreviewed custom case')

def main():
 m=json.loads((ROOT/'manifest.json').read_text(encoding='utf8'))
 for name,h in m['sha256'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h,'Hash mismatch: '+name
 rows=json.loads((ROOT/'findings.json').read_text(encoding='utf8'));seen=set();questions=set();counts=collections.Counter()
 src={(e['file'],e['line']):e['record'] for e in map(json.loads,(ROOT/'selected_source_records.jsonl').read_text(encoding='utf8').splitlines())}
 for e in rows:
  rid=e['file'],e['line'];assert rid not in seen;seen.add(rid);r=e['example'];assert r==src[rid]
  assert hashlib.sha256(json.dumps(r,sort_keys=True,ensure_ascii=False).encode()).hexdigest()==e['record_sha256']
  questions.add(r['question']);counts[e['kind']]+=1
  if e['kind']=='rationale_arithmetic':
   lhs,rhs=e['equation'].split(' = ');a,b=arithmetic(lhs),arithmetic(rhs);assert a==F(e['left_value']) and b==F(e['right_value']) and a!=b
   raw=r['rationale'].splitlines()[e['rationale_line']-1];compact=lambda s:re.sub(r'\s+','',s);assert compact(e['equation']) in compact(raw)
  elif e['kind']=='answer_key':
   vals=[F(v) for v in re.findall(r'\d+(?:\.\d+)?',r['question'])];assert list(map(str,vals))==e['inputs']
   key=re.sub(r'\d+(?:\.\d+)?','#',r['question'].lower());family,fn,_=rules[key];assert family==e['family'];expected=fn(*vals)
   if family=='downstream_time' and e['unit'] in ('min','mins','minutes','minute'):expected*=60
   if family in ('bridge_time','pole_time','platform_time','same_direction_person','opposite_trains') and e['unit'] in ('min','mins','minutes','minute'):expected/=60
   assert expected==F(e['expected_exact'])
   opts=[parseopt(o) for o in r['options']];assert all(o is not None for o in opts)
   actual=opts[ord(r['correct'])-65][0];assert abs(actual/expected-1)>F(1,10)
   good=[i for i,o in enumerate(opts) if abs(o[0]/expected-1)<=F(1,100)]
   if e['corrected_letter']:assert good==[ord(e['corrected_letter'])-65]
   else:assert all(abs(o[0]/expected-1)>F(1,10) for o in opts)
  elif e['kind']=='key_or_conclusion_conflict':
   assert custom(e)==F(e['expected_exact'])
   if e['corrected_letter']:
    opt=r['options'][ord(e['corrected_letter'])-65]
    while re.match(r'^[A-E]\)',opt):opt=opt[2:]
    assert F(opt.strip())==F(e['expected_exact'])
   assert e['rationale_letter']!=e['published_letter']
  else:raise ValueError(e['kind'])
 assert arithmetic('35*56')==1960 and arithmetic('360-323')==37 and arithmetic('(47)+(-27)')==20
 assert arithmetic('3*(1+2+3)')==18 and arithmetic('90+18+15')==123
 assert len(rows)==m['accepted_records'] and len(questions)==m['distinct_question_texts'] and dict(counts)==m['kind_counts']
 result={'status':'PASS','affected_records':len(rows),'distinct_exact_question_texts':len(questions),'record_checks_passed':len(rows),'source_record_hashes_passed':len(rows),'evidence_file_hashes_passed':len(m['sha256']),'kinds':dict(counts),'controls_passed':5,'scope':'Arithmetic cases verify the cited rationale equation only; they do not establish a wrong final answer key.'}
 (ROOT/'validation.json').write_text(json.dumps(result,indent=2),encoding='utf8');print(json.dumps(result))
if __name__=='__main__':main()
