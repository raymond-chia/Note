// Tab Snapshot — 每天固定時間快照所有分頁,保留最近 30 天。資料只存 chrome.storage.local。

const SNAPSHOT_HOUR = 11;    // 每天快照時間(24 小時制)
const SNAPSHOT_MINUTE = 0;
const KEEP_DAYS = 30;        // 保留天數
const ALARM_NAME = "daily-snapshot";

// 排除的登入頁 URL 樣式
const EXCLUDE_PATTERNS = [
  /\/users\/sign_in/i,
  /accounts\.google\.com/i,
  /\/oauth\//i,
];

function isExcluded(url) {
  if (!url) return true;
  if (!/^https?:/i.test(url)) return true; // 跳過 chrome://、about:、擴充頁等
  return EXCLUDE_PATTERNS.some((re) => re.test(url));
}

// 本機日期字串 YYYY-MM-DD(用本地時區,不用 UTC)
function localDateKey(d) {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}-${m}-${day}`;
}

// 計算下一次快照時間點的毫秒 timestamp
function nextSnapshotTime() {
  const now = new Date();
  const next = new Date(
    now.getFullYear(),
    now.getMonth(),
    now.getDate(),
    SNAPSHOT_HOUR,
    SNAPSHOT_MINUTE,
    0,
    0
  );
  if (next.getTime() <= now.getTime()) {
    next.setDate(next.getDate() + 1); // 今天時間已過 → 排明天
  }
  return next.getTime();
}

function scheduleAlarm() {
  chrome.alarms.create(ALARM_NAME, {
    when: nextSnapshotTime(),
    periodInMinutes: 24 * 60,
  });
}

// 執行快照:抓所有一般視窗的分頁,依日期覆蓋當天那份,再清掉超過 30 天的
async function takeSnapshot() {
  const tabs = await chrome.tabs.query({ windowType: "normal" });
  const items = tabs
    // 正在載入的分頁 url 可能為空,實際目標在 pendingUrl
    .map((t) => ({ url: t.url || t.pendingUrl || "", title: t.title || "" }))
    .filter((t) => !isExcluded(t.url))
    .map((t) => ({ url: t.url, title: t.title || t.url }));

  const dateKey = localDateKey(new Date());
  const { snapshots = {} } = await chrome.storage.local.get("snapshots");

  snapshots[dateKey] = {
    date: dateKey,
    savedAt: new Date().toISOString(),
    count: items.length,
    tabs: items,
  };

  // 只留最近 KEEP_DAYS 份(依日期字串排序,字典序即時間序)
  const keys = Object.keys(snapshots).sort();
  while (keys.length > KEEP_DAYS) {
    const oldest = keys.shift();
    delete snapshots[oldest];
  }

  await chrome.storage.local.set({ snapshots });
  return snapshots[dateKey];
}

chrome.runtime.onInstalled.addListener(scheduleAlarm);
chrome.runtime.onStartup.addListener(scheduleAlarm);

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === ALARM_NAME) takeSnapshot();
});

// 供 popup 呼叫:手動快照 / 讀清單
chrome.runtime.onMessage.addListener((msg, _sender, sendResponse) => {
  if (msg.type === "snapshot-now") {
    takeSnapshot().then((snap) => sendResponse({ ok: true, snap }));
    return true; // async
  }
});
