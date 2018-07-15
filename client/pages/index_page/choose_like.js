/*录音页面*/
// pages/record/record.js

const COS = require('../../utils/upload');

const c = require('../../utils/c');
const r = c.r;

Page({

  /**
   * 页面的初始数据
   */
  data: {
    onrecord: false,
    recordPath: '',
    duration: 0,
    array: [
      '风声', '雨声', '读书声'
    ],
    items: [
      {name: '0', value: '动物植物'},
      {name: '1', value: '海浪瀑布'},
      {name: '2', value: '山水林间'},
      {name: '3', value: '自然气候'},
      {name: '4', value: '机器轰鸣'},
      {name: '5', value: '交通工具'},
      {name: '6', value: '古典艺术'},
      {name: '7', value: '现代乐器'},
    ]
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
        onrecord: true
      })
      const recordManager = wx.getRecorderManager()
      var that = this;
      recordManager.onStop(function(res) {
        that.setData({
          recordPath: res.tempFilePath,
          duration: res.duration
        })
        console.log(res);
      })
      recordManager.start({
        duration: 1000 * 60 * 5,
        format: 'mp3'
      })


    } else {
      //结束录音
      const recordManager = wx.getRecorderManager()
      recordManager.stop();
      this.setData({
        onrecord: false
      })




    }
  },
  upload: function(e) {
    var Bucket = 'create404-cos-1253746840';
    var Region = 'ap-guangzhou';
    var cos = new COS({

        getAuthorization: function (options, callback) {
          r({
            data:{
              action: 'signcos'
            },
            success: function(res){
              var data = res.data.data;
              // console.log(data)
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
          img: 'http://y.gtimg.cn/music/photo_new/T002R300x300M000003rsKF44GyaSk.jpg?max_age=2592000',
          name: 'heiheihei',
          intro: 'this is intro',
          location: 'SZ, China',
          duration: parseInt(this.data.duration)
        },
        tags: [{
          'tagname': 'example'
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

      cos.getObjectUrl({
        Bucket: Bucket,
        Region: Region,
        Key: filename,
        Sign: false
      }, function(err, data) {
        console.log('2333')
        console.log(data)
        console.log("http://" + data.Url.slice(8, data.Url.length))
        const player = wx.getBackgroundAudioManager();
        player.title = '此时此刻'
        player.epname = '此时此刻'
        player.singer = '许巍'
        player.coverImgUrl = 'http://y.gtimg.cn/music/photo_new/T002R300x300M000003rsKF44GyaSk.jpg?max_age=2592000'
        player.src = "http://" + data.Url.slice(8, data.Url.length);

      })
    })
  },
  checkboxChange: function(e) {
    console.log('checkbox发生change事件，携带value值为：', e.detail.value)
  }
})