/*发现页面*/
// pages/communtity/community.js

const c = require('../../utils/c.js')
const r = c.r;
Page({

  /**
   * 页面的初始数据
   */
  data: {
    feeds : []
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    r({
      data:{
        action: 'get_explore',
        last_audio_id: ''
      },
      success: function(res){
        console.log(res);
        
      }
    })
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
  gotoDetail: function(e){
    var dID = e.currentTarget.id;
    wx.navigateTo({
      url: '/pages/communtity/detail?dID='+dID
    })
  }
})