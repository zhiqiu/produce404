/*声觅主页面*/
// pages/index_page/index_page.js
const c = require('../../utils/c.js');
const r = c.r;
Page({

  /**
   * 页面的初始数据
   */
  data: {
    feed: {},
    listentype: 'like', // diff or like
    channel: wx.getStorageSync('channel') || 'unset', // unset or channelname
    dataloaded: false
  },

  getData: function(callback){
    var that = this;
    console.log('that')
    console.log(that)
    r({
      data: {
        action: 'get_index',
        listentype: that.data.listentype,
        channel: that.data.channel
      },
      success: function(res) {
        console.log(res)
        that.setData({
          feed: res.data.resp.feed,
          dataloaded: true
        })
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
    this.getData(function(){
      c.play(that.data.feed.audio,that.data.feed.user);
      const player = wx.getBackgroundAudioManager();
      player.onTimeUpdate(function() {
        that.setData({
          audioProgress: parseInt(100 * player.currentTime / player.duration)
        })
      })
    });
    
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
    this.setData({
      channel: wx.getStorageSync('channel') || 'unset'
    })
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function() {

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
  },
  listenDiffToggle: function() {
    this.setData({
      listentype: this.data.listentype === 'like' ? 'diff' : 'like'
    })
  },
  like: function() {
    var nowFeed = this.data.feed;
    nowFeed.isliked = true;
    nowFeed.like_num += 1;
    this.setData({
      feed: nowFeed
    })
    r({
      data:{
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
      data:{
        action: 'dislike_audio',
        audio_id: this.data.feed.audio.audio_id
      }
    })
  },
  
  gotoComments: function() {
    var audioId = this.data.feed.audio.audio_id;
    wx.navigateTo({
      url: '/pages/community/detail?audioId=' + audioId
    })
  },

  gotoAddCollection: function (e) {
    console.log(e)
    var dID = e.currentTarget.id;
    wx.navigateTo({
      url: '/pages/index_page/add_collection?dID=' + dID
    })
  },
  gotoChannel: function(){
    wx.navigateTo({
      url: '/pages/index_page/choose_channel'
    })
  }

})