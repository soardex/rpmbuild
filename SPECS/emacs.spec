%undefine _hardened_build
# This file is encoded in UTF-8.  -*- coding: utf-8 -*-
Summary:        GNU Emacs text editor
Name:           emacs
Epoch:          1
Version:        25.1
Release:        18%{?dist}
License:        GPLv3+
URL:            http://www.gnu.org/software/emacs/
Group:          Applications/Editors
Source0:        ftp://ftp.gnu.org/gnu/emacs/emacs-%{version}.tar.xz
Source1:        emacs.desktop
Source2:        emacsclient.desktop
Source3:        dotemacs.el
Source4:        site-start.el
Source5:        default.el
# Emacs Terminal Mode, #551949, #617355
Source6:        emacs-terminal.desktop
Source7:        emacs-terminal.sh

BuildRequires:  atk-devel cairo-devel freetype-devel fontconfig-devel dbus-devel giflib-devel glibc-devel libpng-devel
BuildRequires:  libjpeg-devel libtiff-devel libX11-devel libXau-devel libXdmcp-devel libXrender-devel libXt-devel
BuildRequires:  libXpm-devel ncurses-devel xorg-x11-proto-devel zlib-devel gnutls-devel
BuildRequires:  librsvg2-devel m17n-lib-devel libotf-devel ImageMagick-devel libselinux-devel
BuildRequires:  GConf2-devel alsa-lib-devel gpm-devel liblockfile-devel libxml2-devel
BuildRequires:  bzip2 cairo texinfo gzip desktop-file-utils
%if 0%{?rhel} == 6
BuildRequires:  gtk2-devel
%else
%if 0%{?rhel} == 7
BuildRequires:  gtk3-devel
BuildRequires:  python2-devel 
# Buildrequire both python2 and python3 on systems containing both,
# since below we turn off the brp-python-bytecompile script
%else
BuildRequires:  gtk3-devel
BuildRequires:  python2-devel
BuildRequires:  python3-devel
%endif
%endif

%ifarch %{ix86}
BuildRequires:  util-linux
%endif

# Emacs doesn't run without dejavu-sans-mono-fonts, rhbz#732422
Requires:       desktop-file-utils dejavu-sans-mono-fonts
Requires(preun): %{_sbindir}/alternatives
Requires(posttrans): %{_sbindir}/alternatives
Requires:       emacs-common = %{epoch}:%{version}-%{release}
Provides:       emacs(bin) = %{epoch}:%{version}-%{release}

%if 0%{!?rhel:1}
# Turn off the brp-python-bytecompile script since this script doesn't
# properly dtect the correct python runtime for the files emacs2.py and
# emacs3.py
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%endif

%define paranoid 1
%if 0%{?fedora}
%define expurgate 0
%else
%define expurgate 1
%endif

%define site_lisp %{_datadir}/emacs/site-lisp
%define site_start_d %{site_lisp}/site-start.d
%define bytecompargs -batch --no-init-file --no-site-file -f batch-byte-compile
%define pkgconfig %{_datadir}/pkgconfig
%define emacs_libexecdir %{_libexecdir}/emacs/%{version}/%{_host}

%description
Emacs is a powerful, customizable, self-documenting, modeless text
editor. Emacs contains special code editing features, a scripting
language (elisp), and the capability to read mail, news, and more
without leaving the editor.

This package provides an emacs binary with support for X windows.

%package nox
Summary: GNU Emacs text editor without X support
Group:   Applications/Editors
Requires(preun): %{_sbindir}/alternatives
Requires(posttrans): %{_sbindir}/alternatives
Requires: emacs-common = %{epoch}:%{version}-%{release}
Provides: emacs(bin) = %{epoch}:%{version}-%{release}

%description nox
Emacs is a powerful, customizable, self-documenting, modeless text
editor. Emacs contains special code editing features, a scripting
language (elisp), and the capability to read mail, news, and more
without leaving the editor.

This package provides an emacs binary with no X windows support for running
on a terminal.

%package common
Summary: Emacs common files
# The entire source code is GPLv3+ except lib-src/etags.c which is
# also BSD.  Manual (info) is GFDL.
License: GPLv3+ and GFDL and BSD
Group: Applications/Editors
Requires(preun): /sbin/install-info
Requires(preun): %{_sbindir}/alternatives
Requires(posttrans): %{_sbindir}/alternatives
Requires(post): /sbin/install-info
Requires: %{name}-filesystem

%description common
Emacs is a powerful, customizable, self-documenting, modeless text
editor. Emacs contains special code editing features, a scripting
language (elisp), and the capability to read mail, news, and more
without leaving the editor.

This package contains all the common files needed by emacs or emacs-nox.

%package el
Summary: Lisp source files included with GNU Emacs
Group: Applications/Editors
Requires: %{name}-filesystem
BuildArch: noarch

%description el
Emacs-el contains the emacs-elisp sources for many of the elisp
programs included with the main Emacs text editor package.

You need to install emacs-el only if you intend to modify any of the
Emacs packages or see some elisp examples.

%package terminal
Summary: A desktop menu item for GNU Emacs terminal.
Group: Applications/Editors
Requires: emacs = %{epoch}:%{version}-%{release}
BuildArch: noarch

%description terminal
Contains a desktop menu item running GNU Emacs terminal. Install
emacs-terminal if you need a terminal with Malayalam support.

Please note that emacs-terminal is a temporary package and it will be
removed when another terminal becomes capable of handling Malayalam.

%package filesystem
Summary: Emacs filesystem layout
Group: Applications/Editors
BuildArch: noarch

%description filesystem
This package provides some directories which are required by other
packages that add functionality to Emacs.

%prep
%setup -q

if test configure.ac -nt aclocal.m4 -o m4/gnulib-comp.m4 -nt aclocal.m4 ; then
    sleep 1
    touch aclocal.m4
fi
if test configure.ac -nt configure -o aclocal.m4 -nt configure ; then
    sleep 1
    touch configure
fi
if test configure.ac -nt src/stamp-h.in -o aclocal.m4 -nt src/stamp-h.in ; then
    sleep 1
    touch src/stamp-h.in
fi
if test aclocal.m4 -nt lib/Makefile.in -o lib/Makefile.am -nt lib/Makefile.in -o lib/gnulib.mk -nt lib/Makefile.in ; then
    sleep 1
    touch lib/Makefile.in
fi
if test -s autogen.sh ; then
    mv autogen.sh autogen.sh.no
    ln -sf /bin/true autogen.sh
fi

# We prefer our emacs.desktop file
cp %SOURCE1 etc/emacs.desktop

grep -v "tetris.elc" lisp/Makefile.in > lisp/Makefile.in.new \
   && mv lisp/Makefile.in.new lisp/Makefile.in

# Avoid trademark issues
%if %{paranoid}
rm -f lisp/play/tetris.el lisp/play/tetris.elc
%endif

%if %{expurgate}
rm -f etc/sex.6 etc/condom.1 etc/celibacy.1 etc/COOKIES etc/future-bug etc/JOKES
%endif

info_files="ada-mode auth autotype bovine calc ccmode cl dbus dired-x ebrowse ede ediff edt efaq-w32 efaq  eieio eintr elisp emacs-gnutls emacs-mime emacs epa erc ert eshell eudc eww flymake forms gnus htmlfontify idlwave ido info mairix-el message mh-e newsticker nxml-mode octave-mode org pcl-cvs pgg rcirc reftex remember sasl sc semantic ses sieve smtpmail speedbar srecode todo-mode tramp url vhdl-mode vip viper widget wisent woman"

cd info
for f in $(ls -1  *.info); do
  f=`echo $f | sed 's/\.info//g'`
  if [ ! -z "${info_files##*$f*}" ] ;then
      echo Please update info_files. $f is missing.>&2
      exit 1
  fi
done
cd ..

%ifarch %{ix86}
%define setarch setarch %{_arch} -R
%else
%define setarch %{nil}
%endif

# Avoid duplicating doc files in the common subpackage
ln -s ../../%{name}/%{version}/etc/COPYING doc
ln -s ../../%{name}/%{version}/etc/NEWS doc

%build
# don't compile with -O2 on arm, it can lead to segfault
%ifarch aarch64
export CFLAGS="-DMAIL_USE_LOCKF $RPM_OPT_FLAGS -O0"
%else
export CFLAGS="-DMAIL_USE_LOCKF $RPM_OPT_FLAGS"
%endif

%if 0%{?rhel} == 6
%define toolkit gtk
%else
%define toolkit gtk3
%endif

%configure --with-dbus --with-gif --with-jpeg --with-png --with-rsvg \
           --with-tiff --with-xft --with-xpm --with-x-toolkit=%{toolkit} --with-gpm=no
make bootstrap
%{setarch} make %{?_smp_mflags}
cp src/emacs emacs-gtk
make distclean

%configure --with-x=no
%{setarch} make %{?_smp_mflags}
cp src/emacs emacs-nox

# Create pkgconfig file
cat > emacs.pc << EOF
sitepkglispdir=%{site_lisp}
sitestartdir=%{site_start_d}

Name: emacs
Description: GNU Emacs text editor
Version: %{epoch}:%{version}
EOF

# Create macros.emacs RPM macro file
cat > macros.emacs << EOF
%%_emacs_version %{version}
%%_emacs_ev %{?epoch:%{epoch}:}%{version}
%%_emacs_evr %{?epoch:%{epoch}:}%{version}-%{release}
%%_emacs_sitelispdir %{site_lisp}
%%_emacs_sitestartdir %{site_start_d}
%%_emacs_bytecompile /usr/bin/emacs -batch --no-init-file --no-site-file --eval '(progn (setq load-path (cons "." load-path)))' -f batch-byte-compile
EOF

%install
make install INSTALL="%{__install} -p" DESTDIR=%{buildroot}

# Let alternatives manage the symlink
rm %{buildroot}%{_bindir}/emacs
touch %{buildroot}%{_bindir}/emacs

# Do not compress the files which implement compression itself (#484830)
gunzip %{buildroot}%{_datadir}/emacs/%{version}/lisp/jka-compr.el.gz
gunzip %{buildroot}%{_datadir}/emacs/%{version}/lisp/jka-cmpr-hook.el.gz

# Install the emacs with GTK support
install -p -m 1755 emacs-gtk %{buildroot}%{_bindir}/emacs-%{version}

# Install the emacs without X
install -p -m 0755 emacs-nox %{buildroot}%{_bindir}/emacs-%{version}-nox

# Make sure movemail isn't setgid
chmod 755 %{buildroot}%{emacs_libexecdir}/movemail

mkdir -p %{buildroot}%{site_lisp}
install -p -m 0644 %SOURCE4 %{buildroot}%{site_lisp}/site-start.el
install -p -m 0644 %SOURCE5 %{buildroot}%{site_lisp}

# This solves bz#474958, "update-directory-autoloads" now finally
# works the path is different each version, so we'll generate it here
echo "(setq source-directory \"%{_datadir}/emacs/%{version}/\")" \
 >> %{buildroot}%{site_lisp}/site-start.el

mv %{buildroot}%{_bindir}/{etags,etags.emacs}
mv %{buildroot}%{_mandir}/man1/{ctags.1.gz,gctags.1.gz}
mv %{buildroot}%{_mandir}/man1/{etags.1.gz,etags.emacs.1.gz}
mv %{buildroot}%{_bindir}/{ctags,gctags}
# BZ 927996
mv %{buildroot}%{_infodir}/{info.info.gz,info.gz}

mkdir -p %{buildroot}%{site_lisp}/site-start.d

# Default initialization file
mkdir -p %{buildroot}%{_sysconfdir}/skel
install -p -m 0644 %SOURCE3 %{buildroot}%{_sysconfdir}/skel/.emacs

# Install pkgconfig file
mkdir -p %{buildroot}/%{pkgconfig}
install -p -m 0644 emacs.pc %{buildroot}/%{pkgconfig}

# Install emacsclient desktop file
install -p -m 0644 %SOURCE2 %{buildroot}/%{_datadir}/applications/emacsclient.desktop

# Install rpm macro definition file
mkdir -p %{buildroot}%{_sysconfdir}/rpm
install -p -m 0644 macros.emacs %{buildroot}%{_sysconfdir}/rpm/

# Installing emacs-terminal binary
install -p -m 755 %SOURCE7 %{buildroot}%{_bindir}/emacs-terminal

# After everything is installed, remove info dir
rm -f %{buildroot}%{_infodir}/dir
rm %{buildroot}%{_localstatedir}/games/emacs/*

# Install desktop files
mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install --dir=%{buildroot}%{_datadir}/applications \
                     %SOURCE1
desktop-file-install --dir=%{buildroot}%{_datadir}/applications \
                     %SOURCE6

# Byte compile emacs*.py with correct python interpreters
%if 0%{?rhel:1}
rm -f %{buildroot}%{_datadir}/%{name}/%{version}/etc/emacs3.py
%else
%py_byte_compile %{__python} %{buildroot}%{_datadir}/%{name}/%{version}/etc/emacs.py
%py_byte_compile %{__python} %{buildroot}%{_datadir}/%{name}/%{version}/etc/emacs2.py
%py_byte_compile %{__python3} %{buildroot}%{_datadir}/%{name}/%{version}/etc/emacs3.py
%endif

#
# Create file lists
#
rm -f *-filelist {common,el}-*-files

( TOPDIR=${PWD}
  cd %{buildroot}

  find .%{_datadir}/emacs/%{version}/lisp \
    .%{_datadir}/emacs/site-lisp \( -type f -name '*.elc' -fprint $TOPDIR/common-lisp-none-elc-files \) -o \( -type d -fprintf $TOPDIR/common-lisp-dir-files "%%%%dir %%p\n" \) -o \( -name '*.el.gz' -fprint $TOPDIR/el-bytecomped-files -o -fprint $TOPDIR/common-not-comped-files \)

)

# Put the lists together after filtering  ./usr to /usr
sed -i -e "s|\.%{_prefix}|%{_prefix}|" *-files
cat common-*-files > common-filelist
cat el-*-files common-lisp-dir-files > el-filelist

%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%preun
%{_sbindir}/alternatives --remove emacs %{_bindir}/emacs-%{version}

%postun
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ] ; then
  %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor || :
fi

%posttrans
%{_sbindir}/alternatives --install %{_bindir}/emacs emacs %{_bindir}/emacs-%{version} 80

%preun nox
%{_sbindir}/alternatives --remove emacs %{_bindir}/emacs-%{version}-nox

%posttrans nox
%{_sbindir}/alternatives --install %{_bindir}/emacs emacs %{_bindir}/emacs-%{version}-nox 70

%post common
for f in %{info_files}; do
  /sbin/install-info %{_infodir}/$f.info.gz %{_infodir}/dir 2> /dev/null || :
done

%preun common
%{_sbindir}/alternatives --remove emacs.etags %{_bindir}/etags.emacs
if [ "$1" = 0 ]; then
  for f in %{info_files}; do
    /sbin/install-info --delete %{_infodir}/$f.info.gz %{_infodir}/dir 2> /dev/null || :
  done
fi

%posttrans common
%{_sbindir}/alternatives --install %{_bindir}/etags emacs.etags %{_bindir}/etags.emacs 80 \
       --slave %{_mandir}/man1/etags.1.gz emacs.etags.man %{_mandir}/man1/etags.emacs.1.gz

%post terminal
update-desktop-database &> /dev/null || :

%postun terminal
update-desktop-database &> /dev/null || :

%files
%{_bindir}/emacs-%{version}
%attr(0755,-,-) %ghost %{_bindir}/emacs
%{_datadir}/appdata/emacs.appdata.xml
%{_datadir}/applications/emacs.desktop
%{_datadir}/applications/emacsclient.desktop
%{_datadir}/icons/hicolor/*/apps/emacs.png
#%{_datadir}/icons/hicolor/*/apps/emacs22.png
%{_datadir}/icons/hicolor/scalable/apps/emacs.svg
%{_datadir}/icons/hicolor/scalable/mimetypes/emacs-document.svg
%{_datadir}/icons/hicolor/scalable/mimetypes/emacs-document23.svg

%files nox
%{_bindir}/emacs-%{version}-nox
%attr(0755,-,-) %ghost %{_bindir}/emacs

%files -f common-filelist common
%config(noreplace) %{_sysconfdir}/skel/.emacs
%{_sysconfdir}/rpm/macros.emacs
%doc doc/NEWS BUGS README doc/COPYING
%{_bindir}/ebrowse
%{_bindir}/emacsclient
%{_bindir}/etags.emacs
%{_bindir}/gctags
#%{_bindir}/rcs-checkin
%{_mandir}/*/*
%{_infodir}/*
%dir %{_datadir}/emacs/%{version}
%{_datadir}/emacs/%{version}/etc
%{_datadir}/emacs/%{version}/site-lisp
%{_libexecdir}/emacs
#%attr(0644,root,root) %config(noreplace) %{_datadir}/emacs/site-lisp/default.el
#%attr(0644,root,root) %config %{_datadir}/emacs/site-lisp/site-start.el

%files -f el-filelist el
%{pkgconfig}/emacs.pc
%doc etc/COPYING
%dir %{_datadir}/emacs/%{version}

%files terminal
%{_bindir}/emacs-terminal
%{_datadir}/applications/emacs-terminal.desktop

%files filesystem
%dir %{_datadir}/emacs
%dir %{_datadir}/emacs/site-lisp
%dir %{_datadir}/emacs/site-lisp/site-start.d

