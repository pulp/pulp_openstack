%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

Name: pulp-openstack
Version: 0.1
Release: 1%{?dist}
Summary: Support for Openstack images in the Pulp platform
Group: Development/Languages
License: GPLv2
URL: http://pulpproject.org
Source0: https://fedorahosted.org/releases/p/u/%{name}/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  rpm-python

%description
Provides a collection of platform plugins and admin client extensions to
provide openstack image support.

%prep
%setup -q

%build
pushd common
%{__python} setup.py build
popd

pushd extensions_admin
%{__python} setup.py build
popd

pushd plugins
%{__python} setup.py build
popd

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}/%{_sysconfdir}/pulp/

pushd common
%{__python} setup.py install --skip-build --root %{buildroot}
popd

pushd extensions_admin
%{__python} setup.py install --skip-build --root %{buildroot}
popd

pushd plugins
%{__python} setup.py install --skip-build --root %{buildroot}
popd

mkdir -p %{buildroot}/%{_usr}/lib/pulp/plugins/types
mkdir -p %{buildroot}/%{_var}/lib/pulp/published/openstack/

cp -R plugins/etc/httpd %{buildroot}/%{_sysconfdir}
# Types
cp -R plugins/types/* %{buildroot}/%{_usr}/lib/pulp/plugins/types/

# Directories
mkdir -p %{buildroot}/%{_sysconfdir}/pulp/agent/conf.d
mkdir -p %{buildroot}/%{_bindir}

# Remove tests
rm -rf %{buildroot}/%{python_sitelib}/test

%clean
rm -rf %{buildroot}



# ---- Openstack Common -----------------------------------------------------------

%package -n python-pulp-openstack-common
Summary: Pulp Openstack support common library
Group: Development/Languages
Requires: python-pulp-common >= 2.4.0
Requires: python-setuptools

%description -n python-pulp-openstack-common
Common libraries for python-pulp-openstack

%files -n python-pulp-openstack-common
%defattr(-,root,root,-)
%dir %{python_sitelib}/pulp_openstack
%{python_sitelib}/pulp_openstack/__init__.py*
%{python_sitelib}/pulp_openstack/common/
%dir %{python_sitelib}/pulp_openstack/extensions
%{python_sitelib}/pulp_openstack/extensions/__init__.py*
%{python_sitelib}/pulp_openstack_common*.egg-info
%doc COPYRIGHT LICENSE AUTHORS


# ---- Plugins -----------------------------------------------------------------
%package plugins
Summary: Pulp Openstack plugins
Group: Development/Languages
Requires: python-pulp-common >= 2.4.0
Requires: python-pulp-openstack-common = %{version} 
Requires: pulp-server >= 2.4.0
Requires: python-semantic-version >= 2.2.0
Requires: python-setuptools
Requires: python-glanceclient >= 0.12
Requires: python-keystoneclient >= 0.6

%description plugins
Provides a collection of platform plugins that extend the Pulp platform
to provide Openstack specific support.

%files plugins

%defattr(-,root,root,-)
%{python_sitelib}/pulp_openstack/plugins/
%config(noreplace) %{_sysconfdir}/httpd/conf.d/pulp_openstack.conf
%{_usr}/lib/pulp/plugins/types/openstack.json
%{python_sitelib}/pulp_openstack_plugins*.egg-info

%defattr(-,apache,apache,-)
%{_var}/lib/pulp/published/openstack/

%doc COPYRIGHT LICENSE AUTHORS


# ---- Admin Extensions --------------------------------------------------------
%package admin-extensions
Summary: The Pulp Openstack admin client extensions
Group: Development/Languages
Requires: python-pulp-common >= 2.4.0
Requires: python-pulp-openstack-common = %{version}
Requires: pulp-admin-client >= 2.4.0
Requires: python-setuptools

%description admin-extensions
pulp-admin extensions for openstack image support

%files admin-extensions
%defattr(-,root,root,-)
%{python_sitelib}/pulp_openstack/extensions/admin/
%{python_sitelib}/pulp_openstack_extensions_admin*.egg-info
%doc COPYRIGHT LICENSE AUTHORS


%changelog
