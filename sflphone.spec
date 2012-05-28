%define major 4
%define libqtsflphone %mklibname qtsflphone %{major}
%define libqtsflphonedevel %mklibname qtsflphone -d

Summary:	A robust standards-compliant enterprise softphone
Name:		sflphone
Version:	1.1.0
Release:	1
Url:		http://www.sflphone.org/
Source0:	https://projects.savoirfairelinux.com/attachments/download/2865/%{name}-%{version}.tar.gz
# pjsip is GPLv2+; sflphone-common is GPLv3+
License:	GPLv2+ and GPLv3+
Group:		Communications
Patch0:		sflphone-1.1.0-mdv-glib.patch
BuildRequires:	openssl-devel libcommoncpp-devel yaml-devel celt-devel
BuildRequires:	ccrtp-devel pkgconfig(libzrtpcpp) astyle gsm-devel
BuildRequires:	pkgconfig(samplerate) pkgconfig(alsa) pulseaudio-devel speex-devel
BuildRequires:	pkgconfig(uuid) dbus-devel pkgconfig(expat)
BuildRequires:	dbus-glib-devel pkgconfig(libnotify) gtk+3-devel glib2-devel
BuildRequires:	webkitgtk3-devel pkgconfig(libgnomeui-2.0) gnome-doc-utils
BuildRequires:	evolution-data-server-devel check-devel >= 0.9.4
BuildRequires:	pcre-devel
BuildRequires:	cmake
BuildRequires:	kdepim4-devel
BuildRequires:	dbus-c++-devel
BuildRequires:	pkgconfig(libebook-1.2)
BuildRequires:	gnome-doc-utils-devel
BuildRequires:	rarian
Suggests:	%{name}-client

%description
SFLphone is a robust standards-compliant enterprise softphone, for desktop and
embedded systems. It is designed to handle several hundreds of calls a day.

Features highlight:
  o  UI-independant telephony core
  o  Enterprise scalability functions
  o  GNOME, KDE and CLI clients
  o  SIP and IAX2 protocols support
  o  Multi-line, call transfer, call hold, call recording
  o  Multi-way conferencing
  o  High definition audio codecs
  o  Signalling and voice encryption (TLS, SRTP)
  o  Pulseaudio support

%package plugins
Summary: A robust standards-compliant enterprise softphone
License: GPLv3+
Requires: %{name}

%description plugins
Plugins for SFLphone software phone.

%package client-gnome
Summary: A robust standards-compliant enterprise softphone
License: GPLv3+
Requires: %{name}
Provides: %{name}-client = %{EVRD}

%description client-gnome
This package contains the GNOME client for SFLphone.

%package client-kde
Summary: A robust standards-compliant enterprise softphone
License: GPLv3+
Requires: %{name}
Provides: %{name}-client = %{EVRD}

%description client-kde
This package contains the KDE client for SFLphone.

%package -n %{libqtsflphone}
Summary: Qt library for SFLphone client
License: GPLv3+

%description -n %{libqtsflphone}
This package contains the Qt library for SFLphone.

%package -n %{libqtsflphonedevel}
Summary: Qt library for SFLphone client
License: GPLv3+
Requires: %{libqtsflphone} = %{version}
Provides: qtsflphone-devel = %{EVRD}

%description -n %{libqtsflphonedevel}
This package contains Qt development files for SFLphone.

%prep
%setup -q
%patch0 -p1
#find kde/ -type f -not -name '*.sh' -exec chmod a-x {} \;

%build
pushd daemon/libs/pjproject
%configure2_5x --enable-libsamplerate
make dep
make
popd

pushd daemon
./autogen.sh
%configure2_5x
%make
popd

pushd plugins
./autogen.sh
%configure2_5x
%make
popd

pushd gnome
./autogen.sh
%configure2_5x --disable-schemas-install --disable-silent-rules
%make
popd

#pushd kde
#cmake
#make
#popd

%install
%makeinstall_std -C daemon
%makeinstall_std -C plugins
%makeinstall_std -C gnome
#makeinstall_std -C kde/build

%find_lang %{name}-client-gnome --with-gnome
#find_lang %{name}-client-kde --with-kde

%files
%doc daemon/AUTHORS daemon/NEWS daemon/README daemon/TODO
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/codecs/
%{_libdir}/%{name}/sflphoned
%{_datadir}/dbus-1/services/org.sflphone.SFLphone.service
%{_mandir}/man1/sflphoned*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/ringtones/

%files plugins
%doc plugins/AUTHORS plugins/NEWS plugins/README
%{_libdir}/%{name}/plugins/

%files client-gnome -f %{name}-client-gnome.lang
%doc gnome/AUTHORS gnome/README gnome/NEWS
%{_sysconfdir}/gconf/schemas/sflphone-client-gnome.schemas
%{_bindir}/%{name}
%{_bindir}/%{name}-client-gnome
%{_datadir}/applications/%{name}.desktop
%{_datadir}/gnome/help/%{name}/
%{_mandir}/man1/sflphone.1*
%{_mandir}/man1/sflphone-client-gnome.1*
%{_datadir}/omf/%{name}/
%{_datadir}/pixmaps/%{name}.svg
%{_datadir}/%{name}/*.svg
%{_datadir}/%{name}/*.gif
%{_datadir}/%{name}/ui/
%{_datadir}/%{name}/webkit/

#files client-kde -f %{name}-client-kde.lang
#doc kde/AUTHORS kde/NEWS kde/README
#%{_bindir}/%{name}-client-kde
#%{_kde_appsdir}/*
#%{_kde_libdir}/kde4/*
#%{_kde_applicationsdir}/*
#%{_mandir}/man1/sflphone-client-kde.1*
#%{_kde_services}/*
#%{_iconsdir}/hicolor/*/apps/sflphone-client-kde.*
#%{_kde_docdir}/HTML/en/*
#%{_datadir}/config.kcfg/sflphone-client-kde.kcfg

#files -n %{libqtsflphone}
#%{qt4lib}/libqtsflphone.so.%{major}
#%{qt4lib}/libqtsflphone.so.%{version}

#files -n %{libqtsflphonedevel}
#%{qt4lib}/libqtsflphone.so
#%{_includedir}/qtsflphone/
