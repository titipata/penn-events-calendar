import { FontAwesomeIcon as Fa } from '@fortawesome/react-fontawesome';
import PropTypes from 'prop-types';
import Pagination from 'rc-pagination';
import localeInfo from 'rc-pagination/lib/locale/en_US';
import React, { useState } from 'react';
import styled from 'styled-components';
import { Events as evUtil, Key } from '../../utils';
import EventList from './EventList';
import { media } from '../../utils/ui';
import LoadingView from '../BaseComponents/LoadingView';

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

const EventsContainer = ({
  currentPageEvents,
  noOfPages,
  noEventDefaultText,
  isLoading,
  handlePagination,
}) => {
  // also keep track of page in local state
  const [currentPage, setCurrentPage] = useState(1);

  // ---- render no data screen
  if (isLoading) {
    return (
      <StyledContainer>
        <LoadingView />
      </StyledContainer>
    );
  }

  if (currentPageEvents.length === 0) {
    return (
      <StyledContainer>
        <p>{noEventDefaultText}</p>
      </StyledContainer>
    );
  }

  return (
    <>
      {
        evUtil.groupByDate(currentPageEvents).map(grp => (
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
            handlePagination(nextPage);
            setCurrentPage(nextPage);
            window.scrollTo(0, 0);
          }}
          current={currentPage}
          total={30 * noOfPages}
          pageSize={30}
          hideOnSinglePage
          locale={localeInfo}
        />
      </PaginationWrapper>
    </>
  );
};

EventsContainer.propTypes = {
  // currentPageEvents is supposed to be preprocessed already
  // including filter incomplete data out and sort by date ascendingly
  currentPageEvents: PropTypes.arrayOf(Object).isRequired,
  noOfPages: PropTypes.number,
  noEventDefaultText: PropTypes.string,
  isLoading: PropTypes.bool.isRequired,
  handlePagination: PropTypes.func,
};

EventsContainer.defaultProps = {
  noEventDefaultText: null,
  noOfPages: 0,
  handlePagination: () => {},
};

export default EventsContainer;
