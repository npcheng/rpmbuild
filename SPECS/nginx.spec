%define realname nginx
%define realver  1.4.2
%define srcext   tar.gz
 
%define page_speed_commit cd80e92
%define psolver           1.6.29.3
 
%if 0%{?suse_version}
%define USER   wwwrun
%define GROUP  www
%define PREFIX /srv/www
%define WEB_USER_HOME /var/lib/lighttpd
%else
%define USER   apache
%define GROUP  apache
%define PREFIX /var/www
%define WEB_USER_HOME /var/www
%endif
 
%define CONF_FILE %{_sysconfdir}/%{name}/%{name}.conf
 
# Common info
Name:          %{realname}
Version:       %{realver}
Release:       16.1
License:       BSD-2-Clause
Group:         Productivity/Networking/Web/Servers
URL:           http://nginx.org/
Summary:       HTTP and reverse proxy server, as well as a mail proxy server
 
# Install-time parameters
Provides:      httpd http_daemon webserver %{?suse_version:suse_help_viewer}
Requires:      logrotate
 
# Build-time parameters
BuildRequires: gcc-c++ libstdc++-devel
BuildRequires: dos2unix
BuildRequires: zlib-devel openssl-devel pcre-devel
BuildRequires: libxml2-devel libxslt-devel gd-devel libGeoIP-devel
%if 0%{?suse_version} || 0%{?fedora} || 0%{?rhel_version} || 0%{?centos_version} >= 600
BuildRequires: libaio-devel
%endif
BuildRoot:     %{_tmppath}/%{name}-root
Source0:       http://nginx.org/download/%{realname}-%{realver}%{?extraver}.%{srcext}
Source1:       nginx.logrotate
Source2:       nginx.init
Source3:       nginx.sysconfig
Source91:      https://github.com/pagespeed/ngx_pagespeed/tarball/%{page_speed_commit}/pagespeed-ngx_pagespeed-%{page_speed_commit}.tar.gz
Source92:      https://dl.google.com/dl/page-speed/psol/%{psolver}.tar.gz
Patch:         nginx-memset_zero.patch
 
#!BuildIgnore: freetype2
 
%description
nginx [engine x] is a HTTP and reverse proxy server, as well as a mail proxy server
 
This nginx package built with Google PageSpeed
 
# Preparation step (unpackung and patching if necessary)
%prep
%setup -q -n %{realname}-%{realver}%{?extraver} -a91
%{__tar} -zxf %{S:92} -C pagespeed-ngx_pagespeed-%{page_speed_commit}
%patch -p1
 
%build
./configure \
 --prefix=%{PREFIX} \
 --sbin-path=%{_sbindir}/%{name} \
 --conf-path=%{CONF_FILE} \
 --error-log-path=%{_localstatedir}/log/%{name}/error.log \
 --http-log-path=%{_localstatedir}/log/%{name}/access.log \
 --pid-path=%{_localstatedir}/run/%{name}.pid \
 --lock-path=%{_localstatedir}/lock/%{name}.lock \
 --user=%{USER} \
 --group=%{GROUP} \
 \
 --http-client-body-temp-path=%{_localstatedir}/cache/%{name}/client_body_temp \
 --http-proxy-temp-path=%{_localstatedir}/cache/%{name}/proxy_temp \
 --http-fastcgi-temp-path=%{_localstatedir}/cache/%{name}/fastcgi_temp \
 --http-uwsgi-temp-path=%{_localstatedir}/cache/%{name}/uwsgi_temp \
 --http-scgi-temp-path=%{_localstatedir}/cache/%{name}/scgi_temp \
%if 0%{?suse_version} || 0%{?fedora} || 0%{?rhel_version} || 0%{?centos_version} >= 600
 --with-file-aio \
%endif
 --with-ipv6 \
 \
 --with-http_ssl_module \
 --with-http_spdy_module \
 --with-http_realip_module \
 --with-http_addition_module \
 --with-http_xslt_module \
 --with-http_image_filter_module \
 --with-http_geoip_module \
 --with-http_sub_module \
 --with-http_dav_module \
 --with-http_flv_module \
 --with-http_mp4_module \
 --with-http_gzip_static_module \
 --with-http_random_index_module \
 --with-http_secure_link_module \
 --with-http_degradation_module \
 --with-http_stub_status_module \
 \
 --with-mail \
 --with-mail_ssl_module \
 \
 --with-cc-opt="%{optflags}" \
 --with-ld-opt="-Wl,--as-needed -Wl,--strip-all" \
 \
 --with-pcre \
 --with-pcre-jit \
 --add-module=%{_builddir}/%{realname}-%{realver}%{?extraver}/pagespeed-ngx_pagespeed-%{page_speed_commit}
%__make %{?_smp_mflags}
 
%install
%__make install DESTDIR=%{buildroot}
iconv -f koi8-r CHANGES.ru > c && %__mv -f c CHANGES.ru
%__install -D -m644 man/nginx.8 %{buildroot}%{_mandir}/man8/nginx.8
%__install -D -m644 %{S:1} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
%__install -d -m755 %{buildroot}%{_initrddir}
sed -r 's|##PREFIX##|%{PREFIX}|; s|##CONF_FILE##|%{CONF_FILE}|' %{S:2} > %{buildroot}%{_initrddir}/%{name}
%__rm -f %{buildroot}%{PREFIX}/html/index.html
%if %{expand:%_vendor == "suse"}
%__mv %{buildroot}%{PREFIX}/html %{buildroot}%{PREFIX}/htdocs
%__install -d -m755 %{buildroot}/var/adm/fillup-templates
sed -r 's|##PREFIX##|%{PREFIX}|; s|##CONF_FILE##|%{CONF_FILE}|' %{S:3} > %{buildroot}/var/adm/fillup-templates/sysconfig.%{name}
%__ln_s -f %{_initrddir}/%{name} %{buildroot}%{_sbindir}/rc%{name}
dos2unix contrib/geo2nginx.pl
%__install -D -m755 contrib/geo2nginx.pl %{buildroot}%{_bindir}/geo2nginx.pl
%else
%__install -d -m755 %{buildroot}/%{_sysconfdir}/sysconfig
sed -r 's|##PREFIX##|%{PREFIX}|; s|##CONF_FILE##|%{CONF_FILE}|' %{S:3} > %{buildroot}/%{_sysconfdir}/sysconfig/%{name}
%endif
%__install -d -m755 %{buildroot}%{_localstatedir}/cache/%{name}
 
%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
 
%files
%defattr(-,root,root)
%doc CHANGES CHANGES.ru LICENSE README
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_sbindir}/nginx
%attr(0755,root,root) %{_initrddir}/%{name}
%dir %attr(0755,%{USER},%{GROUP}) %{_localstatedir}/log/%{name}
%if %{expand:%_vendor == "suse"}
%{_bindir}/geo2nginx.pl
%{_sbindir}/rcnginx
%{PREFIX}/htdocs/*
/var/adm/fillup-templates/sysconfig.%{name}
%else
%{PREFIX}/html/*
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%endif
%doc %{_mandir}/man8/*
%dir %attr(0755,%{USER},%{GROUP}) %{_localstatedir}/cache/%{name}
 
%pre
/usr/sbin/groupadd -r %{GROUP} &>/dev/null ||:
/usr/sbin/useradd  -g %{GROUP} -s /bin/false -r -c "Web-server" -d %{WEB_USER_HOME} %{USER} &>/dev/null ||:
 
%if 0%{?suse_version}
 
%post
%{fillup_and_insserv %{name}}
 
%preun
%{stop_on_removal %{name}}
rm -rf %{_localstatedir}/cache/%{name}/*
 
%postun
%{restart_on_update %{name}}
%{insserv_cleanup}
 
%else
 
%preun
rm -rf %{_localstatedir}/cache/%{name}/*
 
%endif
 
%changelog
