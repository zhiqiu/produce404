  /*“我的”页面*/
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
    msg: [],
    playingIdx: -1,
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
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function() {
    console.log('下拉刷新')
    this.getData();
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function() {

  },

  gotoMyMsg: function() {
    var audioInfo = ''
    wx.navigateTo({
      url: '/pages/mine/my_msg/my_msg?' + audioInfo
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
    wx.navigateTo({
      url: '/pages/mine/mine_medal'
    })
  },

>>>>>>> 68e7437b5f2801aba323bec6ade66ce25ffcb2f3
})