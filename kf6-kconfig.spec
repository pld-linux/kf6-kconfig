#
# Conditional build:
%bcond_with	tests		# test suite

%define		kdeframever	6.18
%define		qt_ver		6.7.0
%define		kf_ver		%{version}
%define		kfname		kconfig

Summary:	Backend for storing application configuration
Summary(pl.UTF-8):	Backend do przechowywania konfiguracji aplikacji
Name:		kf6-%{kfname}
Version:	6.18.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	54933f37b9e12fbe0bcee5a41bf57112
URL:		https://kde.org/
BuildRequires:	Qt6Core-devel >= %{qt_ver}
BuildRequires:	Qt6DBus-devel >= %{qt_ver}
BuildRequires:	Qt6Gui-devel >= %{qt_ver}
BuildRequires:	Qt6Qml-devel >= %{qt_ver}
BuildRequires:	Qt6Quick-devel >= %{qt_ver}
%{?with_tests:BuildRequires:	Qt6Test-devel >= %{qt_ver}}
BuildRequires:	Qt6Xml-devel >= %{qt_ver}
BuildRequires:	cmake >= 3.16
BuildRequires:	kf6-extra-cmake-modules >= %{kf_ver}
BuildRequires:	ninja
BuildRequires:	qt6-linguist >= %{qt_ver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	Qt6DBus >= %{qt_ver}
Requires:	Qt6Gui >= %{qt_ver}
Requires:	Qt6Qml >= %{qt_ver}
Requires:	Qt6Quick >= %{qt_ver}
Requires:	Qt6Xml >= %{qt_ver}
Requires:	kf6-dirs
#Obsoletes:	kf5-kconfig < 6
%requires_eq_to Qt6Core Qt6Core-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KConfig provides an advanced configuration system. It is made of two
parts: KConfigCore and KConfigGui.

KConfigCore provides access to the configuration files themselves. It
features:
- Code generation: describe your configuration in an XML file, and use
  kconfig_compiler to generate classes that read and write
  configuration entries.
- Cascading configuration files (global settings overridden by local
  settings).
- Optional shell expansion support
- The ability to lock down configuration options

KConfigGui provides a way to hook widgets to the configuration so that
they are automatically initialized from the configuration and
automatically propagate their changes to their respective
configuration files.

%description -l pl.UTF-8
KConfig udostępnia zaawansowany system konfiguracji. Składa się z
dwóch części: KConfigCore oraz KConfigGui.

KConfigCore zapewnia dostęp do samych plików konfiguracyjnych.
Funkcjonalność:
- generowanie kodu: wystarczy opisać konfigurację w pliku XML i użyć
  programu kconfig_compiler, aby wygenerować klasy czytające i
  zapisujące wpisy konfiguracji
- kaskadowe pliki konfiguracyjne (globalne ustawienia nadpisywane
  przez lokalne ustawienia)
- opcjonalna obsługa dopełniania poleceń
- możliwość zablokowania opcji konfiguracyjnych

KConfigGui zapewnia sposób podpięcia widżetów do konfiguracji tak, aby
były automatycznie inicjowane z konfiguracji i automatycznie
propagowały zmiany do odpowiednich plików konfiguracyjnych.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt6DBus-devel >= %{qtver}
Requires:	Qt6Qml-devel >= %{qtver}
Requires:	Qt6Xml-devel >= %{qtver}
Requires:	cmake >= 3.16
#Obsoletes:	kf5-kconfig-devel < 6

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

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kfname}5_qt.lang
%defattr(644,root,root,755)
%doc DESIGN README.md TODO
%attr(755,root,root) %{_bindir}/kreadconfig6
%attr(755,root,root) %{_bindir}/kwriteconfig6
%attr(755,root,root) %{_libexecdir}/kf6/kconf_update
%attr(755,root,root) %{_libexecdir}/kf6/kconfig_compiler_kf6
%attr(755,root,root) %{_libdir}/libKF6ConfigCore.so.*.*
%ghost %{_libdir}/libKF6ConfigCore.so.6
%attr(755,root,root) %{_libdir}/libKF6ConfigGui.so.*.*
%ghost %{_libdir}/libKF6ConfigGui.so.6
%attr(755,root,root) %{_libdir}/libKF6ConfigQml.so.*.*
%ghost %{_libdir}/libKF6ConfigQml.so.6
%dir %{_libdir}/qt6/qml/org/kde/config
%attr(755,root,root) %{_libdir}/qt6/qml/org/kde/config/libKF6ConfigQmlplugin.so
%{_libdir}/qt6/qml/org/kde/config/KF6ConfigQml.qmltypes
%{_libdir}/qt6/qml/org/kde/config/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/config/qmldir
%dir %{_datadir}/kconf_update
%{_datadir}/qlogging-categories6/kconfig.categories
%{_datadir}/qlogging-categories6/kconfig.renamecategories

%files devel
%defattr(644,root,root,755)
%{_libdir}/libKF6ConfigCore.so
%{_libdir}/libKF6ConfigGui.so
%{_libdir}/libKF6ConfigQml.so
%{_includedir}/KF6/KConfig
%{_includedir}/KF6/KConfigCore
%{_includedir}/KF6/KConfigGui
%{_includedir}/KF6/KConfigQml
%{_libdir}/cmake/KF6Config
