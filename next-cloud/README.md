# NextCloud
## 概要
k8s上でNextCloudを動かすためのマニフェスト

## メモ
DBはsqliteを使用する

初回起動時、/var/www/html/config/config.phpのtrusted_domainsを*に上書きする必要あり

上書き後、権限変更を忘れずに実施すること

kubectl exec -it <pod名> -- chown www-data:www-data /var/www/html/config/config.php

kubectl exec -it <pod名> -- chmod 777 /var/www/html/config/config.php
