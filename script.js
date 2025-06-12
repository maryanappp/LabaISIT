function loadXML() {
    let xhr = new XMLHttpRequest();
    xhr.open("GET", "book.xml", true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            parseXML(xhr.responseXML);
        }
    };
    xhr.send();
}

function parseXML(xml) {
    let index = document.getElementById("bookIndex").value;
    let books = xml.getElementsByTagName("book");
    
    if (index < 1 || index > books.length) {
        document.getElementById("output").innerHTML = "<p>Некорректный номер книги</p>";
        return;
    }

    let book = books[index - 1]; 
    let details = book.getElementsByTagName("details")[0].children;
    let facts = book.getElementsByTagName("fact");
    let problems = book.getElementsByTagName("problem");

    let output = `<h2>Детали книги</h2><ul>`;
    for (let detail of details) {
        output += `<li><strong>${detail.tagName}:</strong> ${detail.textContent}</li>`;
    }
    output += `</ul><h3>Факты</h3><ul>`;
    for (let fact of facts) {
        output += `<li>${fact.textContent}</li>`;
    }
    output += `</ul><h3>Проблемы</h3><ul>`;
    for (let problem of problems) {
        output += `<li>${problem.textContent}</li>`;
    }
    output += `</ul>`;

    document.getElementById("output").innerHTML = output;
}
