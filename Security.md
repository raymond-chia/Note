## AI

- 檢查密碼強度 https://www.homesecurityheroes.com/ai-password-cracking/

## Analyser

- test ssl configuration https://www.ssllabs.com/ssltest/analyze.html?d=www.google.com&s=142.250.217.132
- OSV-Scanner
- Golang only: https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck

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
- [decompile](https://github.com/raymond-chia/Note/blob/main/Security.md#disassemble--decompile--debug)

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

## Disassemble / Decompile / Debug

- `ghidra`: to assembly and c maybe ?
- `strace`: detect system call
- `ltrace`: detect lib call
- `objdump`
- `gdb + gef`
- Decompile Java: [ref](https://stackoverflow.com/questions/3593420/is-there-a-way-to-get-the-source-code-from-an-apk-file) [ref](https://www.decompiler.com/)
  - [Error occurred during initialization of VM; Could not reserve enough space for object heap](https://stackoverflow.com/questions/20307923/error-occurred-during-initialization-of-vm-could-not-reserve-enough-space-for-ob)
- C#: [dnSpy](https://github.com/dnSpy/dnSpy/releases), [Rider](https://www.jetbrains.com/rider/), [ILSpy](https://github.com/icsharpcode/ILSpy)
- IL2CPP (Unity): [Il2CppInspector](https://github.com/djkaty/Il2CppInspector), [Il2CppDumper](https://github.com/Perfare/Il2CppDumper)

## DKIM

## Email login

- [Avoid user enumeration attack](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html#introduction)
  - Return a consistent message for both existent and non-existent accounts.
  - Ensure that the time taken for the user response message is uniform.
- [Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
  - Salt
  - Pepper
    - HMAC
    - Encrypt
    - Rotation (how ?)
  - [Hash algorithm](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html#work-factors)
    - As a general rule, calculating a hash should take less than one second.
      - Argon2: Argon2id is better than scrypt & bcrypt
      - scrypt
      - bcrypt: The minimum work factor for bcrypt should be 10. Has a maximum length input length of 72 bytes.
        - [Shucking](https://security.stackexchange.com/questions/234794/is-bcryptstrtolowerhexmd5pass-ok-for-storing-passwords)
          - Shucking can be used if a hash without salt is used to reduce input length for bcrypt
          - Dictionary attack with digest
      - PBKDF2
- [Reset password](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html#introduction)
  - Identify user
    - Use a side-channel to communicate the method to reset their password.
    - [One time password](https://github.com/raymond-chia/Note/blob/main/Security.md#one-time-password)
  - Do not make a change to the account until a valid token is presented, such as locking out the account.
  - Implement protections against automated submissions such as CAPTCHA, rate-limiting, security questions or other controls.
  - Ensure that the reset password page adds the Referrer Policy tag with the noreferrer value in order to avoid referrer leakage.
  - The user should confirm the new password they set by writing it twice.
  - Ensure that a secure password policy is in place, and is consistent with the rest of the application.
  - Send the user an email informing them that their password has been reset (do not send the password in the email!).
  - Once they have set their new password, the user should then login through the usual mechanism. Don't automatically log the user in, as this introduces additional complexity to the authentication and session handling code, and increases the likelihood of introducing vulnerabilities.
  - Ask the user if they want to invalidate all of their existing sessions, or invalidate the sessions automatically.

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
     `<uses-permission android:name="android.permission.INTERNET" />`
  7. `apktool b -o repackaged.apk out_dir` ( rebuild )
     - [locales_config.xml not found](https://github.com/iBotPeaches/Apktool/issues/2756#issuecomment-1059370741)
  8. Use apksigner to sign the app
     - [keystore](https://keystore-explorer.org/downloads.html)

## Header

- Strict-Transport-Security
- X-Frame-Options
- Content-Security-Policy
- https://cloud.google.com/cdn/docs/web-security-best-practices

## Language

#### Javascript

- JSON Hijacking
  - Allowing JSON to be returned as anything but an object would make it possible to return a JSON array that contained code that could be run on the client level. [ref](https://stackoverflow.com/questions/43717574/javascript-why-shouldnt-the-server-respond-with-a-json-array)

## Nmap

- Scanner

## OAuth 1.0a

1. The consumer obtains an unauthorized request token
2. The user authorizes the request token
3. The consumer exchanges the request token for an access token

- https://oauth.net/core/1.0a/
- Parameters are separated by comma
  - request token
    ```
    Authorization:
      OAuth oauth_callback="http%3A%2F%2Flocalhost%2Fsign-in-with-twitter%2F",
            oauth_consumer_key="cChZNFj6T5R0TigYB9yd1w",
            oauth_nonce="ea9ec8429b68d6b77cd5600adbbb0456",
            oauth_signature="F1Li3tvehgcraF8DMJ7OyxO4w9Y%3D",
            oauth_signature_method="HMAC-SHA1",
            oauth_timestamp="1318467427",
            oauth_version="1.0"
    ```
  - exchange access token / request protected resource
    ```
    Authorization:
      OAuth oauth_consumer_key="cChZNFj6T5R0TigYB9yd1w",
            oauth_nonce="a9900fe68e2573b27a37f10fbad6a755",
            oauth_signature="39cipBtIOHEEnybAR4sATQTpl2I%3D",
            oauth_signature_method="HMAC-SHA1",
            oauth_timestamp="1318467427",
            oauth_token="NPcudxy0yU5T3tBzho7iCotZ3cnetKwcTIRlX0iwRl0",
            oauth_version="1.0"
    ```
  - Entropy of Secret: use CSPRNG to generate long enough secrets
  - CSRF: use state (OAuth 2.0) / store token verifier in cookie
  - Clickjacking: disable frames e.g. X-Frame-Options

## OAuth 2.0

1. User authorizes the authorization request from client ( protected by TLS )
2. Client exchanges the authorization grant for access token ( protected by TLS )

- http://oauthbible.com/#oauth-2-two-legged
- https://habr.com/en/post/449182/
- http://andrisatteka.blogspot.com/2014/09/how-microsoft-is-giving-your-data-to.html
  - Open redirect by
    1. redirected to another authorization endpoint (should failed)
    1. rejected and redirected to attacker's website
  - How to prevent
    - exact match redirect uri
    - server authenticates client at token endpoint
- https://security.stackexchange.com/questions/140883/is-it-safe-to-store-the-state-parameter-value-in-cookie
- https://auth0.com/docs/secure/attack-protection/state-parameters#use-the-stored-url-to-redirect-users
- https://dhavalkapil.com/blogs/Attacking-the-OAuth-Protocol/
  - 1. Attacker tricks victim to log in attacker's account with given provider by CSRF.
    1. Attacker tricks victim to bind victim's account with given provider by CSRF.
    - use CSRF token to avoid auth request not originated from user
  - 1. Attacker initiates an auth request and obtains auth code.
    1. Attacker tricks victim to bind victim's account with given auth code by CSRF.
    - use the parameter, state, which is user session specific
  - 1. Attacker injects XSS within a web-page under client's domain.
    1. Attacker tricks victim to obtain auth code with redirect uri as injected web-page.
    - check redirect uri from authorization endpoint & access token endpoint
    - exact match redirect uri instead of partial match
  - 1. Attacker registers a client with a provider.
    1. Attacker tricks a victim to log in the client with given provider.
    1. Attacker obtains victim's access token of given provider.
    1. If some clients using implicit flow don't check which client the access token is bound with, attacker can log in as victim.
    - check which client the access token was issued to
    - not using implicit flow
  - 1. Provider validates parameters other than redirect uri first and redirect to given redirect uri when validation fails before validating redirect uri.
    1. Attacker craft a url with invalid arguments including redirect uri.
    1. Provider behaves as an open redirector when redirect uri and at least one more argument is invalid.
    - always validate redirect uri first
- https://sakurity.com/oauth
- https://portswigger.net/web-security/oauth
  - exploit discrepancies between the parsing of the URI
- https://www.oauth.com/oauth2-servers/authorization/the-authorization-response/
- https://tools.ietf.org/html/draft-ietf-oauth-security-topics-13
- Ensure to add the Referrer Policy tag with the noreferrer value in order to avoid referrer leakage.
- Do not pass authentication code / access token in url
  - No implicit grant type
- Mix up
  - One of the authorization server is operated by attacker
  - Client stores the authorization server chosen by user in session
  - Client uses the same redirection endpoint for all authorization servers
- Proof Key for Code Exchange
  - [When public clients (e.g., native and single-page applications) request Access Tokens, some additional security concerns are posed that are not mitigated by the Authorization Code Flow alone.](https://auth0.com/docs/get-started/authentication-and-authorization-flow/authorization-code-flow-with-proof-key-for-code-exchange-pkce)
    - Cannot securely store a Client Secret.
    - May make use of a custom URL scheme to capture redirects (e.g., MyApp://) potentially allowing malicious applications to receive an Authorization Code from your Authorization Server.

## One time password

- [生日攻擊](https://zh.wikipedia.org/wiki/%E7%94%9F%E6%97%A5%E6%94%BB%E5%87%BB)
  - 一個人的生日在某一天的機率是 1/365
  - 30 個人有一個人在某一天的機率是 1 - (364/365)\*\*30 = 0.079
  - 30 個人至少有兩人相同生日的機率 [1 - 365!/((365-30)! \* 365\*\*30)](https://zh.wikipedia.org/wiki/%E7%94%9F%E6%97%A5%E5%95%8F%E9%A1%8C) = 0.706
  - https://auth0.com/blog/birthday-attacks-collisions-and-password-strength/
- [Ensure that generated tokens or codes are:](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html#introduction)
  - Randomly generated using a cryptographically safe algorithm.
  - Sufficiently long to protect against brute-force attacks.
  - Stored securely.
  - Single use and expire after an appropriate period.
  - Linked to an individual user in the database.
  - URL tokens
    - Generate a token to the user and attach it in the URL query string.
    - Send this token to the user via email.
  - [Reset password](https://github.com/raymond-chia/Note/blob/main/Security.md#email-login)
- [time based one time password](https://datatracker.ietf.org/doc/html/rfc6238)

## Sniff

### Fiddler

- [當作 Proxy](https://docs.telerik.com/fiddler/configure-fiddler/tasks/usefiddlerasreverseproxy)
- [Capture Android](https://docs.telerik.com/fiddler/configure-fiddler/tasks/configureforandroid)
- 輸出憑證
  1. Tools/HTTPS 右上角有 Actions
  2. 選 export root certificate to desktop
  3. [憑證輸入 android](https://github.com/raymond-chia/Note/blob/main/Security.md#android)

### Mitmproxy

- sniff docker
  - https://dev.to/jandedobbeleer/intercept-http-traffic-exiting-a-docker-container-3g68

### Wireshark

- For every new TLS 1.3 session handshake, session keys will be created and stored in a local SSL key log file
  1. 指定 SSL key log file 儲存位置
  2. Wireshark `edit/preferences/Protocols/TLS/(Pre)-Master-Secret log filename` 設定 SSL key log file 位置
- https://www.youtube.com/watch?v=GMNOT1aZmD8
- https://www.comparitech.com/net-admin/decrypt-ssl-with-wireshark/

## 滲透測試工具

- Cobalt Strike

## Resources

- https://www.youtube.com/c/JohnHammond010/videos
- https://www.youtube.com/c/DavidBombal/videos
- https://www.hacksplaining.com/lessons
- https://cheatsheetseries.owasp.org/index.html
- https://github.com/cisagov/RedEye/
