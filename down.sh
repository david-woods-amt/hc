scp -r root@atom:/root/hc/scripts /cygdrive/c/hc-download

scp -r root@atom:/var/www/cgi-bin /cygdrive/c/hc-download/web
scp -r root@atom:/var/www/html /cygdrive/c/hc-download/web


scp root@atom:/etc/httpd/conf/httpd.conf /cygdrive/c/hc-download/etc/httpd.conf

scp root@atom:/lib/systemd/system/hc.service /cygdrive/c/hc-download/usr/hc.service