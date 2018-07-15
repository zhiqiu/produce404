/*添加到我的收藏页面*/
// pages/collection/add_collection.js
const c = require('../../utils/c.js')
const r = c.r;
Page({

  /**
   * 页面的初始数据
   */
  data: {
    feed: {},
    hiddenmodalput: true,
    //可以通过hidden是否掩藏弹出框的属性，来指定那个弹出框
    collectionFolders: [{
      collectionId: '',
      name: ''
    }],
    input: ''
  },

  getData: function (options) {
    var that = this;
    console.log(options)
    r({
      data: {
        action: 'get_collections',
      },
      success: function(res) {
        console.log(that.data)
        that.setData({
          collectionFolders: res.data.resp.collections,
        })
        console.log(that.data)
      }
    })
    r({
      data: {
        action: 'get_one_feed',
        audio_id: options.dID
      },
      success: function (res) {
        console.log(res)
        that.setData({
          feed: res.data.resp.feed
        })
      }
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    this.getData(options)
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

  //点击按钮指定的hiddenmodalput弹出框
  modalinput: function() {
    this.setData({
      hiddenmodalput: !this.data.hiddenmodalput
    })
  },
  
  //取消按钮
  cancel: function() {
    this.setData({
      hiddenmodalput: true
    });
  },
  //确认
  confirm: function(res) {
    this.setData({
      hiddenmodalput: true
    })
    var that = this
    r({
      data: {
        action: 'add_collection',
        collection_name: this.data.input
      },
      success: function(res) {
        console.log(1122)
        that.onLoad(that.data.feedId)
      },
      fail: function(res){
        console.log(res.errMsg)
      }
    })
  },

  bindKeyInput: function(e) {
    this.setData({
      input: e.detail.value
    })
  },

  addToCollection: function(e){
    var feedId = this.data.feed.audio.audio_id
    var that = this
    console.log(e)
    r({
      data: {
        action: 'add_into_collection',
        audio_id: feedId,
        collection_id: e.currentTarget.ids
      },
      complete: function() {
        var nowFeed = that.data.feed;
        nowFeed.iscollected = true;
        that.setData({
          feed: nowFeed
        })
        getApp().globalData.prePage.setData({
          feed : nowFeed
        })
        wx.navigateBack({
        })
      }
    })

  }
})