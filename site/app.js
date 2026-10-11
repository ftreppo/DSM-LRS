(() => {
  const dictionary = window.SITE_I18N || {};
  let language = localStorage.getItem("dsm-lrs-language") || "de";
  if (!dictionary[language]) language = "de";

  function applyLanguage() {
    const tr = dictionary[language] || dictionary.de;
    document.documentElement.lang = language;
    document.querySelectorAll("[data-i18n]").forEach((node) => {
      const value = tr[node.dataset.i18n];
      if (typeof value === "string") node.textContent = value;
    });
    document.querySelectorAll("[data-lang]").forEach((node) => {
      node.hidden = node.dataset.lang !== language;
    });
    document.querySelectorAll("[data-language]").forEach((button) => {
      const selected = button.dataset.language === language;
      button.setAttribute("aria-pressed", String(selected));
      button.setAttribute("aria-label", button.textContent + (selected ? " selected" : ""));
    });
  }

  document.querySelectorAll("[data-language]").forEach((button) => {
    button.addEventListener("click", () => {
      language = button.dataset.language;
      localStorage.setItem("dsm-lrs-language", language);
      applyLanguage();
    });
  });

  applyLanguage();
})();
