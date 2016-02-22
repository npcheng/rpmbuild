Name:libmemcached	
Version:1.0.18
Release:0%{?dist}
Summary:libmemcached for memcached

Group:Developmnet/Languages
License:php
URL:https://launchpad.net/libmemcached	
Source0:https://launchpad.net/libmemcached/1.0/1.0.18/+download/%{name}-%{version}.tar.gz

#BuildRequires:	
#Requires:	

%description
libmemcached for wxshake

%prep
%setup -q


%build
./configure --prefix=/data/libmemcached --SUPPORT-CAS

make %{?_smp_mflags}


%install
make install  DESTDIR="%{buildroot}"


%files
%defattr(-,root,root,-)
/data/libmemcached



%changelog

