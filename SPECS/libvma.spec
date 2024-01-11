%{!?configure_options: %global configure_options %{nil}}

Name: libvma
Version: 9.6.4
Release: 1%{?dist}
Summary: A library for boosting TCP and UDP traffic (over RDMA hardware)

License: GPLv2 or BSD
Url: https://github.com/Mellanox/libvma
Source0: https://github.com/Mellanox/libvma/archive/%{version}/%{name}-%{version}.tar.gz

# libvma currently supports only the following architectures
ExclusiveArch: x86_64 ppc64le ppc64 aarch64

BuildRequires: pkgconfig
BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libtool
BuildRequires: gcc-c++
BuildRequires: rdma-core-devel
BuildRequires: systemd-rpm-macros
BuildRequires: pkgconfig(libnl-3.0)
BuildRequires: pkgconfig(libnl-route-3.0)
BuildRequires: make

%description
libvma is a LD_PRELOAD-able library that boosts performance of TCP and
UDP traffic. It allows application written over standard socket API to
handle fast path data traffic from user space over Ethernet and/or
Infiniband with full network stack bypass and get better throughput,
latency and packets/sec rate.

No application binary change is required for that.
libvma is supported by RDMA capable devices that support "verbs"
IBV_QPT_RAW_PACKET QP for Ethernet and/or IBV_QPT_UD QP for IPoIB.

%package devel
Summary: Header files required to develop with libvma
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
This package includes headers for building programs with libvma's
interfaces.

%package utils
Summary: Utilities used with libvma
Requires: %{name}%{?_isa} = %{version}-%{release}

%description utils
This package contains the tool for collecting and analyzing libvma statistic.

%prep
%setup -q
%autosetup -p1

%build
export revision=1
if [ ! -e configure ] && [ -e autogen.sh ]; then
    PRJ_RELEASE=1 ./autogen.sh
fi

%configure %{?configure_options}
%{make_build}

%install
%{make_install}

find $RPM_BUILD_ROOT%{_libdir} -name '*.la' -delete
install -D -m 644 contrib/scripts/vma.service $RPM_BUILD_ROOT/%{_prefix}/lib/systemd/system/vma.service
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/init.d/vma

%post
%systemd_post vma.service

%preun
%systemd_preun vma.service

%postun
%systemd_postun_with_restart vma.service

%files
%{_libdir}/%{name}.so*
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/README
%doc %{_pkgdocdir}/CHANGES
%config(noreplace) %{_sysconfdir}/libvma.conf
%{_sbindir}/vmad
%{_prefix}/lib/systemd/system/vma.service
%license LICENSE
%{_mandir}/man7/vma.*
%{_mandir}/man8/vmad.*

%files devel
%dir %{_includedir}/mellanox
%{_includedir}/mellanox/vma_extra.h

%files utils
%{_bindir}/vma_stats
%{_mandir}/man8/vma_stats.*

%changelog
* Wed Aug 17 2022 Michal Schmidt <mschmidt@redhat.com> - 9.6.4-1
- Update to upstream release 9.6.4.
- Resolves: rhbz#2049572

* Tue Nov 30 2021 Honggang Li <honli@redhat.com> - 9.4.0-1
- Bump version to 9.4.0
- Resolves: rhbz#1982205

* Tue Jul 06 2021 Honggang Li <honli@redhat.com> - 9.3.1-1
- Bump version to 9.3.1
- Resolves: rhbz#1915316

* Thu Feb 04 2021 Honggang Li <honli@redhat.com> - 9.2.2-2
- Skip team interface when check bonding
- Resolves: rhbz#1916670

* Wed Dec 16 2020 Honggang Li <honli@redhat.com> - 9.2.2-1
- Update to upstream v9.2.2 release
- Resolves: rhbz#1851727

* Wed Apr 15 2020 Honggang Li <honli@redhat.com> - 9.0.2-1
- Update to upstream v9.0.2 release
- Resolves: rhbz#1789385

* Tue Jul 23 2019 Jarod Wilson <jarod@redhat.com> - 8.9.5-1
- Update to upstream v8.9.5 release
- Resolves: rhbz#1722259

* Fri May 31 2019 Jarod Wilson <jarod@redhat.com> - 8.7.7-1
- Update to upstream v8.7.7 stable release

* Thu Nov 08 2018 Jarod Wilson <jarod@redhat.com> - 8.7.3-0.1
- Rebase to upstream v8.7.3 pre-release
- Resolves: rhbz#1648011

* Fri Jun 29 2018 Jarod Wilson <jarod@redhat.com> - 8.6.10-0.1
- Rebase to upstream v8.6.10 pre-release, use 0.x release number scheme
  as means to differentiate pre-release from release

* Mon Jun 04 2018 Jarod Wilson <jarod@redhat.com> - 8.6.6-1
- Rebase to upstream v8.6.6 pre-release

* Wed Apr 25 2018 Jarod Wilson <jarod@redhat.com> - 8.6.0-1
- Rebase to upstream v8.6.0 pre-release

* Tue Dec 05 2017 Jarod Wilson <jarod@redhat.com> - 8.4.10-1
- Rebase to upstream v8.4.10 release
- Resolves: rhbz#1456519

* Wed Aug 24 2016 Jarod Wilson <jarod@redhat.com> - 8.1.4-1
- Rebase to 8.1.4 after latest round of coverity fixes upstream
  reduced reported defects to 0
- Related: rhbz#1271624

* Mon Aug 22 2016 Jarod Wilson <jarod@redhat.com> - 8.1.3-1
- Patch in additional coverity fixes from upstream git tree
- Rebase to 8.1.3 to pick up copious coverity corrections
- Related: rhbz#1271624

* Mon Jul 25 2016 Donald Dutile <ddutile@redhat.com> - 8.1.1-1
- Rebase to 8.1.1, re-apply patch to 8.0.1-2
- Add (Build)Requires of libibverbs to 1.2.2
- Resolves: rhbz#1353704

* Wed May 25 2016 Donald Dutile <ddutile@redhat.com> - 8.0.1-2
- ExcludeArch s390's, ppc, i686 and catch in h-file check
- Resolves: rhbz#1271624

* Wed May 25 2016 Donald Dutile <ddutile@redhat.com> - 8.0.1-1
- Initial import to RHEL-7.3
- Resolves: rhbz#1271624

* Sun Mar 13 2016 Alex Vainman <alexv@mellanox.com> - 8.0.1-1
- New upstream release
- Move to dual license: GPLv2 or BSD
- ExcludeArch update
- Removal of extra space in:
  config(noreplace) {_sysconfdir}/security/limits.d/30-libvma-limits.conf
- Add V=1 to make

* Wed Mar  2 2016 Alex Vainman <alexv@mellanox.com> - 7.0.14-2
- Added reasoning for archs exclusion
- Package description improvement
- Removal of the pre scriplet
- Added COPYING and LICENSE files to the package

* Sun Feb 21 2016 Alex Vainman <alexv@mellanox.com> - 7.0.14-1
- New upstream release
- Removal of redundant macros and obsolete/unneeded tags
- Added ExcludeArch, BuildRequires and Require sections
- Fixes and cleanups in the build and installation sections
- Install 30-libvma-limits.conf file under 
  /etc/security/limits.d/
- Fixes related to files/directories ownerships
- Removal of vma_perf_envelope.sh from the utility package
- Update Source tag URL
- Fix most of the rpmlint warnings

* Mon Jan  4 2016 Avner BenHanoch <avnerb@mellanox.com> - 7.0.12-1
- Initial Packaging
