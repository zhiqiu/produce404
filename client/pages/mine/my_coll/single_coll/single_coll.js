/*发现页面*/
// pages/community/community.js

const c = require('../../../../utils/c.js')
const r = c.r;
Page({

  /**
   * 页面的初始数据
   */
  data: {
    playingIdx: -1,  //当前播放的feed Id
    feeds : []
  },
  getData: function (id) {
    var that = this;
    r({
      data: {
        action: 'get_collection_content',
        collection_id: id.audioId
      },
      success: function (res) {
        console.log(res)
        if(res.data.resp)
        {
          that.setData({
            feeds: res.data.resp.feeds
          })
        }
        console.log(that)
      },
      fail: function (res){
        console.log('fail')
      }
    })
  
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.getData(options);
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
    this.getData(true);
    wx.stopPullDownRefresh();
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {
    console.log('下拉刷新')
    this.getData();
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  },

  gotoDetail: function (e) {
    console.log(e)
    var dID = e.currentTarget.id;
    wx.navigateTo({
      url: '/pages/community/detail?audioId=' + dID
    })
  },

  gotoRecord: function (e) {
    wx.navigateTo({
      url: '/pages/record/record'
    })
  },
  clickPlay: function (e) {
    var idx = e.currentTarget.id;
    if (this.data.playingIdx === idx) {
      c.playorpause();
    } else {
      this.setData({
        playingIdx: idx
      })
      c.play(this.data.feeds[idx].audio, this.data.feeds[idx].user)
    }
  },

})