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
    // console.log(moment(timeStr, 'HH:mm:ss').format('LT'));
    return moment(timeStr, 'HH:mm:ss').format('HH:MM A');
  }

  static getDayMonthDate(timeStr) {
    return moment(timeStr, 'DD-MM-YYYY').format('ddd, MMM DD, YYYY');
  }
}

class Events {
  static groupByDate(eventArr) {
    // get all dates from events
    const allDates = eventArr
      .map(ev => ev.node.date_dt)
      .filter(x => x) // filter blank dates out
      .sort((a, b) => (moment(a, 'DD-MM-YYYY') - moment(b, 'DD-MM-YYYY'))) // sort dates
      .filter(x => moment(x, 'DD-MM-YYYY') >= moment()); // filter only incoming dates

    // get sorted unique dates
    const uniqueDates = Array.from(new Set(allDates));
    // groupby date with reduce
    const groupbyDate = uniqueDates.reduce((acc, cur) => (
      [
        ...acc,
        {
          dateFormatted: Datetime.getDayMonthDate(cur),
          events: eventArr.filter(ev => ev.node.date_dt === cur),
        },
      ]
    ), []);

    return groupbyDate;
  }
}

export { Events, Datetime, Key };
