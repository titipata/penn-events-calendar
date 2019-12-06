import { useState, useEffect } from 'react';
import { Events as evUtil } from '../utils';

// define constant for events per page
const EVENT_PER_PAGE = 30;

function usePagination(eventsArray = null) {
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPage, setTotalPage] = useState(null);
  const [currentPageData, setCurrentPageData] = useState([]);

  // for frontpage fetching
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // if there is an eventsArray, it is not a homepage
    if (eventsArray) {
      return;
    }

    setIsLoading(true);
    fetch(`/api/pagination?page=${currentPage}`)
      .then((res) => res.json())
      .then((resJson) => {
        const { total, data } = resJson;

        // set total page
        setTotalPage(total);

        // preprocess events before sending to events list
        const preprocessedEvents = evUtil.getPreprocessedEvents(
          data
            // filter should have been done
            // .filter(x => x.title)
            .map((x) => ({ node: x })),
          true,
        );

        // set current page data
        setCurrentPageData(preprocessedEvents);
        // stop is loading
        setIsLoading(false);
      });
  }, [currentPage, eventsArray]);

  useEffect(() => {
    // do not run this effect if there is no eventsArray
    if (!eventsArray) {
      return;
    }

    // set total page
    setTotalPage(Math.ceil(eventsArray.length / EVENT_PER_PAGE));

    // get indexes of data of this page
    const startInd = EVENT_PER_PAGE * (currentPage - 1);
    const endInd = EVENT_PER_PAGE * currentPage;

    // set current page data
    setCurrentPageData(eventsArray.slice(startInd, endInd));
  }, [currentPage, eventsArray]);

  return [currentPageData, totalPage, setCurrentPage, isLoading];
}

export default usePagination;
