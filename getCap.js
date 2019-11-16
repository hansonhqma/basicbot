const reader = new XMLHttpRequest() || new ActiveXObject('MSXML2.XMLHTTP');

function loadFile() {
    reader.open('get', 'test.txt', true);
    reader.onreadystatechange = displayContents;
    reader.send(null);
}

function displayContents() {
        document.getElementById('box').value = reader.responseText;
}