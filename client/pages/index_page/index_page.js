/*声觅主页面*/
// pages/index_page/index_page.js
const c = require('../../utils/c.js');
const r = c.r;

let animationShowHeight = 300;
Page({

  /**
   * 页面的初始数据
   */
  data: {
    feed: {},
    last_feed: {},
    listentype: 'like', // diff or like
    channel: wx.getStorageSync('channel') || 'unset', // unset or channelname
    dataloaded: false,
    tags: [{
      text: '风声',
      ischoosen: false
    }, {
      text: '雨声',
      ischoosen: false
    }, {
      text: '读书声',
      ischoosen: false
    }, {
      text: '鸟声',
      ischoosen: false
    }, {
      text: '汽笛声',
      ischoosen: false
    }, {
      text: '海浪声',
      ischoosen: false
    }, {
      text: '白噪声',
      ischoosen: false
    }, {
      text: '琴声',
      ischoosen: false
    }, {
      text: '娃娃声',
      ischoosen: false
    }],

    animationData: "",
    showModalStatus: false,
    imageHeight: 0,
    imageWidth: 0,
  },

  getData: function(callback) {
    this.setData({
      last_feed: this.data.feed
    })
    var that = this;
    r({
      data: {
        action: 'get_index',
        listentype: that.data.listentype,
        channel: that.data.channel
      },
      success: function(res) {
        console.log(res)
        that.setData({
          feed: res.data.resp.feed,
          dataloaded: true
        })
        // TODO: feed_next
        callback();
      }
    })
    console.log(that)
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    if (!c.check()) return; // check login
    var that = this;
    this.getData(function() {
      c.play(that.data.feed.audio, that.data.feed.user);
      const player = wx.getBackgroundAudioManager();
      player.onTimeUpdate(function() {
        that.setData({
          audioProgress: parseInt(100 * player.currentTime / player.duration)
        })
      })
    });
    console.log(this)
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
    this.setData({
      channel: wx.getStorageSync('channel') || 'unset'
    })
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
  onShareAppMessage: function(options) {
    return {
      title: '声觅',
      path: '/pages/login_page/login_page',
      // imageUrl
    }
  },
  playorpause: function() {
    c.playorpause();
  },
  listenDiffToggle: function() {
    this.setData({
      listentype: this.data.listentype === 'like' ? 'diff' : 'like'
    })
    var that = this;
    this.getData(function() {
      c.play(that.data.feed.audio, that.data.feed.user);
      const player = wx.getBackgroundAudioManager();
      player.onTimeUpdate(function() {
        that.setData({
          audioProgress: parseInt(100 * player.currentTime / player.duration)
        })
      })
    });
  },
  like: function() {
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
  dislike: function() {
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

  gotoComments: function() {
    var audioId = this.data.feed.audio.audio_id;
    wx.navigateTo({
      url: '/pages/community/detail?audioId=' + audioId
    })
  },

  gotoAddCollection: function(e) {
    console.log(e)
    var dID = e.currentTarget.id;
    wx.navigateTo({
      url: '/pages/index_page/add_collection?dID=' + dID
    })
  },
  gotoChannel: function() {
    wx.navigateTo({
      url: '/pages/index_page/choose_channel'
    })
  },

  gotoPrevious: function() {
    var that = this
    if (this.data.last_feed.audio) {
      console.log(this.data.feed)
      this.setData({
        feed: that.data.last_feed,
        last_feed: {}
      })
      c.play(that.data.feed.audio, that.data.feed.user)
    }
  },

  gotoNext: function() {
    var that = this;
    this.getData(function() {
      c.play(that.data.feed.audio, that.data.feed.user);
      const player = wx.getBackgroundAudioManager();
      player.onTimeUpdate(function() {
        that.setData({
          audioProgress: parseInt(100 * player.currentTime / player.duration)
        })
      })
    });
  },

  showModal: function () {
    // 显示遮罩层
    var animation = wx.createAnimation({
      duration: 200,
      timingFunction: "linear",
      delay: 0
    })
    console.log(animation)
    this.animation = animation
    animation.translateY(-animationShowHeight).step()
    this.setData({
      animationData: animation.export(),
      showModalStatus: true
    })

    setTimeout(function () {
      animation.translateY(100).step()
      this.setData({
        animationData: animation.export()
      })
    }.bind(this), 200)
  },

  hideModal: function () {
    // 隐藏遮罩层
    var animation = wx.createAnimation({
      duration: 200,
      timingFunction: "linear",
      delay: 0
    })
    this.animation = animation;
    animation.translateY(animationShowHeight).step()
    this.setData({
      animationData: animation.export(),
    })
    setTimeout(function () {
      animation.translateY(0).step()
      this.setData({
        animationData: animation.export(),
        showModalStatus: false
      })
    }.bind(this), 200)
  },

  onShow: function () {
    let that = this;
    wx.getSystemInfo({
      success: function (res) {
        animationShowHeight = res.windowHeight;
      }
    })
  },


})