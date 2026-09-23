// popup:列出快照日期 → 選一天 → 在新視窗開啟該天所有分頁。

const datesEl = document.getElementById("dates");
const infoEl = document.getElementById("info");
const restoreBtn = document.getElementById("restore");
const snapBtn = document.getElementById("snap");

let snapshots = {};

async function load() {
  const data = await chrome.storage.local.get("snapshots");
  snapshots = data.snapshots || {};
  render();
}

function render() {
  const keys = Object.keys(snapshots).sort().reverse(); // 最新在最上面
  datesEl.innerHTML = "";

  if (keys.length === 0) {
    const opt = document.createElement("option");
    opt.textContent = "(尚無快照)";
    datesEl.appendChild(opt);
    datesEl.disabled = true;
    restoreBtn.disabled = true;
    infoEl.textContent = "還沒有任何快照。按「立即快照」建立第一份。";
    return;
  }

  datesEl.disabled = false;
  restoreBtn.disabled = false;
  for (const k of keys) {
    const opt = document.createElement("option");
    opt.value = k;
    opt.textContent = `${k}(${snapshots[k].count} 個分頁)`;
    datesEl.appendChild(opt);
  }
  updateInfo();
}

function updateInfo() {
  const snap = snapshots[datesEl.value];
  if (!snap) {
    infoEl.textContent = "";
    return;
  }
  const t = new Date(snap.savedAt);
  infoEl.textContent = `存於 ${t.toLocaleString()},共 ${snap.count} 個分頁`;
}

datesEl.addEventListener("change", updateInfo);

restoreBtn.addEventListener("click", async () => {
  const snap = snapshots[datesEl.value];
  if (!snap || snap.tabs.length === 0) return;
  const urls = snap.tabs.map((t) => t.url);
  await chrome.windows.create({ url: urls });
  window.close();
});

snapBtn.addEventListener("click", () => {
  snapBtn.disabled = true;
  snapBtn.textContent = "快照中…";
  chrome.runtime.sendMessage({ type: "snapshot-now" }, (resp) => {
    snapBtn.disabled = false;
    snapBtn.textContent = "立即快照";
    if (resp && resp.ok) load();
  });
});

load();
