Name:           seabios
Version:        0.5.1
Release:        3%{?dist}
Summary:        Open-source legacy BIOS implementation

Group:          Applications/Emulators
License:        LGPLv3
URL:            http://www.coreboot.org/SeaBIOS
Source0:        http://linuxtogo.org/~kevin/SeaBIOS/%{name}-%{version}.tar.gz

# Patches from git 0.5.1-stable branch
Patch01: 0001-Go-back-to-using-0xf0000000-for-PCI-memory-start.patch
Patch02: 0002-Fix-PkgLength-calculation-for-the-SSDT.patch

# Patches from upstream git
Patch03: seabios-Set-CONFIG_S3_RESUME_VGA_INIT-to-1.patch
Patch04: seabios-smbios-avoid-counting-io-hole-as-ram.patch
Patch05: seabios-Support-for-booting-from-virtio-disks.patch
Patch06: seabios-zero-memory-before-use.patch
Patch07: seabios-do-not-advertise-hpet-to-a-guest-OS.patch
Patch08: seabios-fix-resume-from-S3-with-QXL-device.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: python
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

%patch01 -p1
%patch02 -p1
%patch03 -p1
%patch04 -p1
%patch05 -p1
%patch06 -p1
%patch07 -p1
%patch08 -p1

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
* Tue Jun 29 2010 Justin M. Forbes <jforbes@redhat.com> 0.5.1-3
- Support booting from virtio disks
- zero memory before use
- Fix resume from S3 when using QXL device
- Avoid counting io-hole are RAM
- Do not advertise hpet to guests

* Tue Apr 20 2010 Justin M. Forbes <jforbes@redhat.com> 0.5.1-2
- Ugly hacks to make package noarch and available for arch that cannot build it.
- Disable useless debuginfo

* Wed Mar 03 2010 Justin M. Forbes <jforbes@redhat.com> 0.5.1-1
- Update to 0.5.1 stable release
- Pick up patches required for current qemu

* Thu Jan 07 2010 Justin M. Forbes <jforbes@redhat.com> 0.5.1-0.1.20100108git669c991
- Created initial package
