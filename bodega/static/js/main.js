

const getOptionChart = async () => {
    try {
        const response = await fetch("/get_chart/");
        return await response.json();
    } catch (ex) {
        alert(ex);
    }
};

const getOptionChart2 = async () => {
  try {
      const response = await fetch("/obtener_estadisticas/");
      const { productos_vencidos, productos_por_vencer, total_cantidad_stock } = await response.json();

      return {
          color: ['#CB444A', '#F5C344', '#3579F6'],
          tooltip: {
              trigger: 'item'
          },
          legend: {
            orient: 'vertical',
            align: 'left',
            left: '0',
            top: '0',
          },
          series: [
              {
                  name: 'Access From',
                  type: 'pie',
                  radius: ['40%', '70%'],
                  avoidLabelOverlap: false,
                  itemStyle: {
                      borderRadius: 10,
                      borderColor: '#fff',
                      borderWidth: 2
                  },
                  label: {
                      show: false,
                      position: 'center'
                  },
                  emphasis: {
                      label: {
                          show: true,
                          fontSize: 40,
                          fontWeight: 'bold'
                      }
                  },
                  labelLine: {
                      show: false
                  },
                  

                  data: [
                      { value: productos_vencidos, name: 'Vencidos' },
                      { value: productos_por_vencer, name: 'Por Vencer' },
                      { value: total_cantidad_stock, name: 'OK' }
                  ]
              }
          ],
          
      };
  } catch (ex) {
      alert(ex);
  }
};



const initChart = async () => {
  try {
      const myChart = echarts.init(document.getElementById("chart"));
      const chart2 = echarts.init(document.getElementById("chart2"));

      const optionChart = await getOptionChart();
      const optionChart2 = await getOptionChart2();

      myChart.setOption(optionChart);
      chart2.setOption(optionChart2);

      myChart.resize();
  } catch (ex) {
      alert(ex);
  }
};

window.addEventListener("load", async () => {
  await initChart();
});


