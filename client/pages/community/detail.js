// pages/community/detail.js
const c = require('../../utils/c.js');
const r = c.r;
Page({

  /**
   * 页面的初始数据
   */
  data: {
    feed: {},
    comments: {},
    playing: false
  },
  
  getData: function(callback){
    var that = this;
    console.log('that')
    console.log(that)
    r({
      data: {
        action: 'get_one_feed',
        audio_id: this.data.audioId
      },
      success: function(res) {
        console.log(res)
        that.setData({
          feed: res.data.resp.feed
        })
      }
    })
    r({
      data:{
        action: 'get_comments',
        audio_id: this.data.audioId
      },
      success: function(res){
        console.log(res)
        that.setData({
          comments: res.data.resp.comments
        })
      }
    })
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.setData({
      audioId: options.audioId
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
    this.getData();
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
  gotoComment: function(){
    var audioId = this.data.audioId;
    wx.navigateTo({
      url: '/pages/index_page/add_comment?audioId=' + audioId
    })
  },
  clickPlay : function(){
    if(this.data.playing){
      c.playorpause();
    }else{
      this.setData({
        playing: true
      })
      c.play(this.data.feed.audio,this.data.feed.user)
    }
  },


  like: function (e) {
    var nowFeed = this.data.feed;
    nowFeed.isliked = true;
    nowFeed.like_num += 1;
    this.setData({
      feed: nowFeed
    })
    r({
      data: {
        action: 'like_audio',
        audio_id: this.data.feed.audio.audio_id
      }
    })
  },

  dislike: function (e) {
    var nowFeed = this.data.feed;
    nowFeed.isliked = false;
    nowFeed.like_num -= 1;
    this.setData({
      feed: nowFeed
    })
    r({
      data: {
        action: 'dislike_audio',
        audio_id: this.data.feed.audio.audio_id
      }
    })
  },

})