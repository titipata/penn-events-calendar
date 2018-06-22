import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import registerServiceWorker from './registerServiceWorker';

ReactDOM.render(<App />, document.getElementById('root'));
registerServiceWorker();


var xml2js = require('xml2js');
var parser = new xml2js.Parser();
const http = require('http');

var xml = `
<event>
    <date>2015-02-07</date>
    <starttime/>
    <endtime/>
    <title>Beneath the Surface: Life, Death and Gold in Ancient Panama</title>
    <description>Spectacular finds at a Precolumbian cemetery in central Panama are featured  in Beneath the Surface, a new exhibition which sheds light on a mysterious and complex society that thrived there more than 1,000 years ago.</description>
    <location>Penn Museum</location>
    <room/>
    <url>http://www.penn.museum/beneath/</url>
    <student>0</student>
    <privacy>0</privacy>
    <category id="5">Exhibitions</category>
    <school id="13">Events that fall outside the boundaries of defined schools.</school>
    <owner id="16">University Museum</owner>
    <link id="62279273">http://www.upenn.edu/calendar/?event=62279273</link>
</event>
`

var parseString = require('xml2js').parseString;
parseString(xml, function (err, result) {
    console.dir(result);
});

console.log('test parsing XML');


// fetching XML
var query_url = 'http://www.upenn.edu/calendar-export/?showndays=2';
var xhr = new XMLHttpRequest();
xhr.open('POST', query_url);
console.log('OPENED', xhr);
console.log('OPENED', xhr.status);

parseString(xhr, function (err, result) {
    console.dir(result);
});
