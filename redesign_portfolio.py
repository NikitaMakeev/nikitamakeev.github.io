from pathlib import Path
import base64, html, json, re

source = Path('D:/PortfolioSite/index.html').read_text(encoding='utf-8')
Path('index.before-redesign.html').write_text(source,encoding='utf-8')
s=source
old_dictionary=s.split('const translations = ',1)[1].split(';\n      const buttons',1)[0]
d=json.loads(old_dictionary)
def t(key,en,et,ru):
    for lang,value in zip(('en','et','ru'),(en,et,ru)): d[lang][key]=value
    return f'<span data-i18n="{key}">{html.escape(en)}</span>'
def icon(name):
    svg=Path('brand-icons',name+'.svg').read_text(encoding='utf-8')
    svg=re.sub(r'<title>.*?</title>','',svg)
    return svg.replace('<svg ', '<svg aria-hidden="true" focusable="false" width="20" height="20" fill="currentColor" ',1)
github=re.search(r'<a id="hero-github".*?(<svg.*?</svg>)',s,re.S)[1]
calendar='<svg aria-hidden="true" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.7"><rect x="3" y="5" width="18" height="16" rx="3"/><path d="M7 3v4m10-4v4M3 11h18m-13 5h3m3 0h3"/></svg>'
photo='data:image/png;base64,'+base64.b64encode(Path('portfolioFacePhoto.png').read_bytes()).decode()
t('portraitAlt','Portrait of Nikita Makeev','Nikita Makeevi portree','Портрет Никиты Макеева')
hero=f'''
    <section aria-labelledby="hero-title" class="hero-shell mx-auto max-w-6xl px-5 pt-4 pb-9 md:px-8 md:pt-10 md:pb-14">
      <div class="hero-layout">
        <div class="portrait-card hero-enter">
          <img src="{photo}" width="1122" height="1402" alt="Portrait of Nikita Makeev" data-i18n-alt="portraitAlt" fetchpriority="high" decoding="async" class="portrait-photo">
          <div class="portrait-caption" aria-hidden="true"><span>Nikita Makeev</span><span>Full-Stack · AI</span></div>
        </div>
        <div class="hero-identity">
          <p class="availability"><span class="status-dot" aria-hidden="true"></span>{t('available','Available for projects','Avatud uutele projektidele','Открыт к новым проектам')}</p>
          <p class="identity-name">Nikita Makeev</p>
          <p class="identity-detail">{t('identity','Full-Stack developer · Estonia','Täispinu arendaja · Eesti','Full-Stack разработчик · Эстония')}</p>
        </div>
        <div class="hero-copy hero-enter hero-delay">
          <h1 id="hero-title">{t('heroOne','Automate the busywork.','Automatiseeri rutiin.','Автоматизирую рутину.')}<br><span class="hero-accent">{t('heroTwo','Stop losing leads.','Hoia iga kliendipäringut.','Сохраняю ваши лиды.')}</span></h1>
          <p class="hero-subtitle">{t('heroSub','AI workflows and clean code, built around your business.','Sinu ettevõttele loodud tehisintellekti töövood ja puhas kood.','ИИ и чистый код для процессов вашего бизнеса.')}</p>
          <ul class="hero-points">
            <li>{t('benefitOne','Capture enquiries in one CRM.','Kõik kliendipäringud ühes CRM-is.','Собираю заявки в единой CRM.')}</li>
            <li>{t('benefitTwo','Connect your tools. Cut manual tasks.','Ühenda tööriistad. Vähenda käsitööd.','Связываю сервисы. Убираю ручную работу.')}</li>
            <li>{t('benefitThree','Build, integrate and launch your web app.','Veebirakenduse arendus, integratsioonid ja käivitus.','Разрабатываю и запускаю веб-приложения.')}</li>
          </ul>
        </div>
        <div class="hero-actions">
          <div id="hero-contacts" class="contact-grid">
            <a href="#contact" data-booking-link class="contact-button primary-cta">{calendar}{t('mainCta','Discuss your project','Arutame sinu projekti','Обсудить проект')}</a>
            <a id="hero-github" href="https://github.com/NikitaMakeev" target="_blank" rel="noopener noreferrer" data-i18n-aria="github" aria-label="GitHub profile — opens in a new tab" class="contact-button github-button">{github}<span>GitHub</span></a>
          </div>
          <div class="hero-links">
            <a href="tel:+37256816367" class="contact-button" data-i18n-aria="call" aria-label="Call +372 5681 6367"><span data-i18n="phone">Phone</span></a>
            <a href="https://www.linkedin.com/in/nikita-makeev-b89400331" target="_blank" rel="noopener noreferrer" data-i18n-aria="linkedin" aria-label="LinkedIn — opens in a new tab" class="contact-button">LinkedIn</a>
            <a href="#contact" class="contact-button">Email</a>
          </div>
        </div>
      </div>
      <div class="proof-strip">
        <p><strong>4</strong>{t('proofSites','client websites delivered','valminud kliendiveebi','клиентских сайта')}</p>
        <p><strong>{t('proofLaunchWord','Live','Käivitatud','Запуск')}</strong>{t('proofLaunch','esports platform launched','e-spordiplatvorm','киберспортивной платформы')}</p>
        <p><strong>Go + Flutter</strong>{t('proofPhoto','photo app built end to end','terviklik fotorakendus','фотоприложение с нуля')}</p>
      </div>
    </section>
'''
s=re.sub(r'    <section aria-labelledby="hero-title".*?</section>',lambda _:hero,s,count=1,flags=re.S)

# Blue is the single brand accent; green is reserved for availability.
palette={'#f6f7f2':'#f6f8fc','#183c32':'#122044','#d6f275':'#dfe9ff','#577b2d':'#2458e8','#526257':'#52607a','#5b6b60':'#52607a','#536556':'#52607a','#65765f':'#47659c','#637a54':'#2458e8','#294c3c':'#172b50','#64735f':'#52607a','#6b7a63':'#52607a','#dce2d6':'#dfe5f0','#d4dccf':'#d5deee','#e5e9e0':'#e5eaf4','#eff4e8':'#edf3ff','#e0ebd3':'#dfe9ff','#c1d0ba':'#b9cbee','#c7d4ca':'#c2cfe8','#597567':'#536a92','#bad477':'#bdcffa','#e3fa9e':'#e8efff','#3d5146':'#354561','#2b5144':'#204aba','#eaf0e3':'#edf3ff','#a9bd93':'#a6bcec'}
for a,b in palette.items(): s=s.replace(a,b)

# The diagrams show only the publicly described high-level components.
def diagram(number,nodes,caption,aria,variant):
    body=''
    for i,(label,sub) in enumerate(nodes):
        if i: body+='<span class="flow-arrow" aria-hidden="true"><span></span></span>'
        body+=f'<div class="flow-node"><span class="node-glyph" aria-hidden="true">'+(['◫','⌘','▤'][i])+f'</span><strong>{label}</strong><small>{sub}</small></div>'
    return f'''<figure class="case-diagram {variant}" data-i18n-aria="{aria}" aria-label="{d['en'][aria]}">
      <div class="diagram-topline"><span>{t('simplified','SIMPLIFIED ARCHITECTURE','LIHTSUSTATUD ARHITEKTUUR','УПРОЩЁННАЯ АРХИТЕКТУРА')}</span><span>0{number}</span></div>
      <div class="flow illustration">{body}</div>
      <figcaption>{caption}</figcaption>
    </figure>'''
diagrams=[
 diagram(1,[(t('browser','Web app','Veebirakendus','Веб-интерфейс'),t('participants','Tournaments','Turniirid','Турниры')),(t('services','Backend','Server','Сервер'),t('businessLogic','Business logic','Äriloogika','Бизнес-логика')),(t('database','Database','Andmebaas','База данных'),t('platformData','Platform data','Platvormi andmed','Данные платформы'))],t('conceptTournament','Interface → services → data','Liides → teenused → andmed','Интерфейс → сервисы → данные'),'figureTournament','diagram-blue'),
 diagram(2,[('Flutter',t('interface','Interface','Kasutajaliides','Интерфейс')),('Go API',t('backend','Backend','Serveripool','Серверная часть')),(t('photos','Photos','Fotod','Фото'),t('storage','Storage','Salvestus','Хранение'))],t('conceptPhotos','A connected frontend and backend','Ühendatud kasutajaliides ja server','Связанные интерфейс и сервер'),'figurePhotos','diagram-light'),
 diagram(3,[(t('website','Website','Veebileht','Сайт'),t('enquiries','Enquiries','Päringud','Заявки')),('Bitrix CRM',t('leadTracking','Lead tracking','Päringute haldus','Учёт лидов')),(t('team','Team','Meeskond','Команда'),t('followUp','Follow-up','Järeltegevused','Обработка'))],t('conceptCRM','One place to manage enquiries','Üks koht päringute haldamiseks','Единая система для работы с заявками'),'figureCRM','diagram-blue')
]
di=iter(diagrams)
s=re.sub(r'<figure\b.*?</figure>',lambda _:next(di),s,flags=re.S)
s=s.replace('<article class="reveal ','<article class="reveal case-card shadow-sm hover:shadow-md ')

for key,en,et,ru in [
 ('workTitle','Built. Connected. Launched.','Arendatud. Ühendatud. Käivitatud.','Разработано. Связано. Запущено.'),
 ('nda','A look inside the work. Simplified diagrams, no client data. Source code stays confidential under NDA.','Pilk tehtud tööle. Lihtsustatud skeemid ilma kliendiandmeteta. Lähtekood on konfidentsiaalsuslepingu alusel kaitstud.','Что стоит за проектами: упрощённые схемы без клиентских данных. Исходный код защищён NDA.'),
 ('tournamentWork','Designed the architecture. Connected frontend, backend and database. Deployed and maintained the platform.','Kavandasin arhitektuuri. Ühendasin liidese, serveri ja andmebaasi. Käivitasin ja hooldasin platvormi.','Спроектировал архитектуру. Связал интерфейс, сервер и базу данных. Запустил и поддерживал платформу.'),
 ('photoWork','Built the Go backend and Flutter frontend independently. Delivered one complete application.','Arendasin iseseisvalt Go serveripoole ja Flutteri liidese. Ühendasin need terviklikuks rakenduseks.','Самостоятельно разработал сервер на Go и интерфейс на Flutter. Объединил их в готовое приложение.'),
 ('crmWork','Set up lead tracking in Bitrix CRM. Brought incoming enquiries into one workflow.','Seadistasin päringute jälgimise Bitrix CRM-is. Koondasin saabuvad pöördumised ühte töövoogu.','Настроил учёт лидов в Bitrix CRM. Объединил входящие обращения в единый процесс.'),
 ('toolsTitle','A practical stack. No black boxes.','Praktilised tehnoloogiad. Läbipaistvad lahendused.','Рабочие технологии. Понятные решения.'),
 ('aiText','LLM APIs, document processing and CRM workflows.','LLM-i API-d, dokumenditöötlus ja CRM-i töövood.','API языковых моделей, обработка документов и процессы CRM.'),
 ('devText','Interfaces, backend services, databases and deployment.','Kasutajaliidesed, serveriteenused, andmebaasid ja juurutamine.','Интерфейсы, серверные сервисы, базы данных и запуск.'),
]: t(key,en,et,ru)

# Short evidence lines are supported by the CV; no invented performance claims.
evidence=[t('evidenceTournament','2024 · Production launch','2024 · Platvormi käivitus','2024 · Запуск в продакшен'),t('evidencePhotos','Go + Flutter · End-to-end delivery','Go + Flutter · Terviklik teostus','Go + Flutter · Полный цикл разработки'),t('evidenceCRM','2022–2023 · CRM integration','2022–2023 · CRM-i integratsioon','2022–2023 · Интеграция CRM')]
index=0
def insert_evidence(m):
    global index
    result=m[0]+'<p class="case-evidence"><span aria-hidden="true">✓</span>'+evidence[index]+'</p>'
    index+=1
    return result
s=re.sub(r'<h3\b[^>]*><span data-i18n="(?:tournamentTitle|photosTitle|crmTitle)">.*?</h3>',insert_evidence,s)
# Turn implementation details into scannable bullets for each project.
for key in ['tournamentWork','photoWork','crmWork']:
    bullets={
      'tournamentWork': [('tournamentBullet1','Architecture and full-stack integration.','Arhitektuur ja täispinu integratsioon.','Архитектура и интеграция всех компонентов.'),('tournamentBullet2','Production deployment and maintenance.','Kasutuselevõtt ja hooldus.','Запуск и поддержка в продакшене.')],
      'photoWork':[('photoBullet1','Go backend and Flutter frontend.','Go serveripool ja Flutteri liides.','Сервер на Go и интерфейс на Flutter.'),('photoBullet2','Independent end-to-end implementation.','Iseseisev terviklik teostus.','Самостоятельная разработка полного цикла.')],
      'crmWork':[('crmBullet1','Configured Bitrix CRM lead tracking.','Bitrix CRM-i päringute jälgimise seadistus.','Настройка учёта лидов в Bitrix CRM.'),('crmBullet2','One workflow for incoming enquiries.','Ühtne töövoog saabuvatele päringutele.','Единый процесс для входящих обращений.')]
    }[key]
    new='<ul class="case-bullets">'+''.join('<li>'+t(*b)+'</li>' for b in bullets)+'</ul>'
    s=re.sub(r'<p[^>]*><strong[^>]*><span data-i18n="contribution">.*?</strong> <span data-i18n="'+key+r'">.*?</span></p>',lambda _:new,s)

for name,slug in [('React','react'),('Node.js','nodedotjs'),('Go','go'),('TypeScript','typescript'),('Vue','vuedotjs'),('Flutter','flutter'),('PostgreSQL','postgresql'),('MariaDB','mariadb'),('Tailwind CSS','tailwindcss')]:
    s=s.replace('<li class="tag">'+name+'</li>','<li class="tag tech-tag">'+icon(slug)+'<span>'+name+'</span></li>')

footer=f'''
  <footer id="contact" class="contact-section">
    <div class="mx-auto max-w-6xl px-5 pt-10 pb-5 md:px-8 md:pt-14">
      <div class="contact-layout reveal">
        <div>
          <p class="section-kicker">{t('contactLabel','03 / Your next step','03 / Sinu järgmine samm','03 / Следующий шаг')}</p>
          <h2>{t('footerOne','What is slowing','Mis pidurdab','Что замедляет')}<br><span>{t('footerTwo','your business down?','sinu ettevõtet?','ваш бизнес?')}</span></h2>
          <p class="contact-intro">{t('contactText','Tell me where leads get lost or work gets repetitive. Let’s find a useful first step.','Räägi, kus päringud kaotsi lähevad või töö kordub. Leiame koos praktilise esimese sammu.','Расскажите, где теряются заявки или повторяется ручная работа. Определим первый полезный шаг.')}</p>
          <ul class="contact-checklist">
            <li>{t('callTopic1','Your current workflow','Sinu praegune tööprotsess','Ваш текущий процесс')}</li>
            <li>{t('callTopic2','The bottleneck worth fixing first','Esimene kitsaskoht, mida lahendada','Проблема, которую стоит решить первой')}</li>
            <li>{t('callTopic3','A clear scope for the next step','Järgmise sammu selge ulatus','Понятный объём следующего шага')}</li>
          </ul>
        </div>
        <div class="contact-panel">
          <div id="booking-slot" hidden></div>
          <h3>{t('contactPanelTitle','Let’s talk about your project','Räägime sinu projektist','Обсудим ваш проект')}</h3>
          <p class="contact-panel-note">{t('browserEmailNote','Use Gmail in your browser, or copy my email address.','Ava Gmail brauseris või kopeeri minu e-posti aadress.','Откройте Gmail в браузере или скопируйте мой адрес.')}</p>
          <a href="https://mail.google.com/mail/?view=cm&amp;fs=1&amp;to=nikita.makeev.dev%40gmail.com" target="_blank" rel="noopener noreferrer" id="browser-email" class="primary-cta contact-button">{t('browserEmail','Write in Gmail','Kirjuta Gmailis','Написать в Gmail')}</a>
          <div class="email-copy-row"><span>nikita.makeev.dev@gmail.com</span><button id="copy-email" type="button" hidden>{t('copyEmail','Copy','Kopeeri','Копировать')}</button></div>
          <p id="copy-status" role="status" aria-live="polite" class="copy-status"></p>
          <div class="contact-other-links">
            <a href="tel:+37256816367" class="contact-button">+372 5681 6367</a>
            <a href="https://www.linkedin.com/in/nikita-makeev-b89400331" target="_blank" rel="noopener noreferrer" data-i18n-aria="linkedin" aria-label="LinkedIn — opens in a new tab" class="contact-button">LinkedIn</a>
            <a href="https://github.com/NikitaMakeev" target="_blank" rel="noopener noreferrer" data-i18n-aria="github" aria-label="GitHub profile — opens in a new tab" class="contact-button footer-github">{github}GitHub</a>
          </div>
        </div>
      </div>
      <div class="mt-10 flex flex-wrap justify-between gap-2 border-t border-white/15 pt-5 text-xs text-[#b9cbee]"><p>© 2026 Nikita Makeev</p><p data-i18n="footerLocation">Based in Estonia · Working remotely</p></div>
    </div>
  </footer>
'''
s=re.sub(r'  <footer\b.*?</footer>',lambda _:footer,s,flags=re.S)
t('copySuccess','Email address copied.','E-posti aadress kopeeritud.','Адрес скопирован.')
t('copyFailure','Please select and copy the email address above.','Palun vali ja kopeeri ülal olev e-posti aadress.','Выделите и скопируйте адрес выше.')
t('bookCall','Book a 15-minute call','Broneeri 15-minutiline kõne','Забронировать звонок на 15 минут')

css='''
    /* Brand layer: a blue accent, white case cards, and a human first screen. */
    :root { --accent: #2458e8; --ink: #122044; --muted: #52607a; }
    body { background: #f6f8fc; color: var(--ink); }
    .hero-layout { display: grid; grid-template-columns: 70px minmax(0,1fr); gap: 16px 14px; }
    .portrait-card { width: 70px; height: 78px; border-radius: 18px; overflow: hidden; background: #e2e9fa; box-shadow: 0 0 0 4px white, 0 0 0 5px #dce5f6; }
    .portrait-photo { width: 100%; height: 100%; object-fit: cover; object-position: 50% 38%; }
    .portrait-caption { display: none; }
    .hero-identity { align-self: center; min-width: 0; }
    .availability { display: flex; align-items: center; gap: 8px; font-size: 11px; font-weight: 600; color: #26734b; }
    .status-dot { position: relative; flex: 0 0 7px; width: 7px; height: 7px; background: #2b9e61; border-radius: 50%; }
    .status-dot::after { content: ''; position: absolute; inset: -4px; border: 1px solid #2b9e6170; border-radius: 50%; animation: status-pulse 2.4s ease-out infinite; }
    @keyframes status-pulse { 0% { transform: scale(.6); opacity: .8; } 80%,100% { transform: scale(1.5); opacity: 0; } }
    .identity-name { margin-top: 5px; font-size: 18px; font-weight: 650; letter-spacing: -.03em; }
    .identity-detail { margin-top: 2px; font-size: 11px; color: var(--muted); }
    .hero-copy,.hero-actions { grid-column: 1/-1; min-width: 0; }
    .hero-copy h1 { font-size: clamp(1.85rem,8vw,2.8rem); line-height: 1.07; letter-spacing: -.055em; font-weight: 650; overflow-wrap: anywhere; }
    .hero-accent { color: var(--accent); }
    .hero-subtitle { margin-top: 12px; font-size: 14px; line-height: 1.6; color: var(--muted); max-width: 34rem; }
    .hero-points { display: grid; gap: 5px; margin-top: 12px; font-size: 13px; color: #354561; line-height: 1.5; }
    .hero-points li,.case-bullets li { position: relative; padding-left: 19px; }
    .hero-points li::before,.case-bullets li::before { content: '✓'; color: var(--accent); position: absolute; left: 0; font-weight: 600; }
    .contact-grid { display: grid; grid-template-columns: minmax(0,1fr) auto; gap: 8px; }
    .primary-cta { display: flex; align-items: center; justify-content: center; gap: 9px; min-height: 52px; border-radius: 12px; padding: 12px 15px; background: var(--accent); color: #fff; font-size: 14px; font-weight: 650; line-height: 1.3; text-align: center; box-shadow: 0 5px 14px #2458e81c; }
    .primary-cta svg { flex-shrink: 0; }
    .github-button { display: flex; align-items: center; justify-content: center; gap: 7px; min-height: 52px; padding: 12px 15px; border: 1px solid #bed0fa; border-radius: 12px; background: #e3ecff; color: #1f438f; font-size: 13px; font-weight: 650; }
    .hero-links { display: flex; justify-content: flex-start; gap: 24px; font-size: 12px; color: #415b88; }
    .hero-links a { display: flex; align-items: center; min-height: 44px; }
    .proof-strip { display: grid; grid-template-columns: repeat(3,minmax(0,1fr)); gap: 12px; margin-top: 24px; border-top: 1px solid #dfe5f0; padding-top: 20px; }
    .proof-strip p { display: flex; flex-direction: column; gap: 5px; font-size: 11px; line-height: 1.4; color: #52607a; }
    .proof-strip strong { font-size: 15px; font-weight: 650; color: #122044; }
    .case-card { box-shadow: 0 3px 14px #21396108; }
    .case-diagram { aspect-ratio: 16/9; position: relative; display: flex; flex-direction: column; justify-content: space-between; padding: 14px 12px; overflow: hidden; background-image: radial-gradient(#8fabf326 1px,transparent 1px); background-size: 14px 14px; }
    .diagram-blue { color: #eaf0ff; background-color: #153b87; }
    .diagram-light { color: #203c74; background-color: #eaf0ff; }
    .diagram-topline { display: flex; justify-content: space-between; align-items: center; gap: 5px; font-size: 8px; letter-spacing: .09em; }
    .flow { display: flex; align-items: center; width: 100%; }
    .flow-node { display: flex; flex: 1; min-width: 0; flex-direction: column; align-items: center; justify-content: center; gap: 3px; min-height: 75px; padding: 7px 3px; border: 1px solid #99b7f57a; border-radius: 9px; background: #ffffff0e; text-align: center; }
    .diagram-light .flow-node { background: #ffffffc9; border-color: #c7d5f2; }
    .node-glyph { display: grid; place-items: center; width: 23px; height: 23px; margin-bottom: 3px; border-radius: 6px; background: #ffffff15; font-size: 18px; }
    .flow-node strong { font-size: 10px; line-height: 1.2; font-weight: 650; }
    .flow-node small { font-size: 8px; line-height: 1.2; opacity: .9; }
    .flow-arrow { width: 17px; height: 1px; position: relative; background: #82a5f1; }
    .flow-arrow::after { content: ''; position: absolute; right: 0; top: -2px; width: 5px; height: 5px; border-top: 1px solid #82a5f1; border-right: 1px solid #82a5f1; transform: rotate(45deg); }
    .flow-arrow span { position: absolute; left: 0; top: -2px; width: 4px; height: 4px; background: #fff; border-radius: 50%; animation: data-flow 2.6s ease-in-out infinite; animation-play-state: paused; }
    .diagram-light .flow-arrow span { background: #2458e8; }
    .in-view .flow-arrow span { animation-play-state: running; }
    @keyframes data-flow { 0% { translate: 0 0; opacity: 0; } 20% { opacity: 1; } 80% { opacity: 1; } 100% { translate: 14px 0; opacity: 0; } }
    .case-diagram figcaption { margin-top: 8px; font-size: 8px; line-height: 1.3; letter-spacing: .025em; }
    .case-evidence { display: flex; align-items: center; gap: 6px; margin-top: 12px; font-size: 11px; font-weight: 600; color: #2458e8; }
    .case-bullets { display: grid; gap: 8px; margin-top: 15px; font-size: 13px; line-height: 1.65; color: #52607a; }
    .tag { display: inline-flex; align-items: center; gap: 8px; min-height: 40px; background: #fff; color: #354561; border-color: #dfe5f0; }
    .tech-tag svg { width: 18px; height: 18px; color: #2458e8; flex-shrink: 0; }
    .contact-section { background: #102655; color: #fff; }
    .contact-layout { display: grid; gap: 28px; }
    .section-kicker { font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: .14em; color: #b4c9f0; margin-bottom: 16px; }
    .contact-layout h2 { font-size: 32px; line-height: 1.12; font-weight: 650; letter-spacing: -.04em; }
    .contact-layout h2>span:last-child { color: #a4beff; }
    .contact-intro { margin-top: 18px; max-width: 30rem; color: #c5d4ee; font-size: 14px; line-height: 1.75; }
    .contact-checklist { display: grid; gap: 12px; margin-top: 24px; font-size: 13px; color: #d5e1f6; }
    .contact-checklist li::before { content: '✓'; margin-right: 10px; color: #9ab9ff; }
    .contact-panel { background: #fff; color: #122044; padding: 22px; border-radius: 20px; border: 1px solid #dfe5f0; box-shadow: 0 16px 50px #07173726; min-width: 0; }
    .contact-panel h3 { font-size: 20px; line-height: 1.3; font-weight: 650; letter-spacing: -.03em; }
    .contact-panel-note { margin: 12px 0 20px; font-size: 13px; line-height: 1.6; color: #52607a; }
    .email-copy-row { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 5px; margin-top: 12px; font-size: 12px; }
    .email-copy-row>span { overflow-wrap: anywhere; user-select: all; }
    #copy-email { min-height: 44px; font-size: 12px; font-weight: 600; color: #2458e8; cursor: pointer; }
    .copy-status { min-height: 19px; font-size: 11px; color: #52607a; }
    .contact-other-links { display: flex; flex-wrap: wrap; gap: 0 17px; margin-top: 8px; border-top: 1px solid #e5eaf4; padding-top: 9px; }
    .contact-other-links a { min-height: 44px; display: inline-flex; align-items: center; gap: 6px; font-size: 12px; color: #354561; }
    .footer-github { font-weight: 650; }
    #booking-slot:not([hidden]) { margin-bottom: 20px; border-bottom: 1px solid #e5eaf4; padding-bottom: 20px; }
    #contact a:focus-visible,#contact button:focus-visible { outline-color: #82a9ff; }
    @media (min-width: 768px) {
      .hero-layout { grid-template-columns: 1.4fr 1fr; gap: 20px 52px; align-items: start; }
      .portrait-card { grid-column: 2; grid-row: 1/4; width: 100%; height: auto; aspect-ratio: 4/5; border-radius: 28px; align-self: center; position: relative; }
      .portrait-photo { object-position: center; }
      .portrait-caption { display: flex; flex-direction: column; position: absolute; bottom: 16px; left: 16px; right: 16px; padding: 13px 17px; border-radius: 14px; background: #ffffffec; backdrop-filter: blur(8px); }
      .portrait-caption span:first-child { font-size: 16px; font-weight: 650; }
      .portrait-caption span:last-child { font-size: 11px; color: #52607a; }
      .hero-identity { grid-column: 1; grid-row: 1; }
      .identity-name { display: none; }
      .identity-detail { margin-top: 8px; font-size: 12px; }
      .availability { font-size: 12px; }
      .hero-copy { grid-column: 1; grid-row: 2; }
      .hero-copy h1 { font-size: clamp(2.3rem,4.4vw,3.8rem); }
      .hero-subtitle { font-size: 16px; margin-top: 17px; }
      .hero-points { font-size: 14px; gap: 8px; margin-top: 20px; }
      .hero-actions { grid-column: 1; grid-row: 3; }
      .primary-cta,.github-button { font-size: 14px; }
      .hero-links { font-size: 13px; }
      .proof-strip { margin-top: 36px; padding-top: 24px; }
      .proof-strip p { flex-direction: row; align-items: center; gap: 12px; font-size: 12px; }
      .proof-strip strong { font-size: 20px; }
      .case-diagram { padding: 18px 16px; }
      .diagram-topline { font-size: 9px; }
      .flow-node { min-height: 84px; }
      .flow-node strong { font-size: 11px; }
      .case-diagram figcaption { font-size: 9px; }
      .contact-layout { grid-template-columns: 1fr 1fr; gap: 60px; align-items: center; }
      .contact-layout h2 { font-size: 42px; }
      .contact-panel { padding: 28px; }
    }
    @media (hover: hover) {
      .primary-cta:hover { background: #1b46c5; box-shadow: 0 9px 24px #2458e838; }
      .github-button:hover { background: #d8e5ff; box-shadow: 0 8px 20px #2458e812; }
      .hero-links a:hover { color: #2458e8; box-shadow: none; }
      .project-track article:hover { box-shadow: 0 12px 30px #2458e814; }
    }
    @media (prefers-reduced-motion: reduce) { .status-dot::after,.flow-arrow span { animation: none !important; } }
'''
s=s.replace('  </style>',css+'  </style>',1)

# Replace fallback English text as well, so the page remains readable without JS.
for key,value in d['en'].items():
    s=re.sub(r'(<span data-i18n="'+re.escape(key)+r'">)[^<]*(</span>)',lambda m:m[1]+html.escape(value)+m[2],s)
s=s.replace(old_dictionary,json.dumps(d,ensure_ascii=False,indent=2))
s=s.replace("document.documentElement.lang = language;",'''document.querySelectorAll('[data-i18n-alt]').forEach(element => {
          element.alt = copy[element.dataset.i18nAlt] || element.alt;
        });
        document.getElementById('copy-status').textContent = '';
        document.documentElement.lang = language;''')
s=s.replace("document.getElementById('language-switcher').hidden = false;",'''document.getElementById('language-switcher').hidden = false;
      const copyEmail = document.getElementById('copy-email');
      copyEmail.hidden = false;
      copyEmail.addEventListener('click', async () => {
        const status = document.getElementById('copy-status');
        try {
          await navigator.clipboard.writeText('nikita.makeev.dev@gmail.com');
          status.textContent = translations[currentLanguage].copySuccess;
        } catch {
          status.textContent = translations[currentLanguage].copyFailure;
        }
      });
      // Set only to the owner's verified scheduling page. Empty keeps the project-contact CTA.
      const bookingUrl = '';
      if (bookingUrl && /^https:\\/\\//.test(bookingUrl)) {
        document.querySelectorAll('[data-booking-link]').forEach(link => {
          link.href = bookingUrl;
          link.target = '_blank';
          link.rel = 'noopener noreferrer';
          link.querySelector('[data-i18n]').dataset.i18n = 'bookCall';
        });
        const slot = document.getElementById('booking-slot');
        const link = document.createElement('a');
        link.href = bookingUrl;
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
        link.className = 'primary-cta contact-button';
        link.dataset.i18n = 'bookCall';
        slot.append(link);
        slot.hidden = false;
        setLanguage(currentLanguage);
      }''')
Path('index.html').write_text(s,encoding='utf-8')
print('Redesigned HTML with embedded portrait and SVG icons:',len(s),'characters')
