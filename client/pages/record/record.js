/*录音页面*/
// pages/record/record.js

const COS = require('../../utils/upload');
const c = require('../../utils/c');
const r = c.r;

var QQMapWX = require('../../utils/qqmap-wx-jssdk.js');

Page({

  /**
   * 页面的初始数据
   */
  data: {
    onrecord: false,
    recordPath: '',
    duration: 0,
    recordingAnimation: {},
    comment: '',
    tagArray : ['动物植物', '海浪瀑布', '山水林间', '自然气候', '机器轰鸣', '交通工具', '古典艺术', '现代乐器','无'],
    hasSetTag: false,
    tag: '',
    position: '',
    recordstopped: false
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {

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
  touch: function(e) {
    if (!this.data.onrecord) {
      //开始录音
      this.setData({
        onrecord: true,
        recordstopped: false
      })
      const recordManager = wx.getRecorderManager()
      var that = this;
      recordManager.onStop(function(res) {
        that.setData({
          recordPath: res.tempFilePath,
          duration: res.duration,
          recordstopped: true
        })
        console.log(res);
        wx.showToast({
          title: '录制成功,'+(parseInt(that.data.duration/1000)+1)+'"',
          icon: 'success',
          duration: 2000
        })
        that.setData({
          onrecord: false
        })
      })
      recordManager.start({
        duration: 1000 * 60 * 5,
        format: 'mp3'
      })
    } else {
      //结束录音
      const recordManager = wx.getRecorderManager()
      recordManager.stop();
      
    }
  },
  upload: function(e) {
    if(this.data.onrecord){
      wx.showToast({
        title: '请先结束录音',
        icon: 'loading',
        duration: 2000
      })
      return;
    }
    if(this.data.comment.length === 0){
      wx.showToast({
        title: '请输入文字',
        icon: 'loading',
        duration: 2000
      })
      return;
    }
    var Bucket = 'create404-cos-1253746840';
    var Region = 'ap-guangzhou';
    var that = this
    var cos = new COS({
      getAuthorization: function(options, callback) {
        r({
          data: {
            action: 'signcos'
          },
          success: function(res) {
            var data = res.data.data;

            callback({
              TmpSecretId: data.credentials && data.credentials.tmpSecretId,
              TmpSecretKey: data.credentials && data.credentials.tmpSecretKey,
              XCosSecurityToken: data.credentials && data.credentials.sessionToken,
              ExpiredTime: data.expiredTime,
            });
          }
        })
      },
    });

    var filepath = this.data.recordPath;
    console.log(filepath)
    var filename = Date.parse(new Date()) + c.token + '.mp3';
    r({
      data: {
        action: 'post_audio',
        audio: {
          url: filename,
          img: 'http://cos.ladyrick.com/img-shengmi.png',
          name: that.data.comment,
          intro: that.data.comment,
          location: this.data.position,
          duration: parseInt(this.data.duration/1000)+1
        },
        tags: [{
          'tagname': that.data.tag
        }]
      },
      success: function(s) {
        console.log(s)
      }
    })
    cos.postObject({
      Bucket: Bucket,
      Region: Region,
      Key: filename,
      FilePath: filepath,
      onProgress: function(info) {
        console.log(info);
      }
    }, function(err, data) {
      console.log(err);
      console.log(data);

      wx.showToast({
        title: '提交成功',
        icon: 'success',
        duration: 2000
      })
      wx.navigateBack();
    })
  },

  bindPickerChange: function(e) {
    this.setData({
      hasSetTag : true,
      index: e.detail.value,
      tag: this.data.tagArray[parseInt(e.detail.value)]
    }) 
  },

  getLocation: function() {
    var that = this
    var qqmapsdk = new QQMapWX({
      key: 'TWHBZ-ELKKI-YMVGS-5VR46-D5WHF-ZFFEL' // 必填
    });
    wx.getLocation({
      type: 'wgs84',
      success: function(res) {
        qqmapsdk.reverseGeocoder({
          location: {
            latitude: res.latitude,
            longitude: res.longitude
          },
          success: function(addressRes) {
            console.log(addressRes)
            that.setData({
              position : addressRes.result.ad_info.province + '·' + addressRes.result.ad_info.city
            })
          },
          fail: function(res)
          {
            that.setData({
              position: '广东省·深圳市'
            })
          }
        })
      }
    })
  },

  bindKeyInput: function(e) {
    this.setData({
      comment: e.detail.value
    })
  },
})