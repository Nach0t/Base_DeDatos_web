document.addEventListener('DOMContentLoaded', () => {
  // Load default language
  loadTranslations('en');
});

function loadTranslations(language) {
  // Build the URL for the JSON file
  const url = `/static/JSON/index/${language}.json`;

  fetch(url)
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      document.getElementById('home').textContent = data.home || 'Home';
      document.getElementById('application').textContent = data.application || 'Application';
      document.getElementById('about').textContent = data.about || 'About';
      document.getElementById('contact').textContent = data.contact || 'Contact';
      document.getElementById('title').textContent = data.title || 'Title';
      document.getElementById('titledescription').textContent = data.titledescription || 'Description';
      document.getElementById('techTitle').textContent = data.techTitle || 'Technologies Used';
      document.getElementById('htmlTech').textContent = data.techItems?.HTML || 'HTML';
      document.getElementById('cssTech').textContent = data.techItems?.CSS || 'CSS';
      document.getElementById('jsTech').textContent = data.techItems?.JavaScript || 'JavaScript';
      document.getElementById('howItWorks').textContent = data.howItWorks || 'How it Works';
      document.getElementById('howItWorksDescription').textContent = data.howItWorksDescription || 'Description';
      document.getElementById('footer').innerHTML = data.footer || '&copy; Chuequito Company. All rights reserved.';
    })
    .catch(error => {
      console.error('Error loading translations:', error);
      // Optionally, you can set default text or show an error message here
    });
}

function changeLanguage(language) {
  loadTranslations(language);

}
