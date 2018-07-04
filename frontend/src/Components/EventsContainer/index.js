import { FontAwesomeIcon as Fa } from '@fortawesome/react-fontawesome';
import PropTypes from 'prop-types';
import React from 'react';
import { connect } from 'react-redux';
import { Key, Events as evUtil } from '../../Utils';
import EventsList from './EventsList';
import styled from 'styled-components';

const StyledSectionText = styled.div`
  font-family: 'Source Code Pro';
  font-size: 1.75rem;
  font-weight: bold;
  color: #222;
  /* text-align: center; */
`;

const EvenstContainer = ({ events, loading, error }) => {
  // group by date usage
  // console.log('gbd:', evUtil.groupByDate(events));

  if (error) {
    return (
      <div>Error! {error.message}</div>
    );
  }

  return (
    <React.Fragment>
      {!loading ?
        evUtil.groupByDate(events).map(grp =>
          (
            <React.Fragment key={Key.getShortKey()}>
              <StyledSectionText>
                <Fa icon="calendar-alt" />
                &nbsp;
                {grp.dateFormatted}
              </StyledSectionText>
              <EventsList events={grp.events} />
            </React.Fragment>
          )) :
        <p>Loading XML data...</p>}
    </React.Fragment>
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
