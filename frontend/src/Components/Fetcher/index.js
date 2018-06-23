import React, { Component } from 'react';
import XMLParser from 'xml-js';
import { Key } from '../../Utils';

// define xml2json function
const xml2json = xml => JSON.parse(XMLParser.xml2json(xml, { compact: true, spaces: 2 }));

// Event keys:
// ["date", "starttime", "endtime", "title", "description", "location",
// "room", "url", "student", "privacy", "category", "school", "owner", "link"]
class Fetcher extends Component {
  constructor(props) {
    super(props);
    this.state = {
      xmlQueryURL: 'http://www.upenn.edu/calendar-export/?showndays=20',
      xmlContent: '',
    };
  }

  componentDidMount() {
    this._getData();
  }

  _getData() {
    fetch(this.state.xmlQueryURL)
      .then(res => res.text())
      .then((xmlText) => {
        this.setState({
          xmlContent: xml2json(xmlText).calendar,
        });
        // console.log(Object.keys(this.state.xmlContent.event[0]));
      });
  }

  render() {
    return (
      <ul>
        {this.state.xmlContent ?
          this.state.xmlContent.event.map(ev =>
            (
              <li key={Key.getShortKey()}>
                <div style={{ paddingBottom: '10px' }}>
                  School: {ev.school._text} <br/>
                  Title: {ev.title._text} <br/>
                  Datetime: {ev.date._text}: {ev.starttime._text}-{ev.endtime._text} <br/>
                  Location: Room {ev.room._text}, {ev.location._text} <br/>
                  Owner: {ev.owner._text} <br/>
                  URL: <a href={ev.url._text}>{ev.url._text}</a>
                </div>
              </li>
            )) :
          <p>Loading XML data...</p>}
      </ul>
    );
  }
}

export default Fetcher;
