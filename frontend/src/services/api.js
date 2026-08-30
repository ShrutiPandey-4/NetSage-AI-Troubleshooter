const base=import.meta.env.VITE_API_URL||'http://localhost:8000';
export const api={get:p=>fetch(base+p).then(r=>r.json()),post:(p,b)=>fetch(base+p,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b)}).then(async r=>{const x=await r.json();if(!r.ok)throw new Error(x.detail||'Request failed');return x})};
