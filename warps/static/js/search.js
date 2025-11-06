// Die Daten werden aus dem Django-Kontext geparsed
const rdata = rdata_source;          

// Autocomplete Logik
const searchInput = document.getElementById('search');
const resultsContainer = document.getElementById('search-results');

// Die Funktion zum Filtern und Anzeigen der Ergebnisse
function updateAutocomplete() {
    // Die Eingabe des Benutzers, in Kleinbuchstaben
    const query = searchInput.value.toLowerCase().trim();
    resultsContainer.innerHTML = ''; // Vorherige Ergebnisse löschen
    
    if (query.length === 0) {
        resultsContainer.style.display = 'none';
        return;
    }

    // Filtern der Daten
    const filteredResults = rdata.filter(item => {
        const name = item.name ? item.name.toLowerCase() : '';
        const en = item.eng_name ? item.eng_name.toLowerCase(): '';
        
        // SUCH-LOGIK: Überprüft, ob die Eingabe ('query') im Namen enthalten ist.
        return name.includes(query) || en.includes(query); 
    }).slice(0, 10); // Begrenzen auf z.B. 10 Ergebnisse

    if (filteredResults.length > 0) {
        filteredResults.forEach(item => {
            const resultItem = document.createElement('a');
            resultItem.classList.add('autocomplete-item');

            // **Link erstellen:** Navigiert zur Detailseite basierend auf item_id
            const itemUrl = `/details/${item.item_id}/`; // PASST DIESEN PFAD AN IHR URL-MUSTER AN
            resultItem.href = itemUrl; 
            
            // **Bild und Text erstellen**
            let contentHTML = '';
            
            // Fügen Sie das Bild hinzu, wenn eine URL vorhanden ist
            if (item.image_url) {
                // WICHTIG: Django-Static-URL und/oder Media-Prefix hinzufügen!
                // ANNAHME: Die Bilder liegen im /media/-Ordner. 
                // Je nach Konfiguration muss dies ggf. angepasst werden.
                //const imageUrl = `/media/${item.image}`; 
                //contentHTML += `<img src="${imageUrl}" class="autocomplete-image" alt="${item.name}">`;
            }

            // Fügen Sie den Namen hinzu
            contentHTML += `<span>${item.name || 'Unbekanntes Item'}</span>`; 
            
            resultItem.innerHTML = contentHTML;

            // Event-Listener für Weiterleitung beim Klicken
            resultItem.addEventListener('click', (e) => {
                //e.preventDefault(); // Wird nicht benötigt, da wir href setzen

                // Leitet den Benutzer zur Detailseite weiter
                window.location.href = itemUrl;
            });

            resultsContainer.appendChild(resultItem);
        });
        resultsContainer.style.display = 'block';
    } else {
        resultsContainer.style.display = 'none';
    }
}

// Event-Listener für die Eingabe im Suchfeld
searchInput.addEventListener('input', updateAutocomplete);

// Schließen der Vorschläge beim Klicken außerhalb
document.addEventListener('click', (e) => {
    if (!e.target.closest('.nav-search')) {
        resultsContainer.style.display = 'none';
    }
});