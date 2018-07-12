/*评论页面*/
// pages/record/record.js
const c = require('../../utils/c.js');
const r = c.r;
Page({

  /**
   * 页面的初始数据
   */
  data: {
    channels: [
      {text:'不设置',id:'unset'},
      {text:'频道1',id:'channel1'},
      {text:'频道2',id:'channel2'},
      {text:'频道3',id:'channel3'},
      {text:'频道4',id:'channel4'},
      {text:'频道5',id:'channel5'},
      {text:'频道6',id:'channel6'},
      {text:'频道7',id:'channel7'},
      {text:'频道8',id:'channel8'},
    ]
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    
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
  
  },
  click: function(e){
    wx.setStorageSync('channel',e.currentTarget.id)
    wx.navigateBack()
  }
})