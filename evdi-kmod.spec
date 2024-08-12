%global commit0 eab561a9fe19d1bbc801dd1ec60e8b3318941be7
%global date 20240726
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
#global tag %{version}

# Build only the akmod package and no kernel module packages:
%define buildforkernels akmod

%global debug_package %{nil}

Name:           evdi-kmod
Version:        1.14.5
Release:        2%{!?tag:.%{date}git%{shortcommit0}}%{?dist}
Summary:        DisplayLink VGA/HDMI display driver kernel module
License:        GPLv2
URL:            https://github.com/DisplayLink/evdi

%if 0%{?tag:1}
Source0:        %{url}/archive/v%{version}.tar.gz#/evdi-%{version}.tar.gz
%else
Source0:        %{url}/archive/%{commit0}.tar.gz#/evdi-%{shortcommit0}.tar.gz
%endif

# Get the needed BuildRequires (in parts depending on what we build for):
BuildRequires:  kmodtool

# kmodtool does its magic here:
%{expand:%(kmodtool --target %{_target_cpu} --repo negativo17.org --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
The DisplaLink %{version} display driver kernel module for kernel %{kversion}.

%prep
# Error out if there was something wrong with kmodtool:
%{?kmodtool_check}
# Print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu}  --repo negativo17.org --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%if 0%{?tag:1}
%autosetup -p1 -n evdi-%{version}
%else
%autosetup -p1 -n evdi-%{commit0}
%endif

for kernel_version in %{?kernel_versions}; do
    mkdir _kmod_build_${kernel_version%%___*}
    cp -fr module/* _kmod_build_${kernel_version%%___*}
done

%build
# Catch any fork of RHEL
%if 0%{?rhel}
export EL%{?rhel}FLAG="-DEL%{?rhel}"
%endif

for kernel_version in %{?kernel_versions}; do
    pushd _kmod_build_${kernel_version%%___*}/
        %make_build -C "${kernel_version##*___}" M=$(pwd) modules
    popd
done

%install
for kernel_version in %{?kernel_versions}; do
    mkdir -p %{buildroot}/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
    install -p -m 0755 _kmod_build_${kernel_version%%___*}/*.ko \
        %{buildroot}/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
done
%{?akmod_install}

%changelog
* Mon Aug 12 2024 Simone Caronni <negativo17@gmail.com> - 1.14.5-2.20240726giteab561a
- Update to latest snapshot to allow building on kernel 6.10.

* Tue Jul 02 2024 Simone Caronni <negativo17@gmail.com> - 1.14.5-1
- Update to 1.14.5.

* Tue Apr 16 2024 Simone Caronni <negativo17@gmail.com> - 1.14.4-1
- Update to 1.14.4.

* Thu Feb 08 2024 Simone Caronni <negativo17@gmail.com> - 1.14.2-1
- Update to final 1.14.2.

* Tue Feb 06 2024 Simone Caronni <negativo17@gmail.com> - 1.14.1-6.20240130gitd21a6ea
- Update to latest snapshot.

* Mon Jan 08 2024 Simone Caronni <negativo17@gmail.com> - 1.14.1-5.20240104git0313eca
- Update to latest snapshot.

* Mon Nov 27 2023 Simone Caronni <negativo17@gmail.com> - 1.14.1-4.20231123gita943d98
- Switch to snapshot which include build fixes for latest kernels.

* Mon Nov 20 2023 Simone Caronni <negativo17@gmail.com> - 1.14.1-3
- Add patch for 6.6 kernel.

* Wed Nov 15 2023 Simone Caronni <negativo17@gmail.com> - 1.14.1-2
- Drop custom signing and compressing in favour of kmodtool.

* Wed Aug 23 2023 Simone Caronni <negativo17@gmail.com> - 1.14.1-1
- Update to 1.14.1.

* Fri Jun 02 2023 Simone Caronni <negativo17@gmail.com> - 1.14.0-1
- Update to 1.14.0.

* Mon May 15 2023 Simone Caronni <negativo17@gmail.com> - 1.13.1-3
- EL patch has been merged upstream.

* Wed May 10 2023 Simone Caronni <negativo17@gmail.com> - 1.13.1-2
- Update EL patch.

* Wed Mar 29 2023 Simone Caronni <negativo17@gmail.com> - 1.13.1-1
- Update to 1.13.1.

* Fri Mar 17 2023 Simone Caronni <negativo17@gmail.com> - 1.13.0-1
- Update to 1.13.0.

* Thu Mar 02 2023 Simone Caronni <negativo17@gmail.com> - 1.12.0-3.20230223git6455921
- Fix build on latest EL 8/9 and Fedora kernels.

* Thu Oct 13 2022 Simone Caronni <negativo17@gmail.com> - 1.12.0-2.20221013gitbdc258b
- Update to latest snapshot.

* Tue Aug 09 2022 Simone Caronni <negativo17@gmail.com> - 1.12.0-1.20220725gitb884877
- Update to latest 1.12.0 snapshot.

* Thu Jun 16 2022 Simone Caronni <negativo17@gmail.com> - 1.11.0-2.20220428git39da217
- Add patch for CentOS/RHEL 8.6.

* Sat Apr 30 2022 Simone Caronni <negativo17@gmail.com> - 1.11.0-1.20220428git39da217
- Update to 1.11.0 snapshot.

* Thu Mar 03 2022 Simone Caronni <negativo17@gmail.com> - 1.10.1-1
- Update to 1.10.1.

* Fri Jan 21 2022 Simone Caronni <negativo17@gmail.com> - 1.10.0-1.20220104gitaef6790
- Update to 1.10.0 plus latest commits.

* Thu Dec 02 2021 Simone Caronni <negativo17@gmail.com> - 1.9.1-5.20211202gitd6b2841
- Update to latest snapshot.

* Tue Sep 14 2021 Simone Caronni <negativo17@gmail.com> - 1.9.1-4
- Add automatic signing workaround.

* Thu Sep 02 2021 Simone Caronni <negativo17@gmail.com> - 1.9.1-3
- Update module with latest upstream patches.

* Wed Aug 18 2021 Simone Caronni <negativo17@gmail.com> - 1.9.1-2
- Fix compression and add stripping.

* Tue Apr 13 2021 Simone Caronni <negativo17@gmail.com> - 1:1.9.1-1
- First build.
