%define major	3
%define maj2	5
%define majqt	3
%define	libcore	%mklibname audcore %{maj2}
%define	libqt	%mklibname audqt %{majqt}
%define	libtag	%mklibname audtag %{major}
%define	libaudgui %mklibname audgui %{maj2}
%define devname %mklibname %{name} -d
%define beta %{nil}

Summary:	A versatile and handy media player
Name:		audacious
Version:	4.4.1
%if "%beta" != ""
Release:	1
%else
Release:	1
%endif
License:	GPLv3+
Group:		Sound
Url:		https://audacious-media-player.org/
Source0:	https://distfiles.audacious-media-player.org/%{name}-%{version}.tar.bz2

BuildRequires:  meson
BuildRequires:	chrpath
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:  pkgconfig(libarchive)
BuildRequires:	pkgconfig(Qt6Core)
BuildRequires:	pkgconfig(Qt6Gui)
BuildRequires:	pkgconfig(Qt6Svg)
BuildRequires:	pkgconfig(Qt6Widgets)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libguess) >= 1.2
BuildRequires:	pkgconfig(libguess) >= 1.2
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(ice)

Requires:	audacious-ui = %{EVRD}
Requires:	audacious-plugins
Recommends:	audacious-pulse

%description
Audacious is a media player based on the BMP music playing application.
Its primary goals are usability and usage of current desktop standards.

%package -n %{libcore}
Group:		System/Libraries
Summary:	Library for %{name}
Obsoletes:	%{_lib}audacious1 < 5:3.3.4-2

%description -n %{libcore}
This package contains the library needed by %{name}.

%package -n %{libqt}
Group:		System/Libraries
Summary:	Qt interface library for %{name}
Conflicts:	%{_lib}audacious1 < 5:3.3.4-2
Provides:	audacious-ui = %{EVRD}

%description -n %{libqt}
This package contains the library needed by
the Qt interface of %{name}.

%package -n %{libtag}
Group:		System/Libraries
Summary:	Library for %{name}
Conflicts:	%{_lib}audacious1 < 5:3.3.4-2

%description -n %{libtag}
This package contains the library needed by %{name}.

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libcore} = %{EVRD}
Requires:	%{libqt} = %{EVRD}
Requires:	%{libtag} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
Audacious is a media player based on the BMP music playing application.
Its primary goals are usability and usage of current desktop standards.
This package contains the files needed for developing applications
which use %{name}.

%prep
%autosetup -p1

%build
#gw: else libid3tag does not build
%define _disable_ld_no_undefined 1
export CC=gcc
export CXX=g++
%meson \
        -Dgtk=false \
        -Dqt=true \
        -Dgtk=true \
        -Dlibarchive=true

%meson_build

%install
%meson_install
chrpath -d %{buildroot}%{_bindir}/*

#desktop-file-install --vendor="" \
#	--add-category="X-Audio" \
#	--dir %{buildroot}%{_datadir}/applications \
#	%{buildroot}%{_datadir}/applications/*

#rm -rf %{buildroot}%{_datadir}/audacious/applications/

%find_lang %{name}

rm -f %{buildroot}%{_includedir}/mp4.h

%files -f %{name}.lang
%doc AUTHORS
%{_bindir}/audtool
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/*
%{_mandir}/man1/*

%files -n %{libcore}
%{_libdir}/libaudcore.so.%{maj2}*
%{_libdir}/libaudgui.so.6*

%files -n %{libqt}
%{_libdir}/libaudqt.so.%{majqt}*

%files -n %{libtag}
%{_libdir}/libaudtag.so.%{major}*

%files -n %{devname}
%{_includedir}/%{name}
%{_includedir}/libaudcore
%{_includedir}/libaudqt
%{_includedir}/libaudgui
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
