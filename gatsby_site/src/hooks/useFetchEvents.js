import { useState, useEffect } from 'react';
import useLoadingEvents from './useLoadingEvents';
import { Events as evUtil } from '../utils';

function useFetchEvents(endpoint, payload) {
  const [fetchedEvents, setFetchedEvents] = useState([]);
  const [isLoading, setIsLoading] = useLoadingEvents(fetchedEvents);
  const [fetchOption, setFetchOption] = useState(null);

  useEffect(() => {
    setFetchOption(payload
      ? {
        method: 'POST',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          payload,
        }),
      }
      : {
        method: 'GET',
      });
  }, [payload]);

  useEffect(() => {
    if (!fetchOption) return;

    fetch(endpoint, fetchOption)
      .then(res => res.json())
      .then((resJson) => {
        // stop here if there is no data
        if (!resJson || resJson.length === 0) {
          // set loading is done
          setIsLoading(false);
          return;
        }

        // need to add event data into node here
        const filteredData = evUtil.getPreprocessedEvents(
          resJson.map(x => ({ node: x })),
        );

        // add to global state
        setFetchedEvents(filteredData);
      })
      // eslint-disable-next-line
      .catch(err => console.log(err));
  }, [endpoint, fetchOption, setIsLoading]);

  return [fetchedEvents, isLoading];
}

export default useFetchEvents;
