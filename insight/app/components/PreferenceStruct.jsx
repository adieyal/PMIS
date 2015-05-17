var immstruct = require('immstruct');

var today = new Date();
var month = today.getMonth() + 1;

if(month < 10) {
    month = '0' + month;
}

var structure = immstruct({
    order: 'alphabetic',
    year: today.getFullYear(),
    month: month
});

module.exports = structure;
