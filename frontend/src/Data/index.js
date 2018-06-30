const endPoint = {
  baseURL: 'http://www.upenn.edu/calendar-export',
  dayEndpoint: '/?showndays=',
};

const definedDays = {
  maximumDays: 90,
  defaultDays: 14,
  dayPerWeek: 7,
  dayPerMonth: 30,
};
class API {
  static getDaysLink(days = definedDays.defaultDays) {
    return `${endPoint.baseURL}${endPoint.dayEndpoint}${days}`;
  }

  // Handle HTTP errors since fetch won't.
  static handleErrors(response) {
    if (!response.ok) {
      throw Error(response.statusText);
    }
    return response;
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
