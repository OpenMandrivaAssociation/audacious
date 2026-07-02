#gw: else libid3tag won't not build
#global _disable_ld_no_undefined 0

%bcond_without gtk

%define major	4
%define maj2	6
%define majqt	4
%define majgtk	7
%define	libcore	%mklibname audcore %{maj2}
%define	libqt	%mklibname audqt %{majqt}
%define	libtag	%mklibname audtag %{major}
%define	libaudgui %mklibname audgui %{majgtk}
%define devname %mklibname %{name} -d

Summary:	A versatile and handy media player
Name:	audacious
Version:	4.6.1
Release:	%{?beta:0.%{beta}.}1
License:	GPLv3+
Group:	Sound
Url:		https://audacious-media-player.org/
Source0:	https://distfiles.audacious-media-player.org/%{name}-%{version}.tar.bz2
BuildRequires:	chrpath
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	meson
BuildRequires:	ninja
BuildRequires:	pkgconfig(glib-2.0)
%if %{with gtk}
BuildRequires:	pkgconfig(gtk+-3.0)
%endif
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(libarchive)
BuildRequires:	pkgconfig(libguess) >= 1.2
BuildRequires:	pkgconfig(Qt6Core)
BuildRequires:	pkgconfig(Qt6Gui)
BuildRequires:	pkgconfig(Qt6Svg)
BuildRequires:	pkgconfig(Qt6Widgets)
BuildRequires:	pkgconfig(sm)

Requires:	audacious-ui = %{EVRD}
Requires:	audacious-plugins
Recommends:	audacious-pulse

%description
Audacious is a media player based on the BMP music playing application.
Its primary goals are usability and usage of current desktop standards.

%files -f %{name}.lang
%doc AUTHORS
%{_bindir}/audtool
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/metainfo/%{name}.metainfo.xml
%{_iconsdir}/hicolor/*/apps/*
%{_mandir}/man1/*

#-----------------------------------------------------------------------------

%package -n %{libcore}
Group:		System/Libraries
Summary:	Library for %{name}
%rename	%{_lib}audacious1

%description -n %{libcore}
This package contains the library needed by %{name}.

%files -n %{libcore}
%{_libdir}/libaudcore.so.%{maj2}*

#-----------------------------------------------------------------------------

%package -n %{libqt}
Group:		System/Libraries
Summary:	Qt interface library for %{name}
Provides:	audacious-ui = %{EVRD}

%description -n %{libqt}
This package contains the library needed by
the Qt interface of %{name}.

%files -n %{libqt}
%{_libdir}/libaudqt.so.%{majqt}*

#-----------------------------------------------------------------------------

%package -n %{libaudgui}
Group:		System/Libraries
Summary:	GTK interface library for %{name}
Provides:	audacious-ui = %{EVRD}

%description -n %{libaudgui}
This package contains the library needed by the GTK interface
of %{name}.

%files -n %{libaudgui}
%if %{with gtk}
%{_libdir}/libaudgui.so.%{majgtk}*
%endif

#-----------------------------------------------------------------------------

%package -n %{libtag}
Group:		System/Libraries
Summary:	Library for %{name}

%description -n %{libtag}
This package contains the library needed by %{name}.

%files -n %{libtag}
%{_libdir}/libaudtag.so.%{major}*

#-----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libcore} = %{EVRD}
Requires:	%{libqt} = %{EVRD}
%if %{with gtk}
Requires:	%{libaudgui} = %{EVRD}
%endif
Requires:	%{libtag} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
Audacious is a media player based on the BMP music playing application.
Its primary goals are usability and usage of current desktop standards.
This package contains the files needed for developing applications
which use %{name}.

%files -n %{devname}
%{_includedir}/%{name}
%{_includedir}/libaudcore
%{_includedir}/libaudqt
%if %{with gtk}
%{_includedir}/libaudgui
%{_libdir}/libaudgui.so
%endif
%{_libdir}/libaudcore.so
%{_libdir}/libaudqt.so
%{_libdir}/libaudtag.so
%{_libdir}/pkgconfig/%{name}.pc

#-----------------------------------------------------------------------------

%prep
%autosetup -p1


%build
#export CC=gcc
#export CXX=g++
%meson \
%if %{with gtk}
        -Dgtk=true \
%else
        -Dgtk=false \
%endif
        -Dqt=true \
        -Dlibarchive=true

%meson_build


%install
%meson_install

# Drop unwanted stuff
rm -f %{buildroot}%{_includedir}/mp4.h

chrpath -d %{buildroot}%{_bindir}/*

desktop-file-edit --remove-key="Version" \
				%{buildroot}%{_datadir}/applications/%{name}.desktop

%find_lang %{name}
