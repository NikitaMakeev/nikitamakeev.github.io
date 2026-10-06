from pathlib import Path
import re, json, html

s = Path('D:/PortfolioSite/index.html').read_text(encoding='utf-8')
translations = {k:{} for k in ('en','et','ru')}
def entry(key, en, et, ru):
    for lang,value in zip(('en','et','ru'),(en,et,ru)): translations[lang][key]=value
    return f'<span data-i18n="{key}">{html.escape(en)}</span>'
def text(key, ru, en, et):
    global s
    assert ru in s, key
    replacement=entry(key,en,et,ru)
    s=''.join(part if part.startswith('<') else part.replace(ru,replacement) for part in re.split(r'(<[^>]+>)',s))
def label(key, ru, en, et):
    global s
    entry(key,en,et,ru)
    assert f'aria-label="{ru}"' in s, key
    s=s.replace(f'aria-label="{ru}"',f'data-i18n-aria="{key}" aria-label="{html.escape(en)}"')

s=s.replace('<html lang="ru">','<html lang="en">')
description='Nikita Makeev — Full-Stack разработчик. ИИ-интеграции, автоматизация процессов и веб-приложения, которые помогают бизнесу сохранять клиентов.'
entry('meta','Nikita Makeev — Full-Stack developer. AI integrations, workflow automation and web applications that help businesses retain customers.','Nikita Makeev — täispinu arendaja. Tehisintellekti integratsioonid, tööprotsesside automatiseerimine ja veebirakendused, mis aitavad ettevõtetel kliente hoida.',description)
s=s.replace(f'content="{description}"',f'content="{translations["en"]["meta"]}"')
# Translate leaf text without replacing markup or using innerHTML at runtime.
for row in [
 ('skip','Перейти к содержанию','Skip to content','Liigu sisu juurde'),
 ('projectsNav','Проекты','Projects','Projektid'),
 ('skillsNav','Навыки','Skills','Oskused'),
 ('eyebrow','Разработка для бизнеса','Software for your business','Tarkvara sinu ettevõttele'),
 ('intro','Создаю веб-системы, связываю CRM и внедряю ИИ, чтобы заявки не терялись, а команда работала быстрее.','I build web systems, connect CRMs and integrate AI so leads stay on track and your team works faster.','Loon veebisüsteeme, ühendan CRM-e ja rakendan tehisintellekti, et päringud ei kaoks ning meeskond töötaks kiiremini.'),
 ('start','Начнём с вашей бизнес-задачи','Let’s start with your business challenge','Alustame sinu ettevõtte vajadusest'),
 ('email','Обсудить задачу','Let’s talk','Arutame sinu projekti'),
 ('phone','Телефон','Phone','Telefon'),
 ('location','Эстония · Удалённо','Estonia · Remote','Eesti · Kaugtöö'),
 ('workLabel','01 / Избранные работы','01 / Selected work','01 / Valitud tööd'),
 ('workTitle','От задачи до работающей системы.','From a challenge to a working system.','Vajadusest toimiva süsteemini.'),
 ('nda','Исходный код защищён NDA. Здесь — описание моей работы и ссылки только на публичные сайты. Иллюстрации — условные макеты, без данных клиентов.','Source code is protected by NDA. Here you’ll find my contributions and public websites only. Visuals are illustrative mockups with no client data.','Lähtekood on kaitstud konfidentsiaalsuslepinguga. Siin on minu töö kirjeldused ja lingid avalikele veebilehtedele. Visuaalid on näidismaketid ega sisalda kliendiandmeid.'),
 ('swipe','Листайте проекты в сторону','Swipe to explore projects','Projektide vaatamiseks libista'),
 ('conceptTournament','Концепт / Tournament system','Concept / Tournament system','Näidismakett / Turniirisüsteem'),
 ('conceptPhotos','Концепт / Photo library','Concept / Photo library','Näidismakett / Fotokogu'),
 ('conceptCRM','Концепт / Lead tracking','Concept / Lead tracking','Näidismakett / Päringute haldus'),
 ('delivery','Архитектура · Разработка · Запуск','Architecture · Development · Launch','Arhitektuur · Arendus · Käivitus'),
 ('challenge','Задача:','Challenge:','Ülesanne:'),
 ('contribution','Моя работа:','My contribution:','Minu panus:'),
 ('tournamentTask','запустить платформу киберспортивных турниров с призовыми фондами.','launch an esports tournament platform with prize pools.','käivitada auhinnafondidega e-sporditurniiride platvorm.'),
 ('tournamentWork','спроектировал архитектуру, связал интерфейс, сервер и базу данных. Довёл систему до запуска и поддерживал её стабильность.','designed the architecture and connected the frontend, backend and database. Delivered the production launch and maintained platform stability.','kavandasin arhitektuuri ning ühendasin kasutajaliidese, serveri ja andmebaasi. Viisin platvormi kasutuselevõtuni ja tagasin selle stabiilsuse.'),
 ('private','Публичная ссылка не представлена','No public website shared','Avalik veebileht puudub'),
 ('photoTask','создать веб-приложение для хранения фотографий по принципу Google Photos.','build a Google Photos-style web application for photo storage.','luua Google Photosi laadne veebirakendus fotode hoidmiseks.'),
 ('photoWork','самостоятельно разработал серверную часть на Go и интерфейс на Flutter, объединив их в полноценное приложение.','independently built the Go backend and Flutter frontend, connecting them into a complete application.','arendasin iseseisvalt Go serveripoole ja Flutteri kasutajaliidese ning ühendasin need terviklikuks rakenduseks.'),
 ('crmLabel','Bitrix CRM · Учёт заявок','Bitrix CRM · Lead tracking','Bitrix CRM · Päringute haldus'),
 ('crmTask','организовать учёт входящих заявок для образовательного центра.','organise incoming lead tracking for an education centre.','korraldada koolituskeskuse saabuvate päringute haldus.'),
 ('crmWork','настроил отслеживание лидов в Bitrix CRM, чтобы команда могла управлять обращениями в единой системе.','set up lead tracking in Bitrix CRM so the team could manage enquiries in one system.','seadistasin Bitrix CRM-is päringute jälgimise, et meeskond saaks pöördumisi hallata ühes süsteemis.'),
 ('toolsLabel','02 / Инструменты','02 / Toolkit','02 / Tööriistad'),
 ('toolsTitle','Технологии под вашу задачу.','The right tools for your challenge.','Sinu vajadustele sobivad tehnoloogiad.'),
 ('aiText','Связываю модели, сервисы и данные, чтобы сократить ручную работу.','I connect models, services and data to reduce manual work.','Ühendan mudelid, teenused ja andmed, et vähendada käsitsi tehtavat tööd.'),
 ('devText','Беру на себя весь цикл: от интерфейса и архитектуры до интеграций и запуска.','I handle the full cycle, from interfaces and architecture to integrations and launch.','Võtan enda kanda kogu arendustsükli: kasutajaliidesest ja arhitektuurist integratsioonide ning käivitamiseni.'),
 ('contactLabel','03 / Давайте обсудим','03 / Let’s talk','03 / Võtame ühendust'),
 ('contactText','Расскажите о задаче и текущем процессе. Вместе определим, что стоит автоматизировать первым.','Tell me about your challenge and current workflow. We’ll identify what to automate first.','Räägi oma vajadusest ja praegusest tööprotsessist. Leiame koos, mida tasub esimesena automatiseerida.'),
 ('footerLocation','Эстония · Работаю удалённо','Based in Estonia · Working remotely','Asun Eestis · Töötan kaugtööna'),
]: text(*row)

s=re.sub(r'(id="hero-title"[^>]*>)[\s\S]*?(</h1>)', lambda m:m[1]+'\n            '+entry('heroOne','Less busywork.','Vähem rutiini.','Меньше рутины.')+'<br><span class="text-[#577b2d]">'+entry('heroTwo','More customers.','Rohkem kliente.','Больше клиентов.')+'</span>\n          '+m[2],s)
s=s.replace('Где ваш бизнес<br><span class="text-[#d6f275]">теряет время и заявки?</span>',entry('footerOne','Where is your business','Kuhu kaovad sinu ettevõtte','Где ваш бизнес')+'<br><span class="text-[#d6f275]">'+entry('footerTwo','losing time and leads?','aeg ja kliendipäringud?','теряет время и заявки?')+'</span>')

for row in [
 ('home','Nikita Makeev — на главную','Nikita Makeev — home','Nikita Makeev — avaleht'),
 ('nav','Основная навигация','Main navigation','Põhinavigatsioon'),
 ('call','Позвонить: +372 5681 6367','Call +372 5681 6367','Helista +372 5681 6367'),
 ('linkedin','LinkedIn — откроется в новой вкладке','LinkedIn — opens in a new tab','LinkedIn — avaneb uuel vahelehel'),
 ('github','Профиль GitHub — откроется в новой вкладке','GitHub profile — opens in a new tab','GitHubi profiil — avaneb uuel vahelehel'),
 ('cases','Кейсы: горизонтальная прокрутка на небольших экранах','Projects: scroll horizontally on small screens','Projektid: väikestel ekraanidel keri horisontaalselt'),
 ('figureTournament','Условная иллюстрация турнирной сетки','Illustrative tournament bracket','Turniiritabeli näidismakett'),
 ('figurePhotos','Условная иллюстрация галереи фотографий','Illustrative photo gallery','Fotogalerii näidismakett'),
 ('figureCRM','Условная схема передачи заявки с сайта в CRM','Illustrative website-to-CRM lead flow','Näidisskeem päringu liikumisest veebilehelt CRM-i'),
 ('visitLabel','Visit Website — ivkoolitus.ee, в новой вкладке','Visit ivkoolitus.ee — opens in a new tab','Ava ivkoolitus.ee — avaneb uuel vahelehel'),
 ('aiSkills','Навыки ИИ и автоматизации','AI and automation skills','Tehisintellekti ja automatiseerimise oskused'),
 ('devSkills','Навыки разработки','Development skills','Arendusoskused'),
]: label(*row)

for key,old,en,et,ru in [
 ('tournamentTitle','Esports Tournament Platform','Esports Tournament Platform','E-sporditurniiride platvorm','Платформа киберспортивных турниров'),
 ('photosTitle','Photo Storage Application','Photo Storage Application','Fotode hoidmise rakendus','Приложение для хранения фотографий'),
 ('crmTitle','Lead Tracking for ivkoolitus.ee','Lead Tracking for ivkoolitus.ee','ivkoolitus.ee päringute haldus','Учёт заявок для ivkoolitus.ee'),
 ('aiHeading','AI &amp; Automation','AI & Automation','Tehisintellekt ja automatiseerimine','ИИ и автоматизация'),
 ('devHeading','Full-Stack Development','Full-Stack Development','Täispinu arendus','Full-Stack разработка'),
 ('visit','Visit Website','Visit Website','Vaata veebilehte','Посетить сайт'),
 ('prompts','Prompt Engineering','Prompt Engineering','Viipade koostamine','Промпт-инжиниринг'),
 ('workflows','Workflow Automation','Workflow Automation','Töövoogude automatiseerimine','Автоматизация процессов'),
 ('crmSkill','CRM Integrations','CRM Integrations','CRM-i integratsioonid','Интеграции CRM'),
]:
    s=s.replace('>'+old+'<','>'+entry(key,en,et,ru)+'<')
s=s.replace(' lang="en"','') # Translated headings inherit the selected language.
s=s.replace('<html>','<html lang="en">')

# Remove arrows only from contact links; project navigation keeps its affordance.
def contact_link(m):
    a=m[0]
    if any(v in a for v in ['mailto:','tel:','linkedin.com','github.com']):
        a=a.replace('<span aria-hidden="true">↗</span>','')
        a=a.replace('justify-between','justify-center')
        a=a.replace('class="','class="contact-button ',1)
    return a
s=re.sub(r'<a\b[^>]*>[\s\S]*?</a>',contact_link,s)
github_start=s.index('          <div class="mt-2 flex items-center justify-between')
github_end=s.index('\n        </div>',github_start)
github=entry('githubText','Explore my GitHub','Vaata minu GitHubi','Мой профиль GitHub')
icon='<svg aria-hidden="true" viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M12 .8a11.2 11.2 0 0 0-3.54 21.82c.56.1.77-.24.77-.54v-2.09c-3.13.68-3.79-1.33-3.79-1.33-.51-1.3-1.25-1.65-1.25-1.65-1.03-.71.08-.7.08-.7 1.13.08 1.72 1.16 1.72 1.16 1.01 1.72 2.64 1.22 3.29.93.1-.73.4-1.22.72-1.5-2.5-.28-5.12-1.25-5.12-5.57 0-1.23.44-2.23 1.16-3.02-.12-.28-.5-1.43.11-2.98 0 0 .94-.3 3.08 1.16a10.7 10.7 0 0 1 5.6 0c2.14-1.45 3.08-1.16 3.08-1.16.61 1.55.23 2.7.11 2.98.72.79 1.15 1.79 1.15 3.02 0 4.33-2.62 5.28-5.13 5.56.4.35.76 1.03.76 2.08v3.11c0 .3.2.65.77.54A11.2 11.2 0 0 0 12 .8Z"/></svg>'
s=s[:github_start]+f'''          <a id="hero-github" href="https://github.com/NikitaMakeev" target="_blank" rel="noopener noreferrer" data-i18n-aria="github" aria-label="{translations['en']['github']}" class="contact-button github-button mt-2.5 flex min-h-12 items-center justify-center gap-2.5 rounded-xl border border-[#bad477] bg-[#d6f275] px-4 py-3 text-sm font-semibold text-[#183c32]">{icon}{github}</a>
          <p class="mt-3 text-center text-xs text-[#5b6b60]"><span data-i18n="location">Estonia · Remote</span></p>'''+s[github_end:]
# Make the footer GitHub distinct too.
s=s.replace('>GitHub </a>','>'+icon+'<span>GitHub</span></a>')
s=re.sub(r'(<a[^>]+href="https://github.com/NikitaMakeev"[^>]+class=")([^\"]+)(")',lambda m:m[1]+(m[2] if 'github-button' in m[2] else m[2].replace('border-[#597567]','border-[#bad477] bg-[#d6f275] text-[#183c32] gap-2 font-semibold github-button').replace('hover:bg-white/10','hover:bg-[#e3fa9e]'))+m[3],s)
s=s.replace('header class="mx-auto flex','header class="mx-auto flex flex-wrap')
s=s.replace('class="flex items-center gap-5 text-sm font-medium"','class="flex w-full items-center justify-between gap-3 text-sm font-medium md:w-auto md:justify-end md:gap-5"')
s=s.replace('</nav>', '''<div id="language-switcher" class="language-switcher" role="group" data-i18n-aria="language" aria-label="Choose language" hidden>
        <button type="button" data-lang="en" lang="en" aria-label="English" aria-pressed="true">EN</button>
        <button type="button" data-lang="et" lang="et" aria-label="Eesti" aria-pressed="false">ET</button>
        <button type="button" data-lang="ru" lang="ru" aria-label="Русский" aria-pressed="false">RU</button>
      </div></nav>''')
entry('language','Choose language','Vali keel','Выберите язык')
entry('languageChanged','Language changed to English.','Keeleks on valitud eesti keel.','Выбран русский язык.')
s=s.replace('pt-5 pb-10 md:px-8','pt-3 pb-8 md:px-8').replace('grid items-end gap-8 lg:','grid items-end gap-5 lg:')
s=s.replace('text-[clamp(2rem,8.3vw,3rem)]','text-[clamp(1.9rem,8vw,3rem)]')
s=s.replace('mt-5 max-w-xl','mt-4 max-w-xl')
s=s.replace('class="max-w-3xl','class="hero-enter max-w-3xl',1)
s=s.replace('class="mt-4 max-w-xl','class="hero-enter hero-delay mt-4 max-w-xl',1)
s=s.replace('id="hero-contacts" class="','id="hero-contacts" class="hero-enter hero-delay ',1)
s=s.replace('<article class="','<article class="reveal ',3)
s=s.replace('<div aria-hidden="true" class="','<div aria-hidden="true" class="illustration ',3)
s=s.replace('class="grid w-full max-w-60','class="illustration grid w-full max-w-60')
s=s.replace('class="mt-7 grid gap-8','class="reveal mt-7 grid gap-8')
s=s.replace('class="grid gap-7 md:grid-cols-2','class="reveal grid gap-7 md:grid-cols-2')
css='''
    .language-switcher { display: inline-flex; gap: 2px; padding: 3px; border: 1px solid #d4dccf; border-radius: 12px; background: #fff; }
    .language-switcher[hidden] { display: none; }
    .language-switcher button { min-width: 44px; min-height: 40px; border-radius: 8px; color: #526257; font: inherit; font-size: 12px; font-weight: 600; cursor: pointer; transition: background .2s, color .2s, transform .2s; }
    .language-switcher button[aria-pressed="true"] { color: #d6f275; background: #183c32; }
    .language-switcher button:active { transform: scale(.94); }
    .contact-button { transition: transform .25s, box-shadow .25s, background-color .25s; }
    .contact-button:active { transform: scale(.98); }
    .github-button svg { flex-shrink: 0; }
    .hero-enter { animation: enter .8s cubic-bezier(.2,.7,.2,1) both; }
    .hero-delay { animation-delay: .12s; }
    .reveal { transition: opacity .7s ease, transform .7s cubic-bezier(.2,.7,.2,1), box-shadow .3s; }
    .reveal.waiting { opacity: 0; transform: translateY(22px); }
    .reveal:focus-within { opacity: 1; transform: none; }
    figure .illustration { animation: float 7s ease-in-out infinite; animation-play-state: paused; }
    figure.in-view .illustration { animation-play-state: running; }
    article:nth-child(2) .illustration { animation-delay: -2s; }
    article:nth-child(3) .illustration { animation-delay: -4s; }
    .language-change { animation: language-in .25s ease-out; }
    .tag { transition: transform .2s, border-color .2s, background-color .2s; }
    @keyframes enter { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes float { 0%,100% { translate: 0 0; } 50% { translate: 0 -6px; } }
    @keyframes language-in { from { opacity: .55; translate: 0 3px; } to { opacity: 1; translate: 0 0; } }
    @media (hover: hover) {
      .contact-button:hover { transform: translateY(-3px); box-shadow: 0 8px 20px #183c3217; }
      .github-button:hover { background-color: #e3fa9e; box-shadow: 0 8px 24px #a4c45035; }
      .project-track article:hover { transform: translateY(-4px); box-shadow: 0 10px 28px #183c3210; }
      .tag:hover { transform: translateY(-3px); background: #eff4e8; border-color: #a9bd93; }
      .language-switcher button:not([aria-pressed="true"]):hover { background: #eff4e8; }
    }
    @media (prefers-reduced-motion: reduce) { .reveal.waiting { opacity: 1; transform: none; } }
'''
s=s.replace('    @media (prefers-reduced-motion: reduce)',css+'    @media (prefers-reduced-motion: reduce)',1)
script='''
  <p id="language-status" class="sr-only" role="status" aria-live="polite" aria-atomic="true"></p>
  <script>
    (() => {
      'use strict';
      const translations = __TRANSLATIONS__;
      const buttons = document.querySelectorAll('[data-lang]');
      const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
      let currentLanguage = 'en';
      function setLanguage(language, announce = false) {
        if (!Object.prototype.hasOwnProperty.call(translations, language)) return;
        const copy = translations[language];
        const changed = language !== currentLanguage;
        document.querySelectorAll('[data-i18n]').forEach(element => {
          const value = copy[element.dataset.i18n];
          if (typeof value === 'string') element.textContent = value;
        });
        document.querySelectorAll('[data-i18n-aria]').forEach(element => {
          const value = copy[element.dataset.i18nAria];
          if (typeof value === 'string') element.setAttribute('aria-label', value);
        });
        document.documentElement.lang = language;
        document.querySelector('meta[name="description"]').content = copy.meta;
        buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.lang === language)));
        currentLanguage = language;
        if (announce) {
          try { localStorage.setItem('portfolio-language', language); } catch { /* Storage may be unavailable. */ }
          document.getElementById('language-status').textContent = copy.languageChanged;
        }
        if (announce && changed && !motion.matches) {
          const main = document.querySelector('main');
          main.classList.remove('language-change');
          void main.offsetWidth;
          main.classList.add('language-change');
        }
      }
      let savedLanguage = 'en';
      try { savedLanguage = localStorage.getItem('portfolio-language') || 'en'; } catch { /* English is the default. */ }
      setLanguage(Object.prototype.hasOwnProperty.call(translations, savedLanguage) ? savedLanguage : 'en');
      buttons.forEach(button => button.addEventListener('click', () => setLanguage(button.dataset.lang, true)));
      document.getElementById('language-switcher').hidden = false;

      if ('IntersectionObserver' in window) {
        const reveal = new IntersectionObserver(entries => {
          entries.forEach(entry => {
            if (entry.isIntersecting) {
              entry.target.classList.remove('waiting');
              reveal.unobserve(entry.target);
            }
          });
        }, { threshold: 0.08 });
        document.querySelectorAll('.reveal').forEach(element => {
          if (!motion.matches && element.getBoundingClientRect().top > innerHeight) element.classList.add('waiting');
          reveal.observe(element);
        });
        const figures = new IntersectionObserver(entries => {
          entries.forEach(entry => entry.target.classList.toggle('in-view', entry.isIntersecting));
        });
        document.querySelectorAll('figure').forEach(figure => figures.observe(figure));
        motion.addEventListener('change', () => {
          if (motion.matches) document.querySelectorAll('.waiting').forEach(element => element.classList.remove('waiting'));
        });
      }
    })();
  </script>
'''.replace('__TRANSLATIONS__',json.dumps(translations,ensure_ascii=False,indent=2))
s=s.replace('</body>',script+'</body>')
Path('index.html').write_text(s,encoding='utf-8')
print('Updated index.html:',len(s),'characters;',len(translations['en']),'translation keys per language')
