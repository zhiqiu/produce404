//app.js
'use strict'

const c = require('/utils/c.js')
const r = c.r;
const log = console.log;

App({
  onLaunch: function() {
    c.login();

  },

  globalData: {
    checkAPI: require('/utils/api_test.js'),
    //首页数据
    indexData: {
      feed: {},
      feed_next: {},
    },
    //发现页数据
    exploreData: {
      feeds: [],
    },
    //我的页数据
    myData: {
      userInfo: {
        name: '',
        age: '',
        gender: '',
        address: '',
        birthday: '',
        create_time: '',
        deleted: false,
        openid: "openid1"
      },
      feeds: [], //我的Feed
      collection: [],
      medal: [],
      //我的消息
      //系统消息
      //我的赞
    },
    tag: [],
  },

  initGlobalData: function() {
    var that = this;


    r({
      data: {
        action: 'get_my_feed',
        last_audio_id: ''
      },
      success: function(res) {
        that.globalData.myData.feeds = res.data.resp.feeds
      }
    })

    

    log(that.globalData)
  }
})