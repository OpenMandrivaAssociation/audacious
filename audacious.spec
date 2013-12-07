%define major	1
%define maj2	2
%define	libcore	%mklibname audcore %{major}
%define	libgui	%mklibname audgui %{major}
%define	libtag	%mklibname audtag %{major}
%define	libclient	%mklibname audclient %{maj2}
%define devname %mklibname %{name} -d

Summary:	A versatile and handy media player
Name:		audacious
Epoch:		5
Version:	3.4.1
Release:	2
License:	GPLv3+
Group:		Sound
Url:		http://audacious-media-player.org/
Source0:	http://distfiles.audacious-media-player.org/%{name}-%{version}.tar.bz2

BuildRequires:	chrpath
BuildRequires:	desktop-file-utils
BuildRequires:	gtk-doc
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libguess)
BuildRequires:	pkgconfig(libmcs)
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

%description -n %{libgui}
This package contains the library needed by %{name}.

%package -n %{libtag}
Group:		System/Libraries
Summary:	Library for %{name}
Conflicts:	%{_lib}audacious1 < 5:3.3.4-2

%description -n %{libtag}
This package contains the library needed by %{name}.

%package -n %{libclient}
Group:		System/Libraries
Summary:	Library for %{name}
Obsoletes:	%{_lib}audacious2 < 5:3.3.4-2

%description -n %{libclient}
This package contains the library needed by %{name}.

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libcore} = %{EVRD}
Requires:	%{libgui} = %{EVRD}
Requires:	%{libtag} = %{EVRD}
Requires:	%{libclient} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
Audacious is a media player based on the BMP music playing application.
Its primary goals are usability and usage of current desktop standards.
This package contains the files needed for developing applications
which use %{name}.

%prep
%setup -q

%build
#gw: else libid3tag does not build
%define _disable_ld_no_undefined 1
%configure2_5x \
	--enable-chardet

%make

%install
%makeinstall_std
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
%{_libdir}/libaudcore.so.%{major}*

%files -n %{libgui}
%{_libdir}/libaudgui.so.%{major}*

%files -n %{libtag}
%{_libdir}/libaudtag.so.%{major}*

%files -n %{libclient}
%{_libdir}/libaudclient.so.%{maj2}*

%files -n %{devname}
%{_includedir}/%{name}
%{_includedir}/libaudcore
%{_includedir}/libaudgui
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

