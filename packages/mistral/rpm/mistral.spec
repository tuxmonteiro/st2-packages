%define package mistral
%define svc_user mistral
%define version %(echo -n "${MISTRAL_VERSION:-0.1}")
%define release %(echo -n "${MISTRAL_RELEASE:-1}")

%define _sourcedir ./
%include rpmspec/helpers.spec
%include rpmspec/package_venv.spec

Name: %{package}
Version: %{version}
Release: %{release}
Group: System/Management
License: Apache
Url: https://github.com/StackStorm/mistral
Source0: .
Provides: openstack-mistral
Summary: Mistral workflow service


%description
  <insert long description, indented with spaces>

%define _builddir %{SOURCE0}

%install
  %default_install
  %pip_install_venv
  %service_install mistral mistral-api mistral-server
  make post_install DESTDIR=%{?buildroot}
  # clean up absolute path in record file, so that /usr/bin/check-buildroot doesn't fail
  find /root/rpmbuild/BUILDROOT/%{package}* -name RECORD -exec sed -i '/\/root\/rpmbuild.*$/d' '{}' ';'

%prep
  rm -rf %{buildroot}
  mkdir -p %{buildroot}

%clean
  rm -rf %{buildroot}

%pre
  adduser --no-create-home --system %{svc_user} 2>/dev/null
  exit 0

%post
  %service_post mistral mistral-api mistral-server

%preun
  %service_preun mistral mistral-api mistral-server

%postun
  %service_postun mistral mistral-api mistral-server

%files
  /opt/stackstorm/%{name}
  %config(noreplace) %{_sysconfdir}/mistral/*
  %attr(755, %{svc_user}, %{svc_user}) %{_localstatedir}/log/mistral
%if 0%{?use_systemd}
  %{_unitdir}/mistral.service
  %{_unitdir}/mistral-api.service
  %{_unitdir}/mistral-server.service
%else
  %{_sysconfdir}/rc.d/init.d/mistral
  %{_sysconfdir}/rc.d/init.d/mistral-api
  %{_sysconfdir}/rc.d/init.d/mistral-server
%endif
