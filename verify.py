import argparse, collections, hashlib, json, pathlib, subprocess, sys, urllib.request
ROOT=pathlib.Path(__file__).resolve().parent

def main():
 if not __debug__:raise RuntimeError('Run without Python -O: evidence verifiers require assertions')
 parser=argparse.ArgumentParser();parser.add_argument('--upstream',action='store_true');args=parser.parse_args()
 rows=[json.loads(s) for s in (ROOT/'errata.jsonl').read_text(encoding='utf8').splitlines()];seen=set();counts=collections.Counter()
 for batch in ('initial','scoring'):
  subprocess.run([sys.executable,str(ROOT/'evidence'/batch/'reproduce.py')],check=True,cwd=ROOT)
  findings=json.loads((ROOT/'evidence'/batch/'findings.json').read_text(encoding='utf8'));indexed={e['case_id']:e for e in findings};selected=[e for e in rows if e['batch']==batch]
  assert len(selected)==len(findings)
  for e in selected:
   f=indexed[e['case_id']];identity=(e['file'],e['line']);assert identity not in seen;seen.add(identity)
   assert (e['file'],e['line'],e['source_url'],e['record_sha256'])==(f['file'],f['line'],f['source_url'],f['record_sha256'])
   assert e['issue_type']==f.get('issue_type',f.get('kind'))
   assert e['proposed_label']==f.get('corrected_label',f.get('corrected_letter'))
   assert e['review_status']=='reproduced_audit_finding_author_adjudication_pending'
   counts[e['issue_type']]+=1
 summary=json.loads((ROOT/'summary.json').read_text());assert len(rows)==len(seen)==summary['affected_source_records']==978;assert dict(counts)==summary['category_counts']
 manifest=json.loads((ROOT/'evidence'/'initial'/'manifest.json').read_text())
 if args.upstream:
  cache=ROOT/'source-cache';cache.mkdir(exist_ok=True)
  for filename,meta in manifest['sources'].items():
   p=cache/filename
   if not p.exists():
    url='https://raw.githubusercontent.com/google-deepmind/AQuA/'+manifest['commit']+'/'+filename
    with urllib.request.urlopen(url,timeout=60) as response:data=response.read()
    assert hashlib.sha256(data).hexdigest()==meta['sha256'];p.write_bytes(data)
   data=p.read_bytes();assert hashlib.sha256(data).hexdigest()==meta['sha256']
   assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==meta['git_blob']
   source=[json.loads(s) for s in data.decode('utf8').splitlines()]
   for batch in ('initial','scoring'):
    for e in json.loads((ROOT/'evidence'/batch/'findings.json').read_text(encoding='utf8')):
     if e['file']==filename:assert source[e['line']-1]==e['example']
 print(json.dumps(dict(status='PASS',aqua_records=len(rows),category_counts=dict(counts),fresh_upstream_check=args.upstream)))
if __name__=='__main__':main()
