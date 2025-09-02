# Build only the akmod package and no kernel module packages:
%define buildforkernels akmod

%global debug_package %{nil}

Name:           evdi-kmod
Version:        1.14.11
Release:        1%{?dist}
Summary:        DisplayLink VGA/HDMI display driver kernel module
License:        GPLv2
URL:            https://github.com/DisplayLink/evdi

Source0:        %{url}/archive/v%{version}.tar.gz#/evdi-%{version}.tar.gz
# Required for CentOS Stream (10.1), not required for 10.0:
Patch1:         0001-Revert-CentOS-Stream-10-change.patch

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

%autosetup -p1 -n evdi-%{version}

for kernel_version in %{?kernel_versions}; do
    mkdir _kmod_build_${kernel_version%%___*}
    cp -fr module/* _kmod_build_${kernel_version%%___*}
done

%build

for kernel_version in %{?kernel_versions}; do
    pushd _kmod_build_${kernel_version%%___*}/
        unset CFLAGS
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
* Tue Sep 02 2025 Simone Caronni <negativo17@gmail.com> - 1.14.11-1
- Update to 1.4.11.

* Thu Jun 19 2025 Simone Caronni <negativo17@gmail.com> - 1.14.10-3
- Revert change that works for CentOS Stream (10.1) but not for EL (10.0).

* Wed May 21 2025 Simone Caronni <negativo17@gmail.com> - 1.14.10-2
- Add upstream patches.

* Wed May 14 2025 Simone Caronni <negativo17@gmail.com> - 1.14.10-1
- Update to 1.14.10.

* Thu Mar 27 2025 Simone Caronni <negativo17@gmail.com> - 1.14.9-1
- Update to 1.14.9.

* Sat Jan 11 2025 Simone Caronni <negativo17@gmail.com> - 1.14.8-2
- Module does not compile successfully with default compiler flags (#3).

* Sun Dec 22 2024 Simone Caronni <negativo17@gmail.com> - 1.14.8-1
- Update to 1.14.8.

* Fri Dec 06 2024 Simone Caronni <negativo17@gmail.com> - 1.14.7-2
- Add kernel 6.12 patch and EL 9.5 patch.
- Trim changelog.

* Sun Sep 29 2024 Simone Caronni <negativo17@gmail.com> - 1.14.7-1
- Update to 1.14.7.

* Thu Aug 15 2024 Simone Caronni <negativo17@gmail.com> - 1.14.6-2
- Update to 1.14.6 final.

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
