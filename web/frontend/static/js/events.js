export function showDataCards() {
    const colorDefault = 'bg-white'
    const colorTexthead = 'text-gray-600'
    const colortextmd = 'text-gray-800'

    const kpis = [
    { title: 'Total Revenue', value: '$124,563', change: 12.5, color: colorDefault, colorTexthead: colorTexthead, colortextmd: colortextmd },
    { title: 'Active Users', value: '8,429', change: -2.1, color: colorDefault, colorTexthead: colorTexthead, colortextmd: colortextmd  },
    { title: 'Orders', value: '1,234', change: 8.3, color: colorDefault, colorTexthead: colorTexthead, colortextmd: colortextmd  },
    { title: 'Conversion Rate', value: '3.24%', change: 15.2, color: colorDefault, colorTexthead: colorTexthead, colortextmd: colortextmd  }
  ];

  const container = document.getElementById('kpi-container');

  kpis.forEach(kpi => {
    const card = document.createElement('div');
    card.className = `bg-white rounded-xl shadow p-6 hover:shadow-lg transition ${kpi.color}`;
    card.innerHTML = `
      <h3 class="text-lg font-bold ${colorTexthead}  mb-2">${kpi.title}</h3>
      <p class="text-3xl font-bold ${colortextmd} ">${kpi.value}</p>
      <p class="mt-2 text-white">${kpi.change > 0 ? '+' : ''}${kpi.change}%</p>
    `;
    container.appendChild(card);
  });
}