import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';
import { Key } from '../../Utils';
import EventItem from './EventItem';
import EventsList from './EventsList';

const EvenstContainer = ({ events, loading, error }) => {
  if (error) {
    return (
      <div>Error! {error.message}</div>
    );
  }

  return (
    <EventsList>
      {!loading ?
        events.map(ev =>
          (
            <EventItem key={Key.getShortKey()} ev={ev} />
          )) :
        <p>Loading XML data...</p>}
    </EventsList>
  );
};

EvenstContainer.propTypes = {
  events: PropTypes.arrayOf(Object).isRequired,
  loading: PropTypes.bool.isRequired,
  error: PropTypes.object,
};

EvenstContainer.defaultProps = {
  error: false,
};

const mapStateToProps = state => ({
  events: state.events.items,
  loading: state.events.loading,
  error: state.events.error,
});

export default connect(mapStateToProps)(EvenstContainer);
