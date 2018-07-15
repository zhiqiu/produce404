// pages/mine/mine.js
const c = require('../../utils/c.js')
const r = c.r;
Page({

  /**
   * 页面的初始数据
   */
  data: {
    msg: [],
  },
  getData: function(refresh){
    if(refresh){
      this.setData({
        msg: []
      })
    }
    var that = this;
    var last_msg_id = '';
    if(this.data.msg.length !== 0){
      last_msg_id = this.data.msg[this.data.msg.length - 1].msg_id;
    }
    r({
      data: {
        action: 'get_msg',
        last_msg_id: last_msg_id
      },
      success: function(res) {
        console.log(res)
        var newMsg = that.data.msg.concat(res.data.resp.msgs);
        that.setData({
          msg: newMsg
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
    if(this.data.status === 0)
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
    if(dID === '-1'){
      return ;
    }
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

})