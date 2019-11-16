const fs = require('fs')
const text = fs.readFileSync("test.txt", 'utf-8');
console.log(text);