const endPoint = {
  baseURL: 'http://localhost:5001',
  eventEndpoint: '/api/v1/getevent',
  eventDays: '?days=',
  similarEventsEndpoint: '/api/v1/getsimilarevents/',
};

const definedDays = {
  maximumDays: 90,
  defaultDays: 14,
  dayPerWeek: 7,
  dayPerMonth: 30,
};

class API {
  static getEvent(days = definedDays.defaultDays) {
    return `${endPoint.baseURL}${endPoint.eventEndpoint}${endPoint.eventDays}${days}`;
  }

  static getSimilarEvents(id) {
    return `${endPoint.baseURL}${endPoint.similarEventsEndpoint}${id}`;
  }

  // Handle HTTP errors since fetch won't.
  static handleErrors(response) {
    if (!response.ok) {
      throw Error(response.statusText);
    }
    return response;
  }
}

class DataColor {
  static getCatColor(catStr) {
    const colorCode = {
      Exhibitions: '#ca8b65',
      'Career/Prof': '#ff7562',
      Academic: '#ffb51c',
      Other: '#2d174d',
      'Perf Arts': '#7c98b3',
      Literary: '#ff83bd',
      Community: '#fde583',
      Film: '#27567b',
      Social: '#8fc0e7',
      Health: '#3a8ba2',
      International: '#fae3d9',
      Religion: '#fbf1f1',
      Meetings: '#aaaaaa',
      CNI: '#49a9a6',
      'English Dept': '#a3e8dc',
    };

    return colorCode[catStr];
  }

  static getSchoolColor(catStr) {
    const colorCode = {
      'Medicine/Health System': '#f64242',
      'School of Engineering and Applied Science': '#ffb51c',
      'Computational Neuroscience Initiative': '#49a9a6',
      'English Department': '#a3e8dc',
    };

    return colorCode[catStr];
  }
}

export { API, DataColor };
