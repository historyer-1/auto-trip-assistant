const TOKEN_KEY = 'trip-assistant-token';

let plannerTimer = null;

function ok(data, message) {
    return {code: 0, message: message || 'success', data};
}

function fail(code, message) {
    return {code, message, data: null};
}

/**
 * 保存登录令牌到本地存储。
 * @param {string} token JWT令牌字符串
 * @returns {void} 无返回值
 */
function setToken(token) {
    localStorage.setItem(TOKEN_KEY, token);
}

/**
 * 从本地存储读取登录令牌。
 * @param {void} 无参数
 * @returns {string|null} JWT令牌或空值
 */
function getToken() {
    return localStorage.getItem(TOKEN_KEY);
}

/**
 * 清理本地存储中的登录令牌。
 * @param {void} 无参数
 * @returns {void} 无返回值
 */
function clearToken() {
    localStorage.removeItem(TOKEN_KEY);
}

/**
 * 判断当前请求是否需要自动携带token。
 * @param {string} url 请求路径
 * @returns {boolean} true表示需要携带，false表示无需携带
 */
function shouldAttachToken(url) {
    return url !== '/api/auth/send-code' && url !== '/api/auth/login';
}

function normalizeResult(payload) {
    if (!payload || typeof payload !== 'object') {
        return fail(500, '接口返回格式错误');
    }
    if (typeof payload.code !== 'number') {
        return fail(500, '接口返回缺少 code 字段');
    }
    return {
        code: payload.code,
        message: typeof payload.message === 'string' ? payload.message : '',
        data: Object.prototype.hasOwnProperty.call(payload, 'data') ? payload.data : null
    };
}

async function realApiFetch(url, options) {
    try {
        // 构造默认请求头，并在需要时拼接Authorization令牌。
        const headers = {
            'Content-Type': 'application/json'
        };

        const token = getToken();
        if (token && shouldAttachToken(url)) {
            headers.Authorization = `Bearer ${token}`;
        }

        const response = await fetch(url, {
            credentials: 'same-origin',
            headers,
            ...options
        });

        let payload = null;
        try {
            payload = await response.json();
        } catch (err) {
            if (!response.ok) {
                return fail(response.status, `请求失败: ${response.status}`);
            }
            return fail(500, '响应不是合法 JSON');
        }

        const result = normalizeResult(payload);
        // 401表示登录态失效，需要清理本地token。
        if (response.status === 401) {
            clearToken();
        }
        if (!response.ok && result.code === 0) {
            return fail(response.status, result.message || `请求失败: ${response.status}`);
        }
        return result;
    } catch (err) {
        return fail(500, '网络异常，请稍后重试');
    }
}

async function apiFetch(url, options) {
    return realApiFetch(url, options);
}

function setMessage(text, isError) {
    const message = document.getElementById('loginMessage');
    if (!message) {
        return;
    }
    message.textContent = text;
    message.style.color = isError ? '#c74d3d' : '#8f5a00';
}

function bindLoginPage() {
    const sendCodeBtn = document.getElementById('sendCodeBtn');
    const loginBtn = document.getElementById('loginBtn');
    if (!sendCodeBtn || !loginBtn) {
        return;
    }

    const emailInput = document.getElementById('email');
    const codeInput = document.getElementById('code');
    let countdown = null;
    let remain = 0;

    function startCountdown() {
        remain = 60;
        sendCodeBtn.disabled = true;
        sendCodeBtn.textContent = `${remain}s 后重试`;
        countdown = setInterval(() => {
            remain -= 1;
            if (remain <= 0) {
                clearInterval(countdown);
                sendCodeBtn.disabled = false;
                sendCodeBtn.textContent = '发送验证码';
                return;
            }
            sendCodeBtn.textContent = `${remain}s 后重试`;
        }, 1000);
    }

    sendCodeBtn.addEventListener('click', async () => {
        const email = emailInput.value.trim();
        if (!email) {
            setMessage('请先输入邮箱地址', true);
            return;
        }
        const result = await apiFetch('/api/auth/send-code', {
            method: 'POST',
            body: JSON.stringify({email})
        });
        if (result.code !== 0) {
            setMessage(result.message, true);
            return;
        }
        startCountdown();
        setMessage(result.message, false);
    });

    loginBtn.addEventListener('click', async () => {
        const email = emailInput.value.trim();
        const code = codeInput.value.trim();
        if (!email || !code) {
            setMessage('请输入邮箱和验证码', true);
            return;
        }
        const result = await apiFetch('/api/auth/login', {
            method: 'POST',
            body: JSON.stringify({email, code})
        });
        if (result.code !== 0) {
            setMessage(result.message, true);
            return;
        }
        // 登录成功后持久化token，供后续接口鉴权使用。
        if (result.data && result.data.token) {
            setToken(result.data.token);
        }
        setMessage(result.message, false);
        window.location.href = '/trip/dashboard';
    });
}

async function loadOverview() {
    const box = document.getElementById('overviewBox');
    const result = await apiFetch('/api/trip/overview');
    if (result.code !== 0) {
        box.textContent = result.message;
        return;
    }
    const data = result.data;
    box.innerHTML = `
        <p><strong>目的地：</strong>${data.city}</p>
        <p><strong>日期：</strong>${data.startDate} 至 ${data.endDate}</p>
        <p><strong>建议：</strong>${data.suggestion}</p>
    `;
}

async function loadBudget() {
    const box = document.getElementById('budgetBox');
    const result = await apiFetch('/api/trip/budget');
    if (result.code !== 0) {
        box.textContent = result.message;
        return;
    }
    const d = result.data;
    const items = [
        ['景点门票', d.ticketCost],
        ['酒店住宿', d.hotelCost],
        ['餐饮费用', d.foodCost],
        ['交通费用', d.transportCost],
        ['预计总费用', d.totalCost]
    ];
    box.innerHTML = items.map(item => `
        <div class="budget-item">
            <div>${item[0]}</div>
            <div class="money">¥${item[1]}</div>
        </div>
    `).join('');
}

async function loadMap() {
    const box = document.getElementById('mapBox');
    const result = await apiFetch('/api/trip/map-points');
    if (result.code !== 0) {
        box.textContent = result.message;
        return;
    }

    const pointHtml = result.data.map(point => `
        <div class="map-point" style="left:${point.x}%;top:${point.y}%;" title="${point.name}">${point.id}</div>
    `).join('');

    const legendHtml = result.data.map(point => `<div>${point.id}. ${point.name}</div>`).join('');

    box.innerHTML = `${pointHtml}<div class="map-legend">${legendHtml}</div>`;
}

function renderSpotCard(spot, dayIndex) {
    return `
        <div class="spot-card" data-day="${dayIndex}" data-order="${spot.order}">
            <div class="spot-head">
                <strong>${spot.name}</strong>
                <div class="spot-actions">
                    <button class="icon-btn" type="button" data-action="edit">编辑</button>
                    <button class="icon-btn delete" type="button" data-action="delete">删除</button>
                </div>
            </div>
            <img src="${spot.imageUrl}" alt="${spot.name}">
            <div class="spot-content">
                <label class="field-label">地址</label>
                <input type="text" value="${spot.address}" disabled>
                <label class="field-label">游览时长(分钟)</label>
                <input type="number" value="${spot.minutes}" disabled>
                <label class="field-label">描述</label>
                <textarea rows="2" disabled>${spot.desc}</textarea>
            </div>
        </div>
    `;
}

async function loadDailyPlans() {
    const box = document.getElementById('dailyBox');
    const result = await apiFetch('/api/trip/daily-plans');
    if (result.code !== 0) {
        box.textContent = result.message;
        return;
    }

    box.innerHTML = result.data.map(day => {
        const spots = day.spots.map(spot => renderSpotCard(spot, day.dayIndex)).join('');
        const mealRows = day.meals.map(meal => `
            <tr>
                <td>${meal.type}</td>
                <td>${meal.recommendation}</td>
            </tr>
        `).join('');

        return `
            <div class="day-panel">
                <button type="button" class="day-head" data-day="${day.dayIndex}">
                    <span>第${day.dayIndex}天</span>
                    <span>${day.date}</span>
                </button>
                <div class="day-body" id="day-${day.dayIndex}">
                    <div class="day-meta">
                        <div><strong>行程描述：</strong>${day.description}</div>
                        <div><strong>交通方式：</strong>${day.transport}</div>
                        <div><strong>住宿：</strong>${day.hotel}</div>
                    </div>
                    <h4>景点安排</h4>
                    <div class="spot-grid">${spots}</div>
                    <h4>住宿推荐</h4>
                    <div class="recommend-card">
                        <div class="recommend-title">${day.hotelSuggestion.name}</div>
                        <div>地址：${day.hotelSuggestion.address}</div>
                        <div>价格：${day.hotelSuggestion.priceRange}</div>
                        <div>类型：${day.hotelSuggestion.type}</div>
                        <div>评分：${day.hotelSuggestion.rating}</div>
                        <div>距离：${day.hotelSuggestion.distance}</div>
                    </div>
                    <h4>餐饮安排</h4>
                    <table>
                        <tr><th>时段</th><th>推荐</th></tr>
                        ${mealRows}
                    </table>
                </div>
            </div>
        `;
    }).join('');

    bindDayToggle();
    bindSpotActions();
}

async function loadWeather() {
    const box = document.getElementById('weatherBox');
    const result = await apiFetch('/api/trip/weather');
    if (result.code !== 0) {
        box.textContent = result.message;
        return;
    }

    box.innerHTML = result.data.map(item => `
        <div class="weather-item">
            <strong>${item.date} ${item.condition}</strong>
            <div>温度：${item.temp}</div>
            <div>${item.tip}</div>
        </div>
    `).join('');
}

function bindDayToggle() {
    document.querySelectorAll('.day-head').forEach(head => {
        head.addEventListener('click', () => {
            const day = head.getAttribute('data-day');
            const body = document.getElementById(`day-${day}`);
            body.classList.toggle('open');
        });
    });

    const first = document.querySelector('.day-body');
    if (first) {
        first.classList.add('open');
    }
}

function bindSpotActions() {
    document.querySelectorAll('.icon-btn').forEach(btn => {
        btn.addEventListener('click', event => {
            const action = event.currentTarget.getAttribute('data-action');
            const card = event.currentTarget.closest('.spot-card');
            if (action === 'delete') {
                card.remove();
                return;
            }
            if (action === 'edit') {
                const inputs = card.querySelectorAll('input, textarea');
                const isDisabled = inputs[0] && inputs[0].disabled;
                inputs.forEach(input => {
                    input.disabled = !isDisabled;
                });
                event.currentTarget.textContent = isDisabled ? '保存' : '编辑';
            }
        });
    });
}

function bindToolbar() {
    const logoutBtn = document.getElementById('logoutBtn');
    const backHomeBtn = document.getElementById('backHomeBtn');
    const editTripBtn = document.getElementById('editTripBtn');
    const exportTripBtn = document.getElementById('exportTripBtn');

    if (logoutBtn) {
        logoutBtn.addEventListener('click', async () => {
            const result = await apiFetch('/api/auth/logout', {method: 'POST'});
            if (result.code !== 0) {
                alert(result.message || '退出失败，请重试');
                return;
            }
            window.location.href = '/login';
        });
    }

    if (backHomeBtn) {
        backHomeBtn.addEventListener('click', () => {
            window.scrollTo({top: 0, behavior: 'smooth'});
        });
    }

    if (editTripBtn) {
        editTripBtn.addEventListener('click', () => {
            alert('前端演示：可在每日行程中点击“编辑”修改景点信息。');
        });
    }

    if (exportTripBtn) {
        exportTripBtn.addEventListener('click', () => {
            window.print();
        });
    }
}

function getPlannerElements() {
    return {
        cityInput: document.getElementById('cityInput'),
        startDateInput: document.getElementById('startDateInput'),
        endDateInput: document.getElementById('endDateInput'),
        transportSelect: document.getElementById('transportSelect'),
        hotelSelect: document.getElementById('hotelSelect'),
        extraInput: document.getElementById('extraInput'),
        generateBtn: document.getElementById('generateBtn'),
        generateStatus: document.getElementById('generateStatus'),
        progressBar: document.getElementById('progressBar')
    };
}

function calcTripDays(startDate, endDate) {
    const start = new Date(startDate);
    const end = new Date(endDate);
    if (Number.isNaN(start.getTime()) || Number.isNaN(end.getTime()) || end < start) {
        return 0;
    }
    const diff = end.getTime() - start.getTime();
    return Math.floor(diff / (24 * 60 * 60 * 1000)) + 1;
}

function shiftDate(baseDate, offset) {
    const date = new Date(baseDate);
    if (Number.isNaN(date.getTime())) {
        return baseDate;
    }
    date.setDate(date.getDate() + offset);
    const y = date.getFullYear();
    const m = String(date.getMonth() + 1).padStart(2, '0');
    const d = String(date.getDate()).padStart(2, '0');
    return `${y}-${m}-${d}`;
}

function bindPlanner() {
    const els = getPlannerElements();
    if (!els.generateBtn) {
        return;
    }

    els.generateBtn.addEventListener('click', async () => {
        const formData = {
            city: (els.cityInput.value || '').trim(),
            startDate: els.startDateInput.value,
            endDate: els.endDateInput.value,
            transport: els.transportSelect.value,
            hotel: els.hotelSelect.value,
            extra: (els.extraInput.value || '').trim()
        };

        if (!formData.city || !formData.startDate || !formData.endDate) {
            els.generateStatus.textContent = '请填写完整的目的地与日期信息';
            return;
        }

        const tripDays = calcTripDays(formData.startDate, formData.endDate);
        if (tripDays <= 0) {
            els.generateStatus.textContent = '结束日期不能早于开始日期';
            return;
        }

        if (plannerTimer) {
            clearInterval(plannerTimer);
        }

        els.generateBtn.disabled = true;
        els.generateStatus.textContent = `正在生成 ${formData.city} ${tripDays} 天行程...`;
        els.progressBar.style.width = '0%';

        let progress = 0;
        plannerTimer = setInterval(async () => {
            progress += Math.floor(Math.random() * 18) + 9;
            if (progress >= 100) {
                progress = 100;
            }
            els.progressBar.style.width = `${progress}%`;

            if (progress < 100) {
                return;
            }

            clearInterval(plannerTimer);
            plannerTimer = null;

            await Promise.all([loadOverview(), loadBudget(), loadMap(), loadDailyPlans(), loadWeather()]);

            els.generateStatus.textContent = `已完成：${formData.city} ${tripDays} 天行程已生成`;
            els.generateBtn.disabled = false;
        }, 300);
    });
}

async function bindDashboard() {
    const overviewBox = document.getElementById('overviewBox');
    if (!overviewBox) {
        return;
    }

    const loginCheck = await apiFetch('/api/auth/me');
    if (loginCheck.code !== 0) {
        window.location.href = '/login';
        return;
    }

    bindToolbar();
    bindPlanner();
    await Promise.all([loadOverview(), loadBudget(), loadMap(), loadDailyPlans(), loadWeather()]);
}

document.addEventListener('DOMContentLoaded', () => {
    bindLoginPage();
    bindDashboard();
});

