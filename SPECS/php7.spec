%define version 7.0.3

%define prefix /data/php7
%define release 0%{?dist}
Name: php
Summary: PHP: Hypertext Preprocessor
Group: Development/Languages
License:PHP
Version: %{version}
Release: %{release}
#Source0: http://www.php.net/get/php-%{version}.tar.gz/from/a/mirror
Source0: http://cn2.php.net/get/php-%{version}.tar.gz
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
         --with-config-file-scan-dir=%{prefix}/etc/php.d \
         --with-pear \
	 --disable-debug \
         --with-gd \
         --with-jpeg-dir \
         --with-png-dir \
         --with-zlib \
         --with-freetype-dir \
         --with-mhash \
         --with-mysqli \
         --enable-embedded-mysqli \
         --enable-pdo \
         --with-pdo-mysql \
         --with-xmlrpc \
         --with-gettext \
         --enable-fpm \
         --enable-exif \
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
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php
install -m 700 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/php/session
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/log/php-fpm
install -m 755 -d $RPM_BUILD_ROOT%{_localstatedir}/run/php-fpm


install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_initddir}/php-fpm
install -m 755 %{SOURCE2} $RPM_BUILD_ROOT%{prefix}/etc
install -m 755 %{SOURCE3} $RPM_BUILD_ROOT%{prefix}/etc


install -m 755 -d $RPM_BUILD_ROOT%{prefix}/etc/php-fpm.d
install -m 755 -d $RPM_BUILD_ROOT%{prefix}/etc/php.d
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
%attr(0770,nginx,nginx) %dir %{_localstatedir}/lib/php/session
%{_localstatedir}/lib/php
%{_sysconfdir}/logrotate.d/php-fpm
%{_initddir}/php-fpm

%changelog
* Thu Feb 17 2016 pengcheng <pengcheng.ning@wxhsake.com> 
- fileinfo: use  release  7.0.3
* Thu Jan 26 2016 pengcheng <pengcheng.ning@wxhsake.com> - 7.0.2
- fileinfo: wxshake first version
