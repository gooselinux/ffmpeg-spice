%define svn     20080908
%define bump    15.5spice

Summary:        Stripped-down fork of ffmpeg for libspice
Name:           ffmpeg-spice
Version:        0.4.9
Release:        0.%{bump}.%{svn}%{?dist}
License:        GPLv2+
Group:          Applications/Multimedia
URL:            http://ffmpeg.org/
Source0:        %{name}-0.%{bump}.%{svn}-nopatents.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
ExclusiveArch:  %{ix86} x86_64

%{?_with_amr:BuildRequires: amrnb-devel amrwb-devel}
BuildRequires:  zlib-devel
#don't enable until PIC issues on x86_64 are fixed ('ff_imdct_half_sse' in libavcodec/i386/fft_sse.c)
#BuildRequires:  yasm

%description
This is a stripped down version of upstream FFMPEG including only the codecs
used by SPICE in order to avoid inadvertantly bundling or shipping any
encumbered code or binaries.

%package        libs
Summary:        Libraries for %{name}
Group:          System Environment/Libraries

%description    libs
Codec and format libraries for ffmpeg intended for use with the SPICE virtual desktop protocol.

%package        devel
Summary:        Development package for %{name}
Group:          Development/Libraries
Requires:       %{name}-libs = %{version}-%{release}
Requires:       pkgconfig

%description    devel
Codec and format development files for ffmpeg intended for use with
the SPICE virtual desktop protocol.

%prep
%setup -q -n %{name}-%{svn}

%build
./configure \
    --prefix=%{_prefix} \
    --incdir=%{_includedir}/ffmpeg-spice \
    --libdir=%{_libdir} \
    --shlibdir=%{_libdir} \
    --mandir=%{_mandir} \
    --arch=%{_target_cpu} \
    --extra-cflags="$RPM_OPT_FLAGS -D_ISOC99_SOURCE -D_POSIX_C_SOURCE=200112 -fasm -std=c99 -fno-math-errno -fPIC" \
    --disable-demuxers \
    --disable-ffmpeg \
    --disable-ffserver \
    --disable-ffplay \
    --disable-bsfs \
    --disable-parsers \
    --disable-protocols \
    --disable-muxers \
    --disable-decoders \
    --disable-encoders \
    --enable-encoder=mjpeg \
    --enable-decoder=mjpeg \
    --enable-pthreads \
    --disable-static \
    --enable-shared \
    --enable-gpl \
    --disable-stripping \
    --build_suffix=-spice

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT __doc
make install DESTDIR=$RPM_BUILD_ROOT
cp -a doc __doc
rm -f __doc/{Makefile,*.{1,pl,texi}}
rm -rf $RPM_BUILD_ROOT/%{_libdir}/vhook/

%clean
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files libs
%defattr(-,root,root,-)
%doc COPYING.GPL CREDITS Changelog README __doc/*.*
%{_libdir}/libavcodec-spice.so.*
%{_libdir}/libavformat-spice.so.*
%{_libdir}/libavutil-spice.so.*

%files devel
%defattr(-,root,root,-)
# Note: as of 20070204, --incdir doesn't affect postproc.
%{_includedir}/ffmpeg-spice
%{_libdir}/libavcodec-spice.so
%{_libdir}/libavformat-spice.so
%{_libdir}/libavutil-spice.so
%{_libdir}/pkgconfig/libavcodec-spice.pc
%{_libdir}/pkgconfig/libavformat-spice.pc
%{_libdir}/pkgconfig/libavutil-spice.pc


%changelog
* Tue Dec 8 2009 Uri Lublin <uril@redhat.com> - 0.4.9-0.15.5spice.20080908
- Rename package and files from qffmpeg to ffmpeg-spice
- Removed all 'q' prefix from directories/files/libraries.

* Wed Apr 22 2009 Monty <cmontgom@redhat.com> - 0.4.9-0.15.20080908
- Restrict build architectures

* Wed Apr 22 2009 Monty <cmontgom@redhat.com> - 0.4.9-0.14.20080908
- Bump for RHEL-5 branch

* Fri Mar 20 2009 Monty <cmontgom@redhat.com> - 0.4.9-0.13.20080908
- Correct versioning typo in spec
- Remove unused codecs from build (allowing a stright configure to succeed)

* Mon Feb 16 2009 Monty <cmontgom@redhat.com> - 0.4.9-0.12-20080908
- Correct a typo; make force-tag apparently *still* broken

* Mon Feb 16 2009 Monty <cmontgom@redhat.com> - 0.4.9-0.11-20080908
- Update to a new git snapshot: 7ae0395709bda753ff1fb8cecdc2fc77232cab56
- Revert SVN date-- this is not the date of the local repo, it is the date
  of the matching upstream ABI.  Do not change it.

* Tue Jan 27 2009 Eduardo Habkost <ehabkost@redhat.com> - 0.4.9-0.9-20090127
- Update to a new git snapshot: b088e5f2fe594f92e4f2231733125671de7c25d9

* Fri Jan 23 2009 Monty <cmontgom@redhat.com> - 0.4.9-0.8.20080908
Fix missed change in packaged files in spec, make force-tag is broken

* Fri Jan 23 2009 Monty <cmontgom@redhat.com> - 0.4.9-0.7.20080908
Fix a typo, make force-tag is broken

* Fri Jan 23 2009 Monty <cmontgom@redhat.com> - 0.4.9-0.6.20080908
Fix a typo, make force-tag is broken

* Fri Jan 23 2009 Monty <cmontgom@redhat.com> - 0.4.9-0.5.20080908
- Move to a stripped-down form of 0.4.9 maintained locally
- Remove more mpeg-related code
- Move libav->libqav namespace change from specfile to to source build system

* Wed Dec 17 2008 Jon McCann <jmccann@redhat.com> - 0.4.9-0.4.20080908
- Add mpegvideo and mpegvideo_enc back since required

* Wed Dec 17 2008 Jon McCann <jmccann@redhat.com> - 0.4.9-0.3.20080908
- Fix link target names

* Wed Dec 17 2008 Jon McCann <jmccann@redhat.com> - 0.4.9-0.2.20080908
- Fix names in .pc files

* Mon Dec  8 2008 Jon McCann <jmccann@redhat.com> - 0.4.9-0.1.20080908
- 20080908 snapshot (r25261), last before ABI change
- Remove legally questionable codecs
