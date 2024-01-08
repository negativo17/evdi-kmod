%global commit0 0313ecac7aa3990c6f9a0d0f258c87e20e116bdd
%global date 20240104
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
#global tag %{version}

%global	kmod_name evdi

%global	debug_package %{nil}

# Generate kernel symbols requirements:
%global _use_internal_dependency_generator 0

%{!?kversion: %global kversion %(uname -r)}

Name:           %{kmod_name}-kmod
Version:        1.14.1
Release:        4%{!?tag:.%{date}git%{shortcommit0}}%{?dist}
Summary:        DisplayLink VGA/HDMI display driver kernel module
Epoch:          1
License:        GPLv2
URL:            https://github.com/DisplayLink/%{kmod_name}

%if 0%{?tag:1}
Source0:        %{url}/archive/v%{version}.tar.gz#/%{kmod_name}-%{version}.tar.gz
%else
Source0:        %{url}/archive/%{commit0}.tar.gz#/%{kmod_name}-%{shortcommit0}.tar.gz
%endif

BuildRequires:  elfutils-libelf-devel
BuildRequires:  gcc
BuildRequires:  kernel-devel
BuildRequires:  kmod
BuildRequires:  redhat-rpm-config

%if 0%{?rhel} == 7
BuildRequires:  kernel-abi-whitelists
%else
BuildRequires:  kernel-abi-stablelists
BuildRequires:  kernel-rpm-macros
%endif

%description
This package provides the DisplayLink VGA/HDMI display kernel driver module.
It is built to depend upon the specific ABI provided by a range of releases of
the same variant of the Linux kernel and not on any one specific build.

%package -n kmod-%{kmod_name}
Summary:    %{kmod_name} kernel module(s)

Provides:   kabi-modules = %{kversion}.%{_target_cpu}
Provides:   %{kmod_name}-kmod = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:   module-init-tools

%description -n kmod-%{kmod_name}
This package provides the %{kmod_name} kernel module(s) built for the Linux kernel
using the %{_target_cpu} family of processors.

%post -n kmod-%{kmod_name}
if [ -e "/boot/System.map-%{kversion}.%{_target_cpu}" ]; then
    /usr/sbin/depmod -aeF "/boot/System.map-%{kversion}.%{_target_cpu}" "%{kversion}.%{_target_cpu}" > /dev/null || :
fi
modules=( $(find /lib/modules/%{kversion}.%{_target_cpu}/extra/%{kmod_name} | grep '\.ko$') )
if [ -x "/usr/sbin/weak-modules" ]; then
    printf '%s\n' "${modules[@]}" | /usr/sbin/weak-modules --add-modules
fi

%preun -n kmod-%{kmod_name}
rpm -ql kmod-%{kmod_name}-%{version}-%{release}.%{_target_cpu} | grep '\.ko$' > /var/run/rpm-kmod-%{kmod_name}-modules

%postun -n kmod-%{kmod_name}
if [ -e "/boot/System.map-%{kversion}.%{_target_cpu}" ]; then
    /usr/sbin/depmod -aeF "/boot/System.map-%{kversion}.%{_target_cpu}" "%{kversion}.%{_target_cpu}" > /dev/null || :
fi
modules=( $(cat /var/run/rpm-kmod-%{kmod_name}-modules) )
rm /var/run/rpm-kmod-%{kmod_name}-modules
if [ -x "/usr/sbin/weak-modules" ]; then
    printf '%s\n' "${modules[@]}" | /usr/sbin/weak-modules --remove-modules
fi

%prep
%if 0%{?tag:1}
%autosetup -p1 -n %{kmod_name}-%{version}
%else
%autosetup -p1 -n %{kmod_name}-%{commit0}
%endif

echo "override %{kmod_name} * weak-updates/%{kmod_name}" > kmod-%{kmod_name}.conf

%build
%if 0%{?rhel} == 8
# Also catches CentOS Stream
export EL8FLAG="-DEL8"
%endif

make -C %{_usrsrc}/kernels/%{kversion}.%{_target_cpu} M=$PWD/module modules

%install
export INSTALL_MOD_PATH=%{buildroot}
export INSTALL_MOD_DIR=extra/%{kmod_name}

make -C %{_usrsrc}/kernels/%{kversion}.%{_target_cpu} M=$PWD/module modules_install


install -d %{buildroot}%{_sysconfdir}/depmod.d/
install kmod-%{kmod_name}.conf %{buildroot}%{_sysconfdir}/depmod.d/
# Remove the unrequired files.
rm -f %{buildroot}/lib/modules/%{kversion}.%{_target_cpu}/modules.*

%files -n kmod-%{kmod_name}
/lib/modules/%{kversion}.%{_target_cpu}/extra/*
%config /etc/depmod.d/kmod-%{kmod_name}.conf

%changelog
* Mon Jan 08 2024 Simone Caronni <negativo17@gmail.com> - 1:1.14.1-4.20240104git0313eca
- Update to latest snapshot.

* Mon Nov 27 2023 Simone Caronni <negativo17@gmail.com> - 1:1.14.1-3.20231123gita943d98
- Switch to snapshot which include build fixes for latest kernels.

* Mon Nov 20 2023 Simone Caronni <negativo17@gmail.com> - 1:1.14.1-2
- Add patch for 6.6 kernel.

* Wed Aug 23 2023 Simone Caronni <negativo17@gmail.com> - 1:1.14.1-1
- Update to 1.14.1.

* Fri Jun 02 2023 Simone Caronni <negativo17@gmail.com> - 1:1.14.0-1
- Update to 1.14.0.

* Mon May 15 2023 Simone Caronni <negativo17@gmail.com> - 1:1.13.1-3
- EL patch has been merged upstream.

* Wed May 10 2023 Simone Caronni <negativo17@gmail.com> - 1:1.13.1-2
- Update EL patch.

* Wed Mar 29 2023 Simone Caronni <negativo17@gmail.com> - 1:1.13.1-1
- Update to 1.13.1.

* Tue Mar 21 2023 Simone Caronni <negativo17@gmail.com> - 1:1.13.0-1
- Update to 1.13.0.

* Thu Mar 02 2023 Simone Caronni <negativo17@gmail.com> - 1:1.12.0-3.20230223git6455921
- Fix build on latest EL 8/9 and Fedora kernels.

* Thu Oct 13 2022 Simone Caronni <negativo17@gmail.com> - 1:1.12.0-2.20221013gitbdc258b
- Update to latest snapshot.

* Tue Aug 09 2022 Simone Caronni <negativo17@gmail.com> - 1:1.12.0-1.20220725gitb884877
- Update to latest 1.12.0 snapshot.

* Thu Jun 16 2022 Simone Caronni <negativo17@gmail.com> - 1:1.11.0-2.20220428git39da217
- Add patch for CentOS/RHEL 8.6.

* Sat Apr 30 2022 Simone Caronni <negativo17@gmail.com> - 1:1.11.0-1.20220428git39da217
- Update to 1.11.0 snapshot.

* Thu Mar 03 2022 Simone Caronni <negativo17@gmail.com> - 1:1.10.1-1
- Update to 1.10.1.

* Fri Jan 21 2022 Simone Caronni <negativo17@gmail.com> - 1:1.10.0-1.20220104gitaef6790
- Update to 1.10.0 plus latest commits.

* Tue Apr 13 2021 Simone Caronni <negativo17@gmail.com> - 1:1.9.1-1
- First build.
