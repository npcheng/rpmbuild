%define realname tengine
%define realver  2.1.2
 
#%define psolver           1.6.29.3
 
%define PREFIX /data/tengine
%define USER   nobody
%define GROUP  nobody
%define WEB_USER_HOME %[PREFIX]/html 
 
%define CONF_FILE %{_sysconfdir}/%{name}/%{name}.conf
 
# Common info
Name:          %{realname}
Version:       %{realver}
Release:       0 
License:       BSD-2-Clause
Group:         Productivity/Networking/Web/Servers
URL:           http://nginx.org/
Summary:       HTTP and reverse proxy server, as well as a mail proxy server
 
# Install-time parameters
Provides:      httpd http_daemon webserver %{?suse_version:suse_help_viewer}
Requires:      logrotate
 
# Build-time parameters
BuildRequires: gcc-c++ libstdc++-devel
BuildRequires: zlib-devel openssl-devel pcre-devel
BuildRequires: libxml2-devel libxslt-devel gd-devel 
BuildRoot:     %{_tmppath}/%{name}-root
Source0:       http://tengine.taobao.org/download/%{realname}-%{realver}.tar.gz
Source1:       nginx.logrotate
Source2:       nginx.init
Source3:       nginx.sysconfig
 
%description
tengine is a HTTP server based on nginx
nginx [engine x] is a HTTP and reverse proxy server, as well as a mail proxy server
 
# Preparation step (unpackung and patching if necessary)
%prep
%setup
 
%build
./configure  \
    --prefix=%{PREFIX} \
    --http-client-body-temp-path=%{PREFIX}/cache/client_body_temp \
    --http-proxy-temp-path=%{PREFIX}/cache/proxy_temp \
    --http-fastcgi-temp-path=%{PREFIX}/cache/fastcgi_temp \
    --http-uwsgi-temp-path=%{PREFIX}/cache/uwsgi_temp \
    --http-scgi-temp-path=%{PREFIX}/cache/scgi_temp \
    --without-mail_imap_module \
    --without-mail_pop3_module \
    --without-mail_smtp_module 

%__make %{?_smp_mflags}
 
%install
%__make install DESTDIR=%{buildroot}
%__install -D -m644 %{S:1} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
%__install -d -m755 %{buildroot}%{_initrddir}
#sed -r 's|##PREFIX##|%{PREFIX}|; s|##CONF_FILE##|%{CONF_FILE}|' %{S:2} > %{buildroot}%{_initrddir}/%{name}
%__install -d -m755 %{buildroot}/%{_sysconfdir}/sysconfig
%__install -d -m755 %{buildroot}/%{_sysconfdir}/sysconfig
endif
%endif
%__install -d -m755 %{buildroot}%{_localstatedir}/cache/
 
%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
 
%files
%defattr(-,root,root)
%doc CHANGES CHANGES.ru LICENSE README
%config(noreplace) %{_sysconfdir}/%{name}/*
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{PREFIX}
%attr(0755,root,root) %{_initrddir}/%{name}
%dir %attr(0755,%{USER},%{GROUP}) %{_localstatedir}/log/%{name}
%{PREFIX}/html/*
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%doc %{_mandir}/man8/*
%dir %attr(0755,%{USER},%{GROUP}) %{_localstatedir}/cache/
 
%pre
/usr/sbin/groupadd -r %{GROUP} &>/dev/null ||:
/usr/sbin/useradd  -g %{GROUP} -s /bin/false -r -c "Web-server" -d %{WEB_USER_HOME} %{USER} &>/dev/null ||:

%post
/sbin/chkconfig --add tengine

%changelog
