'use strict'

const c = require('./c.js')
const r = c.r;
const log = console.log;

const test = function(){
	r({
		data:{
			action: 'get_index',
			listentype: 'diff',
			channel: 'unset'
		},
		success: function(res){
			log('get_index')
			log(res)
		}
	})

	var test_audio_id = 'unset';
	r({
		data:{
			action: 'like_audio',
			audio_id: test_audio_id
		},
		success: function(res){
			log('like_audio')
			log(res)
		}
	})

	r({
		data:{
			action: 'get_comments',
			audio_id: test_audio_id
		},
		success: function(res){
			log('get_comments')
			log(res)
		}
	})

	r({
		data:{
			action: 'get_collection_set_name'
		},
		success: function(res){
			log('get_collection_set_name')
			log(res)
		}
	})

	var test_collection_name = 'unset';
	r({
		data:{
			action: 'add_collection_set',
			collection_name: test_collection_name
		},
		success: function(res){
			log('get_collection_set_name')
			log(res)
		}
	})

	r({
		data:{
			action: 'get_explore',
			last_audio_id: ''
		},
		success: function(res){
			log('get_explore')
			log(res)
		}
	})

	r({
		data:{
			action: 'get_one_feed',
			audio_id: test_audio_id
		},
		success: function(res){
			log('get_one_feed')
			log(res)
		}
	})

	var test_feed_obj = {}
	r({
		data:{
			action: 'post_audio',
			feed: test_feed_obj
		},
		success: function(res){
			log('post_audio')
			log(res)
		}
	})
	
	r({
		data:{
			action: 'get_my_feed',
			last_audio_id: ''
		},
		success: function(res){
			log('get_my_feed')
			log(res)
		}
	})
	
	r({
		data:{
			action: 'get_medal',
			last_audio_id: ''
		},
		success: function(res){
			log('get_medal')
			log(res)
		}
	})
	
  r({
    data:{
      action: 'get_user_info',
      last_audio_id: ''
    },
    succcess: function(res){
      log("get_usr_info")
      log(res)
    }
  })

}


module.exports = {
	test: test
}