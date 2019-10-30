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
  static sortDate(dt1, dt2, desc = false) {
    const date1 = moment(dt1, 'DD-MM-YYYY');
    const date2 = moment(dt2, 'DD-MM-YYYY');

    return !desc
      ? date1 - date2
      : date2 - date1;
  }

  static sortStarttime(event1, event2, desc = false) {
    const time1 = moment(event1.starttime, ['h:mA', 'h:m A', 'h:ma', 'h:m a', 'H:m']);
    const time2 = moment(event2.starttime, ['h:mA', 'h:m A', 'h:ma', 'h:m a', 'H:m']);

    // for invalid time (all day or none)
    if (!time1.isValid()) {
      return !desc ? 1 : -1;
    }
    if (!time2.isValid()) {
      return !desc ? -1 : 1;
    }

    return !desc
      ? time1 - time2
      : time2 - time1;
  }

  static sortOwner(event1, event2, desc = false) {
    const owner1 = event1.owner;
    const owner2 = event2.owner;

    return owner1 === owner2
      ? 0
      : !desc
        ? owner1 > owner2
          ? 1
          : -1
        : owner1 < owner2
          ? 1
          : -1;
  }
}

class Events {
  // ---- preprocessing
  static filterEvents(eventArr) {
    return eventArr
      .filter(ev => ev.title) // filter events with no title out
      .filter(ev => ev.date_dt); // filter events with no date_dt out
  }

  static sortEvents(eventArr) {
    return Events.filterEvents(eventArr)
      .sort((ev1, ev2) => Sort.sortDate(
        ev1.date_dt,
        ev2.date_dt,
      ) // sort dates ascendingly
        || Sort.sortStarttime(ev1, ev2) // sort starttime ascendingly
        || Sort.sortOwner(ev1, ev2)); // sort owner ascendingly
  }

  static getFutureEvents(eventArr) {
    return Events.sortEvents(eventArr)
      // as the 'today' to compare has time as 00:00, all the actual events of 'today'
      // are filtered out, fix by subtract 'today' to compare out by 1
      .filter(x => moment(x.date_dt, 'DD-MM-YYYY') >= moment().subtract(1, 'day')); // filter only incoming dates
  }

  // normally just call this function should be enough
  static getPreprocessedEvents(eventArr, futureOnly = false) {
    return futureOnly
      ? Events.getFutureEvents(eventArr)
      : Events.sortEvents(eventArr);
  }

  // ---- grouping
  static groupByDate(preprocessedEventArr) {
    // right after mounting, the data is not yet derived
    if (!preprocessedEventArr || preprocessedEventArr.length === 0) {
      return [];
    }

    // get all dates from preprocessed event array
    const allDates = preprocessedEventArr
      .map(ev => ev.date_dt);
    // get sorted unique dates
    const uniqueDates = Array.from(new Set(allDates)).sort(Sort.sortDate);

    // groupby date with reduce
    const groupbyDate = uniqueDates.reduce((acc, cur) => (
      [
        ...acc,
        {
          dateFormatted: Datetime.getDayMonthDate(cur),
          // group events with the current date and also has title
          events: preprocessedEventArr.filter(ev => ev.date_dt === cur && ev.title),
        },
      ]
    ), []);

    return groupbyDate;
  }

  // paginate structure:
  // [
  //   {
  //     page: x,
  //     data: [ev1, ev2, ev3],
  //   },
  //   {
  //     page: y,
  //     data: [ev4, ev5, ev6],
  //   },
  // ]
  // maxItemsPerPage is default at 30
  static getPaginatedEvents(preprocessedEventArr, maxItemsPerPage = 30) {
    const totalPage = Math.ceil(preprocessedEventArr.length / maxItemsPerPage);
    const paginatedEvents = [...Array(totalPage)].map((_, ind) => ({
      page: ind + 1,
      data: preprocessedEventArr
        .slice(
          ind * maxItemsPerPage,
          maxItemsPerPage * (ind + 1),
        ),
    }));

    return paginatedEvents;
  }

  static getUrlToAddEventToCalendar(eventObj) {
    // todo: revise & refactor this function
    // console.log('evobj', eventObj);
    if (!eventObj) return null;

    const isoFormat = 'YYYYMMDDTHHmmss[Z]';
    const dateOnlyFormat = 'YYYYMMDD';

    const formatDateTime = dt => dt.utc().format(isoFormat);

    let formattedStartTime = '';
    let formattedEndTime = '';

    const {
      date_dt: date,
      starttime: startTime,
      endtime: endTime,
      title,
      location,
      description,
    } = eventObj;

    // if allday or have no starttime - starttime/endtime should not contain
    // T...Z part and the end date should + 1 day
    // if only starttime present, assume 1 hour event

    // assume all day
    if (!startTime || startTime.toLowerCase().includes('all day')) {
      const parsed = moment(`${date}`, 'DD-MM-YYYY');
      formattedStartTime = parsed.format(dateOnlyFormat);
      formattedEndTime = parsed.add(1, 'd').format(dateOnlyFormat);
    }
    // assume 1 hr event
    if (startTime && !endTime) {
      const parsed = moment(`${date} ${startTime}`, 'DD-MM-YYYY hh:mma');
      formattedStartTime = formatDateTime(parsed);
      formattedEndTime = formatDateTime(parsed.add(1, 'h'));
    }
    // complete data
    if (startTime && endTime) {
      const parsedStart = moment(`${date} ${startTime}`, 'DD-MM-YYYY hh:mma');
      const parsedEnd = moment(`${date} ${endTime}`, 'DD-MM-YYYY hh:mma');
      formattedStartTime = formatDateTime(parsedStart);
      formattedEndTime = formatDateTime(parsedEnd);
    }

    let calendarUrl = 'https://calendar.google.com/calendar/render';
    calendarUrl += '?action=TEMPLATE';
    calendarUrl += `&dates=${formattedStartTime}`;
    calendarUrl += `/${formattedEndTime}`;
    calendarUrl += `&location=${encodeURIComponent(location)}`;
    calendarUrl += `&text=${encodeURIComponent(title)}`;
    calendarUrl += `&details=${encodeURIComponent(description)}`;

    return calendarUrl;
  }
}

// https://github.com/jasonsalzman/react-add-to-calendar/blob/master/src/helpers/index.js#L97-L114
const isMobile = () => {
  const testAgent = window.navigator.userAgent || window.navigator.vendor || window.opera;
  /* eslint-disable */
  const pattern1 = /(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i;
  const pattern2 = /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i;
  /* eslint-enable */

  let mobile = false;

  if (pattern1.test(testAgent) || pattern2.test(testAgent.substr(0, 4))) {
    mobile = true;
  }

  return mobile;
};

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
  Events, Datetime, Key, getRandomColorFromText, isMobile,
};
