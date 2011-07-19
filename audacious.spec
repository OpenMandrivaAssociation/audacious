%define name audacious
%define version 3.0
%define svn 0
%define pre 0
%define rel 1
%if %pre
%if %svn
%define release	%mkrel -c %pre.%svn %rel
%define fname %name-%svn
%else
%define release	%mkrel -c  %pre %rel
%define fname %name-%version-%pre
%endif
%else
%define fname %name-%version
%define release %mkrel %rel
%endif
%define major 		1
%define libname 	%mklibname %{name} %{major}
%define major2 		2
%define libname2 	%mklibname %{name} %{major2}
%define libname_devel 	%mklibname %{name} -d

Summary:	A versatile and handy media player
Name:		%name
Version:        %version
Release:	%release
Epoch:		5
Source0:	http://distfiles.atheme.org/%fname.tar.bz2
# Patch to make it check ~/.xmms for skins too
Patch1:		audacious-1.5.1-xmms-skins.patch
License:	GPLv3+
Group:		Sound
Url:		http://audacious-media-player.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:  libmcs-devel >= 0.4.0
BuildRequires:  libmowgli-devel >= 0.9
BuildRequires:	gtk2-devel >= 2.6.0
#BuildRequires:	gtk3-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	libguess-devel
BuildRequires:  desktop-file-utils
BuildRequires:  chrpath
BuildRequires:  gtk-doc
Suggests: audacious-pulse
Requires: audacious-plugins
Requires:	%{libname} = %epoch:%{version}
Requires:	%{libname2} = %epoch:%{version}
Provides:	beep-media-player
Obsoletes:	beep-media-player
Requires(post):  desktop-file-utils
Requires(postun):  desktop-file-utils

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

%package -n %{libname2}
Group:		System/Libraries
Summary:	Library for %{name}
Epoch: %epoch

%description -n %{libname2}
Audacious is a media player based on the BMP music playing application.
Its primary goals are usability and usage of current desktop standards.
This package contains the library needed by %{name}.

%package -n %{libname_devel}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{epoch}:%{version}
Requires:	%{libname2} = %{epoch}:%{version}
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
%if %svn
sh ./autogen.sh
%endif

%build
#gw: else libid3tag does not build
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

%files -f %name.lang
%defattr(0755,root,root,0755)
%_bindir/audtool
%{_bindir}/%{name}
%defattr(0644,root,root,0755)
%doc AUTHORS NEWS README
%{_datadir}/applications/%{name}.desktop
%dir %{_datadir}/%name
%dir %{_datadir}/%name/images
%{_datadir}/%name/images/*.png
%{_datadir}/%name/images/*.xpm
%_datadir/pixmaps/audacious.*
%_datadir/icons/hicolor/*/apps/*
%{_mandir}/man1/*

%files -n %{libname}
%defattr(0644,root,root,0755)
%{_libdir}/*.so.%{major}*

%files -n %{libname2}
%defattr(0644,root,root,0755)
%_libdir/libaudclient.so.%{major2}*

%files -n %{libname_devel}
%defattr(0644,root,root,0755)
%dir %{_includedir}/%name
%{_includedir}/libaudcore
%{_includedir}/libaudgui

%{_includedir}/%name/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
