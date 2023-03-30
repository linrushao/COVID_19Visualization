 function gettime() {
	$.ajax({
		url: "/time",
		timeout: 10000, //超时时间设置为10秒；
		success: function(data) {
			$("#time").html(data)
		},
		error: function(xhr, type, errorThrown) {

		}
	});
}

function get_c1_data() {
	$.ajax({
		url: "/c1",
		success: function(data) {
			$(".num h1").eq(0).html(data.confirm)
			$(".num h1").eq(1).html(data.suspect)
			$(".num h1").eq(2).html(data.heal)
			$(".num h1").eq(3).html(data.dead)
		},
		error: function(xhr, type, errorThrown) {
		}
	})
}

function get_c2_data() {
	$.ajax({
		url: "/c2",
		success: function(data) {
			$(".nu h1").eq(0).html(data.vaccine_sj)
			$(".nu h1").eq(1).html(data.vaccine_zg)
		},
		error: function(xhr, type, errorThrown) {
		}
	})
}

function get_c3_data(){
	 $.ajax({
		 url : "/c3",
		success: function(data) {
				for (var i = 0; i < data.length; i++) {
					$("#ul").append("<li>" + data[i] +  "</li>")
				}
			},
			error: function(xhr, type, errorThrown) {
			}
			// var u = document.getElementById("c3");
			// for (var i = 0; i < data.length; i++) {
			// 	var li = document.createElement("li");
			// 	li.innerHTML = data[i].name;
			// 	u.appendChild(li);
			// }
		// }
	 })
 }


function get_c4_data() {
	$.ajax({
		url:"/c4",
		success: function(data) {
			option_center4.series[0].data = data.kws
			ec_center4.setOption(option_center4)
		},
		error: function(xhr, type, errorThrown) {
		}
	})
}

$(function() {
    //获得当前<ul>
    var $uList = $(".scroll-box ul");
    var timer = null;
    //触摸清空定时器
    $uList.hover(function() {
        clearInterval(timer);
    },
    function() { //离开启动定时器
        timer = setInterval(function() {
            scrollList($uList);
        },
        1000);
    }).trigger("mouseleave"); //自动触发触摸事件
    //滚动动画
    function scrollList(obj) {
        //获得当前<li>的高度
        var scrollHeight = $("ul li:first").height();
        //滚动出一个<li>的高度
        $uList.stop().animate({
            marginTop: -scrollHeight
        },
        600,
        function() {
            //动画结束后，将当前<ul>marginTop置为初始值0状态，再将第一个<li>拼接到末尾。
            $uList.css({
                marginTop: 0
            }).find("li:first").appendTo($uList);
        });
    }
});

function get_l1_data() {
	$.ajax({
		url:"/l1",
		success: function(data) {
			option_left1.xAxis.data = data.day
			option_left1.series[0].data = data.confirm
			option_left1.series[1].data = data.suspect
			option_left1.series[2].data = data.heal
			option_left1.series[3].data = data.dead
			ec_left1.setOption(option_left1)
		},
		error: function(xhr, type, errorThrown) {
		}
	})
}



function get_l2_data() {
	$.ajax({
		url:"/l2",
		success: function(data) {
			option_left2.xAxis.data = data.day
			option_left2.series[0].data = data.confirm_add
			option_left2.series[1].data = data.suspect_add
			ec_left2.setOption(option_left2)
		},
		error: function(xhr, type, errorThrown) {

		}
	})
}


function get_r1_data() {
	$.ajax({
		url:"/r1",
		success: function(data) {
			option_right1.xAxis.data = data.city
			option_right1.series[0].data = data.confirm
			ec_right1.setOption(option_right1)
		},
		error: function(xhr, type, errorThrown) {

		}
	})
}



function get_r2_data() {
	$.ajax({
		url:"/r2",
		success: function(data) {

			option_right2.series[0].data = data.data

			ec_right2.setOption(option_right2)
		},
		error: function(xhr, type, errorThrown) {

		}
	})
}


gettime()
get_c1_data()
get_c2_data()
get_l1_data()
get_l2_data()
get_r1_data()
get_r2_data()
get_c3_data()
get_c4_data()
setInterval(gettime, 1000)
setInterval(get_c1_data, 1000*10)
setInterval(get_c2_data, 1000*10)
setInterval(get_l1_data, 1000*10)
setInterval(get_l1_data, 1000*10)
setInterval(get_r1_data, 1000*10)
setInterval(get_r1_data, 1000*10)
setInterval(get_c3_data, 1000*10)
setInterval(get_c4_data, 1000*10)
