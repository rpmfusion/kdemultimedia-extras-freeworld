
Name:    kdemultimedia-extras-freeworld
Version: 4.5.4
Release: 1%{?dist}
Summary: KDE Multimedia applications

Group:   Applications/Multimedia
# see also: http://techbase.kde.org/Policies/Licensing_Policy
License: GPLv2+
URL:     http://www.kde.org/
Source0: ftp://ftp.kde.org/pub/kde/stable/%{version}/src/kdemultimedia-%{version}.tar.bz2

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  ffmpeg-devel
BuildRequires:  glib2-devel
BuildRequires:  kdelibs4-devel >= %{version}
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-devel

Requires: kdelibs4%{?_isa} >= %{_kde4_version}

Provides: kffmpegthumbnailer = %{version}-%{release}
%if 0%{?fedora} && 0%{?fedora} < 15
Obsoletes: kffmpegthumbnailer <= %{version}-%{release}
%endif


%description
This package contains multimedia applications, including:
* KDE ffmpegthumbnailer service


%prep
%setup -q -n kdemultimedia-%{version}


%build

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}/ffmpegthumbs


%install
rm -rf %{buildroot}

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}/ffmpegthumbs


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc COPYING README AUTHORS
%{_kde4_libdir}/kde4/ffmpegthumbs.so
%{_kde4_datadir}/kde4/services/ffmpegthumbs.desktop


%changelog
* Thu Dec 09 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.5.4-1
- 4.5.4
- drop Obsoletes/Provides: ffmpegthumbnailer(-devel)

* Mon Nov 22 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.5.3-2
- Obsoletes: ffmpegthumbnailer-devel too

* Thu Nov 18 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.5.3-1
- 4.5.3

* Fri Oct 15 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.5.2-1
- 4.5.2

* Sun Sep 19 2010 Magnus Tuominen <magnus.tuominen@gmail.com> - 4.5.1-2
- drop patch
- obsolete < 15

* Mon Sep 13 2010 Magnus Tuominen <magnus.tuominen@gmail.com> - 4.5.1-1
- first attempt on kdemultimedia-extras-freeworld
