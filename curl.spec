%undefine __libtoolize
Name: curl
Version: 7.19.3
Release: alt2

Summary: Gets a file from a FTP, GOPHER or HTTP server
Summary(ru_RU.UTF-8): Утилиты и библиотеки для передачи файлов
License: MPL or MIT
Group: Networking/File transfer
Url: http://curl.haxx.se

Source: %url/download/%name-%version.tar
Patch0: curl-%version-%release.patch

Requires: lib%name = %version-%release

# Automatically added by buildreq on Fri Feb 09 2007
BuildRequires: gcc-c++ glibc-devel-static groff-base libidn-devel libssl-devel zlib-devel libcares-devel

%package -n lib%name
Summary: The shared library for file transfer
Summary(ru_RU.UTF-8): Библиотеки для передачи файлов
Group: System/Libraries
Provides: %name-lib = %version
Obsoletes: %name-lib
Requires: ca-certificates

%package -n lib%name-devel
Summary: Header files for lib%name
Summary(ru_RU.UTF-8): Заголовочные файлы для lib%name
Group: Development/C
Requires: lib%name = %version-%release libidn-devel libssl-devel zlib-devel
Provides: %name-devel = %version
Obsoletes: %name-devel

%package -n lib%name-devel-static
Summary: Static libraries for lib%name
Summary(ru_RU.UTF-8): Статические библиотеки для lib%name
Group: Development/C
Requires: lib%name-devel = %version-%release

%description
Curl is a client to get documents/files from servers, using any of the
supported protocols. The command is designed to work without user
interaction or any kind of interactivity.

Curl offers a busload of useful tricks like proxy support, user
authentication, ftp upload, HTTP post, file transfer resume and more.

NOTE: This version is compiled with SSL (https) support.

%description -l ru_RU.UTF-8
Curl - это клиент для получения файлов или документов с серверов, используя 
один из поддерживаемых протоколов. Команда сделана таким образом, что бы работала 
без вмешательства пользователя (или с вмешательством пользователя).

Curl позволяет делать операции над сетевыми файлами, используя поддержку Прокси, 
авторизацию пользователя, докачку файлов и многое другое.

%description -n lib%name
Lib%name is a library of functions for sending and receiving files through
various protocols, including http and ftp.

You should install this package if you plan to use any applications that
use lib%name.

%description -n lib%name -l ru_RU.UTF-8
Lib%name - это библиотека функций для отправки или получения файлов через 
различные сетевые протоколы, включая http и ftp.

Вам нужно установить этот пакет, если вы планируете использовать приложения 
с использованием lib%name.

%description -n lib%name-devel
Lib%name is a library of functions for sending and receiving files through
various protocols, including http and ftp.

You should install this package if you wish to develop applications that
utilize lib%name.

%description -n lib%name-devel -l ru_RU.UTF-8
Lib%name - это библиотека функций для отправки или получения файлов через
различные сетевые протоколы, включая http и ftp.  

Вам нужно установить этот пакет, если вы планируете разрабатывать приложения
с использованием lib%name.


%description -n lib%name-devel-static
Lib%name is a library of functions for sending and receiving files through
various protocols, including http and ftp.

You should install this package if you wish to develop statically linked
applications that utilize lib%name.

%description -n lib%name-devel-static -l ru_RU.UTF-8
Lib%name - это библиотека функций для отправки или получения файлов через
различные сетевые протоколы, включая http и ftp.

Вам нужно установить этот пакет, если вы планируете разрабатывать статически
скомпилированные  приложения с использованием lib%name.

%prep
%setup -q
%patch0 -p1

%build
%configure --with-ssl \
	    --with-libidn \
	    --enable-ipv6 \
	    --disable-rpat \
	    --disable-ldap \
	    --enable-ares \
	    --without-gssapi \
	    --with-ca-bundle=%_datadir/ca-certificates/ca-bundle.crt

%make_build

%install
%make install DESTDIR=$RPM_BUILD_ROOT

%files
%_bindir/curl
%_man1dir/curl.1*

%files -n lib%name
%_libdir/*.so.*

%doc CHANGES README* docs/{FAQ,FEATURES}

%files -n lib%name-devel
%_libdir/*.so
%_libdir/pkgconfig/libcurl.pc
%_bindir/curl-config
%_includedir/*
%_man3dir/*
%_man1dir/curl-config.1*
%doc docs/{THANKS,BUGS,CONTRIBUTE,INTERNALS,MANUAL,RESOURCES,TheArtOfHttpScripting,TODO,examples}

%files -n lib%name-devel-static
%_libdir/*.a

%changelog
* Mon Feb 09 2009 Anton Farygin <rider@altlinux.ru> 7.19.3-alt2
- curl-config --libs fixed (#18779)

* Wed Jan 28 2009 Anton Farygin <rider@altlinux.ru> 7.19.3-alt1
- new version

* Fri Nov 14 2008 Anton Farygin <rider@altlinux.ru> 7.19.2-alt1
- new version

* Fri Nov 14 2008 Anton Farygin <rider@altlinux.ru> 7.19.1-alt2
- post-ldconfig removed

* Mon Nov 10 2008 Anton Farygin <rider@altlinux.ru> 7.19.1-alt1
- new version

* Mon Sep 15 2008 Anton Farygin <rider@altlinux.ru> 7.19.0-alt2
- enabled c-ares support (#17101)

* Fri Sep 12 2008 Anton Farygin <rider@altlinux.ru> 7.19.0-alt1
- new version

* Thu Jun 05 2008 Anton Farygin <rider@altlinux.ru> 7.18.2-alt1
- new version

* Mon Apr 07 2008 Anton Farygin <rider@altlinux.ru> 7.18.1-alt1
- new version

* Thu Jan 31 2008 Anton Farygin <rider@altlinux.ru> 7.18.0-alt1
- new version

* Thu Nov 15 2007 Anton Farygin <rider@altlinux.ru> 7.17.1-alt2
- disabled ldap support

* Tue Nov 06 2007 Anton Farygin <rider@altlinux.ru> 7.17.1-alt1
- new version

* Fri Sep 14 2007 Anton Farygin <rider@altlinux.ru> 7.17.0-alt1
- new version
- removed patch1 (included to mainstream)
- removed unsused patch0

* Tue Sep 11 2007 Anton Farygin <rider@altlinux.ru> 7.16.4-alt2
- added patch to ftp from sbolshakov@. Fixed anonymous login on some non-standart servers

* Wed Jul 11 2007 Anton Farygin <rider@altlinux.ru> 7.16.4-alt1
- new version with security fixes (CVE-2007-3564)
- disabled kerberos support (by requiest from krb5 mantainer)

* Tue Jul 03 2007 Anton Farygin <rider@altlinux.ru> 7.16.3-alt1
- new version

* Thu Apr 12 2007 Anton Farygin <rider@altlinux.ru> 7.16.2-alt1
- new version

* Mon Feb 12 2007 Anton Farygin <rider@altlinux.ru> 7.16.1-alt3
- fixed curl-config --libs and libcurl.pc (unneeded libs removed)

* Fri Feb 09 2007 Anton Farygin <rider@altlinux.ru> 7.16.1-alt2
- use ca-certificates
- build with gssapi support
- updated build requires

* Wed Jan 31 2007 Anton Farygin <rider@altlinux.ru> 7.16.1-alt1
- new version

* Tue Jan 09 2007 Anton Farygin <rider@altlinux.ru> 7.16.0-alt1
- new version (soname changed)

* Wed Sep 13 2006 Anton Farygin <rider@altlinux.ru> 7.15.5-alt1
- new version

* Fri Mar 24 2006 Anton Farygin <rider@altlinux.ru> 7.15.3-alt1
- new version

* Fri Oct 14 2005 Anton Farygin <rider@altlinux.ru> 7.15.0-alt1
- new version

* Fri Sep 02 2005 Anton Farygin <rider@altlinux.ru> 7.14.1-alt1
- new version

* Tue May 17 2005 Anton Farygin <rider@altlinux.ru> 7.14.0-alt1
- new version

* Fri May 06 2005 Anton Farygin <rider@altlinux.ru> 7.13.2-alt1
- new version

* Fri Mar 04 2005 Anton Farygin <rider@altlinux.ru> 7.13.1-alt1
- 7.13.1

* Mon Feb 07 2005 Anton Farygin <rider@altlinux.ru> 7.13.0-alt2
- lib%name-devel: added requires to libidn-devel libssl-devel zlib-devel

* Tue Feb 01 2005 Anton Farygin <rider@altlinux.ru> 7.13.0-alt1
- new version

* Tue Jan 18 2005 Anton Farygin <rider@altlinux.ru> 7.12.3-alt1
- new version

* Fri Oct 29 2004 Anton Farygin <rider@altlinux.ru> 7.12.2-alt1
- new version

* Fri Oct 15 2004 Anton Farygin <rider@altlinux.ru> 7.12.1-alt1
- new version

* Mon Apr 26 2004 Anton Farygin <rider@altlinux.ru> 7.11.2-alt1
- new version

* Tue Apr 20 2004 Anton Farygin <rider@altlinux.ru> 7.11.1-alt1
- new version

* Thu Mar 18 2004 Anton Farygin <rider@altlinux.ru> 7.11.0-alt1
- new version

* Sun Dec 14 2003 Rider <rider@altlinux.ru> 7.10.8-alt1
- new version

* Wed Apr 30 2003 Rider <rider@altlinux.ru> 7.10.4-alt1
- 7.10.4

* Mon Mar 31 2003 Rider <rider@altlinux.ru> 7.10.3-alt1
- 7.10.3

* Fri Nov 22 2002 Rider <rider@altlinux.ru> 7.10.2-alt1
- new version

* Fri Oct 04 2002 Rider <rider@altlinux.ru> 7.10-alt1
- 7.10

* Fri Jun 14 2002 Rider <rider@altlinux.ru> 7.9.8-alt1
- 7.9.8

* Sat Jun 01 2002 Rider <rider@altlinux.ru> 7.9.7-alt1
- 7.9.7

* Sat Apr 27 2002 Rider <rider@altlinux.ru> 7.9.6-alt1
- 7.9.6

* Wed Mar 27 2002 Rider <rider@altlinux.ru> 7.9.5-alt1
- 7.9.5

* Sat Feb 09 2002 Rider <rider@altlinux.ru> 7.9.4-alt1
- 7.9.4

* Thu Jan 03 2002 Rider <rider@altlinux.ru> 7.9.2-alt1
- 7.9.2
- russian summary and description

* Tue Oct 09 2001 Rider <rider@altlinux.ru> 7.9-alt1
- 7.9

* Fri Aug 24 2001 Rider <rider@altlinux.ru> 7.8.1-alt1
- 7.8.1

* Tue May 22 2001 Alexander Bokovoy <ab@altlinux.ru> 7.7.3-alt2
- Fixed:
    + curl-config moved to libcurl-devel
    + curl-config(1) moved to libcurl-devel

* Tue May 08 2001 Rider <rider@altlinux.ru> 7.7.3-alt1
- 7.7.3

* Wed Apr 25 2001 Rider <rider@altlinux.ru> 7.7.2-alt1
- 7.7.2

* Thu Apr 05 2001 Rider <rider@altlinux.ru> 7.7.1-alt1
- 7.7.1

* Sun Jan 28 2001 Dmitry V. Levin <ldv@fandra.org> 7.6-ipl1mdk
- 7.6

* Sun Jan 21 2001 Dmitry V. Levin <ldv@fandra.org> 7.5.2-ipl2mdk
- RE adaptions.

* Tue Jan  9 2001 DindinX <odin@mandrakesoft.com> 7.5.2-2mdk
- change lisence, according to the author's will (reported by F. Crozat)
- added some sample codes to the -devel package

* Tue Jan  9 2001 DindinX <odin@mandrakesoft.com> 7.5.2-1mdk
- 7.5.2
- small spec updates

* Mon Dec 18 2000 DindinX <odin@mandrakesoft.com> 7.5.1-2mdk
- corrected URL

* Wed Dec 13 2000 DindinX <odin@mandrakesoft.com> 7.5.1-1mdk
- 7.5.1

* Thu Dec 07 2000 Geoffrey lee <snailtalk@mandrakesoft.com> 7.5-2mdk
- manually include fcntl.h, strangely, it has been left out (sucky!!!).

* Mon Dec 04 2000 Geoffrey lee <snailtalk@mandrakesoft.com> 7.5-1mdk
- new and shiny source.
- requires: curl = %%version

* Wed Nov 15 2000 Geoffrey Lee <snailtalk@mandrakesoft.com> 7.4.2-5mdk
- really 7.4.2.
- well we compile with ssl now, so obviously description is wrong (daoudascks)

* Mon Nov 13 2000 Daouda Lo <daouda@mandrakesoft.com> 7.4.2-4mdk
- compiled with ssl (from TitiSux)

* Mon Nov 13 2000 Daouda Lo <daouda@mandrakesoft.com> 7.4.2-3mdk
- relase pre4.

* Fri Nov 10 2000 Lenny Cartier <lenny@mandrakesoft.com> 7.4.2-2mdk
- fiw requires

* Tue Nov 07 2000 Daouda Lo <daouda@mandrakesoft.com> 7.4.2-1mdk
- new release

* Fri Nov 03 2000 DindinX <odin@mandrakesoft.com> 7.4.1-1mdk
- 7.4.1

* Mon Aug 28 2000 Lenny Cartier <lenny@mandrakesoft.com> 7.1-1mdk
- used srpm from Anton Graham <darkimage@bigfoot.com> :
	- new version
	- new -lib and -devel packages

* Mon Aug 28 2000 Lenny Cartier <lenny@mandrakesoft.com> 6.5.2-3mdk
- change description
- clean spec

* Tue Jul 11 2000 Anton Graham <darkimage@bigfoot.com> 6.5.2-2mdk
- Macroification

* Wed May 03 2000 Anton Graham <darkimage@bigfoot.com> 6.5.2-1mdk
- First Mandrake build
