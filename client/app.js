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
        action: 'get_index',
        listentype: 'diff',
        channel: 'unset'
      },
      success: function(res) {
        that.globalData.indexData = {}
        that.globalData.indexData.feed = res.data.resp.feed
        that.globalData.indexData.feed_next = res.data.resp.feed_next
        wx.setStorageSync("index_feed_data", that.globalData.indexData.feed)
      }
    })

    r({
      data: {
        action: 'get_explore',
        last_audio_id: ''
      },
      success: function(res) {
        that.globalData.exploreData = {}
        that.globalData.exploreData.feeds = res.data.resp.feeds
      }
    })

    r({
      data: {
        action: 'get_user_info',
      },
      success: function(res) {
        that.globalData.myData = {}
        that.globalData.myData.userInfo = res.data
      }
    })

    r({
      data: {
        action: 'get_my_feed',
        last_audio_id: ''
      },
      success: function(res) {
        that.globalData.myData.feeds = res.data.resp.feeds
      }
    })

    r({
      data: {
        action: 'get_medal',
        last_audio_id: ''
      },
      success: function(res) {
        that.globalData.myData.medal = res.data.resp.medals
      }
    })

    log(that.globalData)
  }
})