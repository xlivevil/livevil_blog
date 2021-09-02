// 点赞功能主函数
function validate_is_like(url, id, likes) {
	// 取出 LocalStorage 中的数据
	let storage = window.localStorage;
	const storage_str_data = storage.getItem('my_blog_data');
	let storage_json_data = JSON.parse(storage_str_data);
	// 若数据不存在，则创建空字典
	if (!storage_json_data) {
		storage_json_data = {};
	}
	// 检查当前文章是否已点赞。是则 status = true
	const status = check_status(storage_json_data, id);
	if (status) {
		layer.msg('已经点过赞了哟~');
		// 点过赞则立即退出函数
		return;
	} else {
		// 用 Jquery 找到点赞数量，并 +1
		$('span#likes_number')
			.text(likes + 1)
			.css('color', '#dc3545');
	}
	let requestInstance = new Request(url, {
		method: 'post',
    mode: 'same-origin',
		headers: {
			'Content-Type': 'application/json;charset=utf-8',
      'X-CSRFToken': csrftoken
		},
		body: JSON.stringify({"object": "post", "id": id}),
	});
	try {
		let response = fetch(requestInstance).then(response =>{
		let data = response.json();
		if (data['state'] == 200) {
			try {
				storage_json_data[id] = true;
			} catch (e) {
				window.localStorage.clear();
			}
			// 将字典转换为字符串，以便存储到 LocalStorage
			const d = JSON.stringify(storage_json_data);
			// 尝试存储点赞数据到 LocalStorage
			try {
				storage.setItem('my_blog_data', d);
			} catch (e) {
				// code 22 错误表示 LocalStorage 空间满了
				if (e.code === 22) {
					window.localStorage.clear();
					storage.setItem('my_blog_data', d);
				}
			}
		}
  })
	} catch (e) {
		layer.msg('与服务器通信失败..过一会儿再试试呗~');
	}
}

// 辅助点赞主函数，验证点赞状态
function check_status(data, id) {
	// 尝试查询点赞状态
	try {
		if (id in data && data[id]) {
			return true;
		} else {
			return false;
		}
	} catch (e) {
		window.localStorage.clear();
		return false;
	}
}
