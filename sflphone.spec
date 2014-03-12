Summary:	A robust standards-compliant enterprise softphone
Name:		sflphone
Version:	1.2.0
Release:	2
# pjsip is GPLv2+; sflphone-common is GPLv3+
License:	GPLv2+ and GPLv3+
Group:		Communications
Url:		http://www.sflphone.org/
#Source0:	https://projects.savoirfairelinux.com/attachments/download/2865/%{name}-%{version}.tar.gz
# some files are missed in original tarball, so using version from git
Source0:	%{name}-%{version}.tar.xz
BuildRequires:	astyle
BuildRequires:	rarian
BuildRequires:	gsm-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(celt)
BuildRequires:	pkgconfig(check)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(dbus-c++-1)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(evolution-data-server-1.2)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(libccext2)
BuildRequires:	pkgconfig(libccrtp)
BuildRequires:	pkgconfig(libebook-1.2)
BuildRequires:	pkgconfig(libgnomeui-2.0)
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(libpcre)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libzrtpcpp)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(samplerate)
BuildRequires:	pkgconfig(speex)
BuildRequires:	pkgconfig(yaml-0.1)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(webkitgtk-3.0)
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

%files
%doc daemon/AUTHORS daemon/NEWS daemon/README daemon/TODO
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/codecs/
%{_libdir}/%{name}/sflphoned
%{_datadir}/dbus-1/services/org.sflphone.SFLphone.service
%{_mandir}/man1/sflphoned*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/ringtones/

#----------------------------------------------------------------------------

%package plugins
Summary:	A robust standards-compliant enterprise softphone
License:	GPLv3+
Requires:	%{name}

%description plugins
Plugins for SFLphone software phone.

%files plugins
%doc plugins/AUTHORS plugins/NEWS plugins/README
%{_libdir}/%{name}/plugins/

#----------------------------------------------------------------------------

%package client-gnome
Summary:	A robust standards-compliant enterprise softphone
License:	GPLv3+
Requires:	%{name}
Provides:	%{name}-client = %{EVRD}

%description client-gnome
This package contains the GNOME client for SFLphone.

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

#----------------------------------------------------------------------------

%prep
%setup -q

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

%install
%makeinstall_std -C daemon
%makeinstall_std -C plugins
%makeinstall_std -C gnome

%find_lang %{name}-client-gnome --with-gnome

