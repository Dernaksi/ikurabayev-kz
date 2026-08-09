/* Neutral Shift Lab — public profile AI concierge prototype.
   Self-contained, no dependencies. Renders into an existing <section id="ask">.
   Local-only curated answers; no network, model API, tracking, or storage.
   Multilingual: reads <html lang>. */
(function () {
  "use strict";

  /* -------------------- language strings -------------------- */
  var STR = {
    ru: {
      eyebrow: "AI Engineering Lab",
      title: "Спросите лабораторию",
      intro: "Задайте вопрос о методе, исследованиях, публикациях или дорожной карте — ИИ отвечает по проверенному публичному профилю. Приватные данные не раскрываются намеренно.",
      online: "Prototype UI · Source mode: Public facts only",
      demo: "Prototype UI · Source mode: Public facts only",
      emptyKicker: "// готов к запросу",
      emptyText: "Например: «Как устроен метод определения параметров изоляции?» или «Что такое AI Energy Auditor?» Нажмите подсказку ниже или напишите свой вопрос.",
      placeholder: "Спросите о работе Искандера Казбековича…",
      send: "Отправить",
      suggestions: [
        "Чем занимается Искандер Казбекович?",
        "Как устроен метод измерения изоляции?",
        "Что такое AI Energy Auditor?",
        "Какие есть публикации?"
      ]
    },
    en: {
      eyebrow: "AI Engineering Lab",
      title: "Ask the lab",
      intro: "Ask about the method, research, publications, or roadmap — the assistant answers from a verified public profile. Private details are intentionally withheld.",
      online: "Prototype UI · Source mode: Public facts only",
      demo: "Prototype UI · Source mode: Public facts only",
      emptyKicker: "// ready for query",
      emptyText: "For example: “How does the insulation measurement method work?” or “What is the AI Energy Auditor?” Tap a prompt below or type your own question.",
      placeholder: "Ask about Iskander’s work…",
      send: "Send",
      suggestions: [
        "What does Iskander do?",
        "How does the insulation method work?",
        "What is the AI Energy Auditor?",
        "What are the publications?"
      ]
    },
    kk: {
      eyebrow: "AI Engineering Lab",
      title: "Зертханадан сұраңыз",
      intro: "Әдіс, зерттеулер, жарияланымдар немесе даму картасы туралы сұраңыз — ассистент тексерілген ашық профиль бойынша жауап береді. Жеке деректер әдейі ашылмайды.",
      online: "Prototype UI · Source mode: Public facts only",
      demo: "Prototype UI · Source mode: Public facts only",
      emptyKicker: "// сұрауға дайын",
      emptyText: "Мысалы: «Оқшаулауды өлшеу әдісі қалай жұмыс істейді?» немесе «AI Energy Auditor деген не?» Төмендегі кеңесті басыңыз немесе өз сұрағыңызды жазыңыз.",
      placeholder: "Ескендір Қазбекұлының жұмысы туралы сұраңыз…",
      send: "Жіберу",
      suggestions: [
        "Ескендір Қазбекұлы немен айналысады?",
        "Оқшаулауды өлшеу әдісі қалай жұмыс істейді?",
        "AI Energy Auditor деген не?",
        "Қандай жарияланымдар бар?"
      ]
    }
  };

  /* engineering-console labels */
  var CONSOLE = {
    ru: {
      mode: "Source mode: Public facts only",
      flags: ["Prototype UI", "Локально", "Без приватных данных"],
      proto: "Live AI integration pending",
      q: "ЗАПРОС",
      r: "ОТВЕТ"
    },
    en: {
      mode: "Source mode: Public facts only",
      flags: ["Prototype UI", "Local only", "No private data"],
      proto: "Live AI integration pending",
      q: "QUERY",
      r: "RESPONSE"
    },
    kk: {
      mode: "Source mode: Public facts only",
      flags: ["Prototype UI", "Жергілікті", "Жеке деректерсіз"],
      proto: "Live AI integration pending",
      q: "СҰРАУ",
      r: "ЖАУАП"
    }
  };

  /* -------------------- curated fallback answers -------------------- */
  var ANSWERS = {
    ru: [
      { k: ["привет", "здрав", "кто ты", "что ты уме"], a: "Здравствуйте! Я ассистент публичного профиля Искандера Казбековича Курабаева. Спросите о методе, исследованиях, публикациях, патентах или дорожной карте AI Engineering Lab." },
      { k: ["кто ", "чем заним", "о нём", "о нем", "расскажи о", "кем работ"], a: "Курабаев Искандер Казбекович — исследователь в области электротехники, специалист по энергоэффективности, инженер прикладных измерений, PhD и аккредитованный энергоаудитор РК. Старший преподаватель КазАТИУ им. С. Сейфуллина." },
      { k: ["метод", "измер", "изоляц", "как устроен"], a: "Метод следует цепочке «Измерить → Смоделировать → Диагностировать → Проверить»: снимаются сигналы и параметры изоляции, строится модель проводимости и ёмкостной проводимости, диагностируются сети с изолированной нейтралью и ток замыкания на землю, результат проходит инженерную проверку." },
      { k: ["ai", "ии", "auditor", "аудитор", "stm", "лаборатор", "нейросет"], a: "AI Engineering Lab включает два направления в разработке: «AI Energy Auditor» — концепт ИИ-ассистированного энергоаудита с трассируемостью выводов, и «STM32 / измерительная лаборатория» — аппаратный сбор сигналов и измерительный стенд. Это дорожная карта, а не запущенные продукты." },
      { k: ["публикац", "стат", "работ", "doi", "исследован"], a: "Опубликованы работы (2019–2023) по определению параметров изоляции в сетях с изолированной нейтралью и незаземлённых сетях переменного тока: математическое описание метода, лабораторные эксперименты, апробация на действующем экскаваторе и оценка погрешности. Часть работ имеет проверенные DOI (см. раздел «Избранные публикации»)." },
      { k: ["патент", "изобрет"], a: "Публично упоминаются евразийский патент (EA041128B1) на измерение параметров изоляции сетей с изолированной нейтралью по квадрантам комплексной плоскости и патент РК с использованием симметричных составляющих. Полная проверка реестров частично ожидается." },
      { k: ["образован", "phd", "диплом", "учил"], a: "Образование: PhD по направлению «Электротехнические комплексы и системы», магистр технических наук по электроэнергетике и инженер-электрик по электроснабжению промышленных предприятий." },
      { k: ["награ", "призна", "заслуж", "достиж"], a: "Среди отметок: Почётный энергетик (Ассоциация KEA, 2016; Минэнерго РК, 2018), Заслуженный энергетик (Минэнерго РК, 2023) и награда за вклад в энергосбережение (2024)." },
      { k: ["контакт", "связ", "телефон", "почт", "email", "написать", "адрес"], a: "Для первого контакта используйте публичную профессиональную электронную почту в разделе «Контакт» на этой странице. Телефон, личная почта, частные адреса и другие приватные контактные данные намеренно не публикуются. Проверенные публичные профили доступны через ORCID и Scopus." },
      { k: ["orcid", "scopus", "профил"], a: "Проверенные публичные профили: ORCID 0000-0002-4331-4726 и Scopus Author ID 57473761100." }
    ],
    en: [
      { k: ["hello", "hi ", "who are you", "what can you"], a: "Hello! I’m the assistant for Iskander Kurabayev’s public profile. Ask about the method, research, publications, patents, or the AI Engineering Lab roadmap." },
      { k: ["who ", "what does", "about him", "tell me about", "his job"], a: "Iskander Kurabayev is an electrical engineering researcher, energy-efficiency specialist, applied measurement engineer, PhD, and accredited energy auditor of Kazakhstan. He is a Senior Lecturer at S. Seifullin Kazakh Agrotechnical Research University." },
      { k: ["method", "measure", "insulation", "how does"], a: "The method follows a Measure → Model → Diagnose → Verify chain: signals and insulation parameters are captured, a conductance/susceptance model is built, isolated-neutral networks and earth-fault current are diagnosed, and the result passes engineering review." },
      { k: ["ai", "auditor", "stm", "lab", "neural"], a: "The AI Engineering Lab has two in-development tracks: “AI Energy Auditor” — a concept for AI-assisted energy audit with traceable reasoning, and “STM32 / measurement lab” — hardware signal capture and a test bench. These are roadmap directions, not launched products." },
      { k: ["publicat", "paper", "work", "doi", "research"], a: "Published works (2019–2023) address insulation parameters in isolated-neutral and ungrounded AC systems: a mathematical description of the method, laboratory experiments, approbation on an operating excavator, and error estimation. Several works have verified DOIs (see “Selected publications”)." },
      { k: ["patent", "invention"], a: "Publicly noted are a Eurasian patent (EA041128B1) on measuring insulation parameters of isolated-neutral networks via complex-plane quadrants, and a Kazakhstan patent using symmetrical components. Full registry verification is partly pending." },
      { k: ["educat", "phd", "degree", "study"], a: "Education: PhD in “Electrical complexes and systems”, MSc in electrical power engineering, and an engineer-electrician degree in industrial power supply." },
      { k: ["award", "recognit", "honor", "achiev"], a: "Recognition includes Honored Energy Worker (KEA, 2016; Ministry of Energy RK, 2018), Distinguished Energy Worker (Ministry of Energy RK, 2023), and an energy-saving award (2024)." },
      { k: ["contact", "reach", "phone", "mail", "email", "write", "address"], a: "For a first contact, use the public professional email in the “Contact” section on this page. Phone numbers, personal email, private addresses, and other private contact details are intentionally not published. Verified public profiles are available via ORCID and Scopus." },
      { k: ["orcid", "scopus", "profile"], a: "Verified public profiles: ORCID 0000-0002-4331-4726 and Scopus Author ID 57473761100." }
    ],
    kk: [
      { k: ["сәлем", "салем", "кім сен", "не істей ал"], a: "Сәлеметсіз бе! Мен Қорабаев Ескендір Қазбекұлының ашық профилінің ассистентімін. Әдіс, зерттеулер, жарияланымдар, патенттер немесе AI Engineering Lab даму картасы туралы сұраңыз." },
      { k: ["кім ", "немен айнал", "ол туралы", "жұмысы"], a: "Қорабаев Ескендір Қазбекұлы — электртехника саласының зерттеушісі, энергия тиімділігі маманы, қолданбалы өлшеу инженері, PhD және ҚР аккредиттелген энергоаудиторы. С. Сейфуллин атындағы Қазақ агротехникалық зерттеу университетінің аға оқытушысы." },
      { k: ["әдіс", "өлше", "оқшаула", "қалай жұмыс"], a: "Әдіс «Өлшеу → Модельдеу → Диагностикалау → Тексеру» тізбегімен жүреді: сигналдар мен оқшаулау параметрлері алынады, өткізгіштік моделі құрылады, бейтарабы оқшауланған желілер мен жерге тұйықталу тогы диагностикаланады, нәтиже инженерлік тексеруден өтеді." },
      { k: ["ai", "ии", "auditor", "аудитор", "stm", "зертхана", "нейрож"], a: "AI Engineering Lab-та әзірленудегі екі бағыт бар: «AI Energy Auditor» — қорытындылары бақыланатын ИИ-ассистенттік энергоаудит тұжырымдамасы және «STM32 / өлшеу зертханасы» — аппараттық сигнал жинау және стенд. Бұл — даму картасы, іске қосылған өнім емес." },
      { k: ["жарияла", "мақала", "жұмыс", "doi", "зерттеу"], a: "Жарияланған жұмыстар (2019–2023) бейтарабы оқшауланған және жерге тұйықталмаған айнымалы ток желілеріндегі оқшаулау параметрлеріне арналған: әдістің математикалық сипаттамасы, зертханалық эксперименттер, жұмыс істеп тұрған экскаватордағы апробация және қателікті бағалау. Бірнеше жұмыстың тексерілген DOI бар («Таңдаулы жарияланымдар» бөлімін қараңыз)." },
      { k: ["патент", "өнертабыс"], a: "Ашық түрде еуразиялық патент (EA041128B1) — бейтарабы оқшауланған желілердің оқшаулау параметрлерін комплексті жазықтық квадранттары бойынша өлшеу және симметриялық құраушыларды пайдаланатын ҚР патенті аталады. Тізілімдерді толық тексеру ішінара күтілуде." },
      { k: ["білім", "phd", "диплом", "оқыд"], a: "Білімі: «Электртехникалық кешендер мен жүйелер» бойынша PhD, электр энергетикасы бойынша техника ғылымдарының магистрі және өнеркәсіптік электрмен жабдықтау бойынша инженер-электрик." },
      { k: ["марапат", "сыйлық", "жетістік", "құрмет"], a: "Марапаттары: Құрметті энергетик (KEA, 2016; ҚР Энергетика министрлігі, 2018), Еңбек сіңірген энергетик (ҚР Энергетика министрлігі, 2023) және энергия үнемдеуге қосқан үлесі үшін марапат (2024)." },
      { k: ["байланыс", "хабарлас", "телефон", "пошта", "email", "жазу", "мекенжай"], a: "Алғашқы байланыс үшін осы беттегі «Байланыс» бөлімінде көрсетілген ашық кәсіби электрондық поштаны пайдаланыңыз. Телефон нөмірлері, жеке электрондық пошта, жеке мекенжайлар және басқа да жеке байланыс деректері әдейі жарияланбайды. Тексерілген ашық профильдер ORCID және Scopus арқылы қолжетімді." },
      { k: ["orcid", "scopus", "профил"], a: "Тексерілген ашық профильдер: ORCID 0000-0002-4331-4726 және Scopus Author ID 57473761100." }
    ]
  };

  var DEFAULT = {
    ru: "Хороший вопрос. Я отвечаю по проверенному публичному профилю — попробуйте спросить про метод измерения изоляции, исследования, публикации, патенты или AI Engineering Lab. Приватные данные не раскрываются.",
    en: "Good question. I answer from a verified public profile — try asking about the insulation measurement method, research, publications, patents, or the AI Engineering Lab. Private details are not disclosed.",
    kk: "Жақсы сұрақ. Мен тексерілген ашық профиль бойынша жауап беремін — оқшаулауды өлшеу әдісі, зерттеулер, жарияланымдар, патенттер немесе AI Engineering Lab туралы сұрап көріңіз. Жеке деректер ашылмайды."
  };

  function localAnswer(lang, q) {
    var s = (q || "").toLowerCase();
    var set = ANSWERS[lang] || ANSWERS.ru;
    for (var i = 0; i < set.length; i++) {
      for (var j = 0; j < set[i].k.length; j++) {
        if (s.indexOf(set[i].k[j]) !== -1) return set[i].a;
      }
    }
    return DEFAULT[lang] || DEFAULT.ru;
  }

  /* -------------------- render + behaviour -------------------- */
  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  function esc(str) {
    return String(str).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  ready(function () {
    var mount = document.getElementById("ask");
    if (!mount) return;

    var lang = (document.documentElement.lang || "ru").slice(0, 2).toLowerCase();
    if (!STR[lang]) lang = "ru";
    var T = STR[lang];
    var C = CONSOLE[lang] || CONSOLE.ru;
    var hasAI = false;

    mount.classList.add("section", "concierge");
    if (!hasAI) mount.classList.add("demo");

    var chips = T.suggestions.map(function (s) {
      return '<button type="button">' + esc(s) + "</button>";
    }).join("");

    var flags = C.flags.map(function (fl) {
      return '<span class="cm-flag"><i>✓</i>' + esc(fl) + "</span>";
    }).join("");

    mount.innerHTML =
      '<div class="section-heading concierge-heading">' +
        '<p class="eyebrow">' + esc(T.eyebrow) + "</p>" +
        "<h2>" + esc(T.title) + "</h2>" +
        '<p class="concierge-intro">' + esc(T.intro) + "</p>" +
      "</div>" +
      '<div class="concierge-panel">' +
        '<div class="concierge-head">' +
          '<span class="concierge-status">' + esc(hasAI ? T.online : T.demo) + "</span>" +
          '<span class="concierge-tag">' + esc(C.proto) + "</span>" +
        "</div>" +
        '<div class="concierge-modes">' +
          '<span class="cm-title">' + esc(C.mode) + "</span>" +
          flags +
        "</div>" +
        '<div class="concierge-log">' +
          '<div class="concierge-empty"><b>' + esc(T.emptyKicker) + "</b><span>" + esc(T.emptyText) + "</span></div>" +
        "</div>" +
        '<div class="concierge-foot">' +
          '<div class="concierge-chips">' + chips + "</div>" +
          '<form class="concierge-form"><input type="text" autocomplete="off" placeholder="' + esc(T.placeholder) + '"><button type="submit">' + esc(T.send) + " →</button></form>" +
        "</div>" +
      "</div>";

    var log = mount.querySelector(".concierge-log");
    var form = mount.querySelector(".concierge-form");
    var input = mount.querySelector(".concierge-form input");
    var state = { busy: false };
    var tw = null;

    function scrollDown() { log.scrollTop = log.scrollHeight; }

    function addMsg(role, text) {
      var d = document.createElement("div");
      d.className = "msg " + (role === "user" ? "user" : "bot");
      var lbl = document.createElement("span");
      lbl.className = "msg-label";
      lbl.textContent = role === "user" ? C.q : C.r;
      d.appendChild(lbl);
      var s = document.createElement("span");
      s.className = "msg-txt";
      s.textContent = text || "";
      d.appendChild(s);
      log.appendChild(d);
      scrollDown();
      return d;
    }

    function showTyping() {
      var d = document.createElement("div");
      d.className = "concierge-typing";
      d.innerHTML = "<i></i><i></i><i></i>";
      log.appendChild(d);
      scrollDown();
      return d;
    }

    function typewrite(text) {
      var d = addMsg("bot", "");
      var s = d.querySelector(".msg-txt");
      var caret = document.createElement("span");
      caret.className = "caret";
      caret.textContent = "▋";
      d.appendChild(caret);
      var i = 0;
      clearInterval(tw);
      tw = setInterval(function () {
        i += 2;
        s.textContent = text.slice(0, i);
        scrollDown();
        if (i >= text.length) {
          clearInterval(tw);
          caret.remove();
        }
      }, 14);
    }

    function ask(q) {
      q = (q || "").trim();
      if (!q || state.busy) return;
      var empty = log.querySelector(".concierge-empty");
      if (empty) empty.remove();
      addMsg("user", q);
      input.value = "";
      state.busy = true;
      var typing = showTyping();

      var pending = new Promise(function (res) {
        setTimeout(function () { res(localAnswer(lang, q)); }, 480);
      });

      pending
        .catch(function () { return localAnswer(lang, q); })
        .then(function (ans) {
          typing.remove();
          state.busy = false;
          typewrite(ans);
        });
    }

    mount.querySelectorAll(".concierge-chips button").forEach(function (b) {
      b.addEventListener("click", function () { ask(b.textContent); });
    });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      ask(input.value);
    });
  });
})();
