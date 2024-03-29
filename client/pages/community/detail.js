// pages/community/detail.js
const c = require('../../utils/c.js');
const r = c.r;
Page({

  /**
   * 页面的初始数据
   */
  data: {
    feed: {},
    comments: [],
    playing: false,
    hiddenmodalput: true,
    nowCommentUserName: "",
    nowCommentUserOpenId : "",
    commentTmp : {},
    COSBase: c.COSBase,
  },

  getData: function(options) {
    var that = this;
    console.log(options)
    r({
      data: {
        action: 'get_one_feed',
        audio_id: options
      },
      success: function(res) {
        console.log(res)
        that.setData({
          feed: res.data.resp.feed
        })
        r({
          data: {
            action: 'get_comments',
            audio_id: that.data.feed.audio.audio_id
          },
          success: function(res) {
            console.log(res)
            that.setData({
              comments: res.data.resp.comments
            })
          }
        })
      }
    })
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    this.getData(options.audioId);
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

  clickPlay: function() {
    if (this.data.playing) {
      c.playorpause();
    } else {
      this.setData({
        playing: true
      })
      c.play(this.data.feed.audio, this.data.feed.user)
    }
  },

  like: function(e) {
    var nowFeed = this.data.feed;
    nowFeed.isliked = true;
    nowFeed.like_num += 1;
    this.setData({
      feed: nowFeed
    })
    // var feeds = getApp().globalData.prePage.data.feeds
    // if (feeds)  //从社区页和我的页面进去
    // {
    //   for (var singleFeed of feeds)
    //   {
    //     if(singleFeed.audio.audio_id === this.data.feed.audio.audio_id){
    //       singleFeed = nowFeed
    //       console.log(singleFeed)
    //       break
    //     }
    //   }
    //   getApp().globalData.prePage.setData({
    //     feeds: feeds
    //   })
    // }
    // else{
    //   getApp().globalData.prePage.setData({
    //     feed: nowFeed
    //   })
    // }
    r({
      data: {
        action: 'like_audio',
        audio_id: this.data.feed.audio.audio_id
      }
    })
  },

  dislike: function(e) {
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

  gotoAddCollection: function(e) {
    var dID = e.currentTarget.id;
    getApp().globalData.prePage = this
    wx.navigateTo({
      url: '/pages/index_page/add_collection?dID=' + dID
    })
  },

  onShareAppMessage: function(options) {
    return {
      title: '声觅',
      path: '/pages/login_page/login_page',
      // imageUrl
    }
  },

  //点击按钮指定的hiddenmodalput弹出框
  modalinput: function(options) {
    var name = ""
    var id = ""
    if(options.currentTarget.id !== "")
    {
      name = this.data.comments[parseInt(options.currentTarget.id)].user.name
      id = this.data.comments[parseInt(options.currentTarget.id)].user.openid
    }
    this.setData({
      hiddenmodalput: !this.data.hiddenmodalput,
      nowCommentUserName: name,
      nowCommentUserOpenId: id
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
    if (this.data.feed.audio.audio_id) {
      var textTmp = this.data.commentTmp
      console.log(this.data.nowCommentUserOpenId)
      if (this.data.nowCommentUserOpenId !== "")
      {
        textTmp = '@' + this.data.nowCommentUserName + ':' + this.data.commentTmp
      }
      r({
        data: {
          action: 'post_comment',
          audio_id: this.data.feed.audio.audio_id,
          reply_to_user_openid: this.data.nowCommentUserOpenId, //置为空字符串表示直接回复某个feed
          text: textTmp
        },
        success: function(res) {
          console.log(that.data.feed.audio)
          if (that.data.feed.audio) {
            that.getData(that.data.feed.audio.audio_id);
          }
        }
      })
    }


  },

  bindKeyInput: function(e) {
    console.log(e)
    this.setData({
      commentTmp: e.detail.value
    })
  },

  likeComment: function(options){
    var that = this
    var index = parseInt(options.currentTarget.id)
    var commentsTmp = that.data.comments
    if (index < that.data.comments.length)
    {
      commentsTmp[index].isliked = true
      commentsTmp[index].like_num++
      that.setData({
        comments: commentsTmp
      })
      r({
        data: {
          action: 'like_comment',
          comment_id: that.data.comments[index].comment_id
        },
        seccess: function (res) {
        }
      })
    }
  },

  dislikeComment: function (options) {
    var that = this
    var index = parseInt(options.currentTarget.id)
    var commentsTmp = this.data.comments
    if (index < this.data.comments.length) {
      commentsTmp[index].isliked = false
      commentsTmp[index].like_num--
      this.setData({
        comments: commentsTmp
      })
    }
    r({
      data: {
        action: 'dislike_comment',
        comment_id: that.data.comments[index].comment_id
      },
      seccess: function (res) {
      }
    })
  },
})