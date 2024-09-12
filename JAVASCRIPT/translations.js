document.addEventListener('DOMContentLoaded', () => {
  // Load default language
  loadTranslations('en');
});

function loadTranslations(language) {
  fetch(`JSON/index/${language}.json`)
    .then(response => response.json())
    .then(data => {
      document.getElementById('home').textContent = data.home;
      document.getElementById('application').textContent = data.application;
      document.getElementById('about').textContent = data.about;
      document.getElementById('contact').textContent = data.contact;
      document.getElementById('title').textContent = data.title;
      document.getElementById('titledescription').textContent = data.titledescription;
      document.getElementById('techTitle').textContent = data.techTitle;
      document.getElementById('htmlTech').textContent = data.techItems.HTML;
      document.getElementById('cssTech').textContent = data.techItems.CSS;
      document.getElementById('jsTech').textContent = data.techItems.JavaScript;
      document.getElementById('howItWorks').textContent = data.howItWorks;
      document.getElementById('howItWorksDescription').textContent = data.howItWorksDescription;
      document.getElementById('footer').innerHTML = data.footer;
    })
    .catch(error => console.error('Error loading translations:', error));
}

function changeLanguage(language) {
  loadTranslations(language);
}
