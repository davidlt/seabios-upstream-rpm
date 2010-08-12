Name:           seabios
Version:        0.6.0
Release:        1%{?dist}
Summary:        Open-source legacy BIOS implementation

Group:          Applications/Emulators
License:        LGPLv3
URL:            http://www.coreboot.org/SeaBIOS
Source0:        http://linuxtogo.org/~kevin/SeaBIOS/%{name}-%{version}.tar.gz

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
Thu Aug 12 2010 Justin M. Forbes <jforbes@redhat.com> 0.6.0-1
- Update seabios to latest stable so we can drop patches.

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
