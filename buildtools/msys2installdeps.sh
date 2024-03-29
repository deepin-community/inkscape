#!/usr/bin/env bash
# -------------------------------------------------------------------------------
# This script installs all dependencies required for building Inkscape with MSYS2
#   execute it once on an MSYS shell, i.e.
#    - use the "MSYS2 MSYS" shortcut in the start menu or
#    - run "msys2.exe" in MSYS2's installation folder
#
# MSYS2 and installed libraries can be updated later by executing
#   pacman -Syu
# in an MSYS shell
# -------------------------------------------------------------------------------

# select if you want to build 32-bit (i686), 64-bit (x86_64), or both
case "$MSYSTEM" in
  MINGW32)
    ARCH=mingw-w64-i686
    ;;
  MINGW64)
    ARCH=mingw-w64-x86_64
    ;;
  *)
    ARCH={mingw-w64-i686,mingw-w64-x86_64}
    ;;
esac

# set default options for invoking pacman (in CI this variable is already set globally)
if [ -z $CI ]; then
    PACMAN_OPTIONS="--needed --noconfirm"
fi

# sync package databases
pacman -Sy

# install basic development system, compiler toolchain and build tools
eval pacman -S $PACMAN_OPTIONS \
git \
base-devel \
$ARCH-toolchain \
$ARCH-autotools \
$ARCH-cmake \
$ARCH-meson \
$ARCH-ninja

# install Inkscape dependencies (required)
eval pacman -S $PACMAN_OPTIONS \
$ARCH-double-conversion \
$ARCH-gc \
$ARCH-gsl \
$ARCH-libxslt \
$ARCH-boost \
$ARCH-gtk3 \
$ARCH-gtk-doc \
$ARCH-gtkmm3 \
$ARCH-libsoup

# install Inkscape dependencies (optional)
eval pacman -S $PACMAN_OPTIONS \
$ARCH-poppler \
$ARCH-potrace \
$ARCH-libcdr \
$ARCH-libvisio \
$ARCH-libwpg \
$ARCH-aspell \
$ARCH-aspell-en \
$ARCH-gspell \
$ARCH-graphicsmagick \
$ARCH-libjxl

# install Python and modules used by Inkscape
eval pacman -S $PACMAN_OPTIONS \
$ARCH-python \
$ARCH-python-pip \
$ARCH-python-lxml \
$ARCH-python-numpy \
$ARCH-python-cssselect \
$ARCH-python-pillow \
$ARCH-python-six \
$ARCH-python-gobject \
$ARCH-python-pyserial \
$ARCH-python-coverage \
$ARCH-python-packaging \
$ARCH-scour

# install modules needed by extensions manager and clipart importer
eval pacman -S $PACMAN_OPTIONS \
$ARCH-python-appdirs \
$ARCH-python-beautifulsoup4 \
$ARCH-python-filelock \
$ARCH-python-msgpack \
$ARCH-python-lockfile \
$ARCH-python-cachecontrol \
$ARCH-python-idna \
$ARCH-python-urllib3 \
$ARCH-python-chardet \
$ARCH-python-certifi \
$ARCH-python-requests

# install Python modules not provided as MSYS2/MinGW packages
PACKAGES=""
for arch in $(eval echo $ARCH); do
  case ${arch} in
    mingw-w64-i686)
      #/mingw32/bin/pip3 install --upgrade ${PACKAGES}
      ;;
    mingw-w64-x86_64)
      #/mingw64/bin/pip3 install --upgrade ${PACKAGES}
      ;;
  esac
done


# gettext hack - to remove once gettext has the match
function hack_libintl(){
f=/$1/include/libintl.h
sed -i '/^extern int sprintf/a #ifdef __cplusplus\nnamespace std { using ::libintl_sprintf; }\n#endif' $f
cat $f
}

case "$MSYSTEM" in
  MINGW32)
    hack_libintl mingw32
    ;;
  MINGW64)
    hack_libintl mingw64
    ;;
  *)
    hack_libintl mingw32
    hack_libintl mingw64
    ;;
esac
