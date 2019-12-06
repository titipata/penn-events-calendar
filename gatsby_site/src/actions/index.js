const toggleSelectedEvent = (store, selectedEventId) => {
  const { selectedEvents } = store.state;

  store.setState({
    selectedEvents: selectedEvents.includes(selectedEventId)
      ? selectedEvents.filter((x) => x !== selectedEventId)
      : [...selectedEvents, selectedEventId],
  });
};

const rehydrateStore = (store, storeObj) => {
  store.setState(storeObj);
};

export { toggleSelectedEvent, rehydrateStore };
