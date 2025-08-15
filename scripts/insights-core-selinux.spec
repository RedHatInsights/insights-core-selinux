%define distro redhat
%global debug_package %{nil}
%global modulename insights_core
%global selinux_policy_version 42.1.1
%global selinuxtype targeted

Name:           insights-core-selinux
Version:        3.7.0
Release:        1%{?dist}
Summary:        Insights Core SELinux policy

License:        Apache-2.0
URL:            https://github.com/RedHatInsights/insights-core-selinux
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  selinux-policy-devel

Requires:           selinux-policy >= %{selinux_policy_version}
Requires:           selinux-policy-%{selinuxtype} >= %{selinux_policy_version}
Requires(post):     libselinux-utils
Requires(post):     policycoreutils
Requires(post):     selinux-policy-%{selinuxtype}
Requires(post):     selinux-policy-base >= %{selinux_policy_version}
Requires(postun):   libselinux-utils
Requires(postun):   policycoreutils



%description
Insights Core SELinux policy module

%prep
%setup -q -n %{name}-%{version}

%pre
%selinux_relabel_pre -s %{selinuxtype}

%post
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.bz2
%selinux_relabel_post -s %{selinuxtype}

%postun
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} %{modulename}
    %selinux_relabel_post -s %{selinuxtype}
fi

%build
make

%install
install -D -p -m 0644 %{modulename}.pp.bz2 %{buildroot}%{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.bz2
install -D -p -m 0644 %{modulename}.if %{buildroot}%{_datadir}/selinux/devel/include/distributed/%{modulename}.if

%files
%{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.*
%{_datadir}/selinux/devel/include/distributed/%{modulename}.if
%ghost %verify(not md5 size mode mtime) %{_sharedstatedir}/selinux/%{selinuxtype}/active/modules/200/%{modulename}
%license LICENSE


%changelog
* Wed May 21 2025 <xiangceliu@redhat.com>
- Initial Policy for insights-core
