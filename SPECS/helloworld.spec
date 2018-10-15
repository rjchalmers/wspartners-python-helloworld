# -----------------------------------------------------------------------------
# Overview of a spec
# -----------------------------------------------------------------------------
# This file provides the instructions for:
#
#   1) How to build an .rpm file.
#   2) What happens when the RPM is installed or uninstalled.
#
# To deferentiate between the two events, we use 'build time' and 'installation
# time' in the comments. The result of a build is a .rpm file. The result of an
# installation is the software existing on a machine, usually after a 'yum
# install ...' command has been ran.
#
# For more information see:
# - https://confluence.dev.bbc.co.uk/display/platform/Packaging+your+software
# - https://access.redhat.com/articles/216643
# -----------------------------------------------------------------------------

Name: helloworld
Version: 0.1.0%{?buildnum:.%{buildnum}}
Release: 1%{?dist}
Group: System Environment/Daemons
License: Internal BBC use only
Summary: %{name}
Source0: src.tar.gz

# -----------------------------------------------------------------------------
# CentOS packages
# -----------------------------------------------------------------------------
# Because we are using a CentOS 7 base image, at 'installation time', all
# packages CentOS 7 provide are made available for us without us having to
# specify the repository url in the Cosmos component.

# See: http://mirror.centos.org/centos/7/os/x86_64/Packages/
# -----------------------------------------------------------------------------
Requires: python2

# -----------------------------------------------------------------------------
# Apache TLS - Access control
# -----------------------------------------------------------------------------
# Restrict the application to 'services' and 'developers' with valid BBC issued
# certificates (https://github.com/bbc/cloud-httpd-conf/).
#
# As this package is not available in the base CentOS 7 repositories, we have
# to configure the component to make another repository available at
# 'installation time'. If we forgot this step, the installation process will be
# unable to locate this package and will fail.
#
# To see where this repository is defined, search 'cloud-httpd-conf-el7' at
# https://admin.live.bbc.co.uk/cosmos/component/sample-app-python/repositories.
# -----------------------------------------------------------------------------
Requires: cloud-httpd24-ssl-services-devs

# -----------------------------------------------------------------------------
# Requirements for 'build time'
# -----------------------------------------------------------------------------
# For this python application, various packages are required via python-pip,
# defined in the requirements.txt file. These packages are bundled into
# the RPM.
# -----------------------------------------------------------------------------
BuildRequires: python2-devel
BuildRequires: python-pip
BuildRequires: systemd

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%description
%{name}

%prep
%setup -q -n src/

%build 

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/lib/%{name}
mkdir -p %{buildroot}%{_sysconfdir}/bake-scripts
[ ! -d etc/ ] || cp -r etc/ %{buildroot}/
[ ! -d bin/ ] || cp -r bin/ %{buildroot}/usr/
if [ -f %{name}.service ]; then
    mkdir -p %{buildroot}/usr/lib/systemd/system/
    cp %{name}.service %{buildroot}/usr/lib/systemd/system/
fi
PYTHONDONTWRITEBYTECODE=1 CFLAGS="$RPM_OPT_FLAGS" pip install --install-option='--install-platlib=$base/lib/python' --target %{buildroot}/usr/lib/%{name} --no-deps ext/*
for f in $(ls */__init__.py); do
    cp -r $(dirname "$f") %{buildroot}/usr/lib/%{name}/
done
cp -R %{_builddir}/src/bake-scripts %{buildroot}%{_sysconfdir}/bake-scripts/%{name}

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || useradd -r -g %{name} -d / -s /sbin/nologin %{name}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun

%files
%defattr(0755, root, root, 0755)
/usr/bin/*
%defattr(-, root, root, 0755)
/etc/bake-scripts/*
%defattr(0644, root, root, 0755)
/usr/lib/%{name}
/usr/lib/systemd/system/*
