import React, { Component } from 'react';
import XMLParser from 'xml-js';
import { Key } from '../../Utils';
import EventsList from '../EventsList';
import EventItem from '../EventItem';

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
      <EventsList>
        {this.state.xmlContent ?
          this.state.xmlContent.event.map(ev =>
            (
              <EventItem key={Key.getShortKey()} ev={ev} />
            )) :
          <p>Loading XML data...</p>}
      </EventsList>
    );
  }
}

export default Fetcher;
