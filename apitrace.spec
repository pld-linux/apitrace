#
# Conditional build:
%bcond_without	qt		# Qt GUI
%bcond_without	sse42		# SSE 4.2 instructions

%define		qtver	5.15

Summary:	Tools for tracing OpenGL, Direct3D and other graphics APIs
Name:		apitrace
Version:	12.0
Release:	1
License:	MIT
Group:		Development/Tools
Source0:	https://github.com/apitrace/apitrace/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	822b50a96c10911f474cba51d05ff568
Patch0:		system-libs.patch
Patch1:		no-debian-multiarch.patch
URL:		https://apitrace.github.io/
%if %{with qt}
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Network-devel >= %{qtver}
BuildRequires:	Qt5Widgets-devel >= %{qtver}
%endif
BuildRequires:	cmake >= 3.15.0
BuildRequires:	gtest-devel
BuildRequires:	libbacktrace-devel
BuildRequires:	libbrotli-devel >= 1.0.7
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel >= 6:8
BuildRequires:	pkgconfig
BuildRequires:	python3
BuildRequires:	rpmbuild(macros) >= 1.742
BuildRequires:	snappy-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	zlib-devel >= 1.2.6
Requires:	libbrotli >= 1.0.7
Requires:	zlib >= 1.2.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
apitrace consists of a set of tools to:
- trace OpenGL, Direct3D, and DirectDraw APIs calls to a file
- replay OpenGL and Direct3D calls from a file
- inspect OpenGL and Direct3D state at any call while retracing
- visualize and edit trace files

%package gui
Summary:	Qt based GUI for apitrace
Group:		Development/Tools
Requires:	Qt5Core >= %{qtver}
Requires:	Qt5Network >= %{qtver}
Requires:	Qt5Widgets >= %{qtver}

%description gui
Qt based GUI for apitrace.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1

%{__sed} -i -e '1s,/usr/bin/env python3,%{__python3},' scripts/*.py

%build
%cmake -B build \
	-DENABLE_STATIC_SNAPPY:BOOL=OFF \
	%{cmake_on_off qt ENABLE_GUI} \
	%{cmake_on_off sse42 ENABLE_SSE42}

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# Windows only
%{__rm} $RPM_BUILD_ROOT%{_libdir}/apitrace/scripts/{apitrace.PIXExp,convert.py}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.markdown docs/{BUGS,HACKING,NEWS,USAGE}.markdown
%attr(755,root,root) %{_bindir}/apitrace
%attr(755,root,root) %{_bindir}/eglretrace
%attr(755,root,root) %{_bindir}/glretrace
%attr(755,root,root) %{_bindir}/gltrim
%dir %{_libdir}/apitrace
%dir %{_libdir}/apitrace/scripts
%{_libdir}/apitrace/scripts/*.py
%dir %{_libdir}/apitrace/wrappers
%attr(755,root,root) %{_libdir}/apitrace/wrappers/egltrace.so
%attr(755,root,root) %{_libdir}/apitrace/wrappers/glxtrace.so

%if %{with qt}
%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qapitrace
%endif
