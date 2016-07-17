Summary:	The Boehm-Demers-Weiser conservative garbage collector
Summary(pl.UTF-8):	Konserwatywny odśmiecacz pamięci Boehma-Demersa-Weisera
Name:		gc
Version:	7.4.4
Release:	1
License:	BSD-like
Group:		Libraries
Source0:	http://www.hboehm.info/gc/gc_source/%{name}-%{version}.tar.gz
# Source0-md5:	96d18b0448a841c88d56e4ab3d180297
URL:		http://www.hboehm.info/gc/
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake
BuildRequires:	libatomic_ops-devel >= %{version}
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
Requires:	libatomic_ops >= %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gc is a conservative garbage collector for C and C++. It is used as a
replacement for standard malloc() and free(). GC_malloc will attempt
to reclaim inaccessible space automatically by invoking a conservative
garbage collector at appropriate points.

%description -l pl.UTF-8
Gc jest konserwatywnym odśmiecaczem pamięci dla C i C++. Jest używany
jako zamiennik dla standardowych funkcji malloc() i free(). GC_malloc
próbuje odzyskać niedostępna pamięć automatycznie przez wywoływanie
konserwatywnego odśmiecacza pamięci w odpowiednich miejscach.

%package devel
Summary:	Headers for conservative garbage collector
Summary(pl.UTF-8):	Nagłówki dla konserwatywnego odśmiecacza pamięci
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libatomic_ops-devel >= %{version}

%description devel
Headers for conservative garbage collector

%description devel -l pl.UTF-8
Nagłówki dla konserwatywnego odśmiecacza pamięci

%package static
Summary:	Static version of gc library
Summary(pl.UTF-8):	Statyczna wersja biblioteki gc
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static version of gc library

%description static -l pl.UTF-8
Statyczna wersja biblioteki gc

%package c++
Summary:	C++ interface to GC library
Summary(pl.UTF-8):	Interfejs C++ do biblioteki GC
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description c++
C++ interface to GC library.

%description c++ -l pl.UTF-8
Interfejs C++ do biblioteki GC.

%package c++-devel
Summary:	Header files for C++ interface for GC library
Summary(pl.UTF-8):	Pliki nagłówkowe interfejsu C++ do biblioteki GC
Group:		Development/Libraries
Requires:	%{name}-c++ = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}
Requires:	libstdc++-devel

%description c++-devel
Header files for C++ interface for GC library.

%description c++-devel -l pl.UTF-8
Pliki nagłówkowe interfejsu C++ do biblioteki GC.

%package c++-static
Summary:	C++ interface to GC library - static library
Summary(pl.UTF-8):	Interfejs C++ do biblioteki GC - biblioteka statyczna
Group:		Development/Libraries
Requires:	%{name}-c++-devel = %{version}-%{release}

%description c++-static
C++ interface to GC library - static library.

%description c++-static -l pl.UTF-8
Interfejs C++ do biblioteki GC - biblioteka statyczna.

%prep
%setup -q

# don't install docs to %{_datadir}/%{name}
%{__perl} -pi -e 's/^dist_pkgdata_DATA/EXTRA_DIST/' doc/doc.am

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
%ifnarch sparc64
	CPPFLAGS="%{rpmcppflags} -DUSE_LIBC_PRIVATES" \
%endif
	--enable-cplusplus \
	--enable-threads=posix \
	--with-libatomic-ops
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_includedir}/gc/private
install -D -p doc/gc.man $RPM_BUILD_ROOT%{_mandir}/man3/gc.3
# are these still needed? (what is ecls?)
cp -a include/private/* $RPM_BUILD_ROOT%{_includedir}/gc/private

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post   c++ -p /sbin/ldconfig
%postun c++ -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.QUICK README.md doc/README.{cords,environment,linux,macros}
%attr(755,root,root) %{_libdir}/libcord.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcord.so.1
%attr(755,root,root) %{_libdir}/libgc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgc.so.1

%files devel
%defattr(644,root,root,755)
%doc doc/*.html
%attr(755,root,root) %{_libdir}/libcord.so
%attr(755,root,root) %{_libdir}/libgc.so
%{_libdir}/libcord.la
%{_libdir}/libgc.la
%dir %{_includedir}/gc
%{_includedir}/gc/private
%{_includedir}/gc/cord.h
%{_includedir}/gc/cord_pos.h
%{_includedir}/gc/ec.h
%{_includedir}/gc/gc.h
%{_includedir}/gc/gc_allocator.h
%{_includedir}/gc/gc_backptr.h
%{_includedir}/gc/gc_config_macros.h
%{_includedir}/gc/gc_disclaim.h
%{_includedir}/gc/gc_gcj.h
%{_includedir}/gc/gc_inline.h
%{_includedir}/gc/gc_mark.h
%{_includedir}/gc/gc_pthread_redirects.h
%{_includedir}/gc/gc_tiny_fl.h
%{_includedir}/gc/gc_typed.h
%{_includedir}/gc/gc_version.h
%{_includedir}/gc/javaxfc.h
%{_includedir}/gc/leak_detector.h
%{_includedir}/gc/weakpointer.h
%{_includedir}/gc.h
%{_pkgconfigdir}/bdw-gc.pc
%{_mandir}/man3/gc.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libcord.a
%{_libdir}/libgc.a

%files c++
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgccpp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgccpp.so.1

%files c++-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgccpp.so
%{_libdir}/libgccpp.la
%{_includedir}/gc/gc_cpp.h
%{_includedir}/gc_cpp.h

%files c++-static
%defattr(644,root,root,755)
%{_libdir}/libgccpp.a
