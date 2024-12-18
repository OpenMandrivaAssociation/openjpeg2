# openjpeg2 is used by ghostscript, which is used by libspectre,
# which is used by cairo, which is used by gtk-3.0, which is used
# by wine
%ifarch %{x86_64}
%bcond_without compat32
%endif

%define oname OpenJPEG
%define instnme openjpeg

%define major 7
%define lib_name %mklibname openjp2_ %{major}
%define lib_dev %mklibname %{name} -d
%define lib32name %mklib32name openjp2_ %{major}
%define lib32dev %mklib32name %{name} -d

%global optflags %{optflags} -O3

%define common_description The OpenJPEG library is an open-source JPEG 2000 codec written in C\
language. It has been developed in order to promote the use of JPEG\
2000, the new still-image compression standard from the Joint\
Photographic Experts Group (JPEG).

Name: openjpeg2
Version: 2.5.3
Release: 1
Summary: An open-source JPEG 2000 codec 
License: BSD
Group: System/Libraries
Url: https://www.openjpeg.org/
Source0: https://github.com/uclouvain/openjpeg/archive/v%{version}/%{name}-%{version}.tar.gz
# Remove bundled libraries
Patch0: openjpeg2_remove-thirdparty.patch
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(libtiff-4)
BuildRequires: pkgconfig(lcms2)
BuildRequires: cmake
BuildRequires: doxygen
%if %{with compat32}
BuildRequires:	devel(libpng16)
BuildRequires:	devel(libtiff)
BuildRequires:	devel(liblcms2)
BuildRequires:	devel(libz)
%endif

%description
%{common_description}

%package -n %{lib_name}
Summary: %{oname} library
Group: System/Libraries

%description -n	%{lib_name}
This package contains the library needed to run programs dynamically
linked with the %{oname} library.

%{common_description}

%package -n %{lib_dev}
Summary: Development tools for programs using the %{oname} library
Group: Development/C
Requires: %{lib_name} = %{version}
Requires: %{name} = %{version}
Provides: %{name}-devel = %{version}-%{release}
Conflicts: openjpeg-devel < 2.0.0

%description -n	%{lib_dev}
This package contains the header files and libraries needed for
developing programs using the %{oname} library.

%{common_description}

%if %{with compat32}
%package -n %{lib32name}
Summary: %{oname} library (32-bit)
Group: System/Libraries

%description -n	%{lib32name}
This package contains the library needed to run programs dynamically
linked with the %{oname} library.

%{common_description}

%package -n %{lib32dev}
Summary: Development tools for programs using the %{oname} library (32-bit)
Group: Development/C
Requires: %{lib_dev} = %{EVRD}
Requires: %{lib32name} = %{version}
Requires: %{name} = %{version}
Conflicts: openjpeg-devel < 2.0.0

%description -n	%{lib32dev}
This package contains the header files and libraries needed for
developing programs using the %{oname} library.

%{common_description}
%endif

%prep
%autosetup -n openjpeg-%{version} -p1

# Remove all third party libraries just to be sure
rm -rf thirdparty

%if %{with compat32}
%cmake32 \
  -DCMAKE_BUILD_TYPE=Release \
  -DOPENJPEG_INSTALL_BIN_DIR:PATH=%{_bindir} \
  -DOPENJPEG_INSTALL_DATA_DIR:PATH=%{_datadir} \
  -DOPENJPEG_INSTALL_LIB_DIR:PATH=lib \
  -DBUILD_DOC=OFF
cd ..
%endif

%cmake \
  -DCMAKE_BUILD_TYPE=Release \
  -DOPENJPEG_INSTALL_BIN_DIR:PATH=%{_bindir} \
  -DOPENJPEG_INSTALL_DATA_DIR:PATH=%{_datadir} \
  -DOPENJPEG_INSTALL_LIB_DIR:PATH=%{_lib} \
  -DBUILD_DOC=ON


%build
%if %{with compat32}
%make_build -C build32
%endif
%make_build -C build

%install
%if %{with compat32}
%make_install -C build32
%endif
%make_install -C build
sed -i 's!bindir=${prefix}//usr/bin!bindir=${prefix}/usr/bin!g' %{buildroot}/%{_libdir}/pkgconfig/libopenjp2.pc

rm -rf %{buildroot}%{_docdir}
rm -rf %{buildroot}%{_libdir}/libopenjp2.a

%files
%{_bindir}/*
%{_mandir}/man1/*

%files -n %{lib_name}
%{_libdir}/*.so.%{major}
%{_libdir}/*.so.%{version}

%files -n %{lib_dev}
%doc AUTHORS.md CHANGELOG.md LICENSE NEWS.md README.md THANKS.md
%{_includedir}/*
%{_mandir}/man3/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libopenjp2.pc
%{_libdir}/cmake/openjpeg-*

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/*.so.%{major}
%{_prefix}/lib/*.so.%{version}

%files -n %{lib32dev}
%doc AUTHORS.md CHANGELOG.md LICENSE NEWS.md README.md THANKS.md
%{_prefix}/lib/*.so
%{_prefix}/lib/pkgconfig/libopenjp2.pc
%{_prefix}/lib/cmake/openjpeg-*
%endif
