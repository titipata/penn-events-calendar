import { FontAwesomeIcon as Fa } from '@fortawesome/react-fontawesome';
import PropTypes from 'prop-types';
import Pagination from 'rc-pagination';
import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { Events as evUtil, Key } from '../../utils';
import EventList from './EventList';

const StyledContainer = styled.div`
  margin-bottom: 2rem;
`;

const StyledSectionText = styled.div`
  padding-left: 1rem;
  /* text-align: center; */
`;

const StyledH2 = styled.h2`
  font-size: 1.75rem;
  font-weight: normal;
  color: #333;
  margin: 1rem 0;
`;

const EventsContainer = ({ allEvents, noEventDefaultText }) => {
  // local state
  const [currentPage, setCurrentPage] = useState(1);
  const [currentPageData, setCurrentPageData] = useState([]);

  // ---- manage pagination
  // get paginated events
  const paginatedEvents = evUtil.getPaginatedEvents(allEvents);
  // set current page data when currentPage and paginatedEvents is changed
  // as we use globalState to retrieve data from localStorage
  // we don't get the data right after the component is mounted
  // thus we also watch for `allEvents`
  useEffect(() => {
    const { data } = paginatedEvents.find(grp => grp.page === currentPage) || [];
    setCurrentPageData(evUtil.groupByDate(data));
  }, [currentPage, allEvents]);

  // ---- render no data screen
  if (allEvents.length === 0) {
    return (
      <StyledContainer>
        <p>{noEventDefaultText}</p>
      </StyledContainer>
    );
  }

  return (
    <>
      {
        currentPageData.map(grp => (
          <StyledContainer key={Key.getShortKey()}>
            <StyledSectionText>
              <StyledH2>
                <Fa icon="calendar-alt" />
                &nbsp;&nbsp;
                {grp.dateFormatted}
              </StyledH2>
            </StyledSectionText>
            <EventList
              groupedEvents={grp.events}
            />
          </StyledContainer>
        ))
      }
      <Pagination
        onChange={nextPage => setCurrentPage(nextPage)}
        current={currentPage}
        total={allEvents.length - 1}
        pageSize={30}
      />
    </>
  );
};

EventsContainer.propTypes = {
  // allEvents is supposed to be preprocessed already
  // including filter incomplete data out and sort by date ascendingly
  allEvents: PropTypes.arrayOf(Object).isRequired,
  noEventDefaultText: PropTypes.string,
};

EventsContainer.defaultProps = {
  noEventDefaultText: null,
};

export default EventsContainer;
