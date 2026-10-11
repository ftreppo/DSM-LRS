(() => {
  const { ui, updates, events, documents, news } = window.DEMO_DATA;
  let language = localStorage.getItem("dsm-lrs-demo-language") || "de";
  let filter = "all";
  const q = (selector) => document.querySelector(selector);
  const tr = (key) => ui[language][key];
  const date = (value) => new Intl.DateTimeFormat(language, { year:"numeric", month:"short", day:"numeric" }).format(new Date(`${value}T12:00:00`));

  function fillStaticText() { document.querySelectorAll("[data-i18n]").forEach((node) => { node.textContent = tr(node.dataset.i18n); }); document.documentElement.lang = language; document.title = `DSM-LRS — ${tr("demoPill")}`; }
  function renderRoles() { q("#roles").innerHTML = [["public",tr("public"),true],["member",tr("member"),false],["admin",tr("admin"),false],["dsm",tr("dsm"),false]].map(([id,label,active]) => `<span class="role ${active ? "public" : "locked"}" title="${active ? "" : tr("coming")}">${label}</span>`).join(""); }
  function renderUpdates() { q("#updates").innerHTML = updates.map((item) => `<article class="card"><span class="tag">${item.tag}</span><h3>${item[language][0]}</h3><p>${item[language][1]}</p></article>`).join(""); }
  function renderEvents() { q("#events").innerHTML = events.map((item) => `<article class="event"><div class="date-box"><strong>${item.date}</strong><span>${item.month}</span></div><div><h3>${item[language][0]}</h3><p>${item[language][1]}</p></div></article>`).join(""); }
  function renderDocuments() { q("#documents").innerHTML = documents.map((item) => `<article class="document"><span class="tag">DEMO</span><div><h3>${item[language][0]}</h3><p>${item[language][1]}</p></div></article>`).join(""); }
  function categories(item) { const labels = {DYSLEXIA_LRS:tr("filters").dyslexia,DYSCALCULIA:tr("filters").dyscalculia,ASSISTIVE_TECH_AI:tr("filters").ai,RESEARCH:tr("filters").research}; return item.categories.map((category) => labels[category] || category).join(" · "); }
  function renderFilters() { const options = [["all",tr("filters").all],["dyslexia",tr("filters").dyslexia],["dyscalculia",tr("filters").dyscalculia],["ai",tr("filters").ai],["research",tr("filters").research]]; q("#news-filters").innerHTML = options.map(([id,label]) => `<button type="button" data-filter="${id}" aria-pressed="${filter === id}">${label}</button>`).join(""); q("#news-filters").querySelectorAll("button").forEach((button) => button.addEventListener("click", () => { filter = button.dataset.filter; renderFilters(); renderNews(); })); }
  function renderNews() { const map = {dyslexia:"DYSLEXIA_LRS",dyscalculia:"DYSCALCULIA",ai:"ASSISTIVE_TECH_AI",research:"RESEARCH"}; const shown = filter === "all" ? news : news.filter((item) => item.categories.includes(map[filter])); q("#news-items").innerHTML = shown.map((item) => `<article class="news-card"><div class="news-meta"><span class="tag">${categories(item)}</span><span>${item.country}</span></div><p class="news-demo">DEMO / SAMPLE · ${item.source}</p><h3>${item.original_title}</h3><p>${item.content[language].summary}</p><div class="news-meta"><span>${date(item.date)}</span><span>${item.original_language.toUpperCase()}</span></div><a href="${item.source_url}" target="_blank" rel="noopener noreferrer">${tr("readOriginal")} <span aria-hidden="true">↗</span></a></article>`).join(""); }
  function render() { fillStaticText(); renderRoles(); renderUpdates(); renderEvents(); renderDocuments(); renderFilters(); renderNews(); document.querySelectorAll("[data-language]").forEach((button) => { const selected = button.dataset.language === language; button.setAttribute("aria-pressed", String(selected)); button.setAttribute("aria-label", button.textContent + (selected ? " selected" : "")); }); }
  document.querySelectorAll("[data-language]").forEach((button) => button.addEventListener("click", () => { language = button.dataset.language; localStorage.setItem("dsm-lrs-demo-language", language); render(); }));
  render();
})();
