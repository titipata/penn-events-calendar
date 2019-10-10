import { useState, useEffect } from 'react';

function useLoadingAllEvents(allEvents) {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (allEvents.length > 0) {
      setTimeout(() => {
        setIsLoading(false);
      }, 750);
    }
  }, [allEvents]);

  return isLoading;
}

export default useLoadingAllEvents;
