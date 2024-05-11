#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	6.2
%define		qtver		5.15.2
%define		kfname		kconfig

Summary:	Backend for storing application configuration
Name:		kf6-%{kfname}
Version:	6.2.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	edecb863455d7b76a29a1374bad501bc
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6DBus-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	Qt6Xml-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	kf6-extra-cmake-modules >= %{kdeframever}
BuildRequires:	ninja
BuildRequires:	qt6-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	Qt6DBus >= %{qtver}
Requires:	Qt6Gui >= %{qtver}
Requires:	Qt6Xml >= %{qtver}
Requires:	kf6-dirs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
KConfig provides an advanced configuration system. It is made of two
parts: KConfigCore and KConfigGui.

KConfigCore provides access to the configuration files themselves. It
features:

- Code generation: describe your configuration in an XML file, and use
  `kconfig_compiler to generate classes that read and write
  configuration entries.
- Cascading configuration files (global settings overridden by local
  settings).
- Optional shell expansion support (see [docs/options.md](@ref
  options)).
- The ability to lock down configuration options (see
  [docs/options.md](@ref options)).

KConfigGui provides a way to hook widgets to the configuration so that
they are automatically initialized from the configuration and
automatically propagate their changes to their respective
configuration files.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt6DBus-devel >= %{qtver}
Requires:	Qt6Xml-devel >= %{qtver}
Requires:	cmake >= 3.16

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/kconf_update
%ninja_install -C build

%find_lang %{kfname}5_qt --with-qm --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kfname}5_qt.lang
%defattr(644,root,root,755)
%doc DESIGN README.md TODO
%ghost %{_libdir}/libKF6ConfigCore.so.6
%attr(755,root,root) %{_libdir}/libKF6ConfigCore.so.*.*
%ghost %{_libdir}/libKF6ConfigGui.so.6
%ghost %{_libdir}/libKF6ConfigQml.so.6
%dir %{_libdir}/qt6/qml/org/kde/config
%{_libdir}/qt6/qml/org/kde/config/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/config/qmldir
%attr(755,root,root) %{_libdir}/libKF6ConfigQml.so.*.*
%attr(755,root,root) %{_libdir}/libKF6ConfigGui.so.*.*
%attr(755,root,root) %{_bindir}/kreadconfig6
%attr(755,root,root) %{_bindir}/kwriteconfig6
%attr(755,root,root) %{_libexecdir}/kf6/kconf_update
%attr(755,root,root) %{_libexecdir}/kf6/kconfig_compiler_kf6
%dir %{_datadir}/kconf_update
%{_datadir}/qlogging-categories6/kconfig.categories
%{_datadir}/qlogging-categories6/kconfig.renamecategories
%{_libdir}/qt6/qml/org/kde/config/KF6ConfigQml.qmltypes
%attr(755,root,root) %{_libdir}/qt6/qml/org/kde/config/libKF6ConfigQmlplugin.so

%files devel
%defattr(644,root,root,755)
%{_libdir}/libKF6ConfigCore.so
%{_libdir}/libKF6ConfigGui.so
%{_libdir}/libKF6ConfigQml.so
%{_includedir}/KF6/KConfigCore
%{_includedir}/KF6/KConfigGui
%{_includedir}/KF6/KConfigQml
%{_includedir}/KF6/KConfig
%{_libdir}/cmake/KF6Config
