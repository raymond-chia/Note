## 2FA
- gitlab + authy: 如果顯示 invalid pin code, 檢查 gitlab profile 的時區是否設定正確

## Aesthetic

#### Comment

- represent the reason a piece of code exists

#### Naming

- with: unit (sec, min)
- without: abbreviation, types, utils
- https://www.youtube.com/watch?v=-J3wNP6u5YU

## Apple

- 登入用的 key & 查詢收據用的 key 不同
  - 登入用的每個遊戲一把
  - 查詢收據用的全公司一把

## Bash

- 驗證: https://www.shellcheck.net/
- set -ex
  - give verbose output and also will abort your script immediately if part of the script fails.
  - https://stackoverflow.com/questions/38342992/what-does-ex-option-used-in-bash-bin-bash-ex-mean

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

#### Dragonfly

- in memory

#### etcd

- in disk
- for Kubernetes

#### MongoDB

- in disk
- operations
  - get current operations
    - https://www.mongodb.com/docs/manual/reference/method/db.currentOp/
    - for example `db.currentOp( {"waitingForLock": true} )`
  - some operations with retryWrites=true might cause oplog flooding
    - https://www.mongodb.com/docs/manual/core/retryable-writes/#retryable-write-operations

###### replicaset connection

- To avoid automatic server discovery and getting stuck on connecting while using MongoDB connection string, specify a direct connect should be made. This can be done by providing `directConnection=true` or `connect=direct` option in the connection string.
- https://pkg.go.dev/go.mongodb.org/mongo-driver/mongo/options#ClientOptions.SetDirect

###### index

- [drop index will block all operations on the collection](https://www.mongodb.com/docs/manual/reference/method/db.collection.dropIndex/#resource-locking)

#### Redis

- in memory
- [redis docker image (with some modules)](https://hub.docker.com/r/redislabs/redismod)
- [AOF (Append Only File)](https://redis.io/docs/management/persistence/)
  - with RDB-preamble 可以抑制 AOF 大小

#### ZooKeeper

- in memory
- jvm 設定似乎很麻煩, 例如 garbage collection（跟使用的資料有關）

## Docker

#### Command (Frequently used)

-

#### Dockerfile

- Instead of specifying a context, you can pass a single Dockerfile in the URL or pipe the file in via STDIN. To pipe a Dockerfile from STDIN
  `docker build - < Dockerfile`
  https://docs.docker.com/engine/reference/commandline/build/

#### Install docker on mac

- [Use docker-machine + virtualbox](https://stackoverflow.com/questions/44084846/cannot-connect-to-the-docker-daemon-on-macos#answer-49719638)
- [Set ip address used by docker-machine in virtualbox](https://stackoverflow.com/questions/69805077/cannot-start-docker-daemon-at-macbook#answer-70373434)
- [The ip of virtualbox](https://superuser.com/questions/310697/connect-to-the-host-machine-from-a-virtualbox-guest-os#answer-310745)
  1. `brew install docker-machine docker`
  2. `brew install --cask virtualbox`
  3. `docker-machine create -d virtualbox --virtualbox-hostonly-cidr "192.168.63.1/24" default` // (use `docker-machine rm default` if needed)
  4. `eval "$(docker-machine env default)"`
  5. `netstat -rn` on mac/linux host
  6. search for Netif == vboxnet

#### Run with privilege

- docker run --privileged registry:version
  - https://docs.docker.com/engine/reference/commandline/run/#full-container-capabilities---privileged

## DNS
- Ubuntu 18 修改
  - sudo vim /etc/resolv.conf
  - 由上而下填寫 DNS server ip
    - 如果只有 domain name, 可以用 dig 換成 ip

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

- https://andrewlock.net/working-with-stacked-branches-in-git-is-easier-with-update-refs/#enabling-update-refs-by-default
  - 一次更新所有相關的 branches
  - add the following to your .gitconfig file:
    ```
    [rebase]
      updateRefs = true
    ```

#### Github

- Pushing to Github results in 403
  - Github seems only supports ssh way to read&write the repo
  - 1. Edit `.git/config` file under your repo directory.
    1. Find `url=` entry under section `[remote "origin"]`.
    1. Change it from: `url=https://MichaelDrogalis@github.com/derekerdmann/lunch_call.git`
       to: `url=ssh://git@github.com/derekerdmann/lunch_call.git`
       That is, change all the texts before `@` symbol to `ssh://git`
  - https://stackoverflow.com/questions/7438313/pushing-to-git-returning-error-code-403-fatal-http-request-failed
- Add ssh key to github
  - https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account
- [設定 ssh key 之後要推 code 到 github](https://stackoverflow.com/questions/29297154/github-invalid-username-or-password)
  - git remote set-url origin git@github.com:raymond-chia/Note.git

## Google

#### Bigquery

- [data streamed to an ingestion time partitioned table might be delayed](https://cloud.google.com/bigquery/docs/streaming-data-into-bigquery#dataavailability)
  - up to 90 mins

#### Cloud Platform

- `X-Cloud-Trace-Context` 可以協助追蹤 log. https://stackoverflow.com/questions/54313017/what-is-the-purpose-of-x-cloud-trace-context

#### Cloud Storage

- [Bucket name 如果含有 `.` 會被當作 DNS, 需要特別設定](https://cloud.google.com/storage/docs/buckets#naming)
- [Bucket names reside in a single namespace that is shared by all Cloud Storage users](https://cloud.google.com/storage/docs/buckets#considerations)
  - Bucket names are publicly visible  
    Don't use user IDs, email addresses, project names, project numbers, or any personally identifiable information (PII) in bucket names because anyone can probe for the existence of a bucket
- [檔名結尾 `#0` 代表最近的版本](https://cloud.google.com/storage/docs/introduction#resource-name)
  - 如果檔案名稱可能混淆, 需要特別標明

#### Geo IP
- GFEs & Cloud Armor use different IPGeo databases (至少到 2023)
- update once per week

#### Purchase

- Android 沒有 nonconsumable 的區分. 要自行 consume
- https://developer.android.com/google/play/billing/security

#### 畫架構

- https://googlecloudcheatsheet.withgoogle.com/architecture

## GRPC

- https://developers.google.com/protocol-buffers/docs/tutorials
- https://grpc.io/docs/languages/go/generated-code/
- `protoc`
- `protoc-gen-go`: a `protoc` plugin to generate a Go protocol buffer package
- `protoc-gen-doc`: a `protoc` plugin to generate documentation
- [`protoc-go-inject-tag`](https://github.com/favadi/protoc-go-inject-tag)

## HTTP

- [Connection 相關的 header 如 Connection 和 Keep-Alive 在 HTTP/2 中被禁用](https://developer.mozilla.org/zh-TW/docs/Web/HTTP/Headers/Connection)
  - 可能導致無法送請求

## Input

#### Keyboard event

- code = [Physical keys](https://api.flutter.dev/flutter/services/PhysicalKeyboardKey-class.html). Keys which represent a `particular key location` on a QWERTY keyboard. It ignores any modifiers, modes, or keyboard layouts which may be in effect.
- key = Logical keys. Keys which are interpreted in the `context` of any modifiers, modes, or keyboard layouts which may be in effect.
- https://youtu.be/jLqTXkFtEH0?t=360

## Language

#### C#

- NuGet maintains a reference list of packages used in a project and the ability to restore and update those packages from that list

#### Golang

###### Build for Linux

- 64-bit: `GOOS=linux GOARCH=amd64 go build`
  - https://freshman.tech/snippets/go/cross-compile-go-programs/

###### Golang manage multiple version

- https://go.dev/doc/manage-install#installing-multiple
- Use vscode

###### `Gone 410` with private repository

- GOPRIVATE={repository host}
  - https://stackoverflow.com/questions/27500861/whats-the-proper-way-to-go-get-a-private-repository

###### Variables

- `go env` can get GOPATH, GOROOT, ...

###### Check vulnerability

- https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck

###### Game server template

- https://heroiclabs.com/

###### Generics

```go
func F[T any, TPointer interface{
  proto.Message
  *T
}]()
```

- 可以確保 new(T) 滿足 proto.Message

###### Side effect

- 如果對有空間 (cap) 的 slice 做 append, 修改會是 in place
  - https://stackoverflow.com/questions/53572736/append-to-a-new-slice-affect-original-slice

#### Javascript

- MemLab can find memory leaks

###### Redux

- <img src="https://redux.js.org/assets/images/ReduxDataFlowDiagram-49fa8c3968371d9ef6f2a1486bd40a26.gif" width="480" height="360" />
- [reducer](https://redux.js.org/tutorials/fundamentals/part-3-state-actions-reducers#writing-reducers)

###### Reactjs

- useEffect
  - 搭配 fetch: render 時送請求
  - 第二個參數用來檢查要不要觸發
    - 不帶代表每次都跑
    - [] 代表只跑一次
    - https://stackoverflow.com/questions/57760842/why-would-we-use-useeffect-without-a-dependency-array
- [useSelector](https://react-redux.js.org/api/hooks#useselector)
  - Allows you to extract data from the Redux store state

#### Python

- [venv](https://www.infoworld.com/article/3239675/virtualenv-and-venv-python-virtual-environments-explained.html)

## Network

#### Connection reset by peer

- server close session & client send request
- [CDN & Load Balancer timeout](https://medium.com/starbugs/%E8%AC%8E%E4%B9%8B%E8%81%B2%E5%B0%8D-connection-%E8%AA%AA%E9%81%93-%E4%BD%A0%E5%B7%B2%E7%B6%93%E6%AD%BB%E4%BA%86-b53d27c7ecb7#77a6)
- [Google load balancer restarts periodically](https://cloud.google.com/load-balancing/docs/https#timeouts_and_retries)
- https://blog.percy.io/tuning-nginx-behind-google-cloud-platform-http-s-load-balancer-305982ddb340#3b71

## OAuth

#### 1.0a

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

#### Mac

- brew
  - switch version
    - for example
      - brew unlink node
      - brew link node@14

## Probabilistic data structure

- Bloom
  - 適合分散式系統
  - 比較成熟
- Cuckoo
  - 效率好
  - 空間利用率好
  - 可以刪除
  - 限制數量（避免 100% false positive）
  - https://stackoverflow.com/questions/867099/bloom-filter-or-cuckoo-hashing

## Publish server

- [Google cloud run](https://github.com/raymond-chia/Note/blob/main/SRE.md#cloud-run)
- [ngrok](https://ngrok.com/)

## Serialization

- ProtoBuf
- FlatBuffers
  - 可以只解析部份

## Terminal

#### Symbolic link

- Windows: https://docs.microsoft.com/zh-tw/windows-server/administration/windows-commands/mklink
  1. Use command prompt ( not powershell or something else )
  2. mklink `{/d or /j}` `{link name}` `{path to target}`
- Linux: ln -s

#### Open browser from terminal

- Mac: `open https://example.com`
  - https://superuser.com/questions/85151/how-to-open-a-browser-from-terminal
- Linux
  - https://askubuntu.com/questions/682542/is-there-a-way-to-open-browser-using-terminal

## Xcode

- 安裝
  - https://github.com/nodejs/node-gyp/issues/569#issue-55705963
- 版本
  - xcodebuild -version
- 查詢安裝位置
  - xcode-select -p
- if missing files
  - https://stackoverflow.com/questions/53135863/macos-mojave-ruby-config-h-file-not-found#answer-65481787
