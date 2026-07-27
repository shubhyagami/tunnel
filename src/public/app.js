const ws = new WebSocket(`ws://${window.location.host}`);
const logsBody = document.getElementById('logs-body');
const reqCountEl = document.getElementById('req-count');
const tunnelUrlEl = document.getElementById('tunnel-url');
const clearBtn = document.getElementById('clear-logs');
const statusDot = document.querySelector('.status-dot');

let requestCount = 0;

ws.onopen = () => {
    console.log('Connected to local dashboard server');
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);

    if (data.type === 'init') {
        tunnelUrlEl.textContent = data.url || 'Waiting for connection...';
        if (data.url) statusDot.classList.add('online');
    } else if (data.type === 'tunnel_url') {
        tunnelUrlEl.textContent = data.url;
        statusDot.classList.add('online');
    } else if (data.type === 'log') {
        requestCount++;
        reqCountEl.textContent = requestCount;
        appendLog(data.log);
    }
};

function appendLog(log) {
    const tr = document.createElement('tr');
    
    // Status color group
    let statusGroup = '2xx';
    if (log.statusCode >= 300) statusGroup = '3xx';
    if (log.statusCode >= 400) statusGroup = '4xx';
    if (log.statusCode >= 500) statusGroup = '5xx';

    tr.innerHTML = `
        <td style="color: var(--text-muted)">${new Date(log.timestamp).toLocaleTimeString()}</td>
        <td><span class="method ${log.method}">${log.method}</span></td>
        <td class="path">${log.url}</td>
        <td>
            <div class="status status-${statusGroup}">
                <div class="status-indicator"></div>
                ${log.statusCode}
            </div>
        </td>
        <td style="color: var(--text-muted)">${log.duration}ms</td>
    `;
    
    // Insert at top
    logsBody.insertBefore(tr, logsBody.firstChild);
    
    // Keep max 100 logs
    if (logsBody.children.length > 100) {
        logsBody.removeChild(logsBody.lastChild);
    }
}

clearBtn.addEventListener('click', () => {
    logsBody.innerHTML = '';
    requestCount = 0;
    reqCountEl.textContent = '0';
});
