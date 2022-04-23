## Android
- 設定憑證 ( Burp / Fiddler )
  1. [開啟 Nox](https://blog.xuite.net/emuking/DB/590071844)
  2. 憑證命名為 AABBCCDD.0 [( 例如 fiddler 產生的憑證 )](https://github.com/raymond-chia/Note/blob/main/Security.md#fiddler)
  3. `adb devices` 應該列出
    ```
    List of devices attached
    127.0.0.1:{port} device
    ```
  4. `adb connect 127.0.0.1:{port}`
  5. `adb root` ( 取得 root 權限 )
  6. `adb remount` ( 把 system 目錄權限從唯讀改成讀寫 )
  7. `adb push AABBCCDD.0 /system/etc/security/cacerts` ( 複製憑證到 Android )
  8. `adb shell chmod 644 /system/etc/security/cacerts/AABBCCDD.0` ( rwx )
- Nox
  - 內建 Android Debug Bridge ( Nox/bin )
  - 使用 proxy
    1. 下滑
    2. 長按 wifi
    3. 長按目前連上的 wifi
    4. proxy 設定手動
    5. 設定 proxy host name & proxy port
  - [查看 CPU arch](https://blog.csdn.net/qq_36317441/article/details/89494686)
    - adb shell getprop ro.product.cpu.abi

## [Cross-site request forgery](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)
- 假裝受害者發送 request, 執行危險操作
- Do not use GET requests for state changing operations.
- CSRF token
  - The CSRF token can be added through hidden fields, headers, and can be used with forms, and AJAX calls.
  - CSRF tokens in GET requests are potentially leaked at several locations
  - [Double submit cookie](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html#double-submit-cookie)
    - We send a random value in both a cookie and as a request parameter
    - Include the token in an encrypted cookie / use HMAC
      - a sub domain has no way to over-write an properly crafted encrypted cookie
    - Set cookie attribute properly: SameSite, HTTPOnly, Secure
- Remember that any Cross-Site Scripting (XSS) can be used to defeat all CSRF mitigation techniques!
- 別相信 header 資訊 ( picoctf who are you )

## Fiddler
- [當作 Proxy](https://docs.telerik.com/fiddler/configure-fiddler/tasks/usefiddlerasreverseproxy)
- [Capture Android](https://docs.telerik.com/fiddler/configure-fiddler/tasks/configureforandroid)
- 輸出憑證
  1. Tools/HTTPS 右上角有 Actions
  2. 選 export root certificate to desktop

## Frida
- [Frida](https://frida.re/)
- [Objection](https://github.com/sensepost/objection)
- 注入 frida-gadget [ref1](https://koz.io/using-frida-on-android-without-root/) [ref2](https://gist.github.com/elevenchars/380a210bf3c91534e7ef4c346543c743)
  - [Frida Gadget contains most of the functionality of Frida, but encapsulated in a dynamic library that gets loaded by the target app at runtime, allowing you to instrument and modify the target app’s code.](https://www.netspi.com/blog/technical/mobile-application-penetration-testing/four-ways-bypass-android-ssl-verification-certificate-pinning/)
  1. `apktool d -o out_dir original.apk` ( decompile )
  2. download frida gadget
  3. extract the compressed archive
  4. copy frida gadget library in {cpu arch} directory under lib  
    for example: for armeabi (32bit ARM) mobile  
    `cp frida_libs/armeabi/frida-gadget-9.1.26-android-arm.so out_dir/lib/armeabi/libfrida-gadget.so`
  5. inject a System.loadLibrary("frida-gadget") call in entry point  
    find entry point in android:name in AndroidManifest.xml: `<activity android:label="@string/app_name" android:name="com.packagename.path.to.MainActivity">`  
      ```
      const-string v0, "frida-gadget"
      
      invoke-static {v0}, Ljava/lang/System;->loadLibrary(Ljava/lang/String;)V
      ```  
      It's important that this is done early in the app's lifecycle, so we can do it in the MainActivity static constructor.  
      for example:  
      ```
      .method static constructor <clinit>()V
      .locals 1 # this is the number of non-param registers
      {insert here after the .locals line}
      ...
      ```
  6. Add the Internet permission to the manifest if it’s not there already, so that Frida gadget can open a socket.  
    <uses-permission android:name="android.permission.INTERNET" />
  7. `apktool b -o repackaged.apk out_dir` ( rebuild )
    - [locales_config.xml not found](https://github.com/iBotPeaches/Apktool/issues/2756#issuecomment-1059370741)
  8. Use apksigner to sign the app
    - [keystore](https://keystore-explorer.org/downloads.html)

## OAuth 2.0
- Proof Key for Code Exchange
  - [When public clients (e.g., native and single-page applications) request Access Tokens, some additional security concerns are posed that are not mitigated by the Authorization Code Flow alone.](https://auth0.com/docs/get-started/authentication-and-authorization-flow/authorization-code-flow-with-proof-key-for-code-exchange-pkce)
    - Cannot securely store a Client Secret.
    - May make use of a custom URL scheme to capture redirects (e.g., MyApp://) potentially allowing malicious applications to receive an Authorization Code from your Authorization Server.

## One time password
- [生日攻擊](https://zh.wikipedia.org/wiki/%E7%94%9F%E6%97%A5%E6%94%BB%E5%87%BB)
  - 一個人的生日在某一天的機率是 1/365
  - 30 個人有一個人在某一天的機率是 1 - (364/365)**30 = 0.079
  - 30 個人至少有兩人相同生日的機率 [1 - 365!/((365-30)! * 365**30)](https://zh.wikipedia.org/wiki/%E7%94%9F%E6%97%A5%E5%95%8F%E9%A1%8C) = 0.706
  - https://auth0.com/blog/birthday-attacks-collisions-and-password-strength/
  - 不能單靠 one time password 判斷身份
- 密碼組合: H 種, rate limit: R 次
  - 一人連猜 R 次都錯的機率 (H - 1)/H * (H - 2)/H * ... (H - R)/H = `(H - 1)! / ((H - R - 1)! * H ** R)`
  - 連猜 N 人,每人 R 次都錯的機率 ((H - 1)! / ((H - R - 1)! * H ** R)) ** N
    - 六位數, rate limit 3 次, 猜 115500 人有 50% 命中
- [Reset password](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html)

## Wireshark
- for every new TLS 1.3 session handshake, session keys will be created and stored in a local SSL key log file
  1. 指定 SSL key log file 儲存位置
  2. Wireshark `edit/preferences/Protocols/TLS/(Pre)-Master-Secret log filename` 設定 SSL key log file 位置
- https://www.youtube.com/watch?v=GMNOT1aZmD8
- https://www.comparitech.com/net-admin/decrypt-ssl-with-wireshark/

## Resources
- https://www.youtube.com/c/JohnHammond010/videos
- https://www.youtube.com/c/DavidBombal/videos
- https://www.hacksplaining.com/lessons
- https://cheatsheetseries.owasp.org/index.html

