import { fetchEventsBegin, fetchEventsSuccess, fetchEventsError } from '../Actions';
import { XML } from '../Utils';

class API {
  constructor() {
    this.endPoint = {
      baseURL: 'http://www.upenn.edu/calendar-export',
      dayEndpoint: '/?showndays=',
    };
    this.default = {
      maximumDays: 90,
      defaultDays: 14,
      dayPerWeek: 7,
      dayPerMonth: 30,
    };
  }

  getDaysLink(days = this.default.defaultDays) {
    return `${this.endPoint.baseURL}${this.endPoint.dayEndpoint}${days}`;
  }

  // Handle HTTP errors since fetch won't.
  static handleErrors(response) {
    if (!response.ok) {
      throw Error(response.statusText);
    }
    return response;
  }

  static fetchEvents() {
    return (dispatch) => {
      dispatch(fetchEventsBegin());
      return fetch(this.getDaysLink())
        .then(API.handleErrors)
        .then(res => res.text())
        .then((xmlText) => {
          const xmlJson = XML.xml2json(xmlText).calendar;

          dispatch(fetchEventsSuccess(xmlJson));
          return xmlJson;
        })
        .catch(error => dispatch(fetchEventsError(error)));
    };
  }
}

class Category {
  static getColor(catStr) {
    const colorCode = {
      Exhibitions: '#49a9a6',
      'Career/Prof': '#a3e8dc',
      Academic: '#f64242',
      Other: '#ffb51c',
      'Perf Arts': '#ba2644',
      Literary: '#ff6b6b',
      Community: '#ff83bd',
      Film: '#aaaaaa',
      Social: '#61c0bf',
      Health: '#bbded6',
      International: '#fae3d9',
      Religion: '#ffb6b9',
      Meetings: '#7af0b7',
    };

    return colorCode[catStr];
  }
}

export { API, Category };
