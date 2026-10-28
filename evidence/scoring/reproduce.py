import pathlib,json,re,hashlib,math,collections
from fractions import Fraction as F
from value_parser import parse
ROOT=pathlib.Path(__file__).resolve().parent
UNIT_ONLY=r'(?:m|metres|meters|km|kmph|sec|seconds|day|days|year|years|month|months|votes|hrs|hours|min|minutes)?'
NUM=r'(\d+(?:\.\d+)?)'
def scalar(o):
 s=re.sub(r'^[A-E]\)\s*','',o).strip();m=re.fullmatch(r'([+-]?\d+(?:\.\d+)?(?:/\d+)?)\s*([a-zA-Z /.%]*)[.]?',s)
 if not m:raise ValueError('Not a scalar option: '+s)
 return F(m[1]),m[2].strip().lower()
def speeds(q):return [F(n) for n in re.findall(NUM+r'\s*(?:km/hr|km/hour|km/h|kmph)\b',q.lower())]
def pair(q,fields):
 low=q.lower();vs=speeds(low);assert len(vs)==2
 target=re.split(r'\b(?:find|what|calculate)\b',low)[-1]
 assert 'and' in target
 if fields==['downstream','upstream']:
  assert 'downstream and upstream' in target and 'still water' in low.split('find')[0] and 'current' in low.split('find')[0]
  v,c=vs;return v+c,v-c
 assert fields==['still_water','current'] and 'still water' in target and re.search(r'\b(?:stream|current)\b',target)
 return (vs[0]+vs[1])/2,abs(vs[1]-vs[0])/2

def solved(e):
 q=e['example']['question'];low=q.lower();rule=e['formula'];v=speeds(q);t=[F(n) for n in re.findall(NUM+r'\s*(?:seconds?|secs?)\b',low)];lengths=[F(n) for n in re.findall(NUM+r'\s*(?:metres?|meters?|m)\b',low)]
 if rule.startswith('profit_percent='):
  nums=list(map(F,re.findall(r'\d+(?:\.\d+)?',q)));assert len(nums)==2 and 'for $10' in low and 'for $30' in low
  c,s=nums;return (s-c)/c*100
 if rule.startswith('time_seconds'):
  assert len(v)==1 and len(lengths)==2;return sum(lengths)/v[0]*F(18,5)
 if rule.startswith('crossed_length'):
  assert len(v)==len(t)==len(lengths)==1;return v[0]*F(5,18)*t[0]-lengths[0]
 if rule.startswith('stillwater_speed='):
  assert len(v)==2 and 'calculate the speed of a boat in still water' in low
  return sum(v)/2
 if rule.startswith('distinct permutations'):
  word=re.search(r'''word\s*['"“‘](\w+)['"”’]''',low)[1];result=math.factorial(len(word))
  for n in collections.Counter(word).values():result//=math.factorial(n)
  return F(result)
 raise ValueError('Unreviewed rule: '+rule)

def main():
 m=json.loads((ROOT/'manifest.json').read_text(encoding='utf8'))
 for name,h in m['sha256'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h,'Hash mismatch '+name
 rows=json.loads((ROOT/'findings.json').read_text(encoding='utf8'));prior={tuple(x) for x in json.loads((ROOT/'prior_record_ids.json').read_text())};selected={(e['file'],e['line']):e['record'] for e in map(json.loads,(ROOT/'selected_source_records.jsonl').read_text(encoding='utf8').splitlines())};seen=set();counts=collections.Counter();letter_controls=0
 for e in rows:
  rid=e['file'],e['line'];assert rid not in prior and rid not in seen;seen.add(rid);r=e['example'];assert r==selected[rid]
  assert hashlib.sha256(json.dumps(r,sort_keys=True,ensure_ascii=False).encode()).hexdigest()==e['record_sha256']
  assert len(r['options'])==5 and r['correct'] in 'ABCDE';key=ord(r['correct'])-65
  assert all(re.match('^'+chr(65+i)+r'\)',o) for i,o in enumerate(r['options']))
  kind=e['issue_type'];counts[kind]+=1
  if kind=='missing_numeric_choices':
   opts=[o[2:].strip() for o in r['options']];assert all(re.fullmatch(UNIT_ONLY,o,re.I) for o in opts);assert any(c.isdigit() for c in r['question']);assert not re.search(r'what (?:is|are) the units|unit of measure',r['question'],re.I)
  elif kind=='identical_keyed_content':
   opts=[o[2:].strip() for o in r['options']];matches=[chr(i+65) for i,o in enumerate(opts) if o==opts[key]];assert matches==e['matching_labels'] and len(matches)>1
   assert not re.search(r'above|below|both|neither|option|statement|none|all of',opts[key],re.I)
   # Illustrative single-letter scoring control; not a published model evaluation.
   alternative=next(x for x in matches if x!=r['correct']);assert int(r['correct']==r['correct'])==1 and int(alternative==r['correct'])==0;letter_controls+=1
  elif kind=='equivalent_keyed_value':
   vals=[parse(o) for o in r['options']];assert vals[key] is not None;matches=[chr(i+65) for i,v in enumerate(vals) if v==vals[key]];assert matches==e['matching_labels'] and len(matches)>1
   assert vals[key][0]==F(e['value_exact']) and vals[key][1]==e['unit']
   assert not re.search(r'simplest|lowest terms|reduced form|decimal form|decimal notation|scientific notation',r['question'],re.I)
  elif kind=='missing_requested_pair':
   a,b=pair(r['question'],e['pair_fields']);assert a>0 and b>0 and a!=b;assert [str(a),str(b)]==e['expected_pair'];opts=[scalar(o) for o in r['options']];assert len({u for v,u in opts})==1
   assert all(len(re.findall(r'\d+(?:\.\d+)?',o[2:]))==1 for o in r['options'])
  elif kind=='wrong_key_or_missing_option':
   expected=solved(e);assert expected==F(e['expected_exact']) and expected>0;opts=[scalar(o) for o in r['options']];assert len({u for v,u in opts})==1
   assert abs(opts[key][0]/expected-1)>F(1,10);good=[chr(i+65) for i,(v,u) in enumerate(opts) if abs(v/expected-1)<=F(1,100)]
   if e['corrected_label']:assert good==[e['corrected_label']]
   else:assert not good and all(abs(v/expected-1)>F(1,10) for v,u in opts)
  else:raise ValueError(kind)
 assert parse('A)1/2')==parse('C)2/4')
 assert parse('A)27 7/09')==parse('D)27 7/9')==(F(250,9),'')
 assert parse('A)1,2') is None and parse('A)1 2') is None
 assert parse('A)1/2')!=parse('B)1/3')
 assert parse('A)-0 1/2')==(F(-1,2),'')
 assert len(rows)==m['new_affected_records'] and dict(counts)==m['issue_counts']
 assert len({e['example']['question'] for e in rows})==m['new_exact_question_texts']
 assert m['prior_affected_records']+len(rows)==m['cumulative_affected_records']
 result={'status':'PASS','new_affected_records':len(rows),'new_exact_question_texts':m['new_exact_question_texts'],'prior_record_overlap':0,'all_source_record_hashes_verified':len(rows),'evidence_hashes_verified':len(m['sha256']),'issue_counts':dict(counts),'illustrative_letter_scoring_controls':letter_controls,'numeric_parser_controls':6,'cumulative_affected_records':m['cumulative_affected_records'],'limit':'Key-equivalent collisions are confirmed structural conflicts with the one-correct-option contract; actual answer correctness and model-score effects are not inferred for every collision.'}
 (ROOT/'validation.json').write_text(json.dumps(result,indent=2),encoding='utf8');print(json.dumps(result))
if __name__=='__main__':main()
