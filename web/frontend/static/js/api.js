export async function loadSummary() {
  try {
    const res = await fetch('https://api.genderize.io/?name=luc');
    const data = await res.json();
    document.getElementById('textresult').textContent = data.count;
  } catch (err) {
    console.error("Failed to fetch summary:", err);
  }
}