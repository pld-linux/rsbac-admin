#
# TODO:
# - subpackages, %files
#
%define		rcrel	%{nil}
%define		rcver	%{nil}
Summary:	A set of RSBAC utilities
Summary(pl.UTF-8):	Zbiór narzędzi RSBAC
Name:		rsbac-admin
Version:	1.4.5
Release:	0.4
License:	GPL v2
Group:		Applications
#Source0:	ftp://rsbac.org/download/pre/rsbac-1.4.0-rc3/%{name}-%{version}%{rcver}.tar.bz2
Source0:	ftp://rsbac.org/download/code/1.4.5/%{name}-%{version}.tar.bz2
# Source0-md5:	834eee0e5128e2778527b92858092c25
Patch0:		%{name}-make.patch
Patch1:		pam.patch
URL:		http://www.rsbac.org/
BuildRequires:	gettext-tools
BuildRequires:	libtool
BuildRequires:	ncurses-devel
BuildRequires:	pam-devel
BuildRequires:	which
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libdir		/%{_lib}

%description
A set of RSBAC utilities.

%description -l pl.UTF-8
Zbiór narzędzi RSBAC.

%package -n     pam_rsbac
Summary:	RSBAC plugins for PAM
Group:		Libraries

%description -n pam_rsbac
This package contains plugins that enable using RSBAC for
authentication through PAM.

%package -n     nss_rsbac
Summary:	RSBAC NSS module to use RSBAC User Management
Group:		Libraries

%description -n nss_rsbac
This package contains the RSBAC NSS module to use RSBAC User
Management.

%package -n     rsbac-rklogd
Summary:	Standalone daemon to log RSBAC messages
Group:		Base/Kernel

%description -n rsbac-rklogd
This is a standalone daemon to log RSBAC messages to its own facility,
by default the file /var/log/rsbac/rsbac.log To prevent messages to be
logged through syslog too, add the kernel parameter 'rsbac_nosyslog'
at boot. It provides also a log viewer: rklogd-viewer.

%package devel
Summary:	Header files for ... library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki ...
Group:		Development/Libraries
# if base package contains shared library for which these headers are
#Requires:	%{name} = %{version}-%{release}
# if -libs package contains shared library for which these headers are
#Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for ... library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki ....

%prep
%setup -q -n %{name}-%{version}%{rcver}
%patch -P0 -p1
%patch -P1 -p1

%build
%{__make} libs pam nss rklogd tools \
	CC="%{__cc}" \
	OPT="%{rpmcflags} -fPIC -I/usr/include/ncurses" \
	LDFLAGS="%{rpmldflags}" \
	PREFIX="%{_prefix}" \
	LIBTOOL="libtool --tag=CC" \
	DIR_LIBS=%{_libdir} \
	DIR_NSS=%{_libdir} \
	SYSCONFDIR=%{_sysconfdir} \
	VERSION=%{version} \
	VERBOSE=1

	#LDFLAGS="%{rpmldflags} -L../libs/.libs" \
	#LDFLAGS="%{rpmldflags}" \

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX="%{_prefix}" \
	VERBOSE=1 \
	DIR_LIBS=%{_libdir} \
	DIR_NSS=%{_libdir} \
	DIR_PAM=%{_libdir}/security

%find_lang pam_rsbac
%find_lang rsbac-tools

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%post	-n nss_rsbac -p /sbin/ldconfig
%postun	-n nss_rsbac -p /sbin/ldconfig

%files -f rsbac-tools.lang
%defattr(644,root,root,755)
#doc AUTHORS CREDITS ChangeLog NEWS README THANKS TODO
%{_mandir}/man1/*
%attr(755,root,root) %{_libdir}/librsbac.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/librsbac.so.1
%attr(755,root,root) /bin/rsbac_login
%attr(755,root,root) %{_bindir}/acl_*
%attr(755,root,root) %{_bindir}/attr_*
%attr(755,root,root) %{_bindir}/auth_*
%attr(755,root,root) %{_bindir}/backup_*
%attr(755,root,root) %{_bindir}/daz_flush
%attr(755,root,root) %{_bindir}/get_attribute_*
%attr(755,root,root) %{_bindir}/linux2acl
%attr(755,root,root) %{_bindir}/mac_*
%attr(755,root,root) %{_bindir}/net_*
%attr(755,root,root) %{_bindir}/pm_*
%attr(755,root,root) %{_bindir}/rc_*
%attr(755,root,root) %{_bindir}/rsbac_*
%attr(755,root,root) %{_bindir}/switch_*
%attr(755,root,root) %{_bindir}/user_aci.sh

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/rsbac

%files -n pam_rsbac -f pam_rsbac.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/security/pam_rsbac.so
%attr(755,root,root) %{_libdir}/security/pam_rsbac_oldpw.so

%files -n nss_rsbac
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnss_rsbac.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnss_rsbac.so.2

%files -n rsbac-rklogd
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rklogd-viewer
%attr(755,root,root) %{_sbindir}/rklogd
%{_mandir}/man8/rklogd*
