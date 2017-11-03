scp /cygdrive/c/git/hc/scripts/control.py root@atom:/root/hc/scripts/control.py
scp -r /cygdrive/c/git/hc/scripts/common root@atom:/root/hc/scripts

scp -r /cygdrive/c/git/hc/web/html root@atom:/var/www
scp -r /cygdrive/c/git/hc/web/cgi-bin/main.cgi root@atom:/var/www/cgi-bin/main.cgi
scp -r /cygdrive/c/git/hc/web/cgi-bin/post.cgi root@atom:/var/www/cgi-bin/post.cgi

#scp root@atom:/etc/httpd/conf/httpd.conf /cygdrive/c/hc-download/etc/httpd.conf
#scp root@atom:/lib/systemd/system/hc.service /cygdrive/c/hc-download/usr/hc.service