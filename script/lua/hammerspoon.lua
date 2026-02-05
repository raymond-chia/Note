-- ========================================
-- 剪貼簿密碼檢查
-- ========================================

-- ============ 設定區 ============
local CONFIG = {
    -- 警告文字
    title = "⚠️ 安全警告",
    message = "剪貼簿可能包含密碼",

    -- 顯示設定
    text_size = 16,        -- 字體大小（12-24）
    duration = 5,          -- 顯示秒數
    play_sound = true,     -- 播放聲音
}
-- ================================

local lastClipboard = ""

-- 檢查是否包含密碼
local function hasSensitiveData(text)
    if not text or #text < 5 then return false end

    local lower = text:lower()
    local keywords = {"password", "secret", "api_key", "apikey", "token",
"access_key", "private_key"}

    for _, word in ipairs(keywords) do
        if string.find(lower, word) and string.find(lower, "=") and
            (string.find(text, '"') or string.find(text, "'")) then
            return true
        end
    end

    -- 長隨機字串（40+ 字元）
    if string.match(text, "[A-Za-z0-9+/=]{40,}") then return true end

    -- AWS Key
    if string.match(text, "AKIA[A-Z0-9]{16}") then return true end

    return false
end

-- 建立計時器
local clipboardTimer = hs.timer.new(0.5, function()
    local current = hs.pasteboard.getContents()

    if current and current ~= lastClipboard then
        lastClipboard = current

        if hasSensitiveData(current) then
            hs.alert.show(
                CONFIG.title .. "\n" .. CONFIG.message,
                {textSize = CONFIG.text_size},
                CONFIG.duration
            )

            if CONFIG.play_sound then
                hs.sound.getByName("Basso"):play()
            end
        end
    end
end)

-- 啟動計時器
clipboardTimer:start()

-- 啟動提示
hs.alert.show("✅ 剪貼簿守護已啟動", 2)
