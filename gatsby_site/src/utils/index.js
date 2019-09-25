import shortid from 'shortid';
import moment from 'moment';

class Key {
  static getShortKey() {
    return shortid.generate();
  }
}

class Datetime {
  static getMonthDay(dtStr) {
    return moment(dtStr).format('MM.DD').toString();
  }

  static getTime(timeStr) {
    // eslint-disable-next-line
    // console.log(timeStr);
    // console.log(moment(timeStr, 'HH:mm:ss'));

    return moment(timeStr, ['h:mA', 'h:m A', 'h:ma', 'h:m a', 'H:m']).format('hh:mm A');
  }

  static getAssumedEndtime(timeStr) {
    return moment(timeStr, ['h:mA', 'h:m A', 'h:ma', 'h:m a', 'H:m']).add(1, 'hour').format('hh:mm A');
  }

  static getDayMonthDate(timeStr) {
    return moment(timeStr, 'DD-MM-YYYY').format('ddd, MMM DD, YYYY');
  }
}

class Sort {
  // default to ascending
  static sortDate(event1, event2, desc = false) {
    const date1 = moment(event1.node.date_dt, 'DD-MM-YYYY');
    const date2 = moment(event2.node.date_dt, 'DD-MM-YYYY');

    return !desc
      ? date1 - date2
      : date2 - date1;
  }
}

class Events {
  // ---- preprocessing
  static filterEvents(eventArr) {
    return eventArr
      .filter(ev => ev.node.title) // filter events with no title out
      .filter(ev => ev.node.date_dt); // filter events with no date_dt out
  }

  static sortEvents(eventArr) {
    return Events.filterEvents(eventArr)
      .sort(Sort.sortDate); // sort dates ascendingly
  }

  static getFutureEvents(eventArr) {
    return Events.sortEvents(eventArr)
      // as the 'today' to compare has time as 00:00, all the actual events of 'today'
      // are filtered out, fix by subtract 'today' to compare out by 1
      .filter(x => moment(x.node.date_dt, 'DD-MM-YYYY') >= moment().subtract(1, 'day')); // filter only incoming dates
  }

  // normally just call this function should be enough
  static getPreprocessedEvents(eventArr, futureOnly = false) {
    return futureOnly
      ? Events.getFutureEvents(eventArr)
      : Events.sortEvents(eventArr);
  }

  // ---- grouping
  static groupByDate(preprocessedEventArr) {
    // get all dates from preprocessed event array
    const allDates = preprocessedEventArr
      .map(ev => ev.node.date_dt);
    // get sorted unique dates
    const uniqueDates = Array.from(new Set(allDates));
    // groupby date with reduce
    const groupbyDate = uniqueDates.reduce((acc, cur) => (
      [
        ...acc,
        {
          dateFormatted: Datetime.getDayMonthDate(cur),
          // group events with the current date and also has title
          events: preprocessedEventArr.filter(ev => ev.node.date_dt === cur && ev.node.title),
        },
      ]
    ), []);

    return groupbyDate;
  }
}

// get a random hex from input text
const getRandomColorFromText = (text) => {
  if (!text) {
    return '#000000';
  }

  const hex = text
    .split('')
    .map(x => (
      Number(x.charCodeAt(0))
    ).toString(16))
    .join('')
    .substring(1, 7);

  return `#${hex}`;
};

export {
  Events, Datetime, Key, getRandomColorFromText,
};
