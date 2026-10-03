const API=import.meta.env.VITE_API_URL||'http://localhost:8000/api';
export async function getMonitors(){return fetch(`${API}/monitors`).then(r=>r.json())}
export async function getPrices(id:number,period='all'){return fetch(`${API}/monitors/${id}/prices?period=${period}`).then(r=>r.json())}
export async function createMonitor(body:any){return fetch(`${API}/monitors`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}).then(r=>r.json())}
export async function checkMonitor(id:number){return fetch(`${API}/monitors/${id}/check`,{method:'POST'}).then(r=>r.json())}
