/*录音页面*/
// pages/record/record.js


const c = require('../../utils/c');
const r = c.r;

Page({

  /**
   * 页面的初始数据
   */
  data: {
    onrecord: false,
    recordPath: '',
    duration: 0,
    items: [
      {name: '0', value: '动物植物'},
      {name: '1', value: '海浪瀑布'},
      {name: '2', value: '山水林间'},
      {name: '3', value: '自然气候'},
      {name: '4', value: '机器轰鸣'},
      {name: '5', value: '交通工具'},
      {name: '6', value: '古典艺术'},
      {name: '7', value: '现代乐器'},
    ],
    COSBase: c.COSBase,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {

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
  
  clickIndex: function(res){
    wx.switchTab({
      url: '/pages/index_page/index_page'
    })
  }
})