# Note

- 有鑑於總是忘東忘西, 需要有個地方紀錄



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

