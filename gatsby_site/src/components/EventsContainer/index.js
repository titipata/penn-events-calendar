import { FontAwesomeIcon as Fa } from '@fortawesome/react-fontawesome';
import PropTypes from 'prop-types';
import Pagination from 'rc-pagination';
import localeInfo from 'rc-pagination/lib/locale/en_US';
import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import { Events as evUtil, Key } from '../../utils';
import EventList from './EventList';
import { media } from '../../utils/ui';

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

const StyledPagination = styled(Pagination)`
  transform: scale(1.25);
  margin: 10px 15px 20px;
  display: flex;
  flex: initial;
  width: auto;
  justify-content: center;
  align-items: center;
  li {
    outline: none;
    margin-bottom: 0;
  }
  ${media.extraSmall`
    transform: scale(1.05);
  `}
`;

const PaginationWrapper = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
`;

const EventsContainer = ({ allEvents, noEventDefaultText }) => {
  // local state
  const [currentPage, setCurrentPage] = useState(1);
  const [currentPageData, setCurrentPageData] = useState([]);
  const [paginatedEvents, setPaginatedEvents] = useState([]);

  // ---- manage pagination
  // set current page data when currentPage and paginatedEvents is changed
  // as we use globalState to retrieve data from localStorage
  // we don't get the data right after the component is mounted
  // thus we also watch for `allEvents`
  useEffect(() => {
    setPaginatedEvents(evUtil.getPaginatedEvents(allEvents));
  }, [allEvents]);

  useEffect(() => {
    const { data } = paginatedEvents.find(grp => grp.page === currentPage) || [];
    setCurrentPageData(evUtil.groupByDate(data));
  }, [currentPage, paginatedEvents]);

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
      <PaginationWrapper>
        <StyledPagination
          onChange={(nextPage) => {
            setCurrentPage(nextPage);
            window.scrollTo(0, 0);
          }}
          current={currentPage}
          total={allEvents.length - 1}
          pageSize={30}
          hideOnSinglePage
          locale={localeInfo}
        />
      </PaginationWrapper>
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
