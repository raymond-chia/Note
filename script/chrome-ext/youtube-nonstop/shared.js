// 共用的 enabled 狀態操作

function getEnabled(callback) {
  chrome.storage.local.get("enabled", (data) => {
    // ?? 是空值合併運算子：當 data.enabled 為 null 或 undefined 時回傳 false（預設值）
    // 例如首次安裝尚未儲存過 enabled 時，data 會是空物件 {}，data.enabled 為 undefined
    callback(data.enabled ?? false);
  });
}

function setEnabled(value) {
  chrome.storage.local.set({ enabled: value });
}

function toggleEnabled(callback) {
  getEnabled((current) => {
    const next = !current;
    setEnabled(next);
    callback(next);
  });
}
