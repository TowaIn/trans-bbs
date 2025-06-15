# trans-bbs
## 概要
書き込みログイン必須の掲示板

## buildコマンド

docker build -f deploy/Dockerfile -t trans-bbs:v2 .

microk8sのローカルレジストリであるlocalhost:32000に対してpushし使用する
