## 2FA

- gitlab + authy: 如果顯示 invalid pin code, 檢查 gitlab profile 的時區是否設定正確

## Aesthetic

- https://12factor.net/

### Model-Driven (Domain-Driven ?)

- https://www.youtube.com/watch?v=3aoLV5i1feo
  - 一個 model 列出所有 rules

### Comment

- represent the reason a piece of code exists

### Naming

- with: unit (sec, min)
- without: abbreviation, types, utils
- https://www.youtube.com/watch?v=-J3wNP6u5YU

## Apple

- 登入用的 key & 查詢收據用的 key 不同
  - 登入用的每個遊戲一把
  - 查詢收據用的全公司一把

## Captcha like

- Cloudflare Turnstile
  - [避免讓使用者輸入驗證碼](https://blog.cloudflare.com/turnstile-private-captcha-alternative/#we-are-opening-our-captcha-replacement-to-everyone)

## Certificate

- https on localhost https://github.com/FiloSottile/mkcert#mkcert

## Coordinate system

- [hex](https://www.redblobgames.com/grids/hexagons)

## Data

- cache related introduction: https://github.com/SanderMertens/ecs-faq#data-oriented-design

## Database

- memory: Dragonfly, Redis, ZooKeeper
- disk: etcd, MongoDB

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

- To avoid automatic server discovery and getting stuck on connecting while using MongoDB connection string, specify a direct connect should be made. This can be done by providing `directConnection=true` or `connect=direct` option in the connection string.
  - https://pkg.go.dev/go.mongodb.org/mongo-driver/mongo/options#ClientOptions.SetDirect
- slow operation 可能會紀錄在 secondary member of replica set 的 oplog entries
  - https://www.mongodb.com/docs/manual/replication/#slow-operations
- 同步的資料太多
  - 可能限制 primary 寫入的速度
  - 讓 secondary 追上
  - https://www.mongodb.com/docs/manual/replication/#replication-lag-and-flow-control
  - 需要 read majority

#### index

- [drop index will block all operations on the collection](https://www.mongodb.com/docs/manual/reference/method/db.collection.dropIndex/#resource-locking)
- [對 array 設定 unique index, 無法阻止 array 內有重複的值](https://www.mongodb.com/docs/manual/core/index-multikey/?_ga=2.110814017.570310677.1681713217-959579056.1642987351#unique-multikey-index)

#### Others

- 在 secondary 下指令: `rs.secondaryOk()`

### Redis

- in memory
- [redis docker image (with some modules)](https://hub.docker.com/r/redislabs/redismod)
- [AOF (Append Only File)](https://redis.io/docs/management/persistence/)
  - with RDB-preamble 可以抑制 AOF 大小
- redis-cli -n={db number} {command} | xargs redis-cli -n={db number} {command}

### ZooKeeper

- in memory
- jvm 設定似乎很麻煩, 例如 garbage collection (跟使用的資料有關)

### SQL

#### MySQL

- `docker run -itd --name=sql-mysql -e=MYSQL_ROOT_PASSWORD={root 的密碼} -e=MYSQL_DATABASE={預設的資料庫名稱} mysql:8.0.33-debian --default-authentication-plugin=mysql_native_password`
  - `--default-authentication-plugin=mysql_native_password`: mysql 8 uses `caching_sha2_password` as the default authentication plugin instead of `mysql_native_password`  
    有些 client 不支援 caching_sha2_password, 用上述指令使用舊版的 mysql_native_password

#### SQLite

- CRUD 指令結尾要 `;`

## Docker

### Command (Frequently used)

- run with privilege
  - `docker run --privileged {registry:version}`
  - https://docs.docker.com/engine/reference/commandline/run/#full-container-capabilities---privileged
- `docker run -itd -p=27017:27017 --name={container name} mongo:4.4`
- `docker exec -it {container name} bash`
- `docker network inspect bridge` 查看 container 的 ip. bridge 是預設的 docker network

### Dockerfile

- Instead of specifying a context, you can pass a single Dockerfile in the URL or pipe the file in via STDIN. To pipe a Dockerfile from STDIN
  `docker build - < Dockerfile`
  https://docs.docker.com/engine/reference/commandline/build/

### Install docker on mac

- [Use docker-machine + virtualbox](https://stackoverflow.com/questions/44084846/cannot-connect-to-the-docker-daemon-on-macos#answer-49719638)
- [Set ip address used by docker-machine in virtualbox](https://stackoverflow.com/questions/69805077/cannot-start-docker-daemon-at-macbook#answer-70373434)
- [The ip of virtualbox](https://superuser.com/questions/310697/connect-to-the-host-machine-from-a-virtualbox-guest-os#answer-310745)
  1. `brew install docker-machine docker`
  2. `brew install --cask virtualbox`
  3. `docker-machine create -d virtualbox --virtualbox-hostonly-cidr "192.168.63.1/24" default` // (use `docker-machine rm default` if needed)
  4. `eval "$(docker-machine env default)"`
  5. `netstat -rn` on mac/linux host
  6. search for Netif == vboxnet

## DNS

- Ubuntu 18 修改
  - sudo vim /etc/resolv.conf
  - 由上而下填寫 DNS server ip
    - 如果只有 domain name, 可以用 dig 拿 ip

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

## Git

- `git reflog`: 拯救錯誤操作, 比如 reset --hard 到錯誤的地方
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

### Github

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
- [設定 ssh key 之後要推 code 到 github](https://stackoverflow.com/questions/29297154/github-invalid-username-or-password)
  - git remote set-url origin git@github.com:raymond-chia/Note.git

### Gitlab

- table of contents: https://docs.gitlab.com/ee/user/markdown.html#table-of-contents
- Add ssh key to gitlab 可以參考 github
- 自動管理 issue: https://gitlab.com/gitlab-org/ruby/gems/gitlab-triage

## Google

### Bigquery

- [data streamed to an ingestion time partitioned table might be delayed](https://cloud.google.com/bigquery/docs/streaming-data-into-bigquery#dataavailability)
  - up to 90 mins

### Cloud Platform

- `X-Cloud-Trace-Context` 可以協助追蹤 log. https://stackoverflow.com/questions/54313017/what-is-the-purpose-of-x-cloud-trace-context

### Cloud Storage

- [Bucket name 如果含有 `.` 會被當作 DNS, 需要特別設定](https://cloud.google.com/storage/docs/buckets#naming)
- [Bucket names reside in a single namespace that is shared by all Cloud Storage users](https://cloud.google.com/storage/docs/buckets#considerations)
  - Bucket names are publicly visible  
    Don't use user IDs, email addresses, project names, project numbers, or any personally identifiable information (PII) in bucket names because anyone can probe for the existence of a bucket
- [檔名結尾 `#0` 代表最近的版本](https://cloud.google.com/storage/docs/introduction#resource-name)
  - 如果檔案名稱可能混淆, 需要特別標明

### Geo IP

- GFEs & Cloud Armor use different IPGeo databases (至少到 2023)
- update once per week

### Log

- 用 Google Workloads 可以自動加上 filter

### Purchase

- Android 沒有 nonconsumable 的區分. 要自行 consume
- https://developer.android.com/google/play/billing/security

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

## Input

### Keyboard event

- code = [Physical keys](https://api.flutter.dev/flutter/services/PhysicalKeyboardKey-class.html). Keys which represent a `particular key location` on a QWERTY keyboard. It ignores any modifiers, modes, or keyboard layouts which may be in effect.
- key = Logical keys. Keys which are interpreted in the `context` of any modifiers, modes, or keyboard layouts which may be in effect.
- https://youtu.be/jLqTXkFtEH0?t=360

## Language

### Bash

#### 指令

- `which` 搜尋 $PATH, `locate` 每天更新 ?, `find`
- 資料夾
  - 通常 file system name == device. 不過 Google 有時候對不上
    - `df -h`
      - file system name
    - `mount`
      - device name
  - `sudo du -sh .[!.]* * | sort -g` 或 `du -sh *` 可以看這一層各個檔案 / 資料夾大小
    - 差別 ?
- `sudo -u` 切換使用者. `sudo -u --login`
- 在指令結尾加上 `&`, 會在背景執行 (NOTE: [SRE.md 的 Google Compute Engine](https://github.com/raymond-chia/Note/blob/main/SRE.md#compute-engine))

#### script

- 驗證: https://www.shellcheck.net/
- https://google.github.io/styleguide/shellguide.html
- set -euxo pipefail
  - give verbose output and also will abort your script immediately if part of the script fails.
  - https://stackoverflow.com/questions/38342992/what-does-ex-option-used-in-bash-bin-bash-ex-mean
  - https://gist.github.com/mohanpedala/1e2ff5661761d3abd0385e8223e16425
- [bash script 預設不支援 alias, 需要另外處理](https://unix.stackexchange.com/questions/1496/why-doesnt-my-bash-script-recognize-aliases)
- `"${2:-default}"` [用第二個參數, 如果不存在就用 `default`](https://stackoverflow.com/questions/1163145/what-does-2-1-mean-in-bash)
- `=~` 代表右邊會是 regex

### C#

- NuGet maintains a reference list of packages used in a project and the ability to restore and update those packages from that list

### Golang

#### Build

- linux amd 64-bit: `GOOS=linux GOARCH=amd64 go build`
  - https://freshman.tech/snippets/go/cross-compile-go-programs/
- build binary with environment variable: `ldflags`

#### Golang manage multiple version

- https://go.dev/doc/manage-install#installing-multiple
- Use vscode

#### Private Repository, `Gone 410`

- GOPRIVATE={repository host}
  - https://stackoverflow.com/questions/27500861/whats-the-proper-way-to-go-get-a-private-repository
- `git config --global url."git@gitlab.private.com:".insteadOf "https://gitlab.private.com"`
  - ~/.gitconfig 裡面應該要有
    ```
    [url "git@gitlab.private.com:"]
      insteadOf = https://gitlab.private.com
    ```

#### Dependency, GOPATH, ...

- `go env` can get GOPATH, GOROOT, ...
- 如果 Editor linter 無法正確讀取 dependency
  - go1.18 可以用 workspace 處理
    - go work
    - https://stackoverflow.com/questions/58518588/vscode-could-not-import-golang-package
- 指向 local dependency https://go.dev/ref/mod#go-mod-file-replace

#### Check vulnerability

- https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck

#### Generics

```go
func F[T any, TPointer interface{
  proto.Message
  *T
}]()
```

- 可以確保 new(T) 滿足 proto.Message

#### Side effect

- 如果對有空間 (cap) 的 slice 做 append, 修改會是 in place
  - https://stackoverflow.com/questions/53572736/append-to-a-new-slice-affect-original-slice
- for 裡面的 closure 可能 cache 最後的變數

#### Lib

- github.com/redis/go-redis retry 可能有問題

#### Misc

- 1 cpu + golang 能承受 ?k rps
- Game server template: https://heroiclabs.com/

### Javascript

- MemLab can find memory leaks
- Jest 用來測試

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

### Python

- FastAPI: 自動產生 OpenAPI
- [venv](https://www.infoworld.com/article/3239675/virtualenv-and-venv-python-virtual-environments-explained.html)
  - python -m venv .
  - source bin/activate

### Rust

- 指南: https://rust-unofficial.github.io/patterns/intro.html

## Make

- MakeFile: a text file that contains the recipe for building your program

## Network

### Connection reset by peer

- server close session & client send request
- [CDN & Load Balancer timeout](https://medium.com/starbugs/%E8%AC%8E%E4%B9%8B%E8%81%B2%E5%B0%8D-connection-%E8%AA%AA%E9%81%93-%E4%BD%A0%E5%B7%B2%E7%B6%93%E6%AD%BB%E4%BA%86-b53d27c7ecb7#77a6)
- [Google load balancer restarts periodically](https://cloud.google.com/load-balancing/docs/https#timeouts_and_retries)
- https://blog.percy.io/tuning-nginx-behind-google-cloud-platform-http-s-load-balancer-305982ddb340#3b71

### Misc

- 清除 ip 舊的 key: `ssh-keygen -R {ip}`
  - 症狀: `REMOTE HOST IDENTIFICATION HAS CHANGED!`
- whois
  - 查詢 domain name 註冊資訊

## OAuth

### 1.0a

- Make sure consumer key & access token secret are escaped
  - github.com/gomodule/oauth1 v0.2.0 escapes consumer key & access token secret automatically
  - github.com/dghubble/oauth1 v0.7.1 does NOT escape consumer key & access token secret automatically

## OpenSocial

- make request
  - https://developers.google.com/gadgets/docs/reference#makerequest
  - https://opensocial.github.io/spec/2.5.1/Core-Gadget.xml#gadgets.io.makeRequest

## OpenToonz

- Open the OpenToonz Stuff folder. Open the Profiles folder, and open the ENV folder.
- Use a text editor such as NotePad++ to open YOURNAME.env file, and look for the key "SoftwareCurrentFont" and SoftwareCurrentFontSize

## Operating System

### Mac

- brew
  - switch version
    - for example
      - brew unlink node
      - brew link node@14

### Ubuntu

- Left Shift, F12 可以進入特殊模式 (可能要長按或連按)
  - https://askubuntu.com/questions/24006/how-do-i-reset-a-lost-administrative-password
- alias
  - 在 ~/.bashrc 中加上
    ```bash
    if [ -f ~/.bash_aliases ]; then
      . ~/.bash_aliases
    fi
    ```
- [It is a 'magical' key combo you can hit which the kernel will respond to regardless of whatever else it is doing, unless it is completely locked up.](https://www.kernel.org/doc/html/latest/admin-guide/sysrq.html)
- 升級過期的作業系統: https://askubuntu.com/questions/91815/how-to-install-software-or-upgrade-from-an-old-unsupported-release
- 找不到 libstdc++.so.6, 或其他 gcc 相關 lib: https://stackoverflow.com/questions/480764/linux-error-while-loading-shared-libraries-cannot-open-shared-object-file-no-s
  - 有待確認
- crash: `sudo journalctl --since="-5 minutes"` 檢查原因
  - ref https://askubuntu.com/questions/1414900/automatic-logout-using-ubuntu-22-04-lts
  - `journalctl -u {service-name}` 可以看特定 service 的 log
    - `systemctl status {service-name}` 只能看到部份 log
    - https://unix.stackexchange.com/questions/225401/how-to-see-full-log-from-systemctl-status-service
- 安裝 nvidia cuda: sudo ubuntu-drivers autoinstall
- `/var/run/docker.sock` permission
  - `sudo chmod 666 /var/run/docker.sock`
  - `sudo usermod -aG docker $USER`
- chmod 解釋 https://superuser.com/questions/295591/what-is-the-meaning-of-chmod-666

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

## Serialization

- ProtoBuf
  - best practice: https://protobuf.dev/programming-guides/api/
- FlatBuffers
  - 可以只解析部份
- msgpack
  - to json & back: https://github.com/ludocode/msgpack-tools

## Store

### Steam

- sdk 可以用 steam_appid.txt 指定測試的 app id

## Tableau

- control + c 不會中斷任務
  - tsm jobs list
  - tsm jobs cancel

## Terminal

- 切換 wrapping: `alt + z`

### Symbolic link

- Windows: https://docs.microsoft.com/zh-tw/windows-server/administration/windows-commands/mklink
  1. Use command prompt ( not powershell or something else )
  2. mklink `{/d or /j}` `{link name}` `{path to target}`
- Linux: ln -s

### Open browser from terminal

- Mac: `open https://example.com`
  - https://superuser.com/questions/85151/how-to-open-a-browser-from-terminal
- Linux
  - https://askubuntu.com/questions/682542/is-there-a-way-to-open-browser-using-terminal

### Vim

- gg 到開頭
- shift + g 到結尾
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
