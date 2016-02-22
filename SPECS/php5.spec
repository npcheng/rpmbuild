%define version 5.6.17
%define so_version 5
%define release 0

%define prefix /data/php5

Name: php
Summary: PHP: Hypertext Preprocessor
Group: Development/Languages
License:PHP
Version: %{version}
Release: 1%{?dist}

#Source0: http://www.php.net/get/php-%{version}.tar.gz/from/a/mirror
Source0: php-%{version}.tar.gz
Source1: php-fpm.init
Source2: php.ini
Source3: php-fpm.conf
Source4: fpm-www.conf
Source5: php-fpm.logrotate
#Icon: php.gif
URL: http://www.php.net/
Packager: PHP Group <group@php.net>

BuildRoot: /var/tmp/php-%{version}

%description
PHP is an HTML-embedded scripting language. Much of its syntax is
borrowed from C, Java and Perl with a couple of unique PHP-specific
features thrown in. The goal of the language is to allow web
developers to write dynamically generated pages quickly.

%prep

%setup

%build
set -x
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -Wno-pointer-sign"
export CFLAGS

./buildconf --force
./configure  --prefix=%{prefix} \
         --with-config-file-path=%{prefix}/etc \
         --with-pear \
	 --disable-debug \
         --with-gd \
         --with-jpeg-dir \
         --with-png-dir \
         --with-zlib \
         --with-freetype-dir \
         --with-mhash \
         --with-mysql \
         --with-mysqli \
         --enable-pdo \
         --with-pdo-mysql \
         --with-xmlrpc \
         --with-gettext \
         --enable-fpm \
         --enable-exif \
         --enable-wddx \
         --enable-zip \
         --enable-bcmath \
         --enable-calendar \
         --enable-ftp \
         --enable-mbstring \
         --enable-sockets \
         --enable-shmop \
         --enable-dba \
         --with-curl \
	 --with-openssl 

make %{?_smp_mflags}

%install
make install INSTALL_ROOT=%{buildroot}


install -m 755 -d $RPM_BUILD_ROOT%{_initddir}
install -m 755 -d $RPM_BUILD_ROOT/var/log/php-fpm/
install -m 755 -d $RPM_BUILD_ROOT/var/lib/php
install -m 755 -d $RPM_BUILD_ROOT/var/run/php-fpm
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_initddir}/php-fpm

install -m 755 %{SOURCE2} $RPM_BUILD_ROOT%{prefix}/etc
install -m 755 %{SOURCE3} $RPM_BUILD_ROOT%{prefix}/etc

install -m 755 -d $RPM_BUILD_ROOT%{prefix}/etc/php-fpm.d
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{prefix}/etc/php-fpm.d/www.conf

install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/php-fpm

%clean
rm -rf $RPM_BUILD_ROOT
%post
chkconfig --add php-fpm
cat > /etc/profile.d/php.sh <<EOF
if [ -d /data/php7/bin ]; then
   PATH=$PATH:/data/php7/bin
fi
EOF

%preun
    rm -f /etc/profile.d/php.sh
    /sbin/service php-fpm stop
    /sbin/chkconfig --del php-fpm
%postun
    /sbin/service php-fpm condrestart > /dev/null 2>&1 || :


%files
%defattr(-,root,root)
%{prefix}
/var/log/php-fpm/
/var/lib/php
%{_sysconfdir}/logrotate.d/php-fpm
%{_initddir}/php-fpm
#/.channels/.alias/pear.txt
#/.channels/.alias/pecl.txt
#/.channels/.alias/phpdocs.txt
#/.channels/__uri.reg
#/.channels/doc.php.net.reg
#/.channels/pear.php.net.reg
#/.channels/pecl.php.net.reg
#/.depdb
#/.depdblock
#/.filemap
#/.lock

%changelog
* Thu Jan 26 2015 pengcheng <pengcheng.ning@wxhsake.com> - 5.6.17-0
- fileinfo: wxshake first version
# figure out configure options options based on what packages are installed
# to override, use the OVERRIDE_OPTIONS environment variable.  To add
# extra options, use the OPTIONS environment variable.
