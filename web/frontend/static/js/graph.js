export function renderCharts() {
  const categoryCtx = document.getElementById('categoryChart');
  new Chart(categoryCtx, {
      type: 'pie',
      data: {
      labels: ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books'],
      datasets: [{
          data: [30, 25, 20, 15, 10],
          backgroundColor: ['#8884d8', '#82ca9d', '#ffc658', '#ff7c7c', '#8dd1e1']
      }]
      }
  });

  const performanceCtx = document.getElementById('performanceChart');
  new Chart(performanceCtx, {
      type: 'bar',
      data: {
      labels: ['Q1', 'Q2', 'Q3', 'Q4'],
      datasets: [{
          label: 'Performance',
          data: [85, 92, 78, 96],
          backgroundColor: '#8884d8'
      }]
      }
  });
}
