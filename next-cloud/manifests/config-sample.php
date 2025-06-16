<?php
$CONFIG = array (
  'htaccess.RewriteBase' => '/',
  'memcache.local' => '\\OC\\Memcache\\APCu',
  'apps_paths' => 
  array (
    0 => 
    array (
      'path' => '/var/www/html/apps',
      'url' => '/apps',
      'writable' => false,
    ),
    1 => 
    array (
      'path' => '/var/www/html/custom_apps',
      'url' => '/custom_apps',
      'writable' => true,
    ),
  ),
  'upgrade.disable-web' => true,
  'instanceid' => 'oc4y6lfid4gk',
  'passwordsalt' => 'yjqDQO4vG18/ETvWVKLiKFOSz1wwD2',
  'secret' => 'KL4mKhGzgseKWaQrAx21PvXlscyP5sBbokpL1vDVMf53TE9c',
  'trusted_domains' => 
  array (
    0 => '*',
  ),
  'datadirectory' => '/var/www/html/data',
  'dbtype' => 'sqlite3',
  'version' => '31.0.6.2',
  'overwrite.cli.url' => 'http://localhost:32162',
  'installed' => true,
);
