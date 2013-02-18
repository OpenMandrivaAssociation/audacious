%define major 1
%define libname %mklibname %{name} %{major}
%define major2 2
%define libname2 %mklibname %{name} %{major2}
%define libname_devel %mklibname %{name} -d

Summary:	A versatile and handy media player
Name:		audacious
Version:	3.3.4
Release:	1
Epoch:		5
License:	GPLv3+
Group:		Sound
Url:		http://audacious-media-player.org/
Source0:	http://distfiles.audacious-media-player.org/%{name}-%{version}.tar.bz2
BuildRequires:	pkgconfig(libmcs)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(libguess)
BuildRequires:	desktop-file-utils
BuildRequires:	chrpath
BuildRequires:	gtk-doc
Suggests:	audacious-pulse
Requires:	audacious-plugins
Requires:	%{libname} = %{EVRD}
Requires:	%{libname2} = %{EVRD}

%description
Audacious is a media player based on the BMP music playing application.
Its primary goals are usability and usage of current desktop standards.

%package -n %{libname}
Group:		System/Libraries
Summary:	Library for %{name}

%description -n %{libname}
Audacious is a media player based on the BMP music playing application.
Its primary goals are usability and usage of current desktop standards.
This package contains the library needed by %{name}.

%package -n %{libname2}
Group:		System/Libraries
Summary:	Library for %{name}

%description -n %{libname2}
Audacious is a media player based on the BMP music playing application.
Its primary goals are usability and usage of current desktop standards.
This package contains the library needed by %{name}.

%package -n %{libname_devel}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Requires:	%{libname2} = %{EVRD}
Provides:	lib%{name}-devel = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{libname_devel}
Audacious is a media player based on the BMP music playing application.
Its primary goals are usability and usage of current desktop standards.
This package contains the files needed for developing applications
which use %{name}.

%prep
%setup -q

%build
#gw: else libid3tag does not build
%define _disable_ld_no_undefined 1
%configure2_5x --enable-chardet

%make

%install
%makeinstall_std
chrpath -d %{buildroot}%{_bindir}/*

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="Audio" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*
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

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{libname2}
%{_libdir}/libaudclient.so.%{major2}*

%files -n %{libname_devel}
%{_includedir}/%{name}
%{_includedir}/libaudcore
%{_includedir}/libaudgui
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

