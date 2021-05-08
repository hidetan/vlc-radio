# vlc-radio for Pirate Radio project

## build VLC media player
- build on the Raspberry Pi Zero WH.

```
 $ sudo apt-get build-dep vlc
 $ sudo apt-get install python3-bs4

 $ wget http://get.videolan.org/vlc/3.0.12/vlc-3.0.12.tar.xz

 $ tar xf ./vlc-3.0.12.tar.xz
 $ cd vlc-3.0.12/

 $ patch -p2 -b < ../vlc-3.0.12_radiko.patch
 $ patch -p2 -b < ../vlc-3.0.12_retrytls.patch
 $ patch -p2 -b < ../vlc-3.0.12_webui_expand.patch
 $ patch -p2 -b < ../vlc-3.0.12_webui_title.patch

 $ time ./bootstrap
 about 10 minitues.

 $ mkdir ./build
 $ cd ./build
 $ time ../configure --prefix=/opt/vlc-3.0.12
 about 7 minitues.

 $ time make
 about 5 hours. :-P

# $ sudo make install
```

## prepare key file

```
 $ wget -O radiko_key.txt https://raw.githubusercontent.com/jackyzy823/rajiko/master/background.js
```

## run vlc

```
 $ ./test.sh
```

