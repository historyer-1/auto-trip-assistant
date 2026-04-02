const MOCK_FLAG_KEY = 'trip-assistant-mock';
const MOCK_CODE = '123456';

const mockState = {
    sentCode: MOCK_CODE,
    userEmail: 'demo@example.com'
};

const mockData = {
    overview: {
        city: '北京',
        startDate: '2025-11-03',
        endDate: '2025-11-05',
        suggestion: '天气较好，适合户外活动。建议穿舒适步行鞋并注意早晚温差。'
    },
    budget: {
        ticketCost: 150,
        hotelCost: 1200,
        foodCost: 540,
        transportCost: 300,
        totalCost: 2190
    },
    mapPoints: [
        {id: 1, name: '北京站', x: 38, y: 17},
        {id: 2, name: '什刹海', x: 25, y: 27},
        {id: 3, name: '故宫', x: 44, y: 34},
        {id: 4, name: '北海公园', x: 22, y: 33},
        {id: 5, name: '中国国家博物馆', x: 48, y: 48},
        {id: 6, name: '北京欢乐谷', x: 72, y: 42}
    ],
    weather: [
        {date: '11-03', condition: '晴', temp: '11~19C', tip: '紫外线较强，注意防晒'},
        {date: '11-04', condition: '多云', temp: '10~17C', tip: '适合步行游览'},
        {date: '11-05', condition: '小雨', temp: '8~14C', tip: '建议携带雨具'}
    ],
    dailyPlans: [
        {
            dayIndex: 1,
            date: '2025-11-03',
            description: '游览北海公园与什刹海，体验老北京的自然与历史文化。',
            transport: '公共交通',
            hotel: '经济型酒店',
            spots: [
                {
                    order: 1,
                    name: '北海公园',
                    address: '文津街1号',
                    minutes: 120,
                    ticketPrice: 20,
                    desc: '历史悠久的皇家园林，可赏湖光与古建。',
                    imageUrl: 'https://images.unsplash.com/photo-1564501049412-61c2a3083791?auto=format&fit=crop&w=900&q=80'
                },
                {
                    order: 2,
                    name: '什刹海-后海',
                    address: '羊房胡同甲23-3号',
                    minutes: 90,
                    ticketPrice: 0,
                    desc: '胡同与水岸融合，适合傍晚散步和拍照。',
                    imageUrl: 'https://images.unsplash.com/photo-1545569341-9eb8b30979d9?auto=format&fit=crop&w=900&q=80'
                }
            ],
            hotelSuggestion: {
                name: '北京科兴宾馆',
                address: '培新街安国门写楼',
                priceRange: '300-500元',
                type: '经济型酒店',
                rating: 4.0,
                distance: '距景点约5公里'
            },
            meals: [
                {type: '早餐', recommendation: '豆浆油条和包子'},
                {type: '午餐', recommendation: '什刹海附近家常菜馆'},
                {type: '晚餐', recommendation: '后海夜市小吃'}
            ]
        },
        {
            dayIndex: 2,
            date: '2025-11-04',
            description: '白天参观博物馆，晚间前往欢乐谷体验夜景。',
            transport: '地铁+打车',
            hotel: '经济型酒店',
            spots: [
                {
                    order: 1,
                    name: '中国国家博物馆',
                    address: '东长安街16号',
                    minutes: 180,
                    ticketPrice: 0,
                    desc: '馆藏丰富，建议提前预约。',
                    imageUrl: 'https://images.unsplash.com/photo-1588681664899-f142ff2dc9b1?auto=format&fit=crop&w=900&q=80'
                },
                {
                    order: 2,
                    name: '北京欢乐谷',
                    address: '东四环小武基北路',
                    minutes: 220,
                    ticketPrice: 299,
                    desc: '夜场项目多，适合朋友同游。',
                    imageUrl: 'https://images.unsplash.com/photo-1469474968028-56623f02e42e?auto=format&fit=crop&w=900&q=80'
                }
            ],
            hotelSuggestion: {
                name: '东城区轻居酒店',
                address: '崇文门外大街',
                priceRange: '320-480元',
                type: '舒适型酒店',
                rating: 4.3,
                distance: '距地铁站约600米'
            },
            meals: [
                {type: '早餐', recommendation: '酒店简餐'},
                {type: '午餐', recommendation: '博物馆周边套餐'},
                {type: '晚餐', recommendation: '欢乐谷园区简餐'}
            ]
        },
        {
            dayIndex: 3,
            date: '2025-11-05',
            description: '探索森林湿地公园，休闲收尾。',
            transport: '公共交通',
            hotel: '经济型酒店',
            spots: [
                {
                    order: 1,
                    name: '南苑森林湿地公园',
                    address: '公槐桥公园庄',
                    minutes: 150,
                    ticketPrice: 0,
                    desc: '水域与林地景观丰富，适合慢节奏游览。',
                    imageUrl: 'https://images.unsplash.com/photo-1472396961693-142e6e269027?auto=format&fit=crop&w=900&q=80'
                },
                {
                    order: 2,
                    name: '凉水河-榴香森林公园',
                    address: '金桥东街与京庄路辅路交叉口东南200米',
                    minutes: 120,
                    ticketPrice: 0,
                    desc: '植被良好，适合休闲步行与拍照。',
                    imageUrl: 'https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=900&q=80'
                }
            ],
            hotelSuggestion: {
                name: '返程日无需续住',
                address: '可根据返程时间灵活安排',
                priceRange: '-',
                type: '无',
                rating: 0,
                distance: '-'
            },
            meals: [
                {type: '早餐', recommendation: '酒店早餐'},
                {type: '午餐', recommendation: '公园周边简餐'},
                {type: '晚餐', recommendation: '返程途中用餐'}
            ]
        }
    ]
};

let plannerTimer = null;

function ok(data, message) {
    return {code: 0, message: message || 'success', data};
}

function fail(code, message) {
    return {code, message, data: null};
}

function useMockApi() {
    const queryValue = new URLSearchParams(window.location.search).get('mock');
    if (queryValue === '1') {
        localStorage.setItem(MOCK_FLAG_KEY, '1');
        return true;
    }
    if (queryValue === '0') {
        localStorage.setItem(MOCK_FLAG_KEY, '0');
        return false;
    }
    const saved = localStorage.getItem(MOCK_FLAG_KEY);
    if (saved === null) {
        localStorage.setItem(MOCK_FLAG_KEY, '0');
        return false;
    }
    return saved === '1';
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

function tryParseBody(options) {
    if (!options || !options.body) {
        return {};
    }
    try {
        return JSON.parse(options.body);
    } catch (err) {
        return {};
    }
}

async function mockApiFetch(url, options) {
    const method = ((options && options.method) || 'GET').toUpperCase();
    const body = tryParseBody(options);
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (url === '/api/auth/send-code' && method === 'POST') {
        if (!emailRegex.test((body.email || '').trim())) {
            return fail(400, '邮箱格式不正确');
        }
        mockState.userEmail = body.email.trim();
        return ok({email: mockState.userEmail}, '验证码已发送，演示验证码为 123456');
    }

    if (url === '/api/auth/login' && method === 'POST') {
        const email = (body.email || '').trim();
        if (!emailRegex.test(email)) {
            return fail(400, '邮箱格式不正确');
        }
        if ((body.code || '').trim() !== mockState.sentCode) {
            return fail(400, '验证码错误，请输入 123456');
        }
        localStorage.setItem('trip-assistant-user', email);
        return ok({email}, '登录成功');
    }

    if (url === '/api/auth/logout' && method === 'POST') {
        localStorage.removeItem('trip-assistant-user');
        return ok(null, '退出成功');
    }

    if (url === '/api/auth/me' && method === 'GET') {
        const savedEmail = localStorage.getItem('trip-assistant-user');
        if (!savedEmail) {
            return fail(401, '请先登录');
        }
        return ok({email: savedEmail});
    }

    if (!localStorage.getItem('trip-assistant-user')) {
        return fail(401, '请先登录');
    }

    if (url === '/api/trip/overview' && method === 'GET') {
        return ok(mockData.overview);
    }
    if (url === '/api/trip/budget' && method === 'GET') {
        return ok(mockData.budget);
    }
    if (url === '/api/trip/map-points' && method === 'GET') {
        return ok(mockData.mapPoints);
    }
    if (url === '/api/trip/daily-plans' && method === 'GET') {
        return ok(mockData.dailyPlans);
    }
    if (url === '/api/trip/weather' && method === 'GET') {
        return ok(mockData.weather);
    }

    return fail(404, `未找到接口: ${method} ${url}`);
}

async function realApiFetch(url, options) {
    try {
        const response = await fetch(url, {
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json'
            },
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
        if (!response.ok && result.code === 0) {
            return fail(response.status, result.message || `请求失败: ${response.status}`);
        }
        return result;
    } catch (err) {
        return fail(500, '网络异常，请稍后重试');
    }
}

async function apiFetch(url, options) {
    if (useMockApi()) {
        return mockApiFetch(url, options);
    }
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

function applyPlannerToMockData(formData) {
    const days = calcTripDays(formData.startDate, formData.endDate);

    mockData.overview.city = formData.city;
    mockData.overview.startDate = formData.startDate;
    mockData.overview.endDate = formData.endDate;
    mockData.overview.suggestion = `${formData.city} ${days || '-'} 天行程已更新。交通偏好：${formData.transport}；住宿偏好：${formData.hotel}。${formData.extra || '建议提前预约热门景点。'}`;

    mockData.dailyPlans.forEach((day, index) => {
        day.transport = formData.transport;
        day.hotel = formData.hotel;
        day.date = shiftDate(formData.startDate, index);
        day.description = `第${day.dayIndex}天在${formData.city}游览。${formData.extra || '行程节奏以舒适休闲为主。'}`;
    });
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

            applyPlannerToMockData(formData);
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

