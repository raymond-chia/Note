- connection reset by peer
  - server close session & client send request
  - [CDN & Load Balancer timeout](https://medium.com/starbugs/%E8%AC%8E%E4%B9%8B%E8%81%B2%E5%B0%8D-connection-%E8%AA%AA%E9%81%93-%E4%BD%A0%E5%B7%B2%E7%B6%93%E6%AD%BB%E4%BA%86-b53d27c7ecb7#77a6)
  - [Google load balancer restarts periodically](https://cloud.google.com/load-balancing/docs/https#timeouts_and_retries)
  - https://blog.percy.io/tuning-nginx-behind-google-cloud-platform-http-s-load-balancer-305982ddb340#3b71

- Install docker on mac
  - [Use docker-machine + virtualbox](https://stackoverflow.com/questions/44084846/cannot-connect-to-the-docker-daemon-on-macos#answer-49719638)
  - [Set ip address used by docker-machine in virtualbox](https://stackoverflow.com/questions/69805077/cannot-start-docker-daemon-at-macbook#answer-70373434)
  - [The ip of virtualbox](https://superuser.com/questions/310697/connect-to-the-host-machine-from-a-virtualbox-guest-os#answer-310745)
    1. `brew install docker-machine docker`
    2. `brew install --cask virtualbox`
    3. `docker-machine create -d virtualbox --virtualbox-hostonly-cidr "192.168.63.1/24" default` // (use `docker-machine rm default` if needed)
    4. `eval "$(docker-machine env default)"`
    5. `netstat -rn` on mac/linux host
    6. search for Netif == vboxnet
