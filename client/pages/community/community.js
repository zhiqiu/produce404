/*发现页面*/
// pages/community/community.js

const c = require('../../utils/c.js')
const r = c.r;
Page({

  /**
   * 页面的初始数据
   */
  data: {
    playingIdx : -1,  //当前播放的feed Id
    feeds : [],
    last_index : -1
  },
  getData: function(refresh){
    
    var last_audio_id = '';
    if(this.data.feeds.length !== 0){
      last_audio_id =  this.data.feeds[this.data.feeds.length - 1].audio.audio_id;
    }
    if(refresh) last_audio_id = ''
    var that = this;
    r({
      data: {
        action: 'get_explore',
        last_audio_id: last_audio_id
      },
      success: function(res) {
        console.log(res)
        var newFeeds = that.data.feeds.concat(res.data.resp.feeds);
        if(refresh) newFeeds = res.data.resp.feeds;
        that.setData({
          feeds: newFeeds
        })
      }
    })
    console.log(that)
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.getData(true);
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    if(this.data.last_index !== -1){
      var that =this;
      r({
        data:{
          action: 'get_one_feed',
          audio_id: this.data.feeds[this.data.last_index].audio.audio_id
        },
        success: function(res){
          var newfeed = res.data.resp.feed;
          that.data.feeds[that.data.last_index] = newfeed;
          that.setData({
            feeds : that.data.feeds
          })
        }
      })
    }
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
    this.getData();
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {
  
  },
  
  gotoDetail: function(options){
    var index = parseInt(options.currentTarget.id);
    var dID = this.data.feeds[index].audio.audio_id;
    this.data.last_index = index;
    wx.navigateTo({
      url: '/pages/community/detail?audioId='+dID
    })
    // }
  },
  
  gotoRecord: function(e){
    wx.navigateTo({
      url: '/pages/record/record'
    })
  },
  clickPlay: function(e){
    var idx = e.currentTarget.id;
    if(this.data.playingIdx === idx){
      c.playorpause();
    }else{
      this.setData({
        playingIdx: idx
      })
      c.play(this.data.feeds[idx].audio,this.data.feeds[idx].user)
    }
  },
  
})