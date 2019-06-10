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
    return moment(timeStr).format('ddd, MMM DD');
  }
}

export { Datetime, Key };
