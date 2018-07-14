//index.js
var app = getApp();

let animationShowHeight = 300;

Page({
  data: {
    animationData: "",
    showModalStatus: false,
    imageHeight: 0,
    imageWidth: 0,
    tags:[
      { text: '风声', ischoosen: false }, { text: '雨声', ischoosen: false }, { text: '读书声', ischoosen: false }, { text: '鸟声', ischoosen: false }, { text: '汽笛声', ischoosen: false }, { text: '海浪声', ischoosen: false }, { text: '白噪声', ischoosen: false }, { text: '琴声', ischoosen: false }, { text: '娃娃声', ischoosen: false }
    ]
  },
  imageLoad: function(e) {
    this.setData({
      imageHeight: e.detail.height,
      imageWidth: e.detail.width
    });
  },
  
  showModal: function() {
    // 显示遮罩层
    var animation = wx.createAnimation({
      duration: 200,
      timingFunction: "linear",
      delay: 0
    })
    this.animation = animation
    animation.translateY(-animationShowHeight).step()
    this.setData({
      animationData: animation.export(),
      showModalStatus: true
    })

    setTimeout(function() {
      animation.translateY(100).step()
      this.setData({
        animationData: animation.export()
      })
    }.bind(this), 200)
  },

  hideModal: function() {
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
    setTimeout(function() {
      animation.translateY(0).step()
      this.setData({
        animationData: animation.export(),
        showModalStatus: false
      })
    }.bind(this), 200)
  },

  onShow: function() {
    let that = this;
    wx.getSystemInfo({
      success: function(res) {
        animationShowHeight = res.windowHeight;
      }
    })
  },

})