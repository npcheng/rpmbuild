# Hello packaging friend!
#
# If you find yourself using this 'fpm --edit' feature frequently, it is
# a sign that fpm is missing a feature! I welcome your feature requests!
# Please visit the following URL and ask for a feature that helps you never
# need to edit this file again! :)
#   https://github.com/jordansissel/fpm/issues
# ------------------------------------------------------------------------

# Disable the stupid stuff rpm distros include in the build process by default:
#   Disable any prep shell actions. replace them with simply 'true'
%define __spec_prep_post true
%define __spec_prep_pre true
#   Disable any build shell actions. replace them with simply 'true'
%define __spec_build_post true
%define __spec_build_pre true
#   Disable any install shell actions. replace them with simply 'true'
%define __spec_install_post true
%define __spec_install_pre true
#   Disable any clean shell actions. replace them with simply 'true'
%define __spec_clean_post true
%define __spec_clean_pre true
# Disable checking for unpackaged files ?
#%undefine __check_files

# Use md5 file digest method.
# The first macro is the one used in RPM v4.9.1.1
%define _binary_filedigest_algorithm 1
# This is the macro I find on OSX when Homebrew provides rpmbuild (rpm v5.4.14)
%define _build_binary_file_digest_algo 1

# Use gzip payload compression
%define _binary_payload w9.gzdio


Name: tengine
Version: 2.2.0
Release: 1
Summary: tengine
AutoReqProv: no
# Seems specifying BuildRoot is required on older rpmbuild (like on CentOS 5)
# fpm passes '--define buildroot ...' on the commandline, so just reuse that.
BuildRoot: %buildroot
# Add prefix, must not end with /

Prefix: /

Group:  System Enviroment/Daemons
License: unknown
Vendor: root@host3
URL: www.wxshake.com
Packager: <root@host3>

Requires: openssl
Requires: pcre
Requires: zlib
Requires: krb5-libs
%description
tengine

%prep
# noop

%build
# noop
%install
# noop

%clean
# noop




%files
%defattr(-,root,root,-)

# Reject config files already listed or parent directories, then prefix files
# with "/", then make sure paths with spaces are quoted. I hate rpm so much.
/data/tengine/client_body_temp
/data/tengine/conf/nginx.conf.default
/data/tengine/conf/scgi_params.default
/data/tengine/conf/koi-utf
/data/tengine/conf/nginx.conf
/data/tengine/conf/browsers
/data/tengine/conf/koi-win
/data/tengine/conf/fastcgi_params.default
/data/tengine/conf/mime.types.default
/data/tengine/conf/fastcgi.conf.default
/data/tengine/conf/mime.types
/data/tengine/conf/uwsgi_params
/data/tengine/conf/win-utf
/data/tengine/conf/scgi_params
/data/tengine/conf/fastcgi_params
/data/tengine/conf/module_stubs
/data/tengine/conf/fastcgi.conf
/data/tengine/conf/uwsgi_params.default
/data/tengine/scgi_temp
/data/tengine/include/ngx_setproctitle.h
/data/tengine/include/ngx_sha1.h
/data/tengine/include/ngx_inet.h
/data/tengine/include/ngx_syslog.h
/data/tengine/include/ngx_auto_config.h
/data/tengine/include/ngx_murmurhash.h
/data/tengine/include/ngx_http_core_module.h
/data/tengine/include/ngx_event_openssl.h
/data/tengine/include/ngx_md5.h
/data/tengine/include/ngx_files.h
/data/tengine/include/ngx_http.h
/data/tengine/include/ngx_pipe.h
/data/tengine/include/ngx_http_ssl_module.h
/data/tengine/include/ngx_event_connect.h
/data/tengine/include/ngx_regex.h
/data/tengine/include/ngx_shmem.h
/data/tengine/include/ngx_auto_headers.h
/data/tengine/include/ngx_resolver.h
/data/tengine/include/ngx_event.h
/data/tengine/include/ngx_setaffinity.h
/data/tengine/include/ngx_segment_tree.h
/data/tengine/include/ngx_parse.h
/data/tengine/include/ngx_errno.h
/data/tengine/include/ngx_trie.h
/data/tengine/include/ngx_socket.h
/data/tengine/include/ngx_crc.h
/data/tengine/include/ngx_event_posted.h
/data/tengine/include/ngx_http_config.h
/data/tengine/include/ngx_process.h
/data/tengine/include/ngx_alloc.h
/data/tengine/include/ngx_http_upstream_round_robin.h
/data/tengine/include/ngx_crc32.h
/data/tengine/include/ngx_linux.h
/data/tengine/include/ngx_array.h
/data/tengine/include/ngx_connection.h
/data/tengine/include/ngx_cycle.h
/data/tengine/include/ngx_gcc_atomic_x86.h
/data/tengine/include/ngx_palloc.h
/data/tengine/include/ngx_log.h
/data/tengine/include/ngx_atomic.h
/data/tengine/include/ngx_radix_tree.h
/data/tengine/include/ngx_rbtree.h
/data/tengine/include/ngx_sysinfo.h
/data/tengine/include/ngx_file.h
/data/tengine/include/ngx_thread.h
/data/tengine/include/ngx_queue.h
/data/tengine/include/ngx_shmtx.h
/data/tengine/include/ngx_proc.h
/data/tengine/include/ngx_http_cache.h
/data/tengine/include/ngx_http_reqstat.h
/data/tengine/include/ngx_http_ssi_filter_module.h
/data/tengine/include/ngx_event_pipe.h
/data/tengine/include/ngx_http_request.h
/data/tengine/include/ngx_crypt.h
/data/tengine/include/ngx_string.h
/data/tengine/include/nginx.h
/data/tengine/include/ngx_list.h
/data/tengine/include/ngx_process_cycle.h
/data/tengine/include/ngx_config.h
/data/tengine/include/ngx_http_upstream.h
/data/tengine/include/ngx_slab.h
/data/tengine/include/ngx_channel.h
/data/tengine/include/ngx_linux_config.h
/data/tengine/include/ngx_times.h
/data/tengine/include/ngx_time.h
/data/tengine/include/ngx_conf_file.h
/data/tengine/include/ngx_core.h
/data/tengine/include/ngx_http_script.h
/data/tengine/include/ngx_os.h
/data/tengine/include/ngx_hash.h
/data/tengine/include/ngx_buf.h
/data/tengine/include/ngx_user.h
/data/tengine/include/ngx_http_variables.h
/data/tengine/include/ngx_proxy_protocol.h
/data/tengine/include/ngx_event_timer.h
/data/tengine/include/ngx_open_file_cache.h
/data/tengine/html/index.html
/data/tengine/html/info.php
/data/tengine/html/50x.html
/data/tengine/sbin/nginx
/data/tengine/sbin/dso_tool
/data/tengine/proxy_temp
/data/tengine/uwsgi_temp
/data/tengine/fastcgi_temp/2/00
/data/tengine/fastcgi_temp/1/00
/data/tengine/logs/nginx.pid
/data/tengine/logs/error.log
/data/tengine/logs/access.log
/data/tengine/modules/ngx_http_memcached_module.so

%changelog


