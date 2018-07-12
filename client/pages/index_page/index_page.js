/*声觅主页面*/
// pages/index_page/index_page.js
const c = require('../../utils/c.js');
const r = c.r;
Page({

  /**
   * 页面的初始数据
   */
  data: {
    feed: wx.getStorageSync("index_feed_data") || {},
    dataloaded: false
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    if (!c.check()) return;

    if (getApp().globalData.indexData.feed.audio){
      console.log(getApp().globalData.indexData.feed);
      this.setData({
        feed: getApp().globalData.indexData.feed,
        dataloaded: true
      })
    }else{
      this.setData({
        feed: wx.getStorageSync("index_feed_data"),
        dataloaded: true
      })
      
    }
    console.log(this.data)
      
    while(!this.data.dataloaded){ console.log('wait')}
    console.log('aaaa')
    console.log(this.data)
    const player = wx.getBackgroundAudioManager()
    player.title = this.data.feed.audio.name
    player.epname = this.data.feed.audio.intro
    player.singer = this.data.feed.user.name
    player.coverImgUrl = this.data.feed.audio.img
    player.src = this.data.feed.audio.url // 设置了 src 之后会自动播放
    let page = this;
    player.onTimeUpdate(function() {
      page.setData({
        audioProgress: parseInt(100 * player.currentTime / player.duration)
      })
    })
    console.log(this.data)
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
    console.log('下拉切歌')
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function() {
    console.log('上拉切歌')
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
    const player = wx.getBackgroundAudioManager()
    if (player.paused) {
      player.play()
    } else {
      player.pause()
    }

  },
  listenDiffToggle: function() {
    this.setData({
      listenDiff: !this.data.listenDiff
    })
  },
  like: function() {
    this.setData({
      currentLike: true
    })
  },
  dislike: function() {
    this.setData({
      currentLike: false
    })
  },
  gotoComments: function() {
    var audioInfo = ''
    wx.navigateTo({
      url: '/pages/comments/comments?' + audioInfo
    })
  },

  gotoAddCollection: function (e) {
    console.log(e)
    var dID = e.currentTarget.id;
    wx.navigateTo({
      url: '/pages/add_collection/add_collection?dID=' + dID
    })
  },


})