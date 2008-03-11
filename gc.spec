Summary:	The Boehm-Demers-Weiser conservative garbage collector
Summary(pl.UTF-8):	Konserwatywny odśmiecacz pamięci Boehma-Demersa-Weisera
Name:		gc
Version:	7.0
Release:	2
License:	BSD-like
Group:		Libraries
Source0:	http://www.hpl.hp.com/personal/Hans_Boehm/gc/gc_source/%{name}-%{version}.tar.gz
# Source0-md5:	3645ccf5f32ebb27d99b27b0d29e9c38
Patch0:		%{name}-sparc.patch
Patch1:		%{name}-malloc-segv.patch
URL:		http://www.hpl.hp.com/personal/Hans_Boehm/gc/
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	libatomic_ops
BuildRequires:	libtool
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

%prep
%setup -q
%patch0 -p1
%patch1 -p1

# kill libtool.m4 inclusion
%{__perl} -pi -e 's/^sinclude.*//' acinclude.m4

%{__perl} -pi -e 's/^dist_pkgdata_DATA/EXTRA_DIST/' doc/doc.am

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
%ifnarch sparc64
	CPPFLAGS="-DUSE_LIBC_PRIVATES" \
%endif
	--enable-threads=posix
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_includedir}/gc/private
install -D doc/gc.man $RPM_BUILD_ROOT%{_mandir}/man3/gc.3
# are these still needed? (what is ecls?)
install include/private/* $RPM_BUILD_ROOT%{_includedir}/gc/private

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.QUICK doc/README{,.{linux,changes,contributors,environment,macros}}
%doc doc/*.html
%attr(755,root,root) %{_libdir}/libcord.so.*.*.*
%attr(755,root,root) %{_libdir}/libgc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcord.so.1
%attr(755,root,root) %ghost %{_libdir}/libgc.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcord.so
%attr(755,root,root) %{_libdir}/libgc.so
%{_libdir}/libcord.la
%{_libdir}/libgc.la
%{_includedir}/gc
%{_pkgconfigdir}/bdw-gc.pc
%{_mandir}/man3/gc.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libcord.a
%{_libdir}/libgc.a
