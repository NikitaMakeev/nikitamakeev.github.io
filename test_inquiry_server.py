from pathlib import Path
import json, os, subprocess, tempfile, time, urllib.request, urllib.error, uuid

root=Path(__file__).resolve().parent
with tempfile.TemporaryDirectory(prefix='portfolio-form-test-',dir=root) as folder:
    env=os.environ.copy();env.update(PORT='3019',DATA_DIR=folder,HOST='127.0.0.1')
    process=subprocess.Popen(['node',str(root/'server.mjs')],env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=0x08000000)
    base='http://127.0.0.1:3019'
    def request(path='/',body=None,origin=None):
        headers={}
        if body is not None:headers['Content-Type']='application/json'
        if origin:headers['Origin']=origin
        r=urllib.request.Request(base+path,data=json.dumps(body).encode() if body is not None else None,headers=headers)
        try:
            with urllib.request.urlopen(r,timeout=5) as response:return response.status,response.read()
        except urllib.error.HTTPError as error:return error.code,error.read()
    try:
        for _ in range(40):
            try:
                if request()[0]==200:break
            except Exception:time.sleep(.1)
        else:raise RuntimeError('Server did not start')
        assert request('/server.mjs')[0]==404
        assert request('/private-data/inquiries.ndjson')[0]==404
        assert request('/api/inquiries')[0]==405
        records=[]
        for lang in ['en','et','ru']:
            body=dict(requestId=str(uuid.uuid4()),name='Form QA',email='test@example.com',message='Synthetic test enquiry, not a real lead.',website='',language=lang)
            code,data=request('/api/inquiries',body,base)
            assert code==201 and json.loads(data)['accepted'] is True
            records.append(body)
        assert request('/api/inquiries',records[0],base)[0]==201
        data=[json.loads(line) for line in Path(folder,'inquiries.ndjson').read_text(encoding='utf-8').splitlines()]
        assert len(data)==3,'Duplicate request written twice'
        assert {x['language'] for x in data}=={'en','et','ru'}
        assert all(x['receivedAt'] for x in data)
        assert request('/api/inquiries',{**records[0],'email':'invalid'},base)[0]==400
        assert request('/api/inquiries',{**records[0],'message':'short'},base)[0]==400
        assert request('/api/inquiries',records[0],'https://unrelated.example')[0]==403
        assert request('/api/inquiries',{**records[0],'message':'x'*30000},base)[0]==413
        for _ in range(4):last=request('/api/inquiries',records[0],base)[0]
        assert last==429
        print('PASS: persisted EN/ET/RU enquiries, duplicate retry, validation, request size, cross-origin rejection, private paths, rate limiting.')
    finally:
        process.terminate();process.wait(timeout=5)
