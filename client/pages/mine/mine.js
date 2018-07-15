  /*我的页面*/
// pages/mine/mine.js
const c = require('../../utils/c.js')
const r = c.r;
Page({

  /**
   * 页面的初始数据
   */
  data: {
    user: {},
    feeds: [],
    medals: [],
    debug_cnt: 0,
    msg: [],
    playingIdx: -1,
    last_index: -1,
    status: 0   //0表示“声音日迹”，1表示“我的勋章”
  },
  getData: function(refresh){
    if(refresh){
      this.setData({
        feeds: []
      })
    }
    var that = this;
    r({
      data:{
        action: 'get_user_info'
      },
      success:function(res){
        that.setData({
          user: res.data.resp.user
        })
      }
    })
    r({
      data: {
        action: 'get_medal'
      },
      success: function(res) {
        that.setData({
          medals: res.data.resp.medals
        })
      }
    })

    var last_audio_id = '';
    if(this.data.feeds.length !== 0){
      last_audio_id = this.data.feeds[this.data.feeds.length - 1].audio.audio_id;
    }
    r({
      data: {
        action: 'get_my_feed',
        last_audio_id: last_audio_id
      },
      success: function(res) {
        console.log(res)
        var newFeeds = that.data.feeds.concat(res.data.resp.feeds);
        that.setData({
          feeds: newFeeds
        })
      }
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    this.getData(true);
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
    this.getData(true);
    wx.stopPullDownRefresh();
    if(this.data.status === 1){
      this.data.debug_cnt += 1;
      if(this.data.debug_cnt < 5) return;
      wx.setStorageSync('login');
      wx.setStorageSync('server_first_time');
      wx.setStorageSync('token');
      wx.setStorageSync('userInfo');
      c.check();
      c.login();
    }
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function() {
    console.log('下拉刷新')
    if(this.data.status === 0)
      this.getData();
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function() {

  },

  gotoMyMsg: function() {
    wx.navigateTo({
      url: '/pages/mine/mine_msg'
    })
  },

  gotoMyColl: function() {
    var audioInfo = ''
    wx.navigateTo({
      url: '/pages/mine/my_coll/my_coll?' + audioInfo
    })
  },

  gotoMyAgreement: function() {
    var audioInfo = ''
    wx.navigateTo({
      url: '/pages/mine/my_agreement/my_agreement?' + audioInfo
    })
  },

  gotoDetail: function(e){
    console.log(e)
    var dID = e.currentTarget.id;
    wx.navigateTo({
      url: '/pages/community/detail?audioId=' + dID
    })
  },

  gotoMyFeed: function(){
    this.setData({
      status: 0
    })
  },

  gotoMyMedal: function(){
    this.setData({
      status: 1
    })
  },
  clickPlay: function(e){
    var idx = e.currentTarget.id;
    if(this.data.playingIdx === idx){
      c.playorpause();
    }else{
      this.setData({
        playingIdx: idx
      })
      c.play(this.data.feeds[idx].audio,this.data.feeds[idx].user)
    }
  },

})