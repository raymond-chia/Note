"""Google OAuth 2.0 登入測試工具

用於測試 Google OAuth 2.0 設定是否正確，並顯示登入使用者的電子郵件。
"""

from typing import List, Optional
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import googleapiclient.discovery


# ============================================================================
# 常數定義
# ============================================================================

# OAuth 2.0 權限範圍
SCOPES: List[str] = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid",
]

# 設定檔路徑
CLIENT_SECRETS_FILE: str = "secret.json"

# OAuth Flow 訊息
SUCCESS_MESSAGE: str = "登入成功！您可以關閉此視窗。"


# ============================================================================
# 主要函數
# ============================================================================


def login() -> Optional[Credentials]:
    """執行 Google OAuth 2.0 登入流程。

    開啟瀏覽器讓使用者登入 Google 帳號。

    返回：
        Credentials: 認證成功的憑證物件，失敗則返回 None

    拋出：
        FileNotFoundError: 當找不到 secret.json 檔案
    """
    secrets_path = Path(CLIENT_SECRETS_FILE)

    if not secrets_path.exists():
        raise FileNotFoundError(
            f"找不到 {CLIENT_SECRETS_FILE}\n"
            f"請從 Google Cloud Console 下載 OAuth 2.0 Client ID 憑證，\n"
            f"並儲存為 {CLIENT_SECRETS_FILE}"
        )

    try:
        print("正在啟動 Google 登入流程...")
        print("瀏覽器將會開啟 Google 登入頁面\n")

        flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, scopes=SCOPES
        )

        credentials = flow.run_local_server(
            port=0, success_message=SUCCESS_MESSAGE, open_browser=True
        )

        return credentials

    except Exception as e:
        print(f"登入失敗: {e}")
        return None


def get_user_email(credentials: Credentials) -> Optional[str]:
    """取得登入使用者的電子郵件。

    參數：
        credentials: OAuth 2.0 憑證物件

    返回：
        str: 使用者的電子郵件，失敗則返回 None
    """
    try:
        # 使用 OAuth2 API 取得使用者資訊
        service = googleapiclient.discovery.build(
            "oauth2", "v2", credentials=credentials
        )

        user_info = service.userinfo().get().execute()
        return user_info.get("email")

    except Exception as e:
        print(f"取得使用者資訊失敗: {e}")
        return None


def main() -> None:
    """主程式：測試 Google 登入並顯示使用者信箱。"""
    print("=== Google OAuth 2.0 登入測試 ===\n")

    # 執行登入
    credentials = login()

    if not credentials:
        print("\n登入失敗")
        return

    print("✓ 登入成功！\n")

    # 取得並顯示使用者信箱
    email = get_user_email(credentials)

    if email:
        print(f"登入帳號: {email}")
    else:
        print("無法取得使用者信箱")


if __name__ == "__main__":
    main()
