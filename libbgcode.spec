#
%define commit  bc390aab4427589a6402b4c7f65cf4d0a8f987ec
#
# Conditional build:
%bcond_without	python3
#
Summary:	Prusa Block & Binary G-code reader / writer / converter
Name:		libbgcode
Version:	0.1
Release:	0.1
License:	AGPL v3+
Group:		Libraries
Source0:	https://github.com/prusa3d/libbgcode/archive/%{commit}.zip
# Source0-md5:	a7474c7f4c4090388141e5f070505471
URL:		https://github.com/prusa3d/libbgcode/
BuildRequires:	cmake
%{?with_python3:BuildRequires:	python3-devel}
BuildRequires:	rpmbuild(macros) >= 1.294
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A new G-code file format featuring the following improvements over the
legacy G-code:

- Block structure with distinct blocks for metadata vs. G-code
- Faster navigation
- Coding & compression for smaller file size
- Checksum for data validity
- Extensivity through new (custom) blocks. For example, a file
  signature block may be welcome by corporate customers.

%package devel
Summary:	Header files for libbgcode library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libbgcode
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libbgcode library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libbgcode.

%package static
Summary:	Static libbgcode library
Summary(pl.UTF-8):	Statyczna biblioteka libbgcode
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libbgcode library.

%description static -l pl.UTF-8
Statyczna biblioteka libbgcode.

%package -n python3-libbgcode
Summary:	Python 3 binding for libbgcode library
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki libbgcode
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python3-libbgcode
Python binding for libbgcode library.

%description -n python3-libbgcode -l pl.UTF-8
Wiązania Pythona do biblioteki libbgcode.

%prep
%setup -q -n %{name}-%{commit}

%build
install -d build
cd build
%cmake \
	..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
        DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README.md TODO
%attr(755,root,root) %{_libdir}/libbgcode.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbgcode.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbgcode.so
%{_libdir}/libbgcode.la
%{_includedir}/xtract
%{_pkgconfigdir}/libbgcode.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libbgcode.a

%if %{with python3}
%files -n python3-libbgcode
%defattr(644,root,root,755)
%dir %{py3_sitedir}/libbgcode
%dir %{py3_sitescriptdir}/libbgcode
%{py3_sitescriptdir}/libbgcode/__init__.py[co]
%endif
