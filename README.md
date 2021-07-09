# vlc-radio for Pirate Radio project

## build VLC media player
- build on the Raspberry Pi Zero WH.

```
 $ sudo apt-get build-dep vlc
 $ sudo apt-get install python3-bs4

 $ git clone https://github.com/hidetan/vlc-radio.git

 $ cd vlc-radio
 $ wget http://get.videolan.org/vlc/3.0.16/vlc-3.0.16.tar.xz

 $ tar xf ./vlc-3.0.16.tar.xz
 $ cd vlc-3.0.16/

 $ patch -p2 -b < ../vlc-3.0.16_radiko.patch
 $ patch -p2 -b < ../vlc-3.0.16_retrytls.patch
 $ patch -p2 -b < ../vlc-3.0.16_webui_expand.patch
 $ patch -p2 -b < ../vlc-3.0.16_webui_title.patch

 $ time ./bootstrap
 about 10 minitues.

 $ mkdir ./build
 $ cd ./build
 $ time ../configure --prefix=/opt/vlc-3.0.16
 about 7 minitues.

 $ time make
 about 5 hours. :-P

```

## prepare key file

```
 $ cd vlc-radio
 $ wget -O radiko_key.txt https://raw.githubusercontent.com/jackyzy823/rajiko/master/background.js
```

## run vlc

```
 $ cd vlc-radio
 $ ./test.sh
```

