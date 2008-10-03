
# For the files list and SELinux scriptlets.
%define libmpeg %{_libdir}/libmpeg-0.3.0.so

Epoch:	 6
Version: 3.5.10
Release: 1%{?dist}

License: GPLv2+
Name:    kdemultimedia-extras-freeworld
Summary: Freeworld extras for KDE multimedia applications
Group:   Applications/Multimedia
Url:     http://www.kde.org/
Source0: ftp://ftp.kde.org/pub/kde/stable/%{version}/src/kdemultimedia-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot-%(%{__id_u} -n)

%if 0%{?fedora} > 6 
Requires: kdemultimedia3 >= %{version}
BuildRequires: kdelibs3-devel >= %{version}
%else
Requires: kdemultimedia-extras >= 6:%{version}
BuildRequires: kdelibs-devel >= 6:%{version}
%endif
Requires: akode-extras
Requires(hint): xine-lib-extras-freeworld

Obsoletes: kdemultimedia-extras < 6:3.5.0-0.lvn.2
Provides: kdemultimedia-mp3 = %{epoch}:%{version}-%{release}

# upgrade livna -> rpmfusion
Obsoletes: kdemultimedia-extras-nonfree < 6:3.5.9-2
Provides:  kdemultimedia-extras-nonfree = %{epoch}:%{version}-%{release}

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%if 0%{?fedora} > 4 || 0%{?rhel} > 4
BuildRequires: libXxf86dga-devel libXxf86vm-devel
%endif
BuildRequires: akode-devel akode-extras
BuildRequires: taglib-devel libmad-devel lame-devel

%description
This package includes additional files which extend kdemultimedia 
, e.g. with mp3/MPEG playback, including:
* akode_artsplugin (akode-extras)
* krec mp3 export (lame)
* mpeglib_artsplugin
* xine_artsplugin (xine-lib-extras-freeworld)


%prep
%setup -q -n kdemultimedia-%{version}


%build
unset QTDIR || : ; . /etc/profile.d/qt.sh

%configure \
  --disable-debug --disable-warnings \
  --disable-rpath \
  --includedir=%{_includedir}/kde \
  --enable-final \
  --disable-cdparanoia \
  --with-lame

for dir in \
    arts krec krec/mp3_export \
    akode_artsplugin \
    mpeglib \
    mpeglib_artsplug \
; do
    make %{?_smp_mflags} -C $dir
done 


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT

%define mytmp1 __buildroot_ls-lR
for dir in \
    krec/mp3_export \
    akode_artsplugin \
    mpeglib \
    mpeglib_artsplug \
; do
    find $RPM_BUILD_ROOT | sed -e "s!$RPM_BUILD_ROOT!!" > $(pwd)/%{mytmp1}.1
    make -C $dir DESTDIR=$RPM_BUILD_ROOT install
    find $RPM_BUILD_ROOT | sed -e "s!$RPM_BUILD_ROOT!!" > $(pwd)/%{mytmp1}.2
    diff -Nu $(pwd)/%{mytmp1}.1 $(pwd)/%{mytmp1}.2 || :
done

## omit (conflicting) bits we don't want
# -devel(type) bits
rm -rf $RPM_BUILD_ROOT%{_includedir}/kde/{mpeglib,mpeglib_artsplug}
# -extras bits
rm -f $RPM_BUILD_ROOT%{_libdir}/mcop/akodearts.mcop{class,type}
rm -f $RPM_BUILD_ROOT%{_libdir}/mcop/akode{,MPC,SpeexStream,VorbisStream,Xiph}PlayObject.mcopclass
rm -f $RPM_BUILD_ROOT%{_libdir}/libarts_akode.*


%post
/sbin/ldconfig
/usr/sbin/semanage fcontext -f -- -a -t textrel_shlib_t '%{libmpeg}' 2>/dev/null || :
/usr/bin/chcon -t textrel_shlib_t %{libmpeg} 2>/dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then  # erase?
    /usr/sbin/semanage fcontext -f -- -d -t textrel_shlib_t '%{libmpeg}' 2>/dev/null || :
fi


%check
# If this fails, the library name has changed, and the SELinux scripts
# need an update as we don't want to set the security context for files
# we don't own.
[ -f ${RPM_BUILD_ROOT}%{libmpeg} ]


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README
%{_bindir}/yaf-cdda
%{_bindir}/yaf-mpgplay
%{_bindir}/yaf-splay
%{_bindir}/yaf-tplay
%{_bindir}/yaf-vorbis
%{_bindir}/yaf-yuv
%{_libdir}/libyafcore.[ls][ao]
%{_libdir}/libyafxplayer.[ls][ao]
%{_libdir}/kde3/libkrecexport_mp3.[ls][ao]
%{_datadir}/services/krec_exportmp3.desktop
## (akode|mpeglib|xine)_artsplugin (nonfree bits)
#files artsplugin
#defattr(-,root,root,-)
%{_bindir}/mpeglibartsplay
%{_libdir}/libarts_mpeglib-0.3.0.so.*
%{_libdir}/libarts_splay.so.*
%{libmpeg}
%{_libdir}/mcop/CDDAPlayObject.mcopclass
%{_libdir}/mcop/MP3PlayObject.mcopclass
%{_libdir}/mcop/NULLPlayObject.mcopclass
%{_libdir}/mcop/OGGPlayObject.mcopclass
%{_libdir}/mcop/SplayPlayObject.mcopclass
%{_libdir}/mcop/WAVPlayObject.mcopclass
%{_libdir}/mcop/akodeMPEGPlayObject.mcopclass
%if 0%{?fedora} > 4
%{_libdir}/mcop/akodeFFMPEGPlayObject.mcopclass
%endif
## FIXME: devel-type stuff?, omit from packaging? -- Rex
%{_libdir}/libarts_mpeglib.[ls][ao]
%{_libdir}/libarts_splay.[ls][ao]
%{_libdir}/libmpeg.[ls][ao]


%changelog
* Fri Oct 03 2008 Rex Dieter <rdieter@fedoraproject.org> - 6:3.5.10-1
- kde-3.5.10
- for rpmfusion

* Sat Feb 16 2008 Rex Dieter <rdieter@fedoraproject.org> - 6:3.5.9-1
- kde-3.5.9

* Wed Oct 31 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 6:3.5.8-1
- kde-3.5.8

* Mon Aug 13 2007 Rex Dieter <rdieter[AT]users.sf.net> - 6:3.5.7-3
- Requires: kdemultimedia3 (f7+)
- Requires(hint): xine-lib-extras-nonfree

* Mon Aug 13 2007 Rex Dieter <rdieter[AT]users.sf.net> - 6:3.5.7-2
- omit kfile_mpeg (moving to kdemultimedia/kdemultimedia-extras)
- License: GPLv2+

* Tue Jun 12 2007 Rex Dieter <rdieter[AT]users.sf.net> - 6:3.5.7-1
- kde-3.5.7

* Wed May 09 2007 Rex Dieter <rdieter[AT]users.sf.net> - 6:3.5.6-6
- fc7+: no longer Requires: kdemm-extras

* Fri Mar  9 2007 Michael Schwendt <mschwendt[AT]users.sf.net> - 6:3.5.6-5
- Change security context of libmpeg-0.3.0* to textrel_shlib_t
  as it contains lots of hand-written assembler code (#1435)
  without relative addressing.
- Require the minimum version of kdemultimedia-extras which contains
  files previously included in this package.

* Thu Mar 08 2007 Rex Dieter <rexdieter[AT]users.sf.net> - 6:3.5.6-4
- +Epoch:6, there's pkgs in the wild already *with* Epoch.  Yes, Epoch's 
  suck, my bad, but at least no kittens were harmed.
- update %%description

* Mon Feb 12 2007 Rex Dieter <rexdieter[AT]users.sf.net> - 3.5.6-3
- 3.5.6
- drop xine_artsplugin, kfile_mp3 (moved to -extras pkg)
- omit juk bits

* Wed Jan 10 2007 Michael Schwendt <mschwendt[AT]users.sf.net> - 3.5.5-2
- Rebuild with %%make_cvs 0, else requires automake 1.6.1 or newer.

* Wed Nov  1 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 3.5.5-1
- Update to 3.5.5 (kfile_mpeg affected e.g.).

* Sun Oct  8 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 3.5.4-1
- Update to 3.5.4.

* Sun Apr  2 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 3.5.1-2
- Rebuild with updated akode-extras and R akode-extras kdemultimedia-extras

* Thu Mar 16 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 6:3.5.1-1
- Update to 3.5.1.
- Rename package to kdemultimedia-extras-nonfree.
- Drop Epoch 6 and treat this as a completely new package.
- Define QTLIB/QTINC to be safe in multilib environments.
- BR lame-devel  to please the configure check and for krec/mp3_export.
- BR akode-devel akode-extras  to please the akode checks and
  installation of extra files.

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Sun Dec 18 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 6:3.5.0-0.lvn.1
- Update to 3.5.0.

* Mon Aug  1 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 6:3.4.2-0.lvn.1
- Update to 3.4.2.
- Add switch for building/including Juk.

* Thu Jul 14 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 6:3.4.1-0.lvn.1
- Update to 3.4.1.
- Copy admin.visibility (+ no gcc4 blacklisting) patch from FC4 update.
- BR xine-lib-devel and build/include more video stuff.

* Wed May 11 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 6:3.4.0-0.lvn.3
- Really drop obsolete -vorbis patch.

* Mon Apr 25 2005 Dams <anvil[AT]livna.org> - 6:3.4.0-0.lvn.2
- Fix url in Source tag

* Thu Mar 24 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 6:3.4.0-0.lvn.1
- Update to 3.4.0 (stay in sync with Fedora Core development).

* Tue Dec  7 2004 Michael Schwendt <mschwendt[AT]users.sf.net> - 6:3.3.1-0.lvn.3
- Don't build mpg123 plugin.

* Sun Dec  5 2004 Michael Schwendt <mschwendt[AT]users.sf.net> - 6:3.3.1-0.lvn.2
- Include a few more files.

* Sat Dec  4 2004 Michael Schwendt <mschwendt[AT]users.sf.net> - 6:3.3.1-0.lvn.1
- Create initial version based on a heavily stripped and modified
  kdemultimedia package from Fedora Core 3 (the previous changelog
  entry just for reference).

* Wed Oct 13 2004 Than Ngo <than@redhat.com> 6:3.3.1-1
- update to 3.3.1
