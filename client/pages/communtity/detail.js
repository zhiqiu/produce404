// pages/communtity/detail.js
const c = require('../../utils/c.js')
const r = c.r;

Page({

  /**
   * 页面的初始数据
   */
  data: {
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    console.log(111)
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {
  
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

   /* var feedId = this.options.dID;
    var feedTmp = {}
    var that = this;
    console.log(feedId)
    r({
      data: {
        action: 'get_one_feed',
        audio_id: feedId
      },
      success: function (res) {
        that.setData({
          feed: res.data.resp.feed
        })
        console.log(that.data.feed)
      }
    })*/
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {
  
  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {
  
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {
  
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {
  
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {
  
  }
})