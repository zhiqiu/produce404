//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    jumpPath : ''
  },
  //事件处理函数
  onLoad: function(){
    this.setData({
      jumpPath: wx.getStorageSync('debug_page_path')
    })
  },
  pathInput: function(e){
    this.setData({
      jumpPath: e.detail.value
    })
  },
  goto: function(e){
    console.log('redirect: '+this.data.jumpPath);
    wx.setStorageSync('debug_page_path',this.data.jumpPath)
    wx.redirectTo({
      url: this.data.jumpPath
    })
  }
})
