/*声觅主页面*/
// pages/index_page/index_page.js
const c = require('../../utils/c.js');
const r = c.r;


Page({
  data: {
    feed: {},
    last_feed: {},
    paused: false,
    listentype: 'like', // diff or like
    channel: 'unset', // unset or channelname
    dataloaded: false,
    tagArray: c.tagArray,
    animationData: "",
    showModalStatus: false,
    imageHeight: 0,
    imageWidth: 0,
  },

  getData: function(callback) {
    this.setData({
      last_feed: this.data.feed
    })
    var that = this;
    r({
      data: {
        action: 'get_index',
        listentype: that.data.listentype,
        channel: that.data.channel
      },
      success: function(res) {
        console.log(res)
        if(res.data.resp)
        {
          that.setData({
            feed: res.data.resp.feed,
            dataloaded: true
          })
        }
        // TODO: feed_next
        callback();
      }
    })
    console.log(that)
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    if (!c.check()) return; // check login
    var that = this;
    this.getData(function () {
      c.play(that.data.feed.audio, that.data.feed.user);
      const player = wx.getBackgroundAudioManager();
      player.onTimeUpdate(function () {
        that.setData({
          audioProgress: parseInt(100 * player.currentTime / player.duration)
        })
      })
      player.onPause(function(){
        that.setData({
          paused: true
        })
      })
      player.onPlay(function(){
        that.setData({
          paused: false
        })
      })
      player.onNext(function(){
        that.gotoNext();
      })
      player.onPrev(function(){
        that.gotoPrevious();
      })
      player.onEnded(function(){
        that.gotoPrevious();
      })
      that.setData({
        paused: false
      })
    });
    console.log(this)
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function() {
    var that = this;
    if(this.data.feed.audio){
      r({
        data:{
          action: 'get_one_feed',
          audio_id: this.data.feed.audio.audio_id
        },
        success: function(res){
          that.setData({
            feed: res.data.resp.feed
          })
        }
      })
    }
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function() {
    var player = wx.getBackgroundAudioManager()
    player.onEnded(function(){

    })
  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function(options) {
    return {
      title: '声觅',
      path: '/pages/login_page/login_page',
      // imageUrl
    }
  },
  playorpause: function() {
    c.playorpause();
    this.setData({
      paused: !this.data.paused
    })
  },
  listenDiffToggle: function() {
    this.setData({
      listentype: this.data.listentype === 'like' ? 'diff' : 'like'
    })
    var that = this;
    this.getData(function() {
      c.play(that.data.feed.audio, that.data.feed.user);
      const player = wx.getBackgroundAudioManager();
      player.onTimeUpdate(function() {
        that.setData({
          audioProgress: parseInt(100 * player.currentTime / player.duration)
        })
      })
      that.setData({
        paused: false
      })
    });
  },
  like: function() {
    var nowFeed = this.data.feed;
    nowFeed.isliked = true;
    nowFeed.like_num += 1;
    this.setData({
      feed: nowFeed
    })
    r({
      data: {
        action: 'like_audio',
        audio_id: this.data.feed.audio.audio_id
      }
    })
  },
  dislike: function() {
    var nowFeed = this.data.feed;
    nowFeed.isliked = false;
    nowFeed.like_num -= 1;
    this.setData({
      feed: nowFeed
    })
    r({
      data: {
        action: 'dislike_audio',
        audio_id: this.data.feed.audio.audio_id
      }
    })
  },

  gotoComments: function() {
    var audioId = this.data.feed.audio.audio_id;
    console.log(audioId)
    getApp().globalData.prePage = this
    wx.navigateTo({
      url: '/pages/community/detail?audioId=' + audioId
    })
  },

  gotoAddCollection: function(e) {
    var dID = e.currentTarget.id;
    getApp().globalData.prePage = this
    wx.navigateTo({
      url: '/pages/index_page/add_collection?dID=' + dID
    })
  },

  gotoChannel: function() {
    getApp().globalData.preFeed = this.data.feed
    wx.navigateTo({
      url: '/pages/index_page/choose_channel'
    })
  },

  gotoPrevious: function() {
    var that = this
    if (this.data.last_feed.audio) {
      console.log(this.data.feed)
      this.setData({
        feed: that.data.last_feed,
        last_feed: {}
      })
      c.play(that.data.feed.audio, that.data.feed.user)
      this.setData({
        paused: false
      })
    }
  },

  gotoNext: function() {
    var that = this;
    this.getData(function() {
      c.play(that.data.feed.audio, that.data.feed.user);
      const player = wx.getBackgroundAudioManager();
      player.onTimeUpdate(function() {
        that.setData({
          audioProgress: parseInt(100 * player.currentTime / player.duration)
        })
      })
      that.setData({
        paused: false
      })
    });
  },

  bindPickerChange: function (e) {
    this.setData({
      hasSetTag: true,
      index: e.detail.value,
      channel : e.detail.value,
    })
    this.gotoNext()
  },

})