## Bash
- set -ex
  - give verbose output and also will abort your script immediately if part of the script fails.
  - https://stackoverflow.com/questions/38342992/what-does-ex-option-used-in-bash-bin-bash-ex-mean

## Docker
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

## Golang
#### Build for Linux
- 64-bit: GOOS=linux GOARCH=amd64 go build
  - https://freshman.tech/snippets/go/cross-compile-go-programs/
#### Golang manage multiple version
- https://go.dev/doc/manage-install#installing-multiple
- Use vscode
#### `Gone 410` with private repository
- GOPRIVATE={repository host}
  - https://stackoverflow.com/questions/27500861/whats-the-proper-way-to-go-get-a-private-repository

## Google
#### Cloud Run
  1. prepare files to build docker image
      1. create binary that will be executed in docker container
  2. gcloud auth configure-docker
  3. docker build -t {registry}:{version} .
  4. docker push {registry}:{version}
  5. gcloud run deploy --allow-unauthenticated --image {registry}:{version} --port {port}
      - 如果沒有權限設定 `--allow-unauthenticated`, 可以請有權限的人在 web console 對應 service 的 `TRIGGERS`/`Authentication` 設定 `Allow unauthenticated invocations`
      - gcloud run deploy --help for more options
      - On success, the command line displays the service URL.
          - 也可以查詢 web console 對應 service 的 DETAILS
          - https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-go-service#deploy
#### GKE
  1. 按下 Deploy, 並按照表格填寫
  2. 按下 expose, 填寫 dockerfile expose 的 port

## Input
#### Keyboard event
  - code = [Physical keys](https://api.flutter.dev/flutter/services/PhysicalKeyboardKey-class.html). Keys which represent a `particular key location` on a QWERTY keyboard. It ignores any modifiers, modes, or keyboard layouts which may be in effect.
  - key = Logical keys. Keys which are interpreted in the `context` of any modifiers, modes, or keyboard layouts which may be in effect.
  - https://youtu.be/jLqTXkFtEH0?t=360

## MongoDB
#### MongoDB replicaset connection
- To avoid automatic server discovery and getting stuck on connecting while using MongoDB connection string, specify a direct connect should be made. This can be done by providing `directConnection=true` or `connect=direct` option in the connection string.
- https://pkg.go.dev/go.mongodb.org/mongo-driver/mongo/options#ClientOptions.SetDirect

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
