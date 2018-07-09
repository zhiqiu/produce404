/*声觅主页面*/
// pages/index_page/index_page.js
const c = require('../../utils/c.js');
const r = c.r;
Page({

  /**
   * 页面的初始数据
   */
  data: {
    audioImgSrc: 'http://y.gtimg.cn/music/photo_new/T002R300x300M000003rsKF44GyaSk.jpg?max_age=2592000',
    audioName: '此时此刻',
    audioProgress: 0,
    listenDiff: false,
    currentLike: false
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    if(!c.check()) return;
    
    const player = wx.getBackgroundAudioManager()
    player.title = '此时此刻'
    player.epname = '此时此刻'
    player.singer = '许巍'
    player.coverImgUrl = 'http://y.gtimg.cn/music/photo_new/T002R300x300M000003rsKF44GyaSk.jpg?max_age=2592000'
    player.src = 'http://create404-cos-1253746840.file.myqcloud.com/audio/%E4%BA%A4%E9%80%9A%E5%B7%A5%E5%85%B7/%E6%91%A9%E6%89%98%E8%BD%A6%E5%90%AF%E5%8A%A8%E6%97%B6%E7%9A%84%E5%A3%B0%E9%9F%B3.mp3?sign=7dtVHxEoh8Nx8QQo6agxIWy4rjxhPTEyNTM3NDY4NDAmaz1BS0lEaEhmclN3dktFd1NuejFBVnhKWmlmUXpTbXRwWXBxaVAmZT0xNTMzNzI3Nzc1JnQ9MTUzMTEzNTc3NSZyPTExMzc0NDg2MCZmPS9hdWRpby8lRTQlQkElQTQlRTklODAlOUElRTUlQjclQTUlRTUlODUlQjcvJUU2JTkxJUE5JUU2JTg5JTk4JUU4JUJEJUE2JUU1JTkwJUFGJUU1JThBJUE4JUU2JTk3JUI2JUU3JTlBJTg0JUU1JUEzJUIwJUU5JTlGJUIzLm1wMyZiPWNyZWF0ZTQwNC1jb3M=' // 设置了 src 之后会自动播放
    let page = this;
    player.onTimeUpdate(function(){
      page.setData({
        audioProgress : parseInt(100 * player.currentTime / player.duration)
      })
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
    console.log('下拉切歌')
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {
    console.log('上拉切歌')
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function (options) {
    return {
      title: '声觅',
      path: '/pages/login_page/login_page',
      // imageUrl
    }
  },
  playorpause: function(){
    const player = wx.getBackgroundAudioManager()
    if(player.paused){
      player.play()
    }else{
      player.pause()
    }

  },
  listenDiffToggle: function(){
    this.setData({
      listenDiff: !this.data.listenDiff
    })
  },
  like: function(){
    this.setData({
      currentLike: true
    })
  },
  dislike: function(){
    this.setData({
      currentLike: false
    })
  },
  gotoComments: function(){
    var audioInfo = ''
    wx.navigateTo({
      url: '/pages/comments/comments?'+audioInfo
    })
  },
  gotoCollect: function(){
    var audioInfo = ''
    wx.navigateTo({
      url: '/pages/collection/add_collection?'+audioInfo
    })
  }

})