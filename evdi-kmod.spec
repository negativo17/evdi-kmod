# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
%define buildforkernels akmod

%global debug_package %{nil}

%global zipmodules 1

%define __spec_install_post \
  %{__arch_install_post}\
  %{__os_install_post}\
  %{__mod_compress_install_post}

%define __mod_compress_install_post \
  if [ "%{zipmodules}" -eq "1" ] && [ $kernel_version ]; then \
    find %{buildroot}/usr/lib/modules/ -type f -name '*.ko' | xargs xz; \
  fi

Name:           evdi-kmod
Version:        1.9.1
Release:        1%{?dist}
Summary:        DisplayLink VGA/HDMI display driver kernel module
License:        GPLv2
URL:            https://github.com/DisplayLink/evdi

Source0:        https://github.com/DisplayLink/evdi/archive/v%{version}.tar.gz#/evdi-%{version}.tar.gz
Patch0:         https://github.com/DisplayLink/evdi/commit/0f1ad2153de1bc144f2359afa91fbe3fa07e9e7a.patch

# get the needed BuildRequires (in parts depending on what we build for)
BuildRequires:  kmodtool

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo negativo17.org --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
The DisplaLink %{version} display driver kernel module for kernel %{kversion}.

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}
# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu}  --repo negativo17.org --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%autosetup -p1 -n evdi-%{version}

for kernel_version in %{?kernel_versions}; do
    mkdir _kmod_build_${kernel_version%%___*}
    cp -fr module/* _kmod_build_${kernel_version%%___*}
done

%build
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
* Tue Apr 13 2021 Simone Caronni <negativo17@gmail.com> - 1:1.9.1-1
- First build.
