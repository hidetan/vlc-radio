# vlc-radio for Pirate Radio project

## build VLC media player
- build on the Raspberry Pi Zero WH.

```
 $ sudo apt-get build-dep vlc
 $ sudo apt-get install python3-bs4

 $ git clone https://github.com/hidetan/vlc-radio.git

 $ cd vlc-radio
 $ wget https://get.videolan.org/vlc/3.0.18/vlc-3.0.18.tar.xz

 $ tar xf ./vlc-3.0.18.tar.xz
 $ cd vlc-3.0.18

 $ patch -p2 -b < ../vlc-3.0.16_radiko.patch
 $ patch -p2 -b < ../vlc-3.0.16_retry_tls.patch
 $ patch -p2 -b < ../vlc-3.0.16_webui_expand.patch
 $ patch -p2 -b < ../vlc-3.0.16_webui_title.patch
 $ patch -p2 -b < ../vlc-3.0.16_force_exit.patch
 $ patch -p2 -b < ../vlc-3.0.18_vlc-3.0.18_dump_statistics.patch

 $ wget https://code.videolan.org/videolan/vlc/-/raw/master/share/lua/playlist/youtube.lua
 $ mv ./share/lua/playlist/youtube.lua ./share/lua/playlist/youtube.lua.bak
 $ mv ./youtube.lua ./share/lua/playlist/youtube.lua

 $ time ./bootstrap
 about 10 minitues.

 $ mkdir ./build
 $ cd ./build
 $ time ../configure --prefix=/opt/vlc-3.0.18
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

