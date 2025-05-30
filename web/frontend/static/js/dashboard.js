async function loadSummary() {
  try {
    const res = await fetch("http://localhost:5001/api/summary");
    const data = await res.json();
    document.getElementById("users").textContent = data.users;
    document.getElementById("sales").textContent = data.sales;
    document.getElementById("growth").textContent = `${data.growth}%`;
  } catch (err) {
    console.error("Failed to fetch summary:", err);
  }
}

window.onload = loadSummary;