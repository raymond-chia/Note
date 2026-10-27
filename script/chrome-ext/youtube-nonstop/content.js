// YouTube NonStop — 偵測播放停止時自動恢復播放

const getPlayButton = () =>
  document.querySelector(
    "ytmusic-player-bar #play-pause-button button, ytmusic-player-bar tp-yt-paper-icon-button.play-pause-button",
  );

const isPlaying = () => getPlayButton()?.getAttribute("aria-label") === "Pause";

const clickPlay = () => getPlayButton()?.click();

// 定期檢查：啟用且停止 → 自動恢復；關閉且播放中 → 暫停
setInterval(() => {
  // extension 被更新/重新載入後，舊 content script 的 chrome API 會失效
  if (!chrome.runtime?.id) return;
  getEnabled((enabled) => {
    if (enabled && !isPlaying()) {
      clickPlay();
      console.log("[YouTube NonStop] 嘗試自動恢復播放");
    } else if (!enabled && isPlaying()) {
      clickPlay();
      console.log("[YouTube NonStop] 嘗試自動停止播放");
    }
  });
}, 1000);

// 偵測使用者手動暫停 → 關閉 extension
document.addEventListener(
  "click",
  (e) => {
    const btn = getPlayButton();
    if (btn?.contains(e.target)) {
      setEnabled(!isPlaying());
    }
  },
  true,
);

document.addEventListener("keydown", (e) => {
  if (e.code === "Space") {
    setEnabled(!isPlaying());
  }
});
