%define name audacious
%define version 1.5.1
%define svn 0
%define pre 0
%define rel 1
%if %pre
%if %svn
%define release	%mkrel 0.%pre.%svn.%rel
%define fname %name-%svn
%else
%define release	%mkrel 0.%pre.%rel
%define fname %name-%version-%pre
%endif
%else
%define fname %name-%version
%define release %mkrel %rel
%endif
%define major 		1
%define libname 	%mklibname %{name} %{major}
%define libname_devel 	%mklibname %{name} -d

Summary:	A versatile and handy media player
Name:		%name
Version:        %version
Release:	%release
Epoch:		5
Source0:	http://audacious-media-player.org/release/%fname.tbz2
# Patch to make it check ~/.xmms for skins too
Patch1:		audacious-1.5.1-xmms-skins.patch
License:	GPL
Group:		Sound
Url:		http://audacious-media-player.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	libglade2.0-devel
BuildRequires:  libmcs-devel >= 0.4.0
BuildRequires:  libmowgli-devel >= 0.4.0
BuildRequires:	gtk2-devel >= 2.6.0
BuildRequires:	dbus-glib-devel
BuildRequires:  desktop-file-utils
BuildRequires:  chrpath
BuildRequires:  gtk-doc
Requires: audacious-plugins
Requires:	%{libname} = %epoch:%{version}
Provides:	beep-media-player
Obsoletes:	beep-media-player
Requires(post):  desktop-file-utils
Requires(postun):  desktop-file-utils
Suggests: audacious-pulse

%description
Audacious is a media player based on the BMP music playing application.
Its primary goals are usability and usage of current desktop standards.

%package -n %{libname}
Group:		System/Libraries
Summary:	Library for %{name}
Epoch: %epoch

%description -n %{libname}
Audacious is a media player based on the BMP music playing application.
Its primary goals are usability and usage of current desktop standards.
This package contains the library needed by %{name}.

%package -n %{libname_devel}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{epoch}:%{version}
Provides:	lib%{name}-devel = %{epoch}:%{version}-%{release}
Provides:	%{name}-devel = %{epoch}:%{version}-%{release}
Obsoletes:	%mklibname -d %name 5
Epoch: %epoch

%description -n %{libname_devel}
Audacious is a media player based on the BMP music playing application.
Its primary goals are usability and usage of current desktop standards.
This package contains the files needed for developing applications
which use %{name}.

%prep
%if %svn
%setup -q -n %name
%else
%setup -q -n %fname
%endif
%patch1 -p1 -b .ski
#gw add missing file:
#cat > src/audacious/build_stamp.c << EOF
#include <glib.h>
#
#const gchar *svn_stamp = "developer release 4";
#EOF

%if %svn
sh ./autogen.sh
%endif
autoconf

%build
%define _disable_ld_no_undefined 1
%configure2_5x --enable-chardet \
%ifarch %ix86
--disable-sse2 \
%endif

%make
#make documentation-build

%install
rm -rf $RPM_BUILD_ROOT installed-docs
%makeinstall_std
chrpath -d %buildroot%_bindir/*
#mkdir installed-docs
#cp -r doc/audacious/html installed-docs/audacious
#cp -r doc/libaudacious/html installed-docs/libaudacious

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="Audio" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*
rm -rf %buildroot%_datadir/audacious/applications/

%find_lang %name
rm -f %buildroot%_includedir/mp4.h


%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database

%postun
%clean_desktop_database

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%files -f %name.lang
%defattr(0755,root,root,0755)
%_bindir/audtool
%{_bindir}/%name
%defattr(0644,root,root,0755)
%doc AUTHORS NEWS README
%{_datadir}/applications/%name.desktop
%dir %{_datadir}/%name
%dir %{_datadir}/%name/images
%{_datadir}/%name/images/*.png
%{_datadir}/%name/images/*.xpm
%dir %{_datadir}/%name/Skins
%{_datadir}/%name/Skins/*
%{_datadir}/%name/ui/
%{_mandir}/man1/*
%_datadir/pixmaps/%name.png

%files -n %{libname}
%defattr(0644,root,root,0755)
%{_libdir}/*.so.%{major}*

%files -n %{libname_devel}
%defattr(0644,root,root,0755)
#%doc installed-docs/*
%dir %{_includedir}/%name
%{_includedir}/%name/*
%_includedir/libSAD
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
