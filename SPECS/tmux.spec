Name:           tmux
Version:        2.3
Release:        1%{?dist}
Summary:        A terminal multiplexer

Group:          Applications/System
# Most of the source is ISC licensed; some of the files in compat/ are 2 and
# 3 clause BSD licensed.
License:        ISC and BSD
URL:            http://sourceforge.net/projects/tmux
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

BuildRequires:  ncurses-devel
BuildRequires:  libevent-devel

%description
tmux is a "terminal multiplexer."  It enables a number of terminals (or
windows) to be accessed and controlled from a single terminal.  tmux is
intended to be a simple, modern, BSD-licensed alternative to programs such
as GNU Screen.

%prep
%setup -q

%build
%configure
make %{?_smp_mflags} LDFLAGS="%{optflags}"

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALLBIN="install -p -m 755" INSTALLMAN="install -p -m 644"

%post
if [ ! -f %{_sysconfdir}/shells ] ; then
    echo "%{_bindir}/tmux" > %{_sysconfdir}/shells
else
    grep -q "^%{_bindir}/tmux$" %{_sysconfdir}/shells || echo "%{_bindir}/tmux" >> %{_sysconfdir}/shells
fi

%postun
if [ $1 -eq 0 ] && [ -f %{_sysconfdir}/shells ]; then
    sed -i '\!^%{_bindir}/tmux$!d' %{_sysconfdir}/shells
fi

%files
%defattr(-,root,root,-)
%doc CHANGES FAQ TODO
%{_bindir}/tmux
%{_mandir}/man1/tmux.1.*

