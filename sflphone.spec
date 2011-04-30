Summary:	A robust standards-compliant enterprise softphone
Name:		sflphone
Version:	0.9.13
Release:	%mkrel 1
Url:		http://www.sflphone.org/
Source0:	https://projects.savoirfairelinux.com/attachments/download/1811/%{name}-%{version}.tar.gz
Patch0:		sflphone-0.9.11-fix-underlinking.patch
Patch1:		fix_missing_include-file-error-in-f15.patch
Patch2:		sflphone-0.9.12-libnotify-0.7.patch
# pjsip is GPLv2; sflphone-common is GPLv3
License:	GPLv2 and GPLv3
Group:		Communications
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	openssl-devel libcommoncpp-devel yaml-devel celt-devel
BuildRequires:	libccrtp-devel libzrtpcpp-devel astyle libgsm-devel
BuildRequires:	libsamplerate-devel libalsa-devel libpulseaudio-devel libspeex-devel
BuildRequires:	libuuid-devel libdbus-1-devel libexpat-devel
BuildRequires:	libdbus-glib-1-devel libnotify-devel gtk2-devel glib2-devel
BuildRequires:	webkitgtk-devel libgnomeui2-devel gnome-doc-utils
BuildRequires:	evolution-data-server-devel libcheck-devel >= 0.9.4
Suggests:	%{name}-client-gnome

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

%package client-gnome
Summary: A robust standards-compliant enterprise softphone
License: GPLv2
Group:   Communications
Requires: %{name}

%description client-gnome
This package contains the GNOME client for SFLphone.

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1
%patch2 -p0
#%patch0 -p1 -b .underlinking
#(cd sflphone-client-gnome && autoreconf -fi)

%build
pushd sflphone-common/libs/pjproject
%configure2_5x --enable-libsamplerate
make dep
make
popd

pushd sflphone-common
%configure2_5x
%make
popd

pushd sflphone-client-gnome
%configure2_5x --disable-schemas-install --disable-silent-rules
%make
popd

%install
rm -rf %{buildroot}
%makeinstall_std -C sflphone-common
%makeinstall_std -C sflphone-client-gnome

%find_lang %{name}
%find_lang %{name}-client-gnome

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS README CODING
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/codecs/
%{_libdir}/%{name}/plugins/
%{_libdir}/%{name}/sflphoned
%{_datadir}/dbus-1/services/org.sflphone.SFLphone.service
%{_mandir}/man1/sflphoned*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/ringtones/

%files client-gnome -f %{name}-client-gnome.lang
%defattr(-,root,root)
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
