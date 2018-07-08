'use strict'

const baseUrl = 'http://404.ladyrick.com/';
var token = wx.getStorageSync('token') || '';

const r = function(option,api){
	if(!api){
		api = 'api'
	}

	option.url = baseUrl + api;
	option.method = 'GET';
	option.dataType = 'json';
	option.data.token = token;

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
  return true;
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
  check:check
}