/*声觅主页面*/
// pages/index_page/index_page.js
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
    const player = wx.getBackgroundAudioManager()
    player.title = '此时此刻'
    player.epname = '此时此刻'
    player.singer = '许巍'
    player.coverImgUrl = 'http://y.gtimg.cn/music/photo_new/T002R300x300M000003rsKF44GyaSk.jpg?max_age=2592000'
    player.src = 'http://ws.stream.qqmusic.qq.com/M500001VfvsJ21xFqb.mp3?guid=ffffffff82def4af4b12b3cd9337d5e7&uin=346897220&vkey=6292F51E1E384E061FF02C31F716658E5C81F5594D561F2E88B854E81CAAB7806D5E4F103E55D33C16F3FAC506D1AB172DE8600B37E43FAD&fromtag=46' // 设置了 src 之后会自动播放
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
      title: '【分享标题】',
      path: '/contentpath',
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