Summary:	Conservative garbage collector
Summary(pl):	Konserwatywny od�miecacz pami�ci
Name:		gc
Version:	6.3
Release:	1
License:	BSD-like
Group:		Development/Libraries
Source0:	http://www.hpl.hp.com/personal/Hans_Boehm/gc/gc_source/%{name}%{version}.tar.gz
# Source0-md5:	8b37ee18cbeb1dfd1866958e280db871
Patch0:		%{name}-ac_libdl_fix.patch
URL:		http://www.hpl.hp.com/personal/Hans_Boehm/gc/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gc is a conservative garbage collector for C and C++. It is used as a
replacement for standard malloc() and free(). GC_malloc will attempt
to reclaim inaccessible space automatically by invoking a conservative
garbage collector at appropriate points.

%description -l pl
Gc jest konserwatywnym od�miecaczem pami�ci dla C i C++. Jest u�ywany
jako zamiennik dla standardowych funkcji malloc() i free(). GC_malloc
pr�buje odzyska� niedost�pna pami�c automatycznie przez wywo�ywanie
konserwatywnego od�miecacza pami�ci w odpowiednich miejscach.

%package devel
Summary:	Headers for conservative garbage collector
Summary(pl):	Nag��wki dla konserwatywnego od�miecacza pami�ci
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Headers for conservative garbage collector

%description devel -l pl
Nag��wki dla konserwatywnego od�miecacza pami�ci

%package static
Summary:	Static version of gc library
Summary(pl):	Statyczna wersja biblioteki gc
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static version of gc library

%description static -l pl
Statyczna wersja biblioteki gc

%prep
%setup -q -n %{name}%{version}
%patch0 -p1

%build
rm -f acinclude.m4
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--enable-threads=posix
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir}/gc,%{_mandir}/man3}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f include/Makefile*
cp -ar include/* $RPM_BUILD_ROOT%{_includedir}/gc
install doc/gc.man $RPM_BUILD_ROOT%{_mandir}/man3/gc.3

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.QUICK doc/README{,.{linux,changes,contributors,environment,macros}}
%doc doc/*.html
%attr(755,root,root) %{_libdir}/*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/gc
%{_mandir}/man3/gc.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
