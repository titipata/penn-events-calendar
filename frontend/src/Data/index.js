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

export { Category };
