'use strict'

const baseUrl = 'https://404.ladyrick.com/';
const COSBase = 'https://cos.ladyrick.com/';
var token = wx.getStorageSync('token') || '';

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
          action: 'post_userinfo',
          data: wx.getStorageSync('userInfo')
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
        action: 'post_userinfo',
        data: wx.getStorageSync('userInfo')
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
	var code = wx.login({
		success: function(res){
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
										action: 'post_userinfo',
										data: userInfo
									}
								})
							}else{
								wx.setStorageSync('server_first_time',true);
							}
						}
            getApp().initGlobalData();
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
  play: play
}