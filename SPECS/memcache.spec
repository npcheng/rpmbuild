%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}
%{!?php_extdir: %{expand: %%global php_extdir %(/data/php7/bin/php-config --extension-dir)}}
%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)

%define pecl_name memcached
%define php_dir /data/php7/
%define php_bin %{php_dir}bin/
%define php_config %{php_bin}php-config
%define libmemcached /data/libmemcached
Summary:      Extension to work with the Memcached caching daemon
Name:         php7-memcached
Version:      2.2.0_beta
Release:      4%{?dist}
License:      PHP
Group:        Development/Languages
URL:          http://pecl.php.net/package/%{memcached}

AutoReqProv: no
#Source:       http://pecl.php.net/get/%{memcached}-%{version}.tgz
Source:       %{name}-%{version}.tar.gz
#Source1:      LICENSE
#Source2:      xml2changelog
#Patch0:       php-pecl-memcache-3.0.5-fdcast.patch
#Patch1:       php-pecl-memcache-3.0.5-refcount.patch
#Patch2:       php-pecl-memcache-3.0.5-get-mem-corrupt.patch

BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: php >= 7.0.0 ,zlib-devel
#Requires(post): %{__pecl}
#Requires(postun): %{__pecl}
#Provides:     php-pecl(%{pecl_name}) = %{version}-%{release}
#%if 0%{?php_zend_api:1}
#Requires:     php(zend-abi) = %{php_zend_api}
#Requires:     php(api) = %{php_core_api}
#%else
#Requires:     php-api = %{php_apiver}
#%endif
Requires:libmemcached

%description
Memcached is a caching daemon designed especially for
dynamic web applications to decrease database load by
storing objects in memory.

This extension allows you to work with memcached through
handy OO and procedural interfaces.

Memcache can be used as a PHP session handler.


%prep 
%setup

%build
%{php_bin}phpize 
./configure --with-php-config=%{php_config} \
    -with-libmemcached-dir=%{libmemcached}

%{__make} %{?_smp_mflags}


%install
%{__rm} -rf %{buildroot}
%{__make} install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
install -m 755 -d %{buildroot}%{php_dir}/etc/php.d

# Install XML package description
# use 'name' rather than 'pecl_name' to avoid conflict with pear extensions
#%{__mkdir_p} %{buildroot}%{pecl_xmldir}
#%{__install} -m 644 ../package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%clean
%{__rm} -rf %{buildroot}


#%if 0%{?pecl_install:1}
#%post
#%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null 2>&1 || :
#%endif


#%if 0%{?pecl_uninstall:1}
#%postun
#if [ $1 -eq 0 ] ; then
#    %{pecl_uninstall} %{pecl_name} >/dev/nulll 2>&1 || :
#fi
#%endif
%post
cat > %{php_dir}/etc/php.d/%{pecl_name}.ini << 'EOF'
; ----- Enable %{pecl_name} extension module
extension=%{pecl_name}.so
EOF

%files
%defattr(-, root, root, -)
#%doc CHANGELOG %{pecl_name}-%{version}/CREDITS %{pecl_name}-%{version}/README LICENSE
#%doc %{pecl_name}-%{version}/example.php %{pecl_name}-%{version}/memcache.php
#%config(noreplace) %{_sysconfdir}/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
#%{pecl_xmldir}/%{name}.xml


%changelog

