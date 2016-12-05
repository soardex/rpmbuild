# Pass --without docs to rpmbuild if you don't want the documentation

%global gitcoredir          %{_libexecdir}/git-core
%global noarch_sub          1
%global libcurl_devel       libcurl-devel
%global docbook_suppress_sp 0
%global enable_ipv6         0
%global filter_yaml_any     0

%global use_systemd 1
%global gnome_keyring 1

Name:           git
Version:        2.11.0
Release:        1%{?dist}
Summary:        Fast Version Control System
License:        GPLv2
Group:          Development/Tools
URL:            http://git-scm.com/
Source0:        http://git-core.googlecode.com/files/%{name}-%{version}.tar.gz
Source2:        git-init.el
Source3:        git.xinetd.in
Source4:        git.conf.httpd
Source5:        git-gui.desktop
Source6:        gitweb.conf.in
Source12:       git@.service
Source13:       git.socket

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  desktop-file-utils
BuildRequires:  expat-devel
BuildRequires:  gettext
BuildRequires:  %{libcurl_devel}
%if %{gnome_keyring}
BuildRequires:  libgnome-keyring-devel
%endif
BuildRequires:  pcre-devel
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel >= 1.2
%if %{use_systemd}
# For macros
BuildRequires:  systemd
%endif

Requires:       less
Requires:       openssh-clients
Requires:       perl(Error)
Requires:       perl(Term::ReadKey)
Requires:       perl-Git = %{version}-%{release}
Requires:       rsync
Requires:       zlib >= 1.2

Provides:       git-core = %{version}-%{release}
Obsoletes:      git-core <= 1.5.4.3

# Obsolete git-arch
Obsoletes:      git-arch < %{version}-%{release}

%description
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

The git rpm installs the core tools with minimal dependencies.  To
install all git packages, including tools for integrating with other
SCMs, install the git-all meta-package.

%package all
Summary:        Meta-package to pull in all git tools
Group:          Development/Tools
%if %{noarch_sub}
BuildArch:      noarch
%endif
Requires:       git = %{version}-%{release}
Requires:       git-cvs = %{version}-%{release}
Requires:       git-email = %{version}-%{release}
Requires:       git-gui = %{version}-%{release}
Requires:       git-svn = %{version}-%{release}
Requires:       git-p4 = %{version}-%{release}
Requires:       gitk = %{version}-%{release}
Requires:       perl-Git = %{version}-%{release}
Requires:       emacs-git = %{version}-%{release}
Obsoletes:      git <= 1.5.4.3

%description all
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

This is a dummy package which brings in all subpackages.

%package bzr
Summary:        Git tools for working with bzr repositories
Group:          Development/Tools
%if %{noarch_sub}
BuildArch:      noarch
%endif
Requires:       git = %{version}-%{release}
Requires:       bzr

%description bzr
%{summary}.

%package daemon
Summary:        Git protocol dæmon
Group:          Development/Tools
Requires:       git = %{version}-%{release}
%if %{use_systemd}
Requires:	systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%else
Requires:       xinetd
%endif
%description daemon
The git dæmon for supporting git:// access to git repositories

%package -n gitweb
Summary:        Simple web interface to git repositories
Group:          Development/Tools
%if %{noarch_sub}
BuildArch:      noarch
%endif
Requires:       git = %{version}-%{release}

%description -n gitweb
Simple web interface to track changes in git repositories

%package hg
Summary:        Git tools for working with mercurial repositories
Group:          Development/Tools
%if %{noarch_sub}
BuildArch:      noarch
%endif
Requires:       git = %{version}-%{release}
Requires:       mercurial

%description hg
%{summary}.

%package p4
Summary:        Git tools for working with Perforce depots
Group:          Development/Tools
%if %{noarch_sub}
BuildArch:      noarch
%endif
BuildRequires:  python
Requires:       git = %{version}-%{release}
%description p4
%{summary}.

%package svn
Summary:        Git tools for importing Subversion repositories
Group:          Development/Tools
Requires:       git = %{version}-%{release}, subversion, perl(Term::ReadKey)
%description svn
Git tools for importing Subversion repositories.

%package cvs
Summary:        Git tools for importing CVS repositories
Group:          Development/Tools
%if %{noarch_sub}
BuildArch:      noarch
%endif
Requires:       git = %{version}-%{release}, cvs
Requires:       cvsps
Requires:	perl-DBD-SQLite
%description cvs
Git tools for importing CVS repositories.

%package email
Summary:        Git tools for sending email
Group:          Development/Tools
%if %{noarch_sub}
BuildArch:      noarch
%endif
Requires:       git = %{version}-%{release}, perl-Git = %{version}-%{release}
Requires:       perl(Authen::SASL)
Requires:       perl(Net::SMTP::SSL)
%description email
Git tools for sending email.

%package gui
Summary:        Git GUI tool
Group:          Development/Tools
%if %{noarch_sub}
BuildArch:      noarch
%endif
Requires:       git = %{version}-%{release}, tk >= 8.4
Requires:       gitk = %{version}-%{release}
%description gui
Git GUI tool.

%package -n gitk
Summary:        Git revision tree visualiser
Group:          Development/Tools
%if %{noarch_sub}
BuildArch:      noarch
%endif
Requires:       git = %{version}-%{release}, tk >= 8.4
%description -n gitk
Git revision tree visualiser.

%package -n perl-Git
Summary:        Perl interface to Git
Group:          Development/Libraries
%if %{noarch_sub}
BuildArch:      noarch
%endif
Requires:       git = %{version}-%{release}
BuildRequires:  perl(Error), perl(ExtUtils::MakeMaker)
Requires:       perl(Error)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description -n perl-Git
Perl interface to Git.

%package -n perl-Git-SVN
Summary:        Perl interface to Git::SVN
Group:          Development/Libraries
%if %{noarch_sub}
BuildArch:      noarch
%endif
Requires:       git = %{version}-%{release}
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description -n perl-Git-SVN
Perl interface to Git.

%package -n emacs-git
Summary:        Git version control system support for Emacs
Group:          Applications/Editors
Requires:       git = %{version}-%{release}
%if %{noarch_sub}
BuildArch:      noarch
Requires:       emacs(bin) >= %{_emacs_version}
%else
Requires:       emacs-common
%endif

%description -n emacs-git
%{summary}.

%package -n emacs-git-el
Summary:        Elisp source files for git version control system support for Emacs
Group:          Applications/Editors
%if %{noarch_sub}
BuildArch:      noarch
%endif
Requires:       emacs-git = %{version}-%{release}

%description -n emacs-git-el
%{summary}.

%prep
%setup -q

# Use these same options for every invocation of 'make'.
# Otherwise it will rebuild in %%install due to flags changes.
cat << \EOF > config.mak
V = 1
CFLAGS = %{optflags}
BLK_SHA1 = 1
NEEDS_CRYPTO_WITH_SSL = 1
USE_LIBPCRE = 1
ETC_GITCONFIG = %{_sysconfdir}/gitconfig
DESTDIR = %{buildroot}
INSTALL = install -p
GITWEB_PROJECTROOT = %{_var}/lib/git
GNU_ROFF = 1
htmldir = %{_docdir}/%{name}-%{version}
prefix = %{_prefix}
gitwebdir = %{_var}/www/git
EOF

%if "%{gitcoredir}" == "%{_bindir}"
echo gitexecdir = %{_bindir} >> config.mak
%endif

%if %{docbook_suppress_sp}
# This is needed for 1.69.1-1.71.0
echo DOCBOOK_SUPPRESS_SP = 1 >> config.mak
%endif

# Filter bogus perl requires
# packed-refs comes from a comment in contrib/hooks/update-paranoid
# YAML::Any is optional and not available on el5
cat << \EOF > %{name}-req
#!/bin/sh
%{__perl_requires} $* |\
sed \
%if %{filter_yaml_any}
    -e '/perl(YAML::Any)/d' \
%endif
    -e '/perl(packed-refs)/d'
EOF

%global __perl_requires %{_builddir}/%{name}-%{version}/%{name}-req
chmod +x %{__perl_requires}

%build
make configure
sh configure --with-c-compiler=gcc
make %{?_smp_mflags} git-daemon LDFLAGS="-pie -Wl,-z,relro,-z,now" CFLAGS="$RPM_OPT_FLAGS -fPIC"
make %{?_smp_mflags} all -o git-daemon

make -C contrib/emacs

%if %{gnome_keyring}
make -C contrib/credential/gnome-keyring/
%endif

make -C contrib/subtree/

# Remove shebang from bash-completion script
sed -i '/^#!bash/,+1 d' contrib/completion/git-completion.bash

%install
rm -rf %{buildroot}
make %{?_smp_mflags} INSTALLDIRS=vendor install -o git-daemon

%global elispdir %{_emacs_sitelispdir}/git
make -C contrib/emacs install \
    emacsdir=%{buildroot}%{elispdir}
for elc in %{buildroot}%{elispdir}/*.elc ; do
    install -pm 644 contrib/emacs/$(basename $elc .elc).el \
    %{buildroot}%{elispdir}
done
install -Dpm 644 %{SOURCE2} \
    %{buildroot}%{_emacs_sitestartdir}/git-init.el

%if %{gnome_keyring}
install -pm 755 contrib/credential/gnome-keyring/git-credential-gnome-keyring \
    %{buildroot}%{gitcoredir}
# Remove built binary files, otherwise they will be installed in doc
make -C contrib/credential/gnome-keyring/ clean
%endif

make -C contrib/subtree install

mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
install -pm 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/httpd/conf.d/git.conf
sed "s|@PROJECTROOT@|%{_var}/lib/git|g" \
    %{SOURCE6} > %{buildroot}%{_sysconfdir}/gitweb.conf

find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -empty -exec rm -f {} ';'
find %{buildroot} -type f -name perllocal.pod -exec rm -f {} ';'

# Remove remote-helper python libraries and scripts, these are not ready for
# use yet
rm -rf %{buildroot}%{python_sitelib} %{buildroot}%{gitcoredir}/git-remote-testgit

# git-archimport is not supported
find %{buildroot} Documentation -type f -name 'git-archimport*' -exec rm -f {} ';'

exclude_re="archimport|email|git-citool|git-cvs|git-daemon|git-gui|git-remote-bzr|git-remote-hg|gitk|p4|svn"
(find %{buildroot}{%{_bindir},%{_libexecdir}} -type f | grep -vE "$exclude_re" | sed -e s@^%{buildroot}@@) > bin-man-doc-files
(find %{buildroot}{%{_bindir},%{_libexecdir}} -mindepth 1 -type d | grep -vE "$exclude_re" | sed -e 's@^%{buildroot}@%dir @') >> bin-man-doc-files
(find %{buildroot}%{perl_vendorlib} -type f | sed -e s@^%{buildroot}@@) > perl-git-files
(find %{buildroot}%{perl_vendorlib} -mindepth 1 -type d | sed -e 's@^%{buildroot}@%dir @') >> perl-git-files
# Split out Git::SVN files
grep Git/SVN perl-git-files > perl-git-svn-files
sed -i "/Git\/SVN/ d" perl-git-files
rm -rf %{buildroot}%{_mandir}

mkdir -p %{buildroot}%{_var}/lib/git
%if %{use_systemd}
mkdir -p %{buildroot}%{_unitdir}
cp -a %{SOURCE12} %{SOURCE13} %{buildroot}%{_unitdir}
%else
mkdir -p %{buildroot}%{_sysconfdir}/xinetd.d
# On EL <= 5, xinetd does not enable IPv6 by default
enable_ipv6="        # xinetd does not enable IPv6 by default
        flags           = IPv6"
perl -p \
    -e "s|\@GITCOREDIR\@|%{gitcoredir}|g;" \
    -e "s|\@BASE_PATH\@|%{_var}/lib/git|g;" \
%if %{enable_ipv6}
    -e "s|^}|$enable_ipv6\n$&|;" \
%endif
    %{SOURCE3} > %{buildroot}%{_sysconfdir}/xinetd.d/git
%endif

# Install bzr and hg remote helpers from contrib
install -pm 755 contrib/remote-helpers/git-remote-{bzr,hg} %{buildroot}%{gitcoredir}

# Setup bash completion
mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
install -pm 644 contrib/completion/git-completion.bash %{buildroot}%{_sysconfdir}/bash_completion.d/git

# Install tcsh completion
mkdir -p %{buildroot}%{_datadir}/git-core/contrib/completion
install -pm 644 contrib/completion/git-completion.tcsh \
    %{buildroot}%{_datadir}/git-core/contrib/completion/

# Move contrib/hooks out of %%docdir and make them executable
mkdir -p %{buildroot}%{_datadir}/git-core/contrib
mv contrib/hooks %{buildroot}%{_datadir}/git-core/contrib
chmod +x %{buildroot}%{_datadir}/git-core/contrib/hooks/*
pushd contrib > /dev/null
ln -s ../../../git-core/contrib/hooks
popd > /dev/null

# Install git-prompt.sh
mkdir -p %{buildroot}%{_datadir}/git-core/contrib/completion
install -pm 644 contrib/completion/git-prompt.sh \
    %{buildroot}%{_datadir}/git-core/contrib/completion/

# install git-gui .desktop file
desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications %{SOURCE5}

# find translations
%find_lang %{name} %{name}.lang
cat %{name}.lang >> bin-man-doc-files

# quiet some rpmlint complaints
chmod -R g-w %{buildroot}
find %{buildroot} -name git-mergetool--lib | xargs chmod a-x
rm -f {Documentation/technical,contrib/emacs,contrib/credential/gnome-keyring}/.gitignore
chmod a-x Documentation/technical/api-index.sh
find contrib -type f | xargs chmod -x


%clean
rm -rf %{buildroot}

%if %{use_systemd}
%post daemon
%systemd_post git@.service

%preun daemon
%systemd_preun git@.service

%postun daemon
%systemd_postun_with_restart git@.service
%endif

%files -f bin-man-doc-files
%defattr(-,root,root)
%{_datadir}/git-core/
%doc README.md COPYING Documentation/*.txt Documentation/RelNotes contrib/
%{_sysconfdir}/bash_completion.d

%files bzr
%defattr(-,root,root)
%{gitcoredir}/git-remote-bzr

%files hg
%defattr(-,root,root)
%{gitcoredir}/git-remote-hg

%files p4
%defattr(-,root,root)
%{gitcoredir}/*p4*
%{gitcoredir}/mergetools/p4merge
%doc Documentation/*p4*.txt

%files svn
%defattr(-,root,root)
%{gitcoredir}/*svn*
%doc Documentation/*svn*.txt

%files cvs
%defattr(-,root,root)
%doc Documentation/*git-cvs*.txt
%{_bindir}/git-cvsserver
%{gitcoredir}/*cvs*

%files email
%defattr(-,root,root)
%doc Documentation/*email*.txt
%{gitcoredir}/*email*

%files gui
%defattr(-,root,root)
%{gitcoredir}/git-gui*
%{gitcoredir}/git-citool
%{_datadir}/applications/*git-gui.desktop
%{_datadir}/git-gui/

%files -n gitk
%defattr(-,root,root)
%doc Documentation/*gitk*.txt
%{_bindir}/*gitk*
%{_datadir}/gitk

%files -n perl-Git -f perl-git-files
%defattr(-,root,root)
%exclude %{_mandir}/man3/*Git*SVN*.3pm*

%files -n perl-Git-SVN -f perl-git-svn-files
%defattr(-,root,root)

%files -n emacs-git
%defattr(-,root,root)
%doc contrib/emacs/README
%dir %{elispdir}
%{elispdir}/*.elc
%{_emacs_sitestartdir}/git-init.el

%files -n emacs-git-el
%defattr(-,root,root)
%{elispdir}/*.el

%files daemon
%defattr(-,root,root)
%doc Documentation/*daemon*.txt
%if %{use_systemd}
%{_unitdir}/git.socket
%{_unitdir}/git@.service
%else
%config(noreplace)%{_sysconfdir}/xinetd.d/git
%endif
%{gitcoredir}/git-daemon
%{_var}/lib/git

%files -n gitweb
%defattr(-,root,root)
%doc gitweb/INSTALL gitweb/README
%config(noreplace)%{_sysconfdir}/gitweb.conf
%config(noreplace)%{_sysconfdir}/httpd/conf.d/git.conf
%{_var}/www/git/


%files all
# No files for you!

