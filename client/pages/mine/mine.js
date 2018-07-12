/*“我的”页面*/
// pages/mine/mine.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    user: {},
    feeds: {},
    medal: {},
    userMsg: {},
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    this.setData({
      user: getApp().globalData.myData.userInfo.resp.user,
      feeds: getApp().globalData.myData.feeds,
      medal: getApp().globalData.myData.medal,
    }),
    console.log(this.data.feeds)
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

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function() {

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
      url: '/pages/communtity/detail?dID=' + dID
    })
  }
})