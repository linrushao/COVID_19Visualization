var ec_right1 = echarts.init(document.getElementById("r1"),"white");

option_right1 = {
	title: {
		text: '全国各省确诊人数 TOP5',
		textStyle: {
			color: 'white'
		},
		left: 'left'
	},
	color: ['#3398DB'],
	tooltip: {
		trigger: 'axis',
		axisPointer: {
			type: 'shadow'
		}
	},
	
	xAxis: {
		type: 'category',
		axisLabel: {
			color: "#ccc" //刻度线标签颜色
		},
			axisLine: {
			color: "#ccc" //刻度线标签颜色
		},
		axisTick: {
			color: "#ccc" //刻度线标签颜色
		},
		data: []

	},
	yAxis: {
		// name: '数值',
		type: 'value',
		// min: 0, // 设置y轴刻度的最小值
		// max: 1800, // 设置y轴刻度的最大值
		// splitNumber: 9, // 设置y轴刻度间隔个数
		axisLine: {
			show: true
			// lineStyle: {
			// 	// 设置y轴颜色
			// 	color: '#87CEFA'
			// }
		},
		axisLabel: {
			show: true,
			color: 'white',
			fontSize: 12,
			formatter: function(value) {
				if (value >= 1000) {
					value = value / 1000 + 'k';
				}
				return value;
			}
		},
		splitLine: {
			show: true,
			lineStyle: {
				color: '#172738',
				width: 1,
				type: 'solid'
			}
		}
	},
		
	series: [{
		type: 'bar',
		data: [],
		barMaxWidth: "45%"
	}]
};
ec_right1.setOption(option_right1)
