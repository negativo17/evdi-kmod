%global commit0 64559211ec33390dbf4372e1029455ff58e0e739
%global date 20230223
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global tag %{version}

# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
%define buildforkernels akmod

%global debug_package %{nil}

%global mok_algo sha512
%global mok_key /usr/src/akmods/mok.key
%global mok_der /usr/src/akmods/mok.der

%define __spec_install_post \
  %{__arch_install_post}\
  %{__os_install_post}\
  %{__mod_install_post}

%define __mod_install_post \
  if [ $kernel_version ]; then \
    find %{buildroot} -type f -name '*.ko' | xargs %{__strip} --strip-debug; \
    if [ -f /usr/src/akmods/mok.key ] && [ -f /usr/src/akmods/mok.der ]; then \
      find %{buildroot} -type f -name '*.ko' | xargs echo; \
      find %{buildroot} -type f -name '*.ko' | xargs -L1 /usr/lib/modules/${kernel_version%%___*}/build/scripts/sign-file %{mok_algo} %{mok_key} %{mok_der}; \
    fi \
    find %{buildroot} -type f -name '*.ko' | xargs xz; \
  fi

Name:           evdi-kmod
Version:        1.13.1
Release:        3%{!?tag:.%{date}git%{shortcommit0}}%{?dist}
Summary:        DisplayLink VGA/HDMI display driver kernel module
License:        GPLv2
URL:            https://github.com/DisplayLink/evdi

%if 0%{?tag:1}
Source0:        %{url}/archive/v%{version}.tar.gz#/evdi-%{version}.tar.gz
%else
Source0:        %{url}/archive/%{commit0}.tar.gz#/evdi-%{shortcommit0}.tar.gz
%endif

Patch0:         https://github.com/DisplayLink/evdi/commit/c1865ecbf04df6759e336e4c68a3ebf895bd01d1.patch

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
