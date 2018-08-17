'use strict'

const baseUrl = 'http://404.ladyrick.com/';
const COSBase = 'http://produce404-1257046746.cos.ap-guangzhou.myqcloud.com';
var token = wx.getStorageSync('token') || '';

var tagArray = ['动物植物', '海浪瀑布', '山水林间', '自然气候', '机器轰鸣', '交通工具', '古典艺术', '现代乐器','全部频道']

const r = function(option,api){
	if(!api){
		api = 'api'
	}

	option.url = baseUrl + api;
	option.method = 'GET';
	option.dataType = 'json';
	option.data.token = wx.getStorageSync('token');
	if(wx.getStorageSync('server_first_time')){
      wx.setStorageSync('server_first_time',false);
      r({
        data:{
          action: 'set_user_info',
          user: wx.getStorageSync('userInfo')
        }
      })
    }
	wx.request(option);
}

const check = function(){
	if(!wx.getStorageSync('userInfo')){
    wx.redirectTo({
      url : '/pages/login_page/login_page',
      complete: function(e  ){
        console.log(e)
      }
    })
    return false;
  }
  if(wx.getStorageSync('server_first_time')){
    wx.setStorageSync('server_first_time',false);
    r({
      data:{
        action: 'set_user_info',
        user: wx.getStorageSync('userInfo')
      }
    })
  }
  return true;
}
const fixUrl = function(s){
	if(s.startsWith('http')){
		return s;
	}else{
		return COSBase + s;
	}
}
const play = function(audio,user){
	const player = wx.getBackgroundAudioManager();
	player.title = audio.name
	player.epname = audio.intro
	player.singer = user.name
	player.coverImgUrl = audio.img
	player.src = fixUrl(audio.url) // 设置了 src 之后会自动播放
}
const playorpause= function() {
	const player = wx.getBackgroundAudioManager()
	if (player.paused) {
		player.play()
	} else {
		player.pause()
	}
}

const login = function(){
	if(wx.getStorageSync('login')) return;
	var code = wx.login({
		success: function(res){
			wx.setStorageSync('login',true);
			if(res.code){
				r({
					data:{
						action: 'login',
						code: res.code
					},
					success: function(res){
						wx.setStorageSync('token',res.data.resp.token)
						// console.log(res)
						token = res.data.token;
						if(res.data.resp.first_time){
							var userInfo = wx.getStorageSync('userInfo');
							if(userInfo){
								r({
									data:{
										action: 'set_user_info',
										user: userInfo
									}
								})
							}else{
								wx.setStorageSync('server_first_time',true);
							}
						}
					}
				})
			}else{
				console.log('[!] login failed' + res.errMsg);
			}
		},
	});
}


module.exports = {
  login: login,
  r:r,
  baseUrl:baseUrl,
  token:token,
  check:check,
  COSBase: COSBase,
  playorpause: playorpause,
  play: play,
  tagArray: tagArray
}