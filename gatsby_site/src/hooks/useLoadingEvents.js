import { useState, useEffect } from 'react';

function useLoadingAllEvents(allEvents) {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (allEvents.length > 0) {
      const timeoutRef = setTimeout(() => {
        setIsLoading(false);
      }, 750);

      return () => clearTimeout(timeoutRef);
    }

    return undefined;
  }, [allEvents]);

  return isLoading;
}

export default useLoadingAllEvents;
