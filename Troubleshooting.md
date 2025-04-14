## 2FA

- gitlab + authy: 如果顯示 invalid pin code, 檢查 gitlab profile 的時區是否設定正確

## Aesthetic

- https://12factor.net/

### Model-Driven (Domain-Driven ??)

- https://www.youtube.com/watch?v=3aoLV5i1feo
  - 一個 model 列出所有 rules

### Comment

- represent the reason a piece of code exists

### Naming

- with: unit (sec, min)
- without: abbreviation, types, utils
- https://www.youtube.com/watch?v=-J3wNP6u5YU

## Algorithm

- Quad Tree
  - efficiently store data of points on a two-dimensional space
  - 優化碰撞檢測

## Animation

- https://www.youtube.com/watch?v=HsOKwUwL1bE&pp=ygUQYW5pbWF0aW9uIGRldmxvZw%3D%3D

## Apple

- 登入用的 key & 查詢收據用的 key 不同
  - 登入用的每個遊戲一把
  - 查詢收據用的全公司一把
- 測試帳號產生的金流不會顯示在 app store 後台

### Bug

- 收據可能缺乏購買的品項
  - https://developer.apple.com/forums/thread/85380

### Login

- oauth 要 email scope 需要參數 response_mode = form_post

### Purchase

- TestFlight 購買會是 sandbox
- 有區分 consumable / nonconsumable
- 收據 in_app 可能為空 (年久 bug)
  - https://developer.apple.com/forums/thread/85380

## AWS

### CLI

- https://docs.aws.amazon.com/cli/latest/reference/s3/

## Browser

- 高效儲存: https://www.notion.com/blog/how-we-sped-up-notion-in-the-browser-with-wasm-sqlite

### Android Webview

- `shouldOverrideUrlLoading` 當要去載入某個 url 資源時，可以用這判斷現在的流程
- `shouldInterceptRequest` 當 WebView 有一個 Request 要出去時，可以用來抓 AJAX 請求
  不過這個 function 裡拿到的物件只能拿到 Request URL, Method, Header，拿不到 POST Request 的 payloads
  [Request 物件能給的東西](https://developer.android.com/reference/android/webkit/WebResourceRequest)
- `onPageFinished` 當頁面載入完成時，可以做些額外的事情。以現在而言，載入頁面完成後會重新調整 WebView window 的大小

## Captcha like

- Cloudflare Turnstile
  - [避免讓使用者輸入驗證碼](https://blog.cloudflare.com/turnstile-private-captcha-alternative/#we-are-opening-our-captcha-replacement-to-everyone)

## Certificate

- 申請
  - cloudflare
  - godaddy
  - letsencrypt
- https on localhost https://github.com/FiloSottile/mkcert#mkcert

## Checksum

- https://stackoverflow.com/questions/16122067/md5-vs-crc32-which-ones-better-for-common-use
  - security over speed: ~~md5~~, shaXXX
  - speed over security: CRC32

## Coordinate system

- [hex](https://www.redblobgames.com/grids/hexagons)
- [raycasting](https://antongerdelan.net/opengl/raycasting.html)

## Cryptography

### AES

- GCM
- https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Common_modes

## Data

- cache related introduction: https://github.com/SanderMertens/ecs-faq#data-oriented-design

## Database

- memory: Dragonfly, Redis, ZooKeeper
- disk: etcd, MongoDB
- vector 存法是將句子向量化 (embedding), 再儲存向量化後的結果

### Dragonfly

- in memory

### etcd

- in disk
- for Kubernetes

### MongoDB

- in disk
- operations
  - get current operations
    - https://www.mongodb.com/docs/manual/reference/method/db.currentOp/
    - for example `db.currentOp( {"waitingForLock": true} )`
  - some operations with retryWrites=true might cause oplog flooding
    - https://www.mongodb.com/docs/manual/core/retryable-writes/#retryable-write-operations
- change stream 可以監聽資料變化
  - https://www.mongodb.com/docs/manual/changeStreams/
- GridFS: 存放大型資料

#### Schema

- https://www.mongodb.com/blog/post/6-rules-of-thumb-for-mongodb-schema-design
  1. What is the cardinality of the relationship? Is it "one-to-few," "one-to-many," or "one-to-squillions"?
  2. Do you need to access the object on the "N" side separately, or only in the context of the parent object?
  3. What is the ratio of updates-to-reads for a particular field?
  - For `one-to-few`, you can use `an array of embedded documents`
    - no need to access the embedded object outside the context of the parent object
    - 不容易找特定 `子資料`
  - For `one-to-many`, or on occasions when the "N" side must stand alone, you should use `an array of references`
    - 1 連到 N
    - You can also use a `parent-reference` on the "N" side if it optimizes your data access pattern
      - `bi-directional referencing`
      - `no atomic updates`
  - For "one-to-squillions," you should use a `parent-reference` in the document storing the "N" side
    - N 連到 1
    - 避免 16 MB 限制
    - `no atomic updates`
  - If you are referencing, you can `denormalize data` either from the "one" side into the "N" side,  
    or from the "N" side into the "one" side
    - 要 read >> update 才有利
    - `no atomic updates`
    - host 除了有 `子資料` 的 id, 還要常常讀取的資訊
      - 更新時要更新 `子資料` & host 存的部份
    - 或反過來, 子資料要常常讀取的 host 資訊
  1. If you frequently run $lookup operations, consider restructuring your schema through denormalization  
     such that the your application can query a single collection to obtain all of the information it needs
  2. 通常 denormalization 比較好
     1. 除非無法忍受重複的資料 & 增加的讀取效能不重要
     2. 除非 many to many
     3. 除非太大
  - rules of thumb
    - https://www.mongodb.com/blog/post/6-rules-of-thumb-for-mongodb-schema-design
    - https://www.mongodb.com/developer/products/mongodb/mongodb-schema-design-best-practices
    1. Favor embedding unless there is a compelling reason not to
    2. Needing to access an object on its own is a compelling reason not to embed it
    3. Arrays should not grow without bound.
       1. If there are more than a couple of hundred documents on the "many" side, don't embed them
       2. if there are more than a few thousand documents on the "many" side, don't use an array of ObjectID references
       3. High-cardinality arrays are a compelling reason not to embed.
    4. Don't be afraid of application-level joins:
       1. If you index correctly and use the projection specifier, then application-level joins are barely more expensive than server-side joins in a relational database
    5. Consider the read-to-write ratio with denormalization.
       1. A field that will mostly be read and only seldom updated is a good candidate for denormalization.
       2. If you denormalize a field that is updated frequently  
          then the extra work of finding and updating all the instances of redundant data  
          is likely to overwhelm the savings that you get from denormalization
    6. As always with MongoDB, how you model your data depends entirely on your particular application's data access patterns.
       1. You want to structure your data to match the ways that your application queries and updates it
    7. Avoid joins/lookups if possible, but don't be afraid if they can provide a better schema design

#### replica set

- 在 local
  - To avoid automatic server discovery and getting stuck on connecting while using MongoDB connection string, specify a direct connect should be made. This can be done by providing `directConnection=true` or `connect=direct` option in the connection string.
    - `mongodb://{username}:{password}@{host}:{port}/{db name}?authSource={admin db name}&connect=direct`
    - https://pkg.go.dev/go.mongodb.org/mongo-driver/mongo/options#ClientOptions.SetDirect
  - 用一個 node 建立 replica set
    - https://www.mongodb.com/docs/manual/tutorial/convert-standalone-to-replica-set/
- slow operation 可能會紀錄在 secondary member of replica set 的 oplog entries
  - https://www.mongodb.com/docs/manual/replication/#slow-operations
- 同步的資料太多
  - 可能限制 primary 寫入的速度
  - 讓 secondary 追上 ??
  - https://www.mongodb.com/docs/manual/replication/#replication-lag-and-flow-control
  - 需要 read majority

#### index

- [drop index will block all operations on the collection](https://www.mongodb.com/docs/manual/reference/method/db.collection.dropIndex/#resource-locking)
- [對 array 設定 unique index, 無法阻止 array 內有重複的值](https://www.mongodb.com/docs/manual/core/index-multikey/?_ga=2.110814017.570310677.1681713217-959579056.1642987351#unique-multikey-index)

#### Others

- 整合測試: https://github.com/mongodb/mongo/wiki/The-%22failCommand%22-fail-point

### Redis

- in memory
- [redis docker image (with some modules)](https://hub.docker.com/r/redislabs/redismod)
- [It's important to note that even when a command fails, all the other commands in the queue are processed – Redis will not stop the processing of commands.](https://redis.io/docs/interact/transactions/#errors-inside-a-transaction)
- `scan {cursor number} match {regex} count {number}`

### ZooKeeper

- in memory
- jvm 設定似乎很麻煩, 例如 garbage collection (跟使用的資料有關)

### SQL

#### MySQL

- `docker run -itd --name=sql-mysql -e=MYSQL_ROOT_PASSWORD={root 的密碼} -e=MYSQL_DATABASE={預設的資料庫名稱} mysql:8.0.33-debian --default-authentication-plugin=mysql_native_password`
  - `--default-authentication-plugin=mysql_native_password`: mysql 8 uses `caching_sha2_password` as the default authentication plugin instead of `mysql_native_password`  
    有些 client 不支援 caching_sha2_password, 用上述指令使用舊版的 mysql_native_password
- `mysql -h {host} -u {user} -p{password}`
- `use {database};` `show databases;`, `show tables;`

#### PostgreSQL

- 要`避開`的項目: https://philbooth.me/blog/nine-ways-to-shoot-yourself-in-the-foot-with-postgresql
- 查詢誰有指定資料庫權限 `SELECT datacl FROM pg_database WHERE datname = '資料庫名稱';`
- 查詢權限繼承 `\du`
- 切換 `\c 資料庫名稱 使用者名稱`

#### SQLite

- CRUD 指令結尾要 `;`

## Data-oriented Design

- vs `object oriented design`
  - end up with giant object
    - 污染 cache (只要一小塊)
  - hide state
- 分離 data & logic
  - 減少 if
  - 減少 interface ... 偏向 functional ??
- https://www.youtube.com/watch?v=yy8jQgmhbAU&t=1440s

## Docker

### Install docker on mac

- https://dhwaneetbhatt.com/blog/run-docker-without-docker-desktop-on-macos/

```bash
# Install hyperkit and minikube
brew install hyperkit
brew install minikube

# Install Docker CLI
brew install docker
brew install docker-compose

# Start minikube
minikube start

# Tell Docker CLI to talk to minikube's VM
eval $(minikube docker-env)

# Save IP to a hostname
echo "`minikube ip` docker.local" | sudo tee -a /etc/hosts > /dev/null

# Test
docker run hello-world

# mount 需要另外處理
# https://minikube.sigs.k8s.io/docs/handbook/mount/
minikube mount {source directory}:{target directory}
```

- `Error saving credentials: error storing credentials - err: exec: "docker-credential-desktop": executable file not found in $PATH`
  - https://stackoverflow.com/questions/65896681/exec-docker-credential-desktop-exe-executable-file-not-found-in-path
- Start minikube when turning on macos: https://stackoverflow.com/questions/6442364/running-script-upon-login-in-mac-os-x
  - ```bash
    export PATH=PATH:/usr/local/bin
    minikube start
    ```

### Command (Frequently used)

- `docker run -itd --add-host=mongo:{192.168.64.2 或其他 docker 所在 ip} -p=27017:27017 --name={container name} {image}`
- `docker exec -it {container name} bash`
- run with privilege
  - `docker run --privileged {registry:version}`
  - https://docs.docker.com/engine/reference/commandline/run/#full-container-capabilities---privileged
- docker run 可以有很多個 -v
  - 後面的會覆蓋前面的
  - 如果最後掛的 volume 為空, 就會使用 image 本身的
- exec docker container root
  - `-u root`
- 清理 disk 用量 `docker system prune --volumes`
  - To see all volumes: `docker volume ls`
  - To show docker disk usage: `docker system df`
  - 例如用於: `You don't have enough free space in /var/cache/apt/archives`
  - 分開清除: `docker container prune`, `docker image prune`, `docker volume prune`
- `docker network inspect bridge` 查看 container 的 ip. bridge 是預設的 docker network
- mac 不能用 `localhost`, 要用 `host.docker.internal`

### Dockerfile

- `docker build -f=path/to/dockerfile path/to/build/context`
- Instead of specifying a context, you can pass a single Dockerfile in the URL or pipe the file in via STDIN. To pipe a Dockerfile from STDIN
  `docker build - < Dockerfile`
  https://docs.docker.com/engine/reference/commandline/build/
- --mount
  - `RUN --mount=type=cache,target=/app` 臨時掛載 cache
  - `RUN --mount=type=secret,id=DOTENV_LOCAL,dst=.env` 臨時掛載 secret, DOTENV_LOCAL 是標示符

### Docker in Docker

- https://hub.docker.com/_/docker
  - https://jpetazzo.github.io/2015/09/03/do-not-use-docker-in-docker-for-ci
    - https://github.com/nestybox/sysbox: 在 container 開 child container
    - `docker run -v /var/run/docker.sock:/var/run/docker.sock ...` 在 container 開 sibling

### Debug

- 協助縮減大小: https://github.com/wagoodman/dive
- image tag 不能有 `+` 可以有 `-`
  - https://github.com/opencontainers/distribution-spec/issues/154
- 一直 crash, 來不及連進 container

```shell
docker run -it $image_tag bash
strace $command_to_run_program # 執行目標程式, 查看錯誤
```

- docker 導向 proxy
  - 方便 man in the middle
    - https://dev.to/jandedobbeleer/intercept-http-traffic-exiting-a-docker-container-3g68
    - ```sh
      docker run -it --env HTTP_PROXY="mitmproxy:8080" --env HTTPS_PROXY="mitmproxy:8080" --add-host="mitmproxy:$local_ip" $image
      mkdir -p /usr/local/share/ca-certificates/extra # in docker
      openssl x509 -in ~/.mitmproxy/mitmproxy-ca-cert.pem -out crt.crt # new terminal
      docker cp crt.crt $docker_container_ip:/usr/local/share/ca-certificates/extra/crt.crt
      update-ca-certificates # in docker
      ```
  - 設定 docker proxy: https://docs.docker.com/network/proxy/#set-proxy-using-the-cli
  - 取得 mitm cert: https://docs.mitmproxy.org/stable/concepts-certificates/#the-mitmproxy-certificate-authority
  - 設定 crt: https://askubuntu.com/questions/73287/how-do-i-install-a-root-certificate/377570

### Mirror

- 減少 dockerhub 抓取頻率
- gitlab: https://about.gitlab.com/blog/2020/10/30/mitigating-the-impact-of-docker-hub-pull-requests-limits/

## DNS

- Ubuntu 18 修改
  - sudo vim /etc/resolv.conf
  - 由上而下填寫 DNS server ip
    - 如果只有 domain name, 可以用 dig 拿 ip
- `nslookup` vs `dig`
  - 用不同的 resolver

## Format

### Yaml

- anchor
  - https://stackoverflow.com/questions/48940619/yaml-how-to-reuse-single-string-content
  - https://stackoverflow.com/questions/14184971/more-complex-inheritance-in-yaml

```yaml
a: &a "ABC"
b: *a
```

## Formatter

- Clang-format can format proto3
  - 如果在 vscode extensions 下載之後仍然無法使用, 需要另外下載 clang-format
    - mac: brew install clang-format
    - linux: sudo apt install clang-format
      - ref: https://stackoverflow.com/questions/42756602/executable-not-found-please-configure-clang-executable
  - vscode settings.json 範例
    ```json
    {
      "[proto3]": {
        "editor.defaultFormatter": "xaver.clang-format"
      },
      "clang-format.executable": "path to clang-format"
    }
    ```

## Game Engine

### Unity

- particle
  - cpu
  - 可以回播
- compute shader
  - gpu
  - 不能回播
  - spawn, init, update, output
    1. spawn
       - rate
    2. initialize
       - capacity: 最多幾顆. 可以小於 rate. 產生不平均的 particles
       - velocity
       - lifetime
       - position mesh 可以決定從哪裡產生. 某個點, 某個物件表面 ?? skinned mesh ?? 目標 mesh 要啟用 readwrite ??
       - localspace, worldspace
    3. update
       - turbulence 旋轉
       - flipbook player (搭配 output flipbook). 要加上 vfx time
       - collision shape
       - trigger event 搭配 collision shape 可以在碰撞後觸發 gpu event 產生新的 particle
    4. output
       - 可以調整後續變化: over life
       - 可以指定序列圖: flipbook
       - orient face camera
    - 例如只有身體, 腳依靠 vfx 自動連到附近的 collider

## Git

- autocomplete
  - mac: https://gist.github.com/romansavrulin/41e55fba693b4025ed693559083bc3a0
- git 技巧
  - https://www.youtube.com/watch?v=aolI_Rz0ZqY&t=385s
    - 某個資料夾下都用某種 git config (user + email 之類的)
    - `git diff --word-diff`
    - `git reflog`: 查看 git 操作記錄. 搭配 git reset 可以拯救錯誤 git 操作
    - `git config --global rerere.enabled true`: merge conflict 手動修一次. 之後自動修
    - `git maintenance start`: [repository data](https://git-scm.com/docs/git-maintenance)
    - 處理大型 repo 的手段
    - ...
- https://andrewlock.net/working-with-stacked-branches-in-git-is-easier-with-update-refs/#enabling-update-refs-by-default
  - 一次更新所有相關的 branches
  - add the following to your .gitconfig file:
    ```
    [rebase]
      updateRefs = true
    ```
- 不要 diff 某些檔案
  - .gitattributes 加上 `regex.extension binary`
    - 例如 `mock_*_test.go binary`
    - https://git-scm.com/docs/gitattributes#_using_macro_attributes
- stacked PR https://ppwwyyxx.com/blog/2023/Stacked-Diffs-Pull-Requests/
- mirror gitlab, github
  1. https://stackoverflow.com/questions/32762024/how-to-sync-gitlab-with-github
  2. 1. git remote add {name} {git@...}
     1. git push {name} {branch}

#### lfs

- 遇到 `Object does not exist on the server or you don't have permissions to access it`
  - 執行 `git-lfs fetch --all upstream` 然後重試

### Github

- 下載某一個資料夾
  - 在 github repo 按下 `.` 進入 IDE
  - 對要下載的資料夾按下右鍵, 並下載
- Pushing to Github results in 403
  - Github seems only supports ssh way to read&write the repo
  - 1. Edit `.git/config` file under your repo directory.
    1. Find `url=` entry under section `[remote "origin"]`.
    1. Change it from: `url=https://MichaelDrogalis@github.com/derekerdmann/lunch_call.git`
       to: `url=ssh://git@github.com/derekerdmann/lunch_call.git`
       That is, change all the texts before `@` symbol to `ssh://git`
  - https://stackoverflow.com/questions/7438313/pushing-to-git-returning-error-code-403-fatal-http-request-failed
- Add ssh key to github
  - github: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account
  - gitlab: https://docs.gitlab.com/ee/user/ssh.html
  - 不要設定 passphrase
- [設定 ssh key 之後要推 code 到 github](https://stackoverflow.com/questions/29297154/github-invalid-username-or-password)
  - git remote set-url origin git@github.com:raymond-chia/Note.git

### Gitlab

- table of contents: https://docs.gitlab.com/ee/user/markdown.html#table-of-contents
- Add ssh key to gitlab 可以參考 github
- 自動管理 issue: https://gitlab.com/gitlab-org/ruby/gems/gitlab-triage
- CI_REGISTRY_IMAGE 是空值
  - 開啟 container registry: https://stackoverflow.com/questions/73899771/gitlab-predefined-ci-cd-variable-ci-registry-image-empty
- Combine protected branches with `Code Owners` to require experts to approve merge requests before they merge into a protected branch
- 在 ci yaml 依照排列組合執行: https://docs.gitlab.com/ee/ci/yaml/#parallelmatrix
  - 後續步驟用 `needs` 指定是處理哪個 matrix 項目: https://docs.gitlab.com/ee/ci/yaml/#needsparallelmatrix
- Job token permissions 設定跨專案權限

## Google

- 服務狀態: https://status.cloud.google.com

### Bigquery

- [data streamed to an ingestion time partitioned table might be delayed](https://cloud.google.com/bigquery/docs/streaming-data-into-bigquery#dataavailability)
  - up to 90 mins

### Cloud Platform

- `X-Cloud-Trace-Context` 可以協助追蹤 log. https://stackoverflow.com/questions/54313017/what-is-the-purpose-of-x-cloud-trace-context

### Cloud Storage

- [Bucket name 如果含有 `.` 會被當作 DNS, 需要特別設定](https://cloud.google.com/storage/docs/buckets#naming)
- 所有用戶共用 namespace: [Bucket names reside in a single namespace that is shared by all Cloud Storage users](https://cloud.google.com/storage/docs/buckets#considerations)
  - Bucket names are publicly visible  
    Don't use user IDs, email addresses, project names, project numbers, or any personally identifiable information (PII) in bucket names because anyone can probe for the existence of a bucket
- [檔名結尾 `#0` 代表最近的版本](https://cloud.google.com/storage/docs/introduction#resource-name)
  - 如果檔案名稱可能混淆, 需要特別標明

### Firebase

#### FCM

- 權限: Firebase Grow Admin
- 要有 owner 先建立 messaging 草稿, 其他人才能使用

### Geo IP

- GFEs & Cloud Armor use different IPGeo databases (至少到 2023)
- update once per week

### Log

- 用 Google Workloads 可以自動加上 filter

### Purchase

- 指定帳號會是 sandbox ??
- Android 後台沒有 consumable / nonconsumable 的區分. 要自行 consume
- 沒有 acknowledge 會自動退費
- https://developer.android.com/google/play/billing/security
  - https://developers.google.com/android-publisher/api-ref/rest/v3/purchases.products/get 需要權限 `financial report`
- 請先設定權限, 再建立 product https://stackoverflow.com/a/60691844

### 畫架構

- https://googlecloudcheatsheet.withgoogle.com/architecture

## GRPC

- https://developers.google.com/protocol-buffers/docs/tutorials
- https://grpc.io/docs/languages/go/quickstart/
- https://grpc.io/docs/languages/go/generated-code/
- `protoc`
- `protoc-gen-go`: a `protoc` plugin to generate a Go protocol buffer package
- `protoc-gen-doc`: a `protoc` plugin to generate documentation
- [`protoc-go-inject-tag`](https://github.com/favadi/protoc-go-inject-tag)

## HTTP

- [Connection 相關的 header 如 Connection 和 Keep-Alive 在 HTTP/2 中被禁用](https://developer.mozilla.org/zh-TW/docs/Web/HTTP/Headers/Connection)
  - 可能導致無法送請求
- 測試: https://github.com/Orange-OpenSource/hurl
  - runs HTTP requests defined in a simple plain text format

## Input

### Keyboard event

- code = [Physical keys](https://api.flutter.dev/flutter/services/PhysicalKeyboardKey-class.html). Keys which represent a `particular key location` on a QWERTY keyboard. It ignores any modifiers, modes, or keyboard layouts which may be in effect.
- key = Logical keys. Keys which are interpreted in the `context` of any modifiers, modes, or keyboard layouts which may be in effect.
- https://youtu.be/jLqTXkFtEH0?t=360

## Language

- test
  - https://www.youtube.com/watch?v=X4rxi9jStLo
  - 容易新增. 例如 table driven test
  - test coverage
  - edge case
  - exhaustive test
  - 在測試寫另外一種演算法. 效能可以差. reference implementation
  - test data 放在其他檔案. 方便跨語言重用
  - 優化測試的錯誤訊息
  - txtar ??

### Bash

- 驗證: https://www.shellcheck.net/
- 寫法: https://google.github.io/styleguide/shellguide.html
- 指令: https://tldp.org/LDP/Bash-Beginners-Guide/html/
- 測試可以用 shunit2 ??
- set -euxo pipefail
  - give verbose output and also will abort your script immediately if part of the script fails.
  - https://stackoverflow.com/questions/38342992/what-does-ex-option-used-in-bash-bin-bash-ex-mean
  - https://gist.github.com/mohanpedala/1e2ff5661761d3abd0385e8223e16425
- [bash script 預設不支援 alias, 需要另外處理](https://unix.stackexchange.com/questions/1496/why-doesnt-my-bash-script-recognize-aliases)
- `"${3:-default}"` [用第三個參數, 如果不存在就用 `default`](https://stackoverflow.com/questions/1163145/what-does-2-1-mean-in-bash)
- `=~` 代表右邊會是 regex
- grep -a -C6 {regex}: {filename} | less  
  -a 是叫 grep 把 binary file 當作 text file process  
  -C 是顯示 match 到的那行的前後幾行, 後面的數字是要顯示幾行. 他的朋友還有 -A (after) 跟 -B (before)
- curl -D-
  - -D: dump header
  - -: alias to /dev/stdout

#### 問題

- 錯誤訊息: `")syntax error: invalid arithmetic operator (error token is "`
  - https://unix.stackexchange.com/questions/297330/syntax-error-invalid-arithmetic-operator-error-token-is
  - 清掉特殊符號: `${VAR//[ $'\001'-$'\037']}`
- 在 bash 中使用管道 (pipe) 時，每個部分都是在子 shell 中執行的。所以在 while 迴圈中增加的 total 和 distribution 變數只存在於子 shell 中，無法傳回主 shell。
  - 使用 process substitution `< <(command)` 取代管道 `|`

### C#

- NuGet maintains a reference list of packages used in a project and the ability to restore and update those packages from that list
- ProtectedMemory 對記憶體加密

### Golang

#### Build

- linux amd 64-bit: `GOOS=linux GOARCH=amd64 go build`
  - https://freshman.tech/snippets/go/cross-compile-go-programs/
- build binary with environment variable: `ldflags`
  - 例如: `go build -ldflags "-X main.gitHash=$(git rev-parse HEAD)"`

#### Linter

- linter 推薦: https://github.com/uber-go/guide/blob/master/style.md#linting
- golangci-lint + VSCode: https://golangci-lint.run/usage/integrations
  - 可以啟用的 linters: https://golangci-lint.run/usage/linters/

#### Environment Variable

- `go env` can get GOPATH, GOROOT 等等

#### Dependency

- 如果 Editor linter 無法正確讀取 dependency
  - go1.18 可以用 workspace 處理
    - go work
    - https://stackoverflow.com/questions/58518588/vscode-could-not-import-golang-package
- `go clean -modcache`
- 遇到 `ambiguous import`
  - https://stackoverflow.com/questions/57952397/how-to-resolve-conflicting-go-module-dependencies-when-a-top-level-module-and-on
- 指向 local dependency https://go.dev/ref/mod#go-mod-file-replace
- 檢查 dependency vulnerability: https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck

#### Generics

```go
func F[T any, TPointer interface{
  proto.Message
  *T
}]()
```

- 可以確保 new(T) 滿足 proto.Message

#### Golang manage multiple version

- https://go.dev/doc/manage-install#installing-multiple
- Use vscode

#### Private Repository, `Gone 410`

- GOPRIVATE={repository host}
  - https://stackoverflow.com/questions/27500861/whats-the-proper-way-to-go-get-a-private-repository
  - 可能不會讀環境變數 ?? 需要 `GOPRIVATE=gitlab.private.com go mod tidy`
- `git config --global url."git@gitlab.private.com:".insteadOf "https://gitlab.private.com"`
- `git config --global url."https://gitlab.private.com".insteadOf "https://gitlab.com"`
  - ~/.gitconfig 裡面應該要有
    ```
    [url "git@gitlab.private.com:"]
      insteadOf = https://gitlab.private.com
    ```

#### Side effect

- 如果對還有剩餘空間的 slice (cap > len) 做 append, 修改會是 in place
  - https://stackoverflow.com/questions/53572736/append-to-a-new-slice-affect-original-slice
- for 裡面的 closure 可能 cache 最後的變數

#### Misc

- 架構 https://www.gobeyond.dev/standard-package-layout
- 檢查效能 & bug: `staticcheck`, `delve`
- Game server template: https://heroiclabs.com/
- github.com/redis/go-redis 有未知的寫壞原因 ??

### Javascript

- MemLab can find memory leaks
- Jest 用來測試
- bootstrap

#### Redux

- <img src="https://redux.js.org/assets/images/ReduxDataFlowDiagram-49fa8c3968371d9ef6f2a1486bd40a26.gif" width="480" height="360" />
- [reducer](https://redux.js.org/tutorials/fundamentals/part-3-state-actions-reducers#writing-reducers)

#### Reactjs

- useEffect
  - 搭配 fetch: render 時送請求
  - 第二個參數用來檢查要不要觸發
    - 不帶代表每次都跑
    - [] 代表只跑一次
    - https://stackoverflow.com/questions/57760842/why-would-we-use-useeffect-without-a-dependency-array
- [useSelector](https://react-redux.js.org/api/hooks#useselector)
  - Allows you to extract data from the Redux store state
- react datasheet grid

### Mojo

- https://en.wikipedia.org/wiki/Mojo_(programming_language)
- 可以整合 python
- 專門研發 ai
- 速度快

### Python

- 安裝 binary
  - 1. pip3 show --files {app 名稱}
    1. 組合 Location & Files  
       https://stackoverflow.com/questions/74597855/where-does-pip3-install-package-binaries
- pip list
- requests 不能 async 發送請求
  - httpx 可以 async 發送請求
    - https://www.python-httpx.org/async
- 轉換時間 (字串 -> timestamp)
  - `datetime.datetime.strptime("2024-06-25T08-57-17", "%Y-%m-%dT%H-%M-%S").timestamp()`
- in memory cache: https://stackoverflow.com/questions/31771286/python-in-memory-cache-with-time-to-live

#### Dependency

- import package 時要從執行位置開始算

```
- app1
  - __init__.py
  - main.py
  - package
    - __init__.py
    - tool.py
```

若在 app1 的 parent directory 執行  
則 main.py 寫法為

```python
import app1.package.tool
```

##### venv

- https://www.infoworld.com/article/3239675/virtualenv-and-venv-python-virtual-environments-explained.html
- python -m venv .
- ./venv/bin/python -m pip install
- source bin/activate

##### Poetry

- commit lock
  - https://python-poetry.org/docs/basic-usage/#committing-your-poetrylock-file-to-version-control
  - 有些小版號也是 breaking change ... chromadb@0.5.3 -> chromadb@0.5.4
- 指定版本: poetry add chromadb@0.5.3

#### FastAPI

- 自動產生 OpenAPI
  - 不能 pydantic v2 https://github.com/fastapi/fastapi/issues/10360
- 監聽事件: https://fastapi.tiangolo.com/advanced/events/

### Rust

- 指南
  - https://rust-unofficial.github.io/patterns/intro.html
  - memory container: https://github.com/usagi/rust-memory-container-cs/blob/master/3840x2160/rust-memory-container-cs-3840x2160-dark-back.png
  - crate vs module: https://mmapped.blog/posts/03-rust-packages-crates-modules
    - crate 是最小的 compile unit, 可以平行 compile
    - module 可以 dependency cycle

## Make

- MakeFile: a text file that contains the recipe for building your program

## Meta (Facebook)

- 廣告: https://www.facebook.com/ads/library/?active_status=all&ad_type=political_and_issue_ads&country=TW&media_type=all
- 用 business token 來拿 unique id across apps
  - 如果遇到 limited login
    1. 產生 app access token: https://developers.facebook.com/docs/facebook-login/guides/access-tokens/#apptokens
    2. 拿玩家的 unique id across apps: https://developers.facebook.com/docs/facebook-login/limited-login/faq/#faq_2886507154928804

## Network

### Connection reset by peer

- server close session & client send request
- [CDN & Load Balancer timeout](https://medium.com/starbugs/%E8%AC%8E%E4%B9%8B%E8%81%B2%E5%B0%8D-connection-%E8%AA%AA%E9%81%93-%E4%BD%A0%E5%B7%B2%E7%B6%93%E6%AD%BB%E4%BA%86-b53d27c7ecb7#77a6)
- [Google load balancer restarts periodically](https://cloud.google.com/load-balancing/docs/https#timeouts_and_retries)
- https://blog.percy.io/tuning-nginx-behind-google-cloud-platform-http-s-load-balancer-305982ddb340#3b71

### Server 處理 Request

- hmac: 避免偽造
- nonce: 避免 replay attack ??
- request id: 處理重送
  - 用來鎖
  - 用來 cache response
- 定期寫入 DB 比較容易應付大流量
  - 每次 request 寫入 DB, DB 不易撐住
  - 每次 request 先寫入 Redis, 再寫入 DB ??

### Server 處理更新

- 魔獸世界似乎是
  - 早早釋出新版本. 但是有加密
  - 到 patch day 才釋出 decryption key

### Misc

- 清除 ip 舊的 key: `ssh-keygen -R {ip}`
  - 症狀: `REMOTE HOST IDENTIFICATION HAS CHANGED!`
- whois
  - 查詢 domain name 註冊資訊
- 某些 router 會擋住大的 port
- 特殊 ip
  - 0.0.0.0: matches all addresses in the IPv4 address space and is present on most hosts, directed towards a local router
  - 127.0.0.1: 本機

## OAuth

- using popup
  - 避免跳轉使用者正在操作的頁面
  - https://dev.to/didof/oauth-popup-practical-guide-57l9

### 1.0a

- Make sure consumer key & access token secret are escaped
  - github.com/gomodule/oauth1 v0.2.0 escapes consumer key & access token secret automatically
  - github.com/dghubble/oauth1 v0.7.1 does NOT escape consumer key & access token secret automatically

### 2.0

- https://cloud.google.com/identity-platform/docs/android/apple
- Apple 可以在 authorize 回來後就拿到 id token
  - `response_type=code id_token`
  - https://developer.apple.com/documentation/sign_in_with_apple/sign_in_with_apple_js/incorporating_sign_in_with_apple_into_other_platforms#3332113
  - https://stackoverflow.com/questions/59943139/sign-in-with-apple-id-says-invalid-responsetype

#### Google

- popup login 可以斷在拿到 auth code ??
  - 或跑完拿到 access token
- brew install oauth2l

## OpenSocial

- make request
  - https://developers.google.com/gadgets/docs/reference#makerequest
  - https://opensocial.github.io/spec/2.5.1/Core-Gadget.xml#gadgets.io.makeRequest

## OpenToonz

- Open the OpenToonz Stuff folder. Open the Profiles folder, and open the ENV folder.
- Use a text editor such as NotePad++ to open YOURNAME.env file, and look for the key "SoftwareCurrentFont" and SoftwareCurrentFontSize

## Operating System

### Android

- Mac 傳輸檔案到 Android: https://www.android.com/filetransfer/
  - 遇到問題可以試試拔線重插

#### Samsung

- 輔助快選: 前往「設定」→「協助工具」→「互動與敏銳度」→ 開啟「輔助快選」功能

#### 鴻蒙

- 不支援 firebase, google play 2024/07

### Unix

#### 設定

- Setting net.core.somaxconn to higher values is only needed on highloaded servers where new connection rate is so high/bursty that having 128 (50% more in BSD's: 128 backlog + 64 half-open) not-yet-accepted connections is considered normal

#### Mac

- brew
  - switch version
    - for example
      - brew unlink node
      - brew link node@14
- [切換語言: ctrl + space](https://support.apple.com/en-sg/guide/mac-help/mchlp1406/mac)
- 開機的時候做事
  1. 打開 Automator
  2. 選擇應用程式 ??
  3. 執行 shell 工序指令
  4. 寫 bash
  5. 儲存
  - https://support.apple.com/zh-tw/guide/automator/autbbd4cc11c/mac

##### 如果密碼打錯被鎖

- mini
  - 重開機 & 一直壓 command + R
  - 開啟 terminal
  - 輸入 resetpassword
  - 無論是否成功重設, 只要這邊成功登入就可以回開機畫面再登入一次

##### VSCode

- 無法打開應用程式 -47
  - https://stackoverflow.com/questions/78713786/vs-code-is-not-opening-up-in-mac
  - application > right click and Show package contents > navigate to Contents/MacOS > open Electron
  - 可能只需要從 `下載項目` 挪到其他位置就好
- spam cursor over lines: command + alt + arrow
- back: ctrl + -

#### Debian

- procps 內含 `top` 等 command line 指令
- chronyd 管理時間系統

#### Ubuntu

- `/var/run/docker.sock` permission
  - `sudo usermod -aG docker {USER}`
  - `sudo chmod +rw-x /var/run/docker.sock` ??
- `/etc/profile` 設定所有使用者環境 ??
- 時間:
  ```shell
  sudo service chrony stop # 停止調整時間
  sudo date -s "2001-2-3 4:0:0"
  ```
- `systemctl status {SERVICE} --wait` 會等 service 狀態變化完畢
- 找對應字串. 加上 -i 變成替換
  - `sed 's/{尋找的目標. 接受 regex}/{替換的目標}/' {檔案名稱}`
- `sync`: 強迫寫入 disk
  - 不然可能還在 cache. snapshot 的時候會有問題.

##### 安裝, 升級

- 使用 snap 時, 如果 home 不在 /home 下面: https://snapcraft.io/docs/home-outside-home
- 升級過期的作業系統: https://askubuntu.com/questions/91815/how-to-install-software-or-upgrade-from-an-old-unsupported-release
- 安裝 nvidia cuda: 用 `Software & Updates` 的 `Additional Drivers`

##### Cron

- 列出 cron jobs
  - 檢查 `crontab -l`
  - 檢查 `/etc/cron.d` 或其他 /etc/cron.`XXX`
    - https://gist.github.com/snail007/cec5d24f0f4ef0f850fa0b6120bed1cb
- 設定觸發時間 https://stackoverflow.com/questions/584770/how-would-i-get-a-cron-job-to-run-every-30-minutes

##### Debug

- Left Shift, F12 可以進入特殊模式 (可能要長按或連按)
  - https://askubuntu.com/questions/24006/how-do-i-reset-a-lost-administrative-password
- crash: `sudo journalctl --since="-5 minutes"` 檢查原因
  - ref https://askubuntu.com/questions/1414900/automatic-logout-using-ubuntu-22-04-lts
  - `journalctl -u {service-name}` 可以看特定 service 的 log
    - `systemctl status {service-name}` 只能看到部份 log
    - https://unix.stackexchange.com/questions/225401/how-to-see-full-log-from-systemctl-status-service

## Probabilistic data structure

### 是否存在

- Bloom
  - 適合分散式系統
  - 比較成熟
- Cuckoo
  - 效率好
  - 空間利用率好
  - 可以刪除
  - 限制數量 (避免 100% false positive)
  - https://stackoverflow.com/questions/867099/bloom-filter-or-cuckoo-hashing

### 次數

- count-min sketch
  - 用多個 hash table 紀錄次數
  - 每個 hash table 的 hash function 不能一樣
    - 要打散在每個表的位置
  - 所有表的值中, 取`最低`
    - 每次 collision 增加值
- count sketch
  - 用多個 hash table 紀錄次數
  - 每個 hash table 的 hash function 不能一樣
    - 要打散在每個表的位置
    - 還要決定是正數還是負數
  - 所有表的值中, 取`中位數`
    - 每次 collision , 絕對值可能接近 / 遠離 0
- filtered space-saving
  - 用一個表紀錄上下限
    - 上限 & 可能誤差
  - 用第二張表紀錄不在第一張的可能出現次數
    - 先 hash 再紀錄次數
  ***
  - 增加時, 如果已經在第一張表, 直接增加最大值
  - 增加時, 如果不在第一張表
    1. 增加第二張表的對應次數
    2. 如果對應次數增加後超過第一張表最小的最大值
       1. 替換進入第一張表
       2. 增加第一張表對應欄位的`最大值` & `誤差`

### Count Distinct

- hyperloglog

## Publish server

- [Google cloud run](https://github.com/raymond-chia/Note/blob/main/SRE.md#cloud-run)
- [ngrok](https://ngrok.com/)

## Random

- `openssl rand -hex {length}`
- `dd if=/dev/urandom bs=1 count=65536 | sha256sum`

## Regex

- 至少在 vs code
  - replace 可以用 `$0` 保留找到的東西

## Search

- Vector Search

## Security

- 掃描病毒: https://www.virustotal.com/gui/home/upload

## Serialization

- ProtoBuf
  - best practice: https://protobuf.dev/programming-guides/api/
- FlatBuffers
  - 可以只解析部份
- msgpack
  - to json & back: https://github.com/ludocode/msgpack-tools

## Server

### Nginx

- 可以根據設定檔控制回傳內容

## Store

### Steam

- sdk 可以用 steam_appid.txt 指定測試的 app id

## Tableau

- control + c 不會中斷任務
  - tsm jobs list
  - tsm jobs cancel

## Terminal

- 切換 wrapping: `alt + z`
- [It is a 'magical' key combo you can hit which the kernel will respond to regardless of whatever else it is doing, unless it is completely locked up.](https://www.kernel.org/doc/html/latest/admin-guide/sysrq.html)
- 切換使用者
  - `sudo su -l {使用者名稱}`
  - `sudo -u {使用者名稱} --login`
- 背景執行
  - 在指令結尾加上 `&`
    - NOTE: [SRE.md 的 Google Compute Engine](https://github.com/raymond-chia/Note/blob/main/SRE.md#compute-engine)
    - 但是登出時會被砍掉
  - screen
    - 登出不會被砍掉
    - detach: `Ctrl + a 再按下 d 鍵`
    - resume: `screen -r`
- file system
  - 搜尋檔案
    - `which` 搜尋 $PATH
    - `locate` 每天更新 ??
    - `find`
  - 通常 file system name == device. 不過 Google 有時候對不上
    - `df -h`
      - file system name
    - `lsblk`
      - device name
    - `mount` ??
  - `du -sh .[!.]* * | sort -h` 可以看這一層各個檔案 / 資料夾大小
    - 差別 ??
- 看 processes: `top`, `pstree`
- `free` 檢查記憶體用量
- 查看機器: `uname -m`
- `chmod +rwx {filename}` 或 `chmod -rwx {filename}`
  - read, write, execute
- alias
  - 在 ~/.bashrc 中加上
    ```bash
    if [ -f ~/.bash_aliases ]; then
      . ~/.bash_aliases
    fi
    ```
- 用環境變數填寫 script
  - `envsubst < {script}`

### Symbolic link

- Windows: https://docs.microsoft.com/zh-tw/windows-server/administration/windows-commands/mklink
  1. Use command prompt ( not powershell or something else )
  2. mklink `{/d or /j}` `{link name}` `{path to target}`
- Linux: ln -s

### Open browser from terminal

- windows: `start`
  - https://github.com/skratchdot/open-golang
- Mac: `open https://example.com`
  - https://superuser.com/questions/85151/how-to-open-a-browser-from-terminal
- Linux: `xdg-open`
  - https://askubuntu.com/questions/682542/is-there-a-way-to-open-browser-using-terminal

### Vim

- gg 到開頭
- shift + g 到結尾
- dd, dg
- `/{想搜尋的東西}`
  - n 下一個
  - shift + n 上一個
- u 代表 undo

## Xcode

- 安裝
  - https://github.com/nodejs/node-gyp/issues/569#issue-55705963
- 版本
  - xcodebuild -version
- 查詢安裝位置
  - xcode-select -p
- if missing files
  - https://stackoverflow.com/questions/53135863/macos-mojave-ruby-config-h-file-not-found#answer-65481787
