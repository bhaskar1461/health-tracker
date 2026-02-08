const storedApiBase = localStorage.getItem('apiBase');
const defaultApiBase = window.location.origin;
const config = {
  apiBase: (storedApiBase || defaultApiBase).replace(/\/$/, ''),
  token: localStorage.getItem('accessToken') || '',
};

function buildHeaders(extra = {}){
  const headers = {...extra};
  if (config.token){
    headers.Authorization = `Bearer ${config.token}`;
  }
  return headers;
}

function createRing(container, percent){
  // create simple SVG ring
  container.innerHTML = '';
  const size = 120;
  const stroke = 12;
  const r = (size - stroke) / 2;
  const c = document.createElementNS('http://www.w3.org/2000/svg','svg');
  c.setAttribute('width', size);
  c.setAttribute('height', size);
  c.setAttribute('viewBox', `0 0 ${size} ${size}`);
  // defs + gradient
  const defs = document.createElementNS(c.namespaceURI,'defs');
  const gradId = 'g' + Math.floor(Math.random()*100000);
  const lg = document.createElementNS(c.namespaceURI,'linearGradient');
  lg.setAttribute('id', gradId);
  lg.setAttribute('x1','0%'); lg.setAttribute('y1','0%'); lg.setAttribute('x2','100%'); lg.setAttribute('y2','0%');
  const stop1 = document.createElementNS(c.namespaceURI,'stop'); stop1.setAttribute('offset','0%'); stop1.setAttribute('stop-color','#ff9a9e');
  const stop2 = document.createElementNS(c.namespaceURI,'stop'); stop2.setAttribute('offset','100%'); stop2.setAttribute('stop-color','#ff3b30');
  lg.appendChild(stop1); lg.appendChild(stop2); defs.appendChild(lg);

  const bg = document.createElementNS(c.namespaceURI,'circle');
  bg.setAttribute('cx', size/2); bg.setAttribute('cy', size/2); bg.setAttribute('r', r);
  bg.setAttribute('stroke', 'rgba(14,165,233,0.08)'); bg.setAttribute('stroke-width', stroke); bg.setAttribute('fill','none');
  const fg = document.createElementNS(c.namespaceURI,'circle');
  fg.setAttribute('cx', size/2); fg.setAttribute('cy', size/2); fg.setAttribute('r', r);
  fg.setAttribute('stroke', `url(#${gradId})`); fg.setAttribute('stroke-width', stroke); fg.setAttribute('fill','none');
  fg.setAttribute('stroke-linecap','round');
  const circumference = 2 * Math.PI * r;
  fg.setAttribute('stroke-dasharray', `${circumference} ${circumference}`);
  // animate from full to target
  fg.setAttribute('stroke-dashoffset', circumference);
  fg.setAttribute('transform', `rotate(-90 ${size/2} ${size/2})`);
  c.appendChild(defs);
  c.appendChild(bg); c.appendChild(fg);
  // centered label
  const label = document.createElement('div');
  label.className = 'ring-label';
  label.style.position = 'absolute';
  label.style.left = '50%';
  label.style.top = '50%';
  label.style.transform = 'translate(-50%,-50%)';
  label.style.textAlign = 'center';
  label.innerHTML = `<div style="font-weight:700;font-size:16px;color:#0b1220">${Math.round(percent)}%</div><div style="font-size:11px;color:#6b7280">of goal</div>`;
  container.innerHTML = '';
  container.appendChild(c);
  container.appendChild(label);
  // animate stroke
  setTimeout(()=>{
    const offset = circumference * (1 - Math.max(0, Math.min(1, percent/100)));
    fg.style.transition = 'stroke-dashoffset 900ms cubic-bezier(.2,.9,.2,1)';
    fg.setAttribute('stroke-dashoffset', offset);
  },50);
}

function renderCards(latest){
  const cards = document.getElementById('cards');
  cards.innerHTML = '';
  const items = [
    {title: 'Move', value: latest.calories_burned ? `${latest.calories_burned} cal` : '—', color:'#ff3b30'},
    {title: 'Exercise', value: latest.exercise_minutes ? `${latest.exercise_minutes} min` : '—', color:'#34c759'},
    {title: 'Stand', value: latest.stand_hours ? `${latest.stand_hours} hr` : '—', color:'#007aff'},
  ];
  for(const it of items){
    const el = document.createElement('div'); el.className='small-card';
    el.innerHTML = `<div><div class="title">${it.title}</div><div class="value">${it.value}</div></div>`;
    cards.appendChild(el);
  }
}

function renderSleepChart(sleepStages){
  const c = document.getElementById('sleepChart');
  c.innerHTML = '';
  try{
    const stages = typeof sleepStages === 'string' ? JSON.parse(sleepStages) : sleepStages;
    // stages: {rem, core, deep}
    const total = (stages.rem||0) + (stages.core||0) + (stages.deep||0);
    if(total === 0) { c.textContent = 'No sleep stages'; return }
    const width = 100;
    const remW = (stages.rem/total)*100;
    const coreW = (stages.core/total)*100;
    const deepW = (stages.deep/total)*100;
    const rem = document.createElement('div'); rem.className='sleep-seg'; rem.style.width = '0%'; rem.style.background='#4f46e5';
    const core = document.createElement('div'); core.className='sleep-seg'; core.style.width = '0%'; core.style.background='#60a5fa';
    const deep = document.createElement('div'); deep.className='sleep-seg'; deep.style.width = '0%'; deep.style.background='#06b6d4';
    c.appendChild(rem); c.appendChild(core); c.appendChild(deep);
    // animate widths
    setTimeout(()=>{ rem.style.width = remW+'%'; rem.style.opacity=1; core.style.width = coreW+'%'; core.style.opacity=1; deep.style.width = deepW+'%'; deep.style.opacity=1 },30);
  }catch(e){ c.textContent='Invalid sleep data' }
}

function renderHRChart(latest){
  const svg = document.getElementById('hrChart');
  while(svg.firstChild) svg.removeChild(svg.firstChild);
  // simple single value bar representing resting heart rate
  const val = latest.resting_heart_rate || 0;
  const max = 200;
  const h = 60; const w = 200;
  const barW = 20; const x = 20;
  const height = Math.max(2, (val/max)*h);
  const rect = document.createElementNS('http://www.w3.org/2000/svg','rect');
  rect.setAttribute('x', x); rect.setAttribute('y', h - height + 10); rect.setAttribute('width', barW); rect.setAttribute('height', height);
  rect.setAttribute('fill', '#ff3b30'); svg.appendChild(rect);
  const txt = document.createElementNS(svg.namespaceURI,'text'); txt.setAttribute('x', x+barW+8); txt.setAttribute('y', h/2+12);
  txt.setAttribute('fill','#111'); txt.setAttribute('font-size','12'); txt.textContent = `${val} BPM`;
  svg.appendChild(txt);
}

async function fetchSummary(){
  const el = document.getElementById('summary');
  try{
    const res = await fetch(`${config.apiBase}/api/v1/health-data/summary`, {headers: buildHeaders()});
    if(!res.ok){ el.textContent = 'No summary (start backend and create a user)'; return }
    const data = await res.json();
    const latest = data.latest;
    el.innerHTML = '';
    if(!latest){ el.textContent='No health entries yet.'; return }
    const pre = document.createElement('pre'); pre.textContent = '';
    el.appendChild(pre);
    // Populate ring: use calories progress against a goal (example goal 500 cal)
    const goal = 500;
    const percent = latest.calories_burned ? Math.min(100, (latest.calories_burned/goal)*100) : 0;
    createRing(document.getElementById('activityRing'), percent);
    renderCards(latest);
    renderSleepChart(latest.sleep_stages);
    renderHRChart(latest);
  }catch(e){ el.textContent = 'Error fetching summary: '+e.message }
}

async function submitEntry(){
  const form = document.getElementById('dataForm');
  const fd = new FormData(form);
  const body = {};
  for(const [k,v] of fd.entries()){
    if(v === '') continue;
    if(['calories_burned','exercise_minutes','stand_hours','resting_heart_rate','respiratory_rate','sleep_duration','sleep_quality'].includes(k)){
      body[k] = Number(v);
    } else {
      body[k] = v;
    }
  }
  try{
    document.getElementById('submitBtn').disabled = true;
    const res = await fetch(`${config.apiBase}/api/v1/health-data/`, {method: 'POST', headers: buildHeaders({'Content-Type':'application/json'}), body: JSON.stringify(body)});
    if(!res.ok){ const txt = await res.text(); alert('Failed: '+txt); return }
    alert('Entry created');
    fetchSummary();
  }catch(e){ alert('Error: '+e.message) }
  finally{ document.getElementById('submitBtn').disabled = false }
}

async function syncFromZepp(){
  try{
    document.getElementById('syncBtn').disabled = true;
    document.getElementById('syncBtn').textContent = 'Syncing...';
    const res = await fetch(`${config.apiBase}/api/v1/health-data/sync-zepp`, {method: 'POST', headers: buildHeaders({'Content-Type':'application/json'})});
    if(!res.ok){
      const error = await res.json();
      alert('Sync failed: ' + (error.detail || 'Unknown error'));
      return;
    }
    const data = await res.json();
    alert('Successfully synced from Zepp!\nCalories: ' + (data.data.calories_burned || 0));
    fetchSummary();
  }catch(e){ alert('Error syncing: '+e.message) }
  finally{
    document.getElementById('syncBtn').disabled = false;
    document.getElementById('syncBtn').textContent = 'Sync from Zepp';
  }
}

function loadConfigUI(){
  const apiBaseInput = document.getElementById('apiBaseInput');
  const tokenInput = document.getElementById('tokenInput');
  if (apiBaseInput) apiBaseInput.value = config.apiBase;
  if (tokenInput) tokenInput.value = config.token;
}

function saveConfig(){
  const apiBaseInput = document.getElementById('apiBaseInput');
  const tokenInput = document.getElementById('tokenInput');
  if (apiBaseInput && apiBaseInput.value){
    config.apiBase = apiBaseInput.value.replace(/\/$/, '');
    localStorage.setItem('apiBase', config.apiBase);
  }
  if (tokenInput){
    config.token = tokenInput.value.trim();
    if (config.token){
      localStorage.setItem('accessToken', config.token);
    } else {
      localStorage.removeItem('accessToken');
    }
  }
  fetchSummary();
}

window.addEventListener('load', ()=>{ 
  loadConfigUI();
  fetchSummary();
  document.getElementById('submitBtn').addEventListener('click', submitEntry);
  document.getElementById('syncBtn').addEventListener('click', syncFromZepp);
  const saveBtn = document.getElementById('saveConfigBtn');
  if (saveBtn) saveBtn.addEventListener('click', saveConfig);
})
