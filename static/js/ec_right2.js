var ec_right2 = echarts.init(document.getElementById("r2"),"white");

var option_right2 = {
  title: {
    text: '全球各国疫苗接种人数 TOP10',
    textStyle:{
      //文字颜色
      color:'#ccc',

  },


    left: 'center'
    
  },
  tooltip: {
    trigger: 'item'
  },
  legend: {
    orient: 'vertical',
    textStyle: {
      color: '#ccc'  // 图例文字颜色
    },

    left: 'left',
  },

  series: [
    {
      type: 'pie',
      dataType : 'json',
      radius: '75%',
        data: [],
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      },
       label:{//饼图图形上的文本标签
                normal: {
                  undefined,
                  show: true,
                  position: 'inner', //标签的位置
                  textStyle: {
                    undefined,
                    fontWeight: 300,
                    fontSize: 10,    //文字的字体大小
                    
                  },
                  formatter: '{d}%'
                }
      }
    }
  ]
};

ec_right2.setOption(option_right2)
