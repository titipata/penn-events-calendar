import PropTypes from 'prop-types';
import { Component } from 'react';
import { connect } from 'react-redux';
import { fetchEventsBegin, fetchEventsError, fetchEventsSuccess } from '../../Actions';
import { API } from '../../Data';
import { XML } from '../../Utils';

// This component is used to fetch data only

// Event keys:
// ["date", "starttime", "endtime", "title", "description", "location",
// "room", "url", "student", "privacy", "category", "school", "owner", "link"]
class Fetcher extends Component {
  componentDidMount() {
    this.getData();
  }

  getData() {
    this.props.fetchEventsBegin();

    fetch(API.getDaysLink())
      .then(API.handleErrors)
      .then(res => res.text())
      .then((xmlText) => {
        const fetchedEvents = XML.xml2json(xmlText).calendar.event;

        this.props.fetchEventsSuccess(fetchedEvents);
      })
      .catch(err => this.props.fetchEventsError(err));
  }

  render() {
    return null;
  }
}

Fetcher.propTypes = {
  fetchEventsBegin: PropTypes.func.isRequired,
  fetchEventsSuccess: PropTypes.func.isRequired,
  fetchEventsError: PropTypes.func.isRequired,
};

const mapDispatchToProps = dispatch => ({
  fetchEventsBegin: () => dispatch(fetchEventsBegin()),
  fetchEventsSuccess: xmlJson => dispatch(fetchEventsSuccess(xmlJson)),
  fetchEventsError: error => dispatch(fetchEventsError(error)),
});

export default connect(
  null,
  mapDispatchToProps,
)(Fetcher);
