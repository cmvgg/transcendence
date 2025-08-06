document.addEventListener("DOMContentLoaded", () => {
  const selector = document.getElementById("language-selector");
  const lang = localStorage.getItem("language") || "en";
  selector.value = lang;
  loadLanguage(lang);

  selector.addEventListener("change", (e) => {
    const newLang = e.target.value;
    localStorage.setItem("language", newLang);
    loadLanguage(newLang);
  });
});

function loadLanguage(lang) {
  fetch(`/static/locales/${lang}.json`)
    .then(res => res.json())
    .then(data => {
      document.querySelectorAll("[data-i18n]").forEach(el => {
        const key = el.getAttribute("data-i18n");
        const text = key.split(".").reduce((o, i) => o && o[i], data);
        if (text) el.textContent = text;
      });
    });
}