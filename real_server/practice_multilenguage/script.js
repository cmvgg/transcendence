document.addEventListener('DOMContentLoaded', () => {
	const languageSelector = document.getElementById('language-selector');
	const savedLanguage = localStorage.getItem('language') || 'es';
	languageSelector.value = savedLanguage;
  
	function loadLanguage(lang) {
	  fetch(`locales/${lang}.json`)
		.then(res => res.json())
		.then(translations => {
		  document.querySelectorAll('[data-i18n]').forEach(el => {
			const key = el.getAttribute('data-i18n');
			// Soportamos keys con puntos para objetos anidados
			const text = key.split('.').reduce((obj, k) => obj && obj[k], translations);
			el.textContent = text || key;
		  });
		});
	}
  
	loadLanguage(savedLanguage);
  
	languageSelector.addEventListener('change', (e) => {
	  const newLang = e.target.value;
	  localStorage.setItem('language', newLang);
	  loadLanguage(newLang);
	});
  });
  