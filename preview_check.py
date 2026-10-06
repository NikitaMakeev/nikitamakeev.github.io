import asyncio, base64, json, subprocess, time, urllib.request, os, tempfile
from pathlib import Path
import websockets

root = Path(__file__).resolve().parent
temporary_data=tempfile.TemporaryDirectory(prefix='browser-form-test-',dir=root)
server_env=os.environ.copy();server_env.update(PORT='3020',HOST='127.0.0.1',DATA_DIR=temporary_data.name)
form_server=subprocess.Popen(['node',str(root/'server.mjs')],env=server_env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,creationflags=0x08000000)
proc = subprocess.Popen([
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless', '--disable-gpu', '--no-first-run', '--no-default-browser-check',
    '--remote-debugging-port=9338', f'--user-data-dir={root / ".qa-profile"}', 'about:blank'
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=0x08000000)

async def main():
    for _ in range(50):
        try:
            tabs=json.load(urllib.request.urlopen('http://127.0.0.1:9338/json'))
            break
        except Exception:
            await asyncio.sleep(.2)
    async with websockets.connect(tabs[0]['webSocketDebuggerUrl'], max_size=10_000_000) as ws:
        seq=0
        async def call(method, params=None):
            nonlocal seq
            seq+=1
            await ws.send(json.dumps({'id':seq,'method':method,'params':params or {}}))
            while True:
                message=json.loads(await asyncio.wait_for(ws.recv(), timeout=30))
                if message.get('id')==seq:
                    if 'error' in message: raise RuntimeError(message)
                    return message.get('result',{})
        await call('Page.enable')
        await call('Page.navigate', {'url':'http://127.0.0.1:3020/'})
        for _ in range(60):
            ready=await call('Runtime.evaluate', {'expression':'document.querySelector("#hero-contacts") && getComputedStyle(document.querySelector("#hero-contacts")).display === "grid"','returnByValue':True})
            if ready['result'].get('value'): break
            await asyncio.sleep(.25)
        else:
            debug=await call('Runtime.evaluate', {'expression':'JSON.stringify({url:location.href,state:document.readyState,body:document.body?.innerText.slice(0,100),sheets:document.styleSheets.length,grid:document.querySelector("#hero-contacts")?.className})','returnByValue':True})
            print(debug,flush=True)
            raise RuntimeError('Tailwind did not load')
        async def evaluate(expression):
            result=await call('Runtime.evaluate', {'expression':expression,'returnByValue':True})
            assert 'exceptionDetails' not in result,result
            return result['result'].get('value')
        # Start with a clean language preference and test the actual button handlers.
        await evaluate("localStorage.removeItem('portfolio-language')")
        for lang in ['en','et','ru']:
            await evaluate(f'document.querySelector(\'[data-lang="{lang}"]\').click()')
            assert await evaluate('document.documentElement.lang')==lang
            assert await evaluate('document.querySelectorAll(\'[aria-pressed="true"]\').length')==1
            assert await evaluate('localStorage.getItem("portfolio-language")')==lang
            assert not await evaluate('[...document.querySelectorAll(".contact-button")].some(e=>e.textContent.includes("↗"))')
            assert not await evaluate('document.querySelector("#projects").innerHTML.includes("github.com")')
            if lang!='ru': assert not await evaluate('/[А-Яа-яЁё]/.test(document.body.innerText)')
            for width,height in [(320,640),(390,844),(768,1024),(1440,1000)]:
                await call('Emulation.setDeviceMetricsOverride', {'width':width,'height':height,'deviceScaleFactor':1,'mobile':True})
                await asyncio.sleep(.35)
                metrics=json.loads(await evaluate('JSON.stringify({width:innerWidth, scrollWidth:document.documentElement.scrollWidth,contactsBottom:document.querySelector("#hero-github").getBoundingClientRect().bottom})'))
                print(lang,width,metrics,flush=True)
                assert metrics['scrollWidth']==width, 'Horizontal overflow'
                if width<768: assert metrics['contactsBottom'] <= height, 'Contacts below fold'
                if width in [390,1440]:
                    shot=await call('Page.captureScreenshot',{'format':'png','captureBeyondViewport':False})
                    (root/f'preview-{lang}-{width}.png').write_bytes(base64.b64decode(shot['data']))
        await call('Page.reload')
        await asyncio.sleep(1)
        assert await evaluate('document.documentElement.lang')=='ru','Language not restored'
        await call('Emulation.setEmulatedMedia', {'features':[{'name':'prefers-reduced-motion','value':'reduce'}]})
        assert await evaluate('getComputedStyle(document.querySelector(".hero-enter")).animationName')=='none'
        assert await evaluate('getComputedStyle(document.querySelector(".illustration")).animationName')=='none'
        await evaluate('localStorage.removeItem("portfolio-language")')
        await call('Page.reload')
        await asyncio.sleep(1)
        assert await evaluate('document.documentElement.lang')=='en','English not default'
        assert await evaluate('document.querySelector(".portrait-photo").naturalWidth')==1122
        assert await evaluate('document.querySelectorAll(".tech-tag svg").length')==9
        assert await evaluate('document.querySelector("#inquiry-submit").disabled') is False
        await evaluate('document.querySelector("#inquiry-name").value="Browser QA";document.querySelector("#inquiry-email").value="qa@example.com";document.querySelector("#inquiry-message").value="Synthetic browser test only, not a real lead.";document.querySelector("#inquiry-submit").click()')
        for _ in range(30):
            if await evaluate('document.querySelector("#form-status").textContent.startsWith("Request received")'):break
            await asyncio.sleep(.2)
        else:raise AssertionError('Form did not report successful save')
        entries=Path(temporary_data.name,'inquiries.ndjson').read_text().splitlines()
        assert len(entries)==1
        assert json.loads(entries[0])['email']=='qa@example.com'
        assert await evaluate('document.querySelector("#inquiry-message").value')==''
        await call('Network.enable')
        await call('Network.setBlockedURLs',{'urls':['*api/inquiries*']})
        await evaluate('document.querySelector("#inquiry-email").value="qa@example.com";document.querySelector("#inquiry-message").value="This text must survive a failed request.";document.querySelector("#inquiry-submit").click()')
        for _ in range(30):
            if await evaluate('document.querySelector("#form-status").dataset.error==="true"'):break
            await asyncio.sleep(.2)
        else:raise AssertionError('Form did not report request failure')
        assert await evaluate('document.querySelector("#inquiry-message").value')=='This text must survive a failed request.'
        assert await evaluate('document.querySelector("#inquiry-submit").disabled') is False
        await call('Network.setBlockedURLs',{'urls':[]})
        await evaluate('document.querySelector("#inquiry-form").reset();document.querySelector("#form-status").textContent=""')
        for width,height in [(390,844),(1440,1000)]:
            await call('Emulation.setDeviceMetricsOverride',{'width':width,'height':height,'deviceScaleFactor':1,'mobile':True})
            for area in ['projects','contact']:
                await evaluate(f'document.getElementById("{area}").scrollIntoView()')
                await asyncio.sleep(.2)
                shot=await call('Page.captureScreenshot',{'format':'png','captureBeyondViewport':False})
                (root/f'preview-{area}-{width}.png').write_bytes(base64.b64decode(shot['data']))
        await call('Page.navigate',{'url':(root/'index.html').as_uri()})
        await asyncio.sleep(1)
        assert await evaluate('document.querySelector("#inquiry-submit").disabled') is True
        assert await evaluate('document.querySelector("#form-offline").hidden') is False
        print('PASS: all languages, portrait, logos, reduced motion, real form save, network failure preserves input, offline HTML fallback.',flush=True)
        await call('Browser.close')

try:
    asyncio.run(main())
finally:
    try: proc.wait(timeout=5)
    except subprocess.TimeoutExpired: proc.terminate()
    form_server.terminate();form_server.wait(timeout=5)
    temporary_data.cleanup()
