import asyncio, base64, json, subprocess, time, urllib.request
from pathlib import Path
import websockets

root = Path(__file__).resolve().parent
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
        await call('Page.navigate', {'url':(root/'index.html').as_uri()})
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
        print('PASS: all languages, saved selection, English default, contact links, NDA, reduced motion.',flush=True)
        await call('Browser.close')

try:
    asyncio.run(main())
finally:
    try: proc.wait(timeout=5)
    except subprocess.TimeoutExpired: proc.terminate()
