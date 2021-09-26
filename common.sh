# -*- coding: utf-8 -*-

TMPDIR="$(mktemp -d --suffix .vlc-radio)"
playlist=${TMPDIR}/radio.m3u8
cache_prefix="./.__cache__."

export http_user_gent="Mozilla/5.0 (X11; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"

trap "trap - SIGTERM && /bin/rm -rf ${TMPDIR} ; kill -- -$$" SIGINT SIGTERM EXIT

function make_playlist() {
    local playlist_valname="$1"
    local m3u8_name="$2"
    local makecmd="$3"
    local cache_file="${cache_prefix}_${m3u8_name}"

    eval "export ${playlist_valname}=${TMPDIR}/${m3u8_name}"

    if [ -e "${cache_file}" ] ; then
        cp -av "${cache_file}" "${TMPDIR}/${m3u8_name}"
    else
        ${makecmd}
        if [ "$?" = 0 ]; then
            cp -av "${TMPDIR}/${m3u8_name}" "${cache_file}"
        else
            eval "${playlist_valname}="
        fi
    fi
}

make_playlist "nhk_playlist" "nhk.m3u8" "./nhk_playlist.py"
make_playlist "listenradio_playlist" "listenradio.m3u8" "./listenradio_playlist.py"
make_playlist "jcba_playlist" "jcba.m3u8" "./jcba_playlist.py"
make_playlist "csra_playlist" "csra.m3u8" "./csra_playlist.py"

make_playlist "radiko_playlist" "radiko.m3u8" "./radiko_playlist.py"
if [ -n "${radiko_playlist}" ]; then
#    export radiko_check_host="radiko.jp"
#    export radiko_check_path="/v2/api/ts/playlist.m3u8?station_id="
    export radiko_check_host="f-radiko.smartstream.ne.jp"
    export radiko_check_path="/_definst_/simul-stream.stream/"
    export radiko_reusekey_interval=$((15 * 60))

    export radiko_auth_helper="./radiko_auth.py"
    export radiko_auth_key="./radiko_key.txt"
    export radiko_user_agent_file="${TMPDIR}/radiko_header_useragent.txt"
    export radiko_auth_header_file="${TMPDIR}/radiko_header_token.txt"
fi

make_playlist "dabp_au_playlist" "dabp_au.m3u8" "./dabp_au_playlist.py"

#
podcast_playlist=${TMPDIR}/podcast.m3u8
cat > "${podcast_playlist}" <<__EOF__
#EXTM3U
# -*- coding: utf-8 -*-

#EXTINF:0,NHKラジオニュース
https://www.nhk.or.jp/r-news/podcast/nhkradionews.xml

#EXTINF:-1,*** REBOOT VLC ***
http://reboot.reboot/reboot

#EXTINF:-1,*** EXIT VLC ***
http://exit.exit/exit

#EXTINF:0,SUNTORY SATURDAY WAITING BAR AVANTI
https://www.tfm.co.jp/podcasts/avanti/podcast.xml
__EOF__

#
{
    echo '#EXTM3U'
    echo '# -*- coding: utf-8 -*-'
    echo ''

    if [ -e ./okini.m3u8 ]; then
        echo '#EXTINF:-1,おきに'
        echo "${PWD}/okini.m3u8"
        echo ''
    fi

    if [ -n "${nhk_playlist}" ]; then
        echo '#EXTINF:-1,NHK'
        echo "${nhk_playlist}"
        echo ''
    fi

    if [ -n "${radiko_playlist}" ]; then
        echo '#EXTINF:-1,radiko'
        echo "${radiko_playlist}"
        echo ''
    fi

    if [ -n "${listenradio_playlist}" ]; then
        echo '#EXTINF:-1,ListenRadio'
        echo "${listenradio_playlist}"
        echo ''
    fi

    if [ -n "${jcba_playlist}" ]; then
        echo '#EXTINF:-1,JCBA'
        echo "${jcba_playlist}"
        echo ''
    fi

    if [ -n "${csra_playlist}" ]; then
        echo '#EXTINF:-1,CSRA'
        echo "${csra_playlist}"
        echo ''
    fi

    if [ -n "${dabp_au_playlist}" ]; then
        echo '#EXTINF:-1,DAB+AU'
        echo "${dabp_au_playlist}"
        echo ''
    fi

    echo '#EXTINF:-1,podcast'
    echo "${podcast_playlist}"
    echo ''

    echo '#EXTINF:-1,BBC'
    echo "${PWD}/bbc.m3u8"
    echo '#EXTINF:-1,AFN'
    echo "${PWD}/afn.m3u8"
    echo '#EXTINF:-1,北欧系'
    echo "${PWD}/nordic.m3u8"
    echo '#EXTINF:-1,香港'
    echo "${PWD}/hk.m3u8"
    echo '#EXTINF:-1,manual'
    echo "${PWD}/manual.m3u8"

    echo '#EXTINF:-1,pimoroni Pirate Radio default PL'
    echo 'https://github.com/pimoroni/phat-beat/raw/master/projects/vlc-radio/vlcd/etc/vlcd/default.m3u'
    echo ''

} > "${playlist}"


