%define major	3
%define maj2	5
%define majqt	2
%define	libcore	%mklibname audcore %{maj2}
%define	libgui	%mklibname audgui %{maj2}
%define	libqt	%mklibname audqt %{majqt}
%define	libtag	%mklibname audtag %{major}
%define devname %mklibname %{name} -d
%define beta %{nil}

%bcond_without gtk

Summary:	A versatile and handy media player
Name:		audacious
Version:	4.0
%if "%beta" != ""
Release:	0.%beta.1
%else
Release:	1
%endif
License:	GPLv3+
Group:		Sound
Url:		http://audacious-media-player.org/
Source0:	http://distfiles.audacious-media-player.org/%{name}-%{version}.tar.bz2

BuildRequires:	chrpath
BuildRequires:	desktop-file-utils
BuildRequires:	gtk-doc
BuildRequires:	pkgconfig(dbus-glib-1)
%if %{with gtk}
BuildRequires:	pkgconfig(gtk+-2.0)
%endif
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(libguess) >= 1.2
Requires:	audacious-ui = %{EVRD}
Requires:	audacious-plugins
Suggests:	audacious-pulse

%description
Audacious is a media player based on the BMP music playing application.
Its primary goals are usability and usage of current desktop standards.

%package -n %{libcore}
Group:		System/Libraries
Summary:	Library for %{name}
Obsoletes:	%{_lib}audacious1 < 5:3.3.4-2

%description -n %{libcore}
This package contains the library needed by %{name}.

%package -n %{libgui}
Group:		System/Libraries
Summary:	Library for %{name}
Conflicts:	%{_lib}audacious1 < 5:3.3.4-2
Provides:	audacious-ui = %{EVRD}

%description -n %{libgui}
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
%if %{with gtk}
Requires:	%{libgui} = %{EVRD}
%endif
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
%configure \
	--enable-chardet \
%if %{without gtk}
	--disable-gtk \
%endif
	--enable-qt

%make_build

%install
%make_install
chrpath -d %{buildroot}%{_bindir}/*

desktop-file-install --vendor="" \
	--remove-category="Application" \
	--add-category="Audio" \
	--dir %{buildroot}%{_datadir}/applications \
	%{buildroot}%{_datadir}/applications/*

rm -rf %{buildroot}%{_datadir}/audacious/applications/

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

%if %{with gtk}
%files -n %{libgui}
#{_libdir}/libaudgui.so.%{maj2}*
%endif

%files -n %{libqt}
%{_libdir}/libaudqt.so.%{majqt}*

%files -n %{libtag}
%{_libdir}/libaudtag.so.%{major}*

%files -n %{devname}
%{_includedir}/%{name}
%{_includedir}/libaudcore
%if %{with gtk}
#{_includedir}/libaudgui
%endif
%{_includedir}/libaudqt
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

