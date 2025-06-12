document.addEventListener('DOMContentLoaded', function() {
    fetch('books.xml')
        .then(response => response.text())
        .then(xmlString => {
            const parser = new DOMParser();
            const xmlDoc = parser.parseFromString(xmlString, "text/xml");
            displayBooks(xmlDoc);
        })
        .catch(error => console.error('Error loading XML:', error));
});

function displayBooks(xml) {
    const libraryDiv = document.getElementById('library');
    const books = xml.getElementsByTagName('book');
    
    for (let i = 0; i < books.length; i++) {
        const book = books[i];
        const bookDiv = document.createElement('div');
        bookDiv.className = 'book';
        
        const metadata = book.getElementsByTagName('metadata')[0];
        const title = metadata.getElementsByTagName('title')[0].textContent;
        const author = metadata.getElementsByTagName('author')[0].textContent;
        const year = metadata.getElementsByTagName('year')[0].textContent;
        const genre = metadata.getElementsByTagName('genre')[0].textContent;
        const pages = metadata.getElementsByTagName('pages')[0].textContent;
        
        const content = book.getElementsByTagName('content')[0];
        const facts = content.getElementsByTagName('fact');
        const themes = content.getElementsByTagName('theme');
        
        const analysis = book.getElementsByTagName('analysis')[0];
        const problems = analysis.getElementsByTagName('problem');
        const reviews = analysis.getElementsByTagName('review');
        
        bookDiv.innerHTML = `
            <h2 class="book-title">${title}</h2>
            <div class="book-author">${author}</div>
            
            <div class="book-details">
                <div class="detail-item">${year}</div>
                <div class="detail-item">${genre}</div>
                <div class="detail-item">${pages}</div>
            </div>
            
            <div class="description">
                <div class="facts">
                    <div class="section-title">Факты о книге:</div>
                    ${Array.from(facts).map(fact => `<div class="fact">${fact.textContent}</div>`).join('')}
                </div>
                
                <div class="themes">
                    <div class="section-title">Темы:</div>
                    ${Array.from(themes).map(theme => `<div class="theme">${theme.textContent}</div>`).join('')}
                </div>
                
                <div class="problems">
                    <div class="section-title">Основные проблемы:</div>
                    ${Array.from(problems).map(problem => `<div class="problem">${problem.textContent}</div>`).join('')}
                </div>
                
                <div class="reviews">
                    <div class="section-title">Рецензии:</div>
                    ${Array.from(reviews).map(review => `<div class="review">${review.textContent}</div>`).join('')}
                </div>
            </div>
        `;
        
        libraryDiv.appendChild(bookDiv);
        
        if (i < books.length - 1) {
            libraryDiv.appendChild(document.createElement('hr'));
        }
    }
}