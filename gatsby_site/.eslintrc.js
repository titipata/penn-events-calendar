module.exports = {
  extends: [
    "airbnb",
    "react-app",
  ],
  plugins: [
    "react",
    "react-hooks",
    "jest",
  ],
  parser: "babel-eslint",
  rules: {
    "no-nested-ternary": "off",
    "react/jsx-filename-extension": [1, { "extensions": [".js", ".jsx"] }],
    "no-underscore-dangle": 0,
    "react/prop-types": ["error", { "ignore": ["navigation", "data"] }],
    "global-require": 0,
    "react-hooks/rules-of-hooks": "error",
    "react-hooks/exhaustive-deps": "warn",
  },
  globals: {
    __PATH_PREFIX__: true,
  },
  env: {
    "jest/globals": true,
  },
}
