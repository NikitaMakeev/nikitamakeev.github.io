from pathlib import Path
import json,re,html
s=Path('index.html').read_text(encoding='utf-8')
old=s.split('const translations = ',1)[1].split(';\n      const buttons',1)[0]
d=json.loads(old)
def t(key,en,et,ru):
    for lang,value in zip(('en','et','ru'),(en,et,ru)):d[lang][key]=value
    return '<span data-i18n="'+key+'">'+html.escape(en)+'</span>'
form='''<h3>'''+t('formTitle','Tell me about your project','Räägi oma projektist','Расскажите о проекте')+'''</h3>
          <p class="contact-panel-note">'''+t('formIntro','A few lines about the problem are enough to start.','Alustuseks piisab paarist lausest probleemi kohta.','Для начала хватит пары строк о задаче.')+'''</p>
          <form id="inquiry-form">
            <label for="inquiry-name">'''+t('formName','Your name (optional)','Sinu nimi (valikuline)','Ваше имя (необязательно)')+'''</label>
            <input id="inquiry-name" name="name" type="text" maxlength="100" autocomplete="name">
            <label for="inquiry-email">'''+t('formEmail','Email','E-post','Электронная почта')+'''</label>
            <input id="inquiry-email" name="email" type="email" maxlength="254" autocomplete="email" required>
            <label for="inquiry-message">'''+t('formMessage','What would you like to improve?','Mida soovid paremaks muuta?','Что вы хотите улучшить?')+'''</label>
            <textarea id="inquiry-message" name="message" rows="3" minlength="10" maxlength="4000" required></textarea>
            <div class="form-trap" aria-hidden="true"><label for="inquiry-website">Website</label><input id="inquiry-website" name="website" tabindex="-1" autocomplete="off"></div>
            <p class="form-privacy">'''+t('formPrivacy','Your details will be used to discuss this enquiry.','Sinu andmeid kasutatakse selle päringu arutamiseks.','Эти данные нужны для обсуждения вашей заявки.')+'''</p>
            <button id="inquiry-submit" type="submit" class="primary-cta contact-button" disabled>'''+t('sendRequest','Send project enquiry','Saada projektipäring','Отправить заявку')+'''</button>
            <p id="form-status" role="status" aria-live="polite"></p>
            <p id="form-offline" class="form-offline" data-i18n="formOffline">To submit, open this page through the included server. You can also use the contact options below.</p>
            <noscript><p class="form-offline">Enable JavaScript to submit the form, or use the contact options below.</p></noscript>
          </form>
          <div class="contact-divider">'''+t('orDirect','Or contact me directly','Või võta otse ühendust','Или свяжитесь напрямую')+'''</div>'''
start=s.index('          <h3><span data-i18n="contactPanelTitle"')
end=s.index('          <a href="https://mail.google.com',start)
s=s[:start]+form+'\n'+s[end:]
# Keep the direct email fallback visually secondary to the real form.
s=s.replace('id="browser-email" class="primary-cta contact-button"','id="browser-email" class="browser-email-link contact-button"')
t('formOffline','To submit, open this page through the included server. You can also use the contact options below.','Saatmiseks ava leht kaasasoleva serveri kaudu. Võid kasutada ka allolevaid kontaktivõimalusi.','Для отправки откройте страницу через прилагаемый сервер. Также можно связаться со мной ниже.')
t('sending','Sending…','Saadan…','Отправляем…')
t('requestReceived','Request received. Thank you — I’ll follow up using your email.','Päring on vastu võetud. Aitäh! Võtan sinuga e-posti teel ühendust.','Заявка получена. Спасибо! Свяжусь с вами по указанной почте.')
t('requestFailed','Could not confirm delivery. Your text is still here. Please retry or use a contact option below.','Saatmist ei õnnestunud kinnitada. Sinu tekst on alles. Proovi uuesti või kasuta allolevaid kontaktivõimalusi.','Не удалось подтвердить отправку. Текст сохранён в форме. Повторите попытку или свяжитесь со мной ниже.')
t('requestRateLimit','Too many attempts. Please try again in a few minutes or contact me directly.','Liiga palju katseid. Proovi mõne minuti pärast või võta otse ühendust.','Слишком много попыток. Попробуйте через несколько минут или свяжитесь напрямую.')
t('requestInvalid','Please check your email and enter at least 10 characters about your project.','Kontrolli e-posti aadressi ja kirjelda projekti vähemalt 10 tähemärgiga.','Проверьте почту и опишите проект минимум в 10 символах.')
css='''
    #inquiry-form { display: grid; gap: 7px; }
    #inquiry-form label { margin-top: 8px; font-size: 12px; font-weight: 600; color: #354561; }
    #inquiry-form input,#inquiry-form textarea { width: 100%; min-width: 0; min-height: 46px; border: 1px solid #cdd8ee; border-radius: 9px; background: #f8faff; padding: 10px 12px; color: #122044; font: inherit; font-size: 16px; line-height: 1.5; }
    #inquiry-form textarea { min-height: 105px; resize: vertical; }
    #inquiry-form input:focus-visible,#inquiry-form textarea:focus-visible { outline: 2px solid #2458e8; outline-offset: 2px; }
    #inquiry-form .form-trap { position: absolute; left: -10000px; width: 1px; height: 1px; overflow: hidden; }
    .form-privacy { margin: 6px 0 9px; font-size: 11px; line-height: 1.5; color: #52607a; }
    #inquiry-submit { width: 100%; cursor: pointer; }
    #inquiry-submit:disabled { opacity: .55; cursor: not-allowed; transform: none; }
    #form-status { min-height: 18px; font-size: 12px; line-height: 1.5; color: #2458e8; }
    #form-status[data-error="true"] { color: #a72e32; }
    .form-offline { font-size: 12px; line-height: 1.5; color: #52607a; }
    .contact-divider { border-top: 1px solid #e5eaf4; margin: 18px 0 6px; padding-top: 16px; font-size: 12px; color: #52607a; }
    .browser-email-link { display: inline-flex; align-items: center; min-height: 44px; font-size: 13px; font-weight: 600; color: #2458e8; }
    #contact { scroll-margin-top: 20px; }
'''
s=s.replace('  </style>',css+'  </style>',1)
s=s.replace(old,json.dumps(d,ensure_ascii=False,indent=2))
s=s.replace("let currentLanguage = 'en';", "let currentLanguage = 'en';\n      let formStatusKey = '';\n      let sending = false;")
s=s.replace("currentLanguage = language;", """currentLanguage = language;
        if (formStatusKey) document.getElementById('form-status').textContent = copy[formStatusKey];
        if (sending) document.querySelector('#inquiry-submit [data-i18n]').textContent = copy.sending;""")
js='''
      const form = document.getElementById('inquiry-form');
      const submit = document.getElementById('inquiry-submit');
      const formStatus = document.getElementById('form-status');
      const served = location.protocol === 'http:' || location.protocol === 'https:';
      submit.disabled = !served;
      document.getElementById('form-offline').hidden = served;
      let requestId = '';
      form.addEventListener('input', () => { requestId = ''; });
      form.addEventListener('submit', async event => {
        event.preventDefault();
        if (!served || sending || !form.reportValidity()) return;
        const values = new FormData(form);
        if (String(values.get('message')).trim().length < 10) {
          formStatusKey = 'requestInvalid';
          formStatus.textContent = translations[currentLanguage][formStatusKey];
          formStatus.dataset.error = 'true';
          return;
        }
        requestId ||= crypto.randomUUID();
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 15000);
        sending = true;
        submit.disabled = true;
        form.setAttribute('aria-busy', 'true');
        submit.querySelector('span').textContent = translations[currentLanguage].sending;
        formStatus.textContent = '';
        formStatusKey = '';
        try {
          const response = await fetch('/api/inquiries', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'same-origin',
            signal: controller.signal,
            body: JSON.stringify({
              requestId, name: values.get('name').trim(), email: values.get('email').trim(),
              message: values.get('message').trim(), website: values.get('website'), language: currentLanguage
            })
          });
          const result = await response.json();
          if (!response.ok || result.accepted !== true) {
            const error = new Error('Request not accepted');
            error.status = response.status;
            throw error;
          }
          form.reset();
          requestId = '';
          formStatusKey = 'requestReceived';
          formStatus.dataset.error = 'false';
        } catch (error) {
          formStatusKey = error.status === 429 ? 'requestRateLimit' : error.status === 400 ? 'requestInvalid' : 'requestFailed';
          formStatus.dataset.error = 'true';
        } finally {
          clearTimeout(timeout);
          sending = false;
          submit.disabled = false;
          form.removeAttribute('aria-busy');
          submit.querySelector('span').textContent = translations[currentLanguage].sendRequest;
          formStatus.textContent = translations[currentLanguage][formStatusKey];
        }
      });
'''
s=s.replace("      if ('IntersectionObserver' in window)",js+"\n      if ('IntersectionObserver' in window)")
Path('index.html').write_text(s,encoding='utf-8')
print('Added translated inquiry form and progressive fallback.')
