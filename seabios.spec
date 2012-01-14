Name:           seabios
Version:        0.6.2
Release:        4%{?dist}
Summary:        Open-source legacy BIOS implementation

Group:          Applications/Emulators
License:        LGPLv3
URL:            http://www.coreboot.org/SeaBIOS
Source0:        http://www.linuxtogo.org/~kevin/SeaBIOS/%{name}-%{version}.tar.gz

Patch00: seabios-0.6.2-build.patch
Patch01: seabios-0.6.2-fix-QXL.patch
Patch02: seabios-do-not-advertise-S4-S3-in-DSDT.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: python iasl
ExclusiveArch: %{ix86} x86_64

Requires: %{name}-bin = %{version}-%{release}

# Seabios is noarch, but required on architectures which cannot build it.
# Disable debuginfo because it is of no use to us.
%global debug_package %{nil}

%description
SeaBIOS is an open-source legacy BIOS implementation which can be used as
a coreboot payload. It implements the standard BIOS calling interfaces
that a typical x86 proprietary BIOS implements.

%ifarch %{ix86} x86_64 
%package bin
Summary: Seabios for x86
Buildarch: noarch

%description bin
SeaBIOS is an open-source legacy BIOS implementation which can be used as
a coreboot payload. It implements the standard BIOS calling interfaces
that a typical x86 proprietary BIOS implements.
%endif

%prep
%setup -q

%patch00 -p1
%patch01 -p1
%patch02 -p1

# Makefile changes version to include date and buildhost
sed -i 's,VERSION=%{version}.*,VERSION=%{version},g' Makefile


%build
%ifarch %{ix86} x86_64 
export CFLAGS="$RPM_OPT_FLAGS"
make 
%endif


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/seabios
%ifarch %{ix86} x86_64 
install -m 0644 out/bios.bin $RPM_BUILD_ROOT%{_datadir}/seabios
%endif


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc COPYING COPYING.LESSER README TODO

%ifarch %{ix86} x86_64 
%files bin
%defattr(-,root,root,-)
%dir %{_datadir}/seabios/
%{_datadir}/seabios/bios.bin
%endif


%changelog
* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 05 2011 Justin M. Forbes <jforbes@redhat.com> - 0.6.2-3
- Stop advertising S3 and S4 in DSDT (bz#741375)
- incdule iasl buildreq

* Wed Jul 13 2011 Justin M. Forbes <jforbes@redhat.com> - 0.6.2-2
- Fix QXL bug in 0.6.2

* Wed Jul 13 2011 Justin M. forbes <jforbes@redhat.com> - 0.6.2-1
- Update to 0.6.2 upstream for a number of bugfixes

* Mon Feb 14 2011 Justin M. forbes <jforbes@redhat.com> - 0.6.1-1
- Update to 0.6.1 upstream for a number of bugfixes

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 10 2010 Justin M. Forbes <jforbes@redhat.com> 0.6.0-1
- Update seabios to latest stable so we can drop patches.

* Tue Apr 20 2010 Justin M. Forbes <jforbes@redhat.com> 0.5.1-2
- Ugly hacks to make package noarch and available for arch that cannot build it.
- Disable useless debuginfo

* Wed Mar 03 2010 Justin M. Forbes <jforbes@redhat.com> 0.5.1-1
- Update to 0.5.1 stable release
- Pick up patches required for current qemu

* Thu Jan 07 2010 Justin M. Forbes <jforbes@redhat.com> 0.5.1-0.1.20100108git669c991
- Created initial package
