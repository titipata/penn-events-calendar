const toggleSelectedEvent = (store, selectedEventId) => {
  const { selectedEvents } = store.state;

  store.setState({
    selectedEvents: selectedEvents.includes(selectedEventId)
      ? selectedEvents.filter(x => x !== selectedEventId)
      : [...selectedEvents, selectedEventId],
  });
};

const saveToLocalStorage = (store) => {
  console.log(`should save ${store} to localStorage here..`);
};

export { toggleSelectedEvent, saveToLocalStorage };
