//app.js
const c = require('/utils/c.js')

App({
  onLaunch: function () {
    c.login();
  },
  globalData: {

  }
})