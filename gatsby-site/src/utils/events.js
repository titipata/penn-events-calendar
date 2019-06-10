import { Datetime } from '.';

class Events {
  static getText(eventItem) {
    return {
      date: eventItem.date._text,
      starttime: eventItem.starttime._text,
      endtime: eventItem.endtime._text,
      title: eventItem.title._text,
      description: eventItem.description._text,
      location: eventItem.location._text,
      room: eventItem.room._text,
      url: eventItem.url._text,
      student: eventItem.student._text,
      privacy: eventItem.privacy._text,
      category: eventItem.category._text,
      school: eventItem.school._text,
      owner: eventItem.owner._text,
      link: eventItem.link._text,
    };
  }

  static getId(eventItem) {
    return eventItem.link._attributes.id;
  }

  static groupByDate(eventArr) {
    // get all dates from events
    const allDates = eventArr.map(ev => ev.date);
    // get only unique dates
    const uniqueDates = [...new Set(allDates)];
    // groupby date with reduce
    const groupbyDate = uniqueDates.reduce((acc, cur) => (
      [
        ...acc,
        {
          dateFormatted: Datetime.getDayMonthDate(cur),
          events: eventArr.filter(ev => ev.date === cur),
        },
      ]
    ), []);

    return groupbyDate;
  }
}

export default Events;
