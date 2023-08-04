## Book

### 核心

- 預先準備
- 編寫文件
- 減少人工介入

### Error Budget

- 99.99% `availability` == 0.01% `unavailability` == 0.01% `error budget`
  - 也可以設定其他數字
- 盡情更新, 直到用完 error budget

### Monitor

- 警報應該分析問題嚴重程度
  - alert
    - 需要`立刻`有人工介入
  - ticket
    - 需要有人工介入
  - logging

### Postmortem

1. 發生什麼事情
2. 原因
3. 下次怎麼避免 / 處理

### Update

1. progressive rollout
2. 快速發現問題
3. rollback

### 雜項

- 人工操作的時間上限 50%. 剩下時間拿去開發取代人工的程式
  - 讓開發人員分擔部份工作

## Database

- Point in time recovery (以 MongoDB 為例)
  1. 用最新的備份建立 DB
  2. 載入要被替換的 DB 的 oplog
     - 到出問題的時間點之前
  3. 替換 DB

### Redis

- 設定 /etc/redis/redis.conf
  - /etc/redis/sentinel.conf
  - 在 cli 打 `INFO`, `CONFIG GET *`
- Persistence
  - RDB: snapshot
  - AOF: 操作紀錄
    - fsync 保存紀錄到 disk
  - 二合一: aof-use-rdb-preamble
  - https://redis.io/docs/management/persistence/

## [DNS](https://www.cloudflare.com/learning/dns/what-is-dns/)

- Trailing Dots tell the DNS server that this is a Fully Qualified Domain Name.
  - 例如 `example.com.`
  - 設定 resource record 時需要特別標明為 FQDN, 以免被加上不預期的 root domain
- 註冊
  - Google DNS 之類的不會幫忙註冊, 需要另外處理（例如找 [Gandi](https://docs.gandi.net/zh-hant/domain_names/register/new_gtld.html), [Google](https://cloud.google.com/dns/docs/update-name-servers)）
- 四種 server
  - DNS recursor (recursive resolver)
    - 幫忙查詢的 server
    - 例如 Cloudflare 1.1.1.1, Google 8.8.8.4, 8.8.8.8
  - root nameserver
  - top level domain server
  - authoritative nameserver
- Recursive Query & Iterative Query
  - machine 透過 recursive query 詢問 recursor
  - recursor 用 iterative query 查詢 root, top level domain, authoritative nameserver
- <img src="https://cf-assets.www.cloudflare.com/slt3lc6tev37/1O1o3jhs0ztWsD00k8RLIJ/f33c1793a7e21cb92678c1f35ef1b245/dns_record_request_sequence_cname_subdomain.png" width=500/>
- cache
  - browser / application
  - operating system
  - recursor
    - A record: 直接回 ip
    - NS record: 直接從紀錄的 NS record 開始詢問
    - top level domain server
    - root server: 通常是 cache 清空才需要查詢

### [Resource Record](https://www.cloudflare.com/learning/dns/dns-records/)

- 每個代表網域名稱的檔案叫做 `zone file`
- zone file 裡面有多筆 `resource record`
- `@` 代表 current domain
  - https://serverfault.com/questions/426326/what-is-the-name-for-a-dns-record-starting-with
- TTL 代表可以 cache 多久

#### SOA

- start of authority
- 每個檔案都需要 & 只能有一個
- 描述該 zone
- 同步 primary & secondary 稱為 zone transfer
  - 先傳 SOA, 用 serial 判斷要不要更新
  - 透過 tcp

| 欄位    | 意義                                                                                                                    |
| ------- | ----------------------------------------------------------------------------------------------------------------------- |
| MNAME   | primary nameserver for the zone                                                                                         |
| RNAME   | email <br> 例如 admin.example.com 代表 admin@example.com <br> 不用 `@` 大概是因為 `@` 在 resource record 裡面有特殊含意 |
| SERIAL  | 版號 <br> secondary server 用來判斷要不要更新                                                                           |
| REFRESH | secondary server 的 polling 間隔                                                                                        |
| RETRY   | 如果 primary 失聯, polling 間隔                                                                                         |
| EXPIRE  | 如果 primary 失聯, secondary 還可以運作多久                                                                             |
| TTL     |                                                                                                                         |

#### NS

- nameserver
- 指向 domain name
- 不能指向 CNAME
- 表明在哪個 nameserver 可以查到目標 domain name

#### A

- address
- domain name 轉 ipv4

#### AAAA

- domain name 轉 ipv6

#### [PTR](https://www.cloudflare.com/learning/dns/dns-records/dns-ptr-record/)

- pointer
- ip 轉 domain name
- ip 以相反的方式紀錄
  - ipv4 結尾要 `.in-addr.arpa`
    - `192.0.2.255` => `255.2.0.192.in-addr.arpa`
  - ipv6 結尾要 `.ip6.arpa`
- 用途
  - email anti-spam filter
  - logging

#### [SRV](https://www.cloudflare.com/learning/dns/dns-records/dns-srv-record/)

- service
- domain name + port
- 不能指向 CNAME
- priority `越低`優先度越高
  - 同 priority 時, weight `越高`, 優先度越高

#### CNAME

- canonical name
- domain name 轉 domain name
- 幫主機設定別名
- 例如 sub domain name 共用 root domain name 的 ip
  - sub domain name 用 CNAME 指向 root domain name
  - 主機收到 request 再根據 url 判斷要給哪個網頁
- 避免 CNAME 指向另外一個 CNAME（浪費效能）

#### MX

- mail exchange
- 指向 domain name
- 不能指向 CNAME
- 導向處理信件的伺服器
- Simple Mail Transfer Protocol
- priority 越低優先度越高

#### [TXT](https://www.cloudflare.com/learning/dns/dns-records/dns-txt-record/)

- text
- 讓管理者備註
  - 還能用來處理垃圾信件
    - 用來實作 Domain Keys Identified Mail (DKIM)
      - 簽名
    - Sender Policy Framework (SPF)
      - 標示用哪些 server 送信
    - Domain-based Message Authentication, Reporting & Conformance (DMARC)
  - 還能用來驗證 domain ownership

## Google

- attach disk 需要 format & mount. Google 不會自動處理.
  - https://cloud.google.com/compute/docs/disks/add-persistent-disk

### Big Query

- limit 不影響收費
  - 用多個 cpu 搜尋資料庫
  - 查詢所有資料之後才處理 limit
- https://cloud.google.com/blog/products/data-analytics/cost-optimization-best-practices-for-bigquery

### Cloud CDN

- [不同種類的 Google CDN](https://cloud.google.com/cdn/docs/choose-cdn-product)
- [Cache Mode](https://cloud.google.com/cdn/docs/caching)
  - `CACHE_ALL_STATIC` (default): 沒有 cache control header, content type header 符合[條件](https://cloud.google.com/cdn/docs/caching#static)
  - `USE_ORIGIN_HEADERS`: [Cache control](https://cloud.google.com/cdn/docs/caching#cache_control_directives)
  - `FORCE_CACHE_ALL`: 覆蓋原本的 cache 設定
    - 不同的 vary header 不會共用 cache entry
- [可以客製化 cache key](https://cloud.google.com/cdn/docs/caching#cache-keys)
  - 多個 schemes, hosts 拿到同樣的結果
    - [Cache 跨 project 共用](https://cloud.google.com/cdn/docs/overview#eviction)
      - 同地區
  - 不同 query string, header, cookie 拿到不同的結果
- Negative caching: 根據 response code, cache 一段時間
- [Serve stale content](https://cloud.google.com/cdn/docs/serving-stale-content)
  - 避免被故障影響, 減少延遲
  - 兩筆 log:
    - 給 user 的內容
    - async 最新資訊
  - client 可以用 max-stale header
- [Non-cacheable content based on origin headers](https://cloud.google.com/cdn/docs/caching#non-cacheable_content)
- [Bypass by header](https://cloud.google.com/cdn/docs/caching#bypassing-cache)
- [Invalidation](https://cloud.google.com/cdn/docs/cache-invalidation-overview)
  - 1 per min
- [支援 Byte-range requests: 一次只拿部份](https://cloud.google.com/cdn/docs/caching#byte-range-requests)
- CDN 支援 ETag, Last-Modified
  - 需要在 response 特別標示 ETag, Last-Modified
- [TTL](https://cloud.google.com/cdn/docs/using-ttl-overrides)

|             | FORCE_CACHE_ALL    | CACHE_ALL_STATIC   | 意義                                                     |
| ----------- | ------------------ | ------------------ | -------------------------------------------------------- |
| Default TTL | :heavy_check_mark: | :heavy_check_mark: | CDN 預設值                                               |
| Max TTL     |                    | :heavy_check_mark: | CDN 最大值 <br> FORCE_CACHE_ALL 會覆蓋, 所以只要 default |
| Client TTL  | :heavy_check_mark: | :heavy_check_mark: | client TTL                                               |

- [Log](https://cloud.google.com/cdn/docs/logging)
- response size 小於約 80kb 的話會開始變成掛 CDN 比較貴，因為有 per request 計算的 cache lookup 費用  
  小到 3kb 的話連 APAC hit rate 90% 都還是 CDN 比較貴

### Cloud Run

1. prepare files to build docker image
   1. create binary that will be executed in docker container
2. `gcloud auth configure-docker`
3. `docker build -t {registry}:{version} .`
4. `docker push {registry}:{version}`
5. `gcloud run deploy --allow-unauthenticated --image {registry}:{version} --port {port}`
   - 如果沒有權限設定 `--allow-unauthenticated`, 可以請有權限的人在 web console 對應 service 的 `TRIGGERS`/`Authentication` 設定 `Allow unauthenticated invocations`
   - `gcloud run deploy --help` for more options
   - On success, the command line displays the service URL.
     - 也可以查詢 web console 對應 service 的 DETAILS
     - https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-go-service#deploy

### Cloud Storage

- https://github.com/raymond-chia/Note/blob/main/Troubleshooting.md#cloud-storage
- [每個 object 可以自行決定 storage class (standard, coldline, ...)](https://cloud.google.com/storage/docs/storage-classes#classes)
  - Autoclass 可以自動設定 storage class
- Built-in Cache vs Cloud CDN: https://cloud.google.com/storage/docs/caching#with
  - CDN cache size 其他資訊: https://cloud.google.com/cdn/docs/caching#maximum-size
- Object Lifecycle, Retention, Object Hold (類似 lock), Object Versioning, Compress (Transcoding)
  - Versioning 需要自行刪除過時的版本, 就算取消 versioning 也要手動刪除

### Compute Engine

- `gcloud compute ssh` 連上 vm 跑 user background process
  - 登出前會停掉 background process, 然後才能登出
  - https://unix.stackexchange.com/questions/682793/why-background-process-terminated-after-ssh-session-closed/682794#682794
- 用網頁連上 vm 跑 user background process
  - 關閉網頁不會停掉 background process
  - 關機時才會停掉

### Database

- 連線
  - 先建立一個 control console vm ?
    - `gcloud compute ssh --zone={zone} --project={project} control-console -- -N -L {port}:{remote-host}:{port}`
  - [iap](#IAP)

### GKE

1. 按下 Deploy, 並按照表格填寫
2. 按下 expose, 填寫 dockerfile expose 的 port

- GKE 可以放在 managed instance groups
- https://cloud.google.com/kubernetes-engine/docs/concepts/cluster-autoscaler#balancing_across_zones
  - cluster autoscaler attempts to keep these managed instance group sizes balanced when `scaling up`
    - scale down 的時候直接砍 underutilized nodes
      - 也就是 scale down 的時候, `group sizes` 可能`分佈不均`
- 用 workload 可以快速找到 log explorer
  - deployment
    - 掌管 ReplicaSets
    - rolling update
    - rollback
    - version control
  - stateful set
    - 會依照固定順序更新
    - 特性
      - consistent & unique identiy
      - persistent storage
      - stable network identity
  - daemon set
    - 1 pod per node
    - 可以用來
      - 收集 logs
      - monitor
      - manage network traffic across entire cluster

---

#### Log

- `labels."compute.googleapis.com/resources_name"` 是 node name (VM name)
- `resource.lables.pod_name` 是 pod name

### IAP

- `gcloud compute start-iap-tunnel ${target_instance.name} ${target_port} --project=${project_id} --local-host-port=localhost:9999 --zone=${target_instance.zone}`

### Load Balancer

- Google 內部服務也用 Global Server Load Balancer 尋找 ip
- [Choose](https://cloud.google.com/load-balancing/docs/choosing-load-balancer)  
  <img src="https://cloud.google.com/static/load-balancing/images/choose-lb.svg" width=480/>
- [External TCP/UDP Network Load Balancing](https://cloud.google.com/load-balancing/docs/network/networklb-backend-service)
  - 不影響 source & destination ip, protocol, port
  - 不會關掉連線
    - 無法自行擋住惡意連線
  - 不會處理 SSL
  - architecture
    - backend service
      - ipv4 (standard, premium), ipv6 (premium)
      - auto scaling with managed instance groups
      - distribution control
        - health check
        - source ip based traffic steering
        - session affinity  
          [connection tracking](https://cloud.google.com/load-balancing/docs/network/networklb-backend-service#tracking-mode)
        - connection draining
          - in progress requests are given time to complete when a VM is removed or when an endpoint is removed
        - failover policy
      - component
        - 1 regional external backend service (決定 balancer 怎麼導流量到 backend instance groups)
        - multiple regional external ip addresses  
          [multiple regional external forwarding rules](https://cloud.google.com/load-balancing/docs/network/networklb-backend-service#forwarding-rule-protocols)
          - protocol, ip address, port based
        - multiple backend instance groups
      - must create firewall rules that allow your load balancing traffic and health check probes to reach the backend VMs
    - target pool
      - legacy
  - <img src=https://cloud.google.com/static/load-balancing/images/tcp-forwarding-rule.svg width=300>
- [External HTTP(S) Load Balancing](https://cloud.google.com/load-balancing/docs/https)
  - header
    - 保存 Host header
    - X-Forwarded-For
      - `X-Forwarded-For: ...,<client-ip>,<load-balancer-ip>`
  - Global external HTTP(S) load balancer
    - PREMIUM
    - An external forwarding rule
    - Health check
    - Firewall rules
    - A target HTTP(S) proxy
      - Support SSL certificates (https://console.cloud.google.com/net-services/loadbalancing/advanced/sslCertificates/list)
      - 可能會改 header 大小寫
      - URL map
        - Request path, cookies, headers
    - Support cloud trace
    - Support custom headers (似乎不能搭配 Cloud CDN)
  - Regional external HTTP(S) load balancer
    - STANDARD
    - A proxy-only subnet is used to send connections from the load balancer to the backends. [ref](https://cloud.google.com/load-balancing/docs/https#proxy-only-subnet)
      - <img src="https://cloud.google.com/static/load-balancing/images/ilb-l7-components.svg" width=300>
      - Backend VMs or endpoints of all regional external HTTP(S) load balancers in a region and VPC network receive connections from the proxy-only subnet.
        - 應該是指所有 VM 只會看到 proxy-only subnet 來的 load balancer connection
    - Health check
    - Firewall rules
      - 1 for health check
      - 1 for proxy-only subnet
    - A target HTTP(S) proxy
    - 如果要用 cloud trace 或 custom headers, 可以用 standard tier 的 Global external HTTP(S) load balancer `(classic)`
      - 但是 url map 的功能比較少
  - <img src=https://cloud.google.com/static/load-balancing/images/https-forwarding-rule.svg width=300>

#### Distribution

- 以 backend instance group 或 network endpoint group 為單位
- [步驟](https://cloud.google.com/load-balancing/docs/https#request-distribution)
  1. Maglev
  2. 1st Google Front End
     - 2nd Google Front End 分配根據各個 region 的 load balancer 剩餘 capacity 比例
     - region load balancer 就不用選了
  3. 2nd Google Front End (知道 backend capacity usage)
  4. load balancer
     - balancing mode
  5. group
     - LocalityLbPolicy
- 三種 balancing mode
  1. connection
     - [表格](https://cloud.google.com/load-balancing/docs/backend-service#connection_balancing_mode)
     - concurrent connections the backend can handle
  2. rate
     - [表格](https://cloud.google.com/load-balancing/docs/backend-service#rate_balancing_mode)
     - 最大 RPS
  3. utilization
     - utilization of VMs
     - 會嘗試預估未來的 utilization
  - 無論哪種 balancing mode, 如果 backend 都滿了就會超過限制的值
- [各種 balancer 支援的 balancing mode 表](https://cloud.google.com/load-balancing/docs/backend-service#balancing-mode-combos)
- 如果用量太少, 會集中在一個 region
- 如果用量太多, 某些 group 會超過上限

### Signed URL

- 有存取限制 & 時間限制的 URL
- 例如: 臨時上傳 / 下載檔案

### 費用相關

- CDN 判斷 ip 所在地區跟 cloud armor, load balancer 的可能不一致
  - 不同步可能持續數周
  - subdivision 為空的似乎有問題
- `networking service` 只有 CDN
- `compute engine service` 含有 egress, load balancer
  - 要查網路流量不能只看 networking
  - load balancer 收費有上限

## Grafana

- `%` = regex 的 `*`

### query

- 例如
  - sum by (`label key`)(rate(`label name`{`filter key`=`value`,project_id="$project"}[1m]))
  - https://prometheus.io/docs/prometheus/latest/querying/examples

## Kubernetes

- https://docs.google.com/presentation/d/10mm4ugzDvG93e4xEe8KsenIEnN9VnDFcpH19zo93Ghw/edit#slide=id.p
- https://kubernetes.io/docs/tutorials/

### namespace

- 在一個 cluster 內分組 (group)
  - 避免不同 team, project 互相干擾
  - `resource quotas`: [限制各個 namespace 可用的資源](#限制資源)
    - 是用來管控 cpu, memory 這類資源
    - 盡量用 label 控管其他資源
- names of resources need to be unique within a namespace
- namespaced object vs cluster-wide object
  - `namespaced`: deployments, services, ...
    - 不能跨 namespace 共享
  - `cluster-wide`: storage class, nodes, persistent volumes, ...
- For a production cluster, consider not using the `default` namespace
  - [initial namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/#initial-namespaces)
    - default
    - kube-node-lease
    - kube-public
    - kube-system: addons
      - DNS, web ui, container resource monitoring, cluster level logging
  - kube-xxx 未來可能被 kubernetes 使用

### 組成

- https://kubernetes.io/docs/concepts/overview/components/
- control plane
  - 管理 cluster
  - 有 etcd
    - consistent & highly available key value store
    - Kubernetes' backing store for all cluster data
  - 有 kube-apiserver 的部份可以 scale horizontally
    - 大概 control plane 其他部份都支援 horizontally scaling ?
  - 其他
- node
  - vm 或實體電腦
  - worker in cluster
  - 有 kubelet
    - agent for managing the node
    - communicating with control plane
    - 確保 pod specs 標示的 containers 都有在 pod 內
  - 有 container runtime
  - 有 kube-proxy 讓 pod 能連網
- pod
  - [可以被其他的 pod 或 cluster 內的其他服務看到](https://kubernetes.io/docs/tutorials/kubernetes-basics/deploy-app/deploy-interactive/)
  - STDOUT 會變成 container 的 log

### kustomize

- https://kubernetes.io/docs/concepts/overview/working-with-objects/kubernetes-objects
  - apiVersion
    - Which version of the Kubernetes API you're using to create this object
  - kind
    - What kind of object you want to create
  - metadata
    - Data that helps uniquely identify the object, including a name string, UID, and optional namespace
  - spec
    - What state you desire for the object
    - https://kubernetes.io/docs/reference/kubernetes-api/
- 用 patch 而不用 replace 只會修改使用者動到的部份. 例如多人在 local 同時修改 & patch
  - 變複雜
  - 或許 replace 之前先 `kubectl diff -Rf {directory}`
  - 不能刪除, 不能修改 ?
- apply 前都先 diff 看看, 避免不預期的狀況. 例如 image tag 是舊的
- hpa 會定期覆蓋實際的 replica set 數量
  - HorizontalPodAutoscaler
  - kubectl delete hpa {name} ?

### kubectl

- 顯示 namespace 下面的所有東西
  ```shell
  kubectl api-resources --verbs=list --namespaced -o name | xargs -n 1 kubectl get --show-kind --ignore-not-found
  # 如果要過濾部份 `| grep -v -e pod/ -e replicaset/ -e deployment/`
  ```
  - kubectl get all 可能只會顯示 pod, service, deployment, replicaset

#### 砍 node 步驟

- `kubectl cordon {node name}`
  - 禁止在 node 新增 pod (unschedulable)
- `kubectl delete pod {pod name}`
- `kubectl get pods -o wide`
  - 確認至少一個 pod 搬到其他 node
- `kubectl drain {node name}`
  - mark node as unschedulable
  - 砍 mirror pods & DaemonSet pods 以外的 pods
- `kubectl describe nodes`
  - 確認 pods 搬到其他 node
- `kubectl delete node {node name}`

### 其他功能

- proxy
  - 可以用來連到 cluster 內部
- service

  - 管理如何連到 pods
  - type
    - cluster ip
      - 只有 cluster 內部可以連到
    - node port
      - 可以從外部連
      - `{node ip}:{node port}`
    - load balancer
      - 需要 kubernetes 運行的 cloud 支援
    - external name
      - 用 DNS 的 CNAME
  - 透過 label & selector
    - label
      - 標在 object 上
      - 可以動態修改
      - 例如: 標示環境, 版本, 歸類
  - [會產生 DNS record](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)

    - 靠 kubelet 修改 pod 的 `/etc/resolv.conf`
      - search `{namespace}.svc.{cluster domain name}` `svc.{cluster domain name}` `{cluster domain name}`
    - pod 預設可以用 domain name 連同一個 namespace & default namespace
    - 跨 namespace 可能需要 fully qualified domain name

      - `test` namespace 的 pod 要連 `prod` namespace `data` service 底下的資源 (都在 `cluster.local` 這組 cluster)

        | client 呼叫的 domain name    | 是否能連到 |
        | ---------------------------- | ---------- |
        | data                         | :x:        |
        | data.prod                    | :o:        |
        | data.prod.svc.cluster.local. | :o:        |

    - namespace 可能蓋掉 public top level domains
    - services & pods 有對應的 DNS records

- pods can communicate with all other pods on any other node without NAT
  - containers within a Pod must coordinate port usage
- deployment
  - 控制如何產生 & 更新
    - 控制 replica set
      - rolling update 時, 逐漸新增新的 replica set, 逐漸減少舊的 replica set
  - 查看狀態
  - 重新啟動
- kubernetes api
  - control plane 與 nodes 之間溝通
  - kubectl 也是使用 kubernetes api
    - `kubectl exec -it {pod name} -- bash` 可以連到 pod 裡面
    - `kubectl port-forward {pod name} port:port` port forward 到 local
- 設定環境變數
  - Dockerfile
  - kubernetes.yml
  - ConfigMaps
    - non-confidential key-value pairs
  - secrets
    - confidential key-value pairs
    - base64

#### GKE 額外支援 cluster level logs

- 新的 lifecycle
- 只支援 stdout, stderr
- node 要跑 fluentd
  - DaemonSet
  - 預設上傳 logs 到 cloud logging
  - 看設定
    - `kubectl -n {namespace} get daemonsets` 找名字
    - `kubectl describe ds {daemon set name}` 找 config map
    - `kubectl get -n {namespace} configmap {config map key} -o json | jq`
- 會特殊處理 `jsonPayload` 這個欄位
- <img src=https://cloud.google.com/static/logging/docs/images/routing-overview-17-09-21.png/>
  - https://cloud.google.com/logging/docs/routing/overview

### 限制資源

- [針對 namespace: Resource Quotas](https://kubernetes.io/docs/concepts/policy/resource-quotas/)
  - quota system 追蹤 namespace 用量
    - 只會檢查新建立的 resource
      - => 如果已經建立 resources 才改 quota 不影響既有 resources
  - 限制 cpu / memory 時, 每個 pod 都要標明 request 或 limit
    - 拒絕建立沒有標明的 pod
    - 可以用 LimitRanger 產生預設值
    - [可以限制的資源](https://kubernetes.io/docs/concepts/policy/resource-quotas/#compute-resource-quota)
  - 其他資源限制不用每個 pod 都標明
    - 不標明就無視限制
    - When using a CRI container runtime, container logs will count against the ephemeral storage quota
  - 只能設定固定值, 不能按照比例限制
- [針對 `contanier` 設定限制](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)
  - 確保 node 有 request 值以上的資源
  - 確保用量沒有超過 limit 值
    - 例如用 out of memory 阻止
    - runtime 實作者決定
  - cpu & memory
    - 沒填寫 request 會用 limit 值
    - cpu 以一個 core 為單位
      - 可以填小數點
      - 小於 1.0 建議以 m 為單位 (milliCPU)
      - 最小 0.001, 建議填成 1m
    - memory 以 byte 為單位
      - 十進位  
        | m | k | M | G | T | P | E |
        | ----- | ---- | ---- | ---- | ---- | ---- | --- |
        | milli | kilo | mega | giga | tera | peta | exa |
      - 二進位
        | Ki | Mi | Gi | Ti | Pi | Ei |
        | -------- | -------- | -------- | -------- | -------- | -------- |
        | kibibyte | mebibyte | gibibyte | tebibyte | pebibyte | exbibyte |
        - 1M, 1Mi, ...
    - linux
      - cpu limit
        - 定期檢查有沒有超時
        - 超時就暫時不給執行
      - cpu request
        - 較大的會搶贏
      - memory limit
        - process 要 memory 時, 檢查是否要觸發 out of memory
        - 可能只砍掉 1 個 process, 而非砍掉 container
        - 包含 pages in memory backed volumes (例如 emptyDir)
          - 而非直覺的 ephemeral storage limit
      - memory request
        - 超過 request & node memory 不夠, 會砍對應的 pod
  - ephemeral storage
    - container's writable layer / log usage 超過限制 `=>` pod eviction
    - pod 內所有 containers local ephemeral storage usage + pod's emptyDir 超過限制 `=>` pod eviction
    - [監控方式](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#resource-emphemeralstorage-consumption)
      - periodic scanning
        - 沒辦法追蹤已經刪除, 但是還被閱讀的檔案
      - filesystem project quota
        - operating-system level feature
        - 單純監控
        - 更快更準確
    - kubelet 有時可能沒有監測 ephemeral storage
      - 不會 evict pod
      - `writable container layers`, `node-level logs`, `emptyDir` 不夠時, node taints itself as short on local storage
        - evict pods that don't specifically tolerate the taint
  - pod request & limit = pod 內部 container request & limit 總和
  - 可能超過 total allocatable, 搶 reserved

### 切換 context

- `kubectl config ...`
  - https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/
- `gcloud container clusters get-credentials {CLUSTER_NAME} --project={PROJECT_ID} --region={COMPUTE_REGION}`
  - https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl

## Metrics, Monitor

- [metrics guide](https://www.digitalocean.com/community/tutorials/an-introduction-to-metrics-monitoring-and-alerting)
  - target
    - host: cpu, disk, ...
    - application
    - network
    - server pool
    - external dependency
  - 定期判斷哪些 metrics 重要
    - 節省開銷, 降低複雜度
    - early project 缺乏時間
  - 獨立
    - independent from most other infrastructure（降低對其他服務的影響）
    - reliability
    - dashboard UX
    - maintain historical data（簡化舊資料或丟進 long-term storage）
    - correlate factors from different sources（beware clock skew）
    - easy to adjust metrics
      - remove decommissioned machines without destroying collected data ?
    - alert
      - fine-tune alerting parameters
      - notify with existing applications（用現成的軟體簡化）
      - 持續一段時間才觸發, 避免 temporary spikes
- [counter](https://prometheus.io/docs/concepts/metric_types/#counter)
  - 紀錄次數
- [gauge](https://prometheus.io/docs/concepts/metric_types/#gauge)
  - 紀錄數值變化
- [histogram](https://prometheus.io/docs/concepts/metric_types/#histogram)
  - 紀錄分佈
  - ddsketch: dynamic buckets
- 避免 label value 太多變化
- 4 golden signals
  - latency
  - traffic
  - errors
  - saturation

### Logs

#### [Kubernetes](https://kubernetes.io/docs/concepts/cluster-administration/logging/)

- `kubectl logs -n {namespace} --all-containers=true -l {key}={value}`
  - https://github.com/johanhaleby/kubetail
- 不在 container 的 logs
  - kubelet, container runtime, ...
- in container
  1. container 內部程式 寫到 stdout, stderr
  2. container runtime 在 pod 外面寫 log
     - kubernetes 控制的
  3. kubelet 負責 rotate logs
     - container 重開會保留 log
     - pod 重開不會保留 log
- https://stackoverflow.com/questions/57565838/docker-how-the-json-file-driver-works
  - k8s + docker 要搭配 docker log driver: `json-file` (至少儲存位置要一樣)
    - `docker inspect {container}` 找 LogConfig
  - k8s 負責 rotate logs

#### VM

- 通常放在 `/var/log`
- mongo 可能放在 `/data`

### Prometheus

- run Prometheus scrapper using docker
  - run docker https://prometheus.io/docs/prometheus/latest/installation/#volumes-bind-mount
  - edit yaml https://prometheus.io/docs/prometheus/latest/getting_started/#configure-prometheus-to-monitor-the-sample-targets
- 會在 metrics name 結尾加上 `_bucket`, `_count`, `_sum`
  - https://prometheus.io/docs/concepts/metric_types/#histogram
  - https://github.com/prometheus/client_golang/blob/v1.16.0/prometheus/registry.go#L840
  - 可以用 `kubectl port-forward` 到 local, 然後 curl `localhost:9200/metrics` 確認 metrics

## Mongo

### Cloud Manager

- mongocli auth login
- mongocli config set 設定 api key
  - mongocli iam projects list 檢查有權限看哪些專案

---

- 如果曾經用 mongocli auth login 過  
  然後才設定 api key  
  等到 access token 過期（大概 refresh token 也過期了？）  
  就會卡在 Error: session expired
  - 如果想去 mongocli auth login  
     會卡在 Error: you are already authenticated with an API key
  1. 要先去 ~/.config/mongocli/config.toml 搶救 api key
     - https://www.mongodb.com/docs/mongocli/stable/configure/configuration-file/#configuration-file-location
  2. 然後 mongocli auth logout（會清空 config）
  3. 填回 api key

## Terraform

### type

- [string](https://developer.hashicorp.com/terraform/language/expressions/strings)
  - jsonencode, yamlencode
  - heredoc
    ```terraform
    <<-EOT
    ...content...
    EOT
    ```
    - EOT 可以換成任意字（EOT = end of text）
    - `<<` 不會 trim 每一行的 leading space
    - `<<-` 會 trim 每一行的 leading space
      - 根據所有行數中最短的 leading space, trim 每一行
    - 不支援 \X 格式的 escape
  - template
    - interpolation
      - ```terraform
        "Hello, ${var.name}!"
        ```
    - [directive](https://developer.hashicorp.com/terraform/language/expressions/strings#directives)
      - 支援條件 & 迴圈
      - if
        ```terraform
        "%{ if var.input }if result%{ else }else result%{ endif }"
        ```
        沒有 else if  
        替代方案:
        - ```terraform
          "Hello, ${var.input == "cond 1" ? "if result" : (var.input == "cond 2" ? "else if result" : "else result")}"
          ```
      - for loop
        ```terraform
        "%{ for name in local.input }Hello ${name}\n%{ endfor }"
        # or
        <<EOT
        %{ for name in local.input ~}
        Hello ${name}
        %{ endfor ~}
        EOT
        ```
        `~` 是用來去掉 heredoc + directive 產生的 newline
- number
- bool
- list: 每個 element `同` type
- tuple: 每個 element `不用同` type
- set
- map: key 為 string, 每個 value `同` type
- object
  - key 必須是 string
  - expression 當作 key 時, 用 `()` 包起來: `{(var.name) = "name"}`
  - key 需要先標明（沒有標明的不會用）
    - [可以標示 optional](https://developer.hashicorp.com/terraform/language/expressions/type-constraints#optional-object-type-attributes)
- null

### 常用指令

- `terraform show`
  - 可以顯示 state snapshot
  - 可以加上 -json
- `terraform output`
  - 可以顯示 output
  - 可以加上 -json
- `terraform state mv`
  - 純改名 or 純搬運位置
- auto complete
  - `terraform -install-autocomplete`
- [terraform fmt](https://marketplace.visualstudio.com/items?itemName=HashiCorp.terraform#formatting)
- `terraform apply -target {component}` 可以優先處理某個 component
  - apply 完成, 不代表 instance startup-script 也完成
  - 有時候要多次 apply 才會全部完成
    - 也許是順序問題 ?

### [keep track of real infrastructure in a state file](https://developer.hashicorp.com/terraform/tutorials/gcp-get-started/infrastructure-as-code#track-your-infrastructure)

- `terraform.tfstate`
- 含有機密資料
- 避免每次都查詢最新狀態
  - `-refresh=false` & `-target`
  - 避免 rate limit 之類的
  - 會直接把 tfstate 當作最新狀態
- 如果要解析 state (供後續處理), 可以另外儲存
  - 分開設定權限控管
  - 避免直接解析 state, 減少 terraform state 格式變動造成困擾
- [different version of cli might update state file (corruption)](https://developer.hashicorp.com/terraform/tutorials/cloud/cloud-migrate)

### `.terraform` 也可能有機密資料, 不要進 version control (例如 git)

### [分開設定機密資料的方法](https://developer.hashicorp.com/terraform/language/settings/backends/configuration#partial-configuration)

- backend [可以放在 `*.tfbackend`](https://developer.hashicorp.com/terraform/language/settings/backends/configuration#file)
  - 建議命名為 `*.{backend-type}.tfbackend`
  - [更換 backend 時, 先備份 terraform.tfstate 比較安全](https://developer.hashicorp.com/terraform/language/settings/backends/configuration#initialization)
  - 如果使用 remote backend & 沒有成功更新
    - [需要手動更新到 remote backend](https://developer.hashicorp.com/terraform/language/state/backends#manual-state-pull-push)
  - [force unlock](https://developer.hashicorp.com/terraform/language/state/locking#force-unlock)
- https://www.vaultproject.io/
- TerraformVariable can avoid secrets been written in cdktf.json https://developer.hashicorp.com/terraform/cdktf/create-and-deploy/best-practices#read-secrets-with-terraform-variables

### all `*.tf` files in a directory will be merged when applies Terraform

- root module can import other modules ([child modules](https://registry.terraform.io/browse/modules))
  - version
    - https://developer.hashicorp.com/terraform/language/modules/syntax#version
    - https://developer.hashicorp.com/terraform/language/modules/sources
    - child 只標示最低版本 & 排除明確不能用的版本
    - root 控制最終版本
    - [provider configurations are inherited by child modules](https://developer.hashicorp.com/terraform/language/modules/develop/providers#implicit-provider-inheritance)
      - not provider source
      - not version requirements
      - each module must declare its own provider requirements
- can use output values from one as input values of another
  - sensitive 可以避免資料洩漏到 cli
  - [如果 id 使用到 sensitive data, 仍然會洩漏](https://developer.hashicorp.com/terraform/language/values/variables#cases-where-terraform-may-disclose-a-sensitive-variable)
  - tfstate 會洩漏
- [分開設定機密資料的方法](#分開設定機密資料的方法)
- [混合人工與機器產生的檔案 (override)](https://developer.hashicorp.com/terraform/language/files/override)

### [Workspace](https://developer.hashicorp.com/terraform/language/state/workspaces)

- 用來以同一份設定管理不同組資源

### 變數

- locals 可以一次設定多個變數
- variable 可以手動輸入 or 環境變數輸入 or `terraform.tfvars` or `*.auto.tfvars`
  - https://developer.hashicorp.com/terraform/language/values/variables
  - 無視檔案裡面沒用到的變數: [-compact-warnings](https://developer.hashicorp.com/terraform/language/values/variables#values-for-undeclared-variables)
  - 可以設定檢查條件 `validation`
  - 優先度: 環境變數 < terraform.tfvars < terraform.tfvars.json < `*.auto.tfvars` or `*auto.tfvars.json`（字母順序） < -var or -var-file（前後順序）

### create, destroy, update in-place, re-create

- [Refactor](https://developer.hashicorp.com/terraform/language/modules/develop/refactoring) 需要特殊處理, 避免 terraform 另外產生新的 infrastructure 取代舊的 infrastructure
- [強制取代](https://developer.hashicorp.com/terraform/language/modules/syntax#replacing-resources-within-a-module)

### [example](https://developer.hashicorp.com/terraform/language)

```terraform
terraform {
  required_providers {
    # 可以自行命名, 簡單起見就用官方名稱
    google = {
      source  = "hashicorp/google"
      # ~> only update to newest patch version
      version = "~>3.5.0"
    }
  }
}

# 可以省略
# 要符合 required_providers 第一層定義的名稱
provider "google" {
  # 如果要在一個 module 裡面設定多個 providers, 可以用 alias
  # resource 裡面用 provider = google.alias 來指定
  # https://developer.hashicorp.com/terraform/language/providers/requirements#handling-local-name-conflicts
  alias = "alias"
  # 只能用事先可以決定值的 expression. 可以參考 count / for_each
}

# 第一個要符合 provider 裡面設定的 schema
# 預設 provider 為第一個的 prefix, 在此為 google
resource "google_compute_network" "{name}" {...}

# 根據依賴關係, 可能要 apply phase 才能取得 => 在 apply phase 才取得的無法用在 count / for_each 等地方
# 可以用 local 避開依賴: https://developer.hashicorp.com/terraform/language/data-sources#data-resource-dependencies
data "google_storage_bucket" "{name}" {...}
```

- expression
  - https://developer.hashicorp.com/terraform/language/expressions
  - "${variable}"
- meta-argument
  - [count](https://developer.hashicorp.com/terraform/language/meta-arguments/count)
    - 需要在操作 resource 之前決定好
    - [根據依賴關係, data resource 有可能也不能用](https://developer.hashicorp.com/terraform/language/data-sources#data-resource-behavior)
    - iterate
      - `type.name[*].attribute` [splat expression](#splat-expression)
      - `type.name[index].attribute`
      - `[for element in type.name: element.attribute]` [會建立 list](#terraform-for-expression)
  - [for_each](https://developer.hashicorp.com/terraform/language/meta-arguments/for_each)
    - keys 不能用 impure function
      - 需要在操作 resource 之前決定好
      - [根據依賴關係, data resource 有可能也不能用](https://developer.hashicorp.com/terraform/language/data-sources#data-resource-behavior)
        - [可以用 local 避開依賴關係](https://developer.hashicorp.com/terraform/language/data-sources#data-resource-dependencies)
    - chain for_each between resources
    - count 會因為刪減原本的 array 而被影響
    - for_each 要 map, set 有值的更動才會被影響
    - 會暴露值. 不能用在機密資訊
    - iterate
      - `values(type.name)[*].attribute` [splat expression 只適用於 list, tuple, set](#splat-expression)
      - `type.name["key"].attribute`
      - `[for value in type.name: value.attribute]` [會建立 list](#terraform-for-expression)
  - [lifecycle](https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle)
  - provider: 如果某服務有多種設定, 可以選擇用其中一個
  - depends_on: 強制等待其他 block 完成
    - 如果 block 有用到其他 block 就會自動等待, 所以平常不需要用這個降低效能
  - provisioner: 從 0 客製功能
    - （無直接關聯）自製 providers
      - https://developer.hashicorp.com/terraform/language/providers/requirements#in-house-providers
- [precondition & postcondition](https://developer.hashicorp.com/terraform/language/expressions/custom-conditions)
- `&&` & `||` 兩側都一定會跑: [no short-circuit](https://developer.hashicorp.com/terraform/language/expressions/operators#logical-operators)
- [functions](https://developer.hashicorp.com/terraform/language/functions)
  - `min([55, 2453, 2]...)` ... 拆開 list & tuple
  - [impure function 被實際呼叫的時機](https://developer.hashicorp.com/terraform/language/expressions/function-calls#when-terraform-calls-functions)
- [dynamic blocks](https://developer.hashicorp.com/terraform/language/expressions/dynamic-blocks)

### Terraform for expression

- 可以用於 list, set, tuple, map, object
- to tuple
  - `[for v in map: v]`
  - `[for k, v in map: "${k}: ${v}"]`
  - `[for v in list: v]`
  - `[for i, v in list: "${i} ${v}"]`
- to object
  - `{for i, v in list: i => v}`: `key` => `value`
  - 其他參考 to tuple
  - 多個 value 放在同一個 key 下
    - `{for name, user in var.users: user.role => name...}`
- 過濾
  - `[for s in list: s if s != ""]` 過濾空的 element
- 排序
  - set of strings 按照 value 排序
  - set of other types 隨機排序
  - map 按照 key 排序
  - object 按照 attribute 排序

### Splat expression

- 只適用於 list, tuple, set
- single value as list
  - null 會被轉成 empty tuple
  - 其他會轉成含一個 element 的 tuple
    ```terraform
    data "name" {
      for_each = var.settings[*] # var.settings 可以為 null, single object, ...
      ...
    }
    ```

## Ansible

- 同時操作多個 vm/docker image
  - AI 版本 [Project Wisdom](https://www.ithome.com.tw/news/153708)
- `pip install ansible`
- `ansible all -i {ip},{ip,...} -m {module} -a {arguments} --become --become-user={user}`
  - module: https://docs.ansible.com/ansible/latest/collections/index_module.html
  - arguments 可以是 `json` 或 `key=value`
  - `-i` 如果是接 ip 一定要有 `,`, 否則會被當作是 inventory
- `ansible-playbook -i {ip},{ip,...} {file_name}.yaml`
  - yaml demo
    ```yaml
    - name: Playbook name
      hosts: all
      tasks:
        - name: Task name
          ansible.builtin.copy:
            src: backup.sh
            dest: ~/backup.sh # put to tableau's $HOME instead of uploader's $HOME
          become: true
          become_user: tableau
    ```
- 如果用 become 切換到 unprivileged user, 可能需要在目標機器安裝 acl
  - [Install POSIX.1e filesystem acl](https://docs.ansible.com/archive/ansible/2.3/become.html)

## Misc

- Gnuplot 畫圖
- https://sre.google/books/

### 費用

- 花錢的主要原因
  - cpu
  - mem
  - disk
  - network
- app store & google play 可以去掉下載消耗的 CDN 費用

### 管理

- DB 需要 persistent disk, 如果用 k8s 需要特別處理
- `kubectl` 操作 k8s
- `kustomize`, `terraform` 管理 k8s/vm 設定
  - [autocomplete kustomize](https://github.com/kubernetes-sigs/kustomize/blob/be8d60fb9f2fff23b2e2367c0acd393997fa9d47/cmd/config/internal/generateddocs/commands/docs.go#L41)
- `mongo cloud manager` 管理 mongo 設定
