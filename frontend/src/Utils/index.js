import shortid from 'shortid';

class Key {
  static getShortKey() {
    return shortid.generate();
  }
}

export { Key };
