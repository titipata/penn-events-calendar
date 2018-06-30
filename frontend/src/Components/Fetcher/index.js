import React, { Component } from 'react';
// import XMLParser from 'xml-js';
import { Key } from '../../Utils';
import EventsList from '../EventsList';
import EventItem from '../EventItem';
// import { Fetcher as ff } from '../../Data';
import { API } from '../../Data';
import { connect } from 'react-redux';
import { consolidateStreamedStyles } from 'styled-components';

// define xml2json function
// const xml2json = xml => JSON.parse(XMLParser.xml2json(xml, { compact: true, spaces: 2 }));

// Event keys:
// ["date", "starttime", "endtime", "title", "description", "location",
// "room", "url", "student", "privacy", "category", "school", "owner", "link"]
class Fetcher extends Component {
  // constructor(props) {
  //   super(props);
  //   this.state = {
  //     xmlQueryURL: 'http://www.upenn.edu/calendar-export/?showndays=20',
  //     xmlContent: '',
  //   };
  // }

  componentDidMount() {
    // console.log('---dispatch:', this.props.dispatch);
    // console.log('---:', API.fetchEvents());
    this.props.dispatch(API.fetchEvents());
    // this._getData();
  }

  // _getData() {
  // this.setState({
  //   xmlContent: ff.getData(),
  // });
  // fetch(this.state.xmlQueryURL)
  //   .then(res => res.text())
  //   .then((xmlText) => {
  //     this.setState({
  //       xmlContent: xml2json(xmlText).calendar,
  //     });
  //     // console.log(Object.keys(this.state.xmlContent.event[0]));
  //   });
  // }

  render() {
    return (
      <EventsList>
        {this.props.events ?
          this.props.events.event.map(ev =>
            (
              <EventItem key={Key.getShortKey()} ev={ev} />
            )) :
          <p>Loading XML data...</p>}
      </EventsList>
    );
  }
}

const mapStateToProps = state => ({
  events: state.events.items,
  loading: state.events.loading,
  error: state.events.error,
});

export default connect(mapStateToProps)(Fetcher);

// export default Fetcher;
