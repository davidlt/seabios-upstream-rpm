Name:           seabios
Version:        0.5.1
Release:        1%{?dist}
Summary:        Open-source legacy BIOS implementation

Group:          Applications/Emulators
License:        LGPLv3
URL:            http://www.coreboot.org/SeaBIOS
Source0:        http://linuxtogo.org/~kevin/SeaBIOS/%{name}-%{version}.tar.gz

# Patches from git 0.5.1-stable branch
Patch01: 0001-Go-back-to-using-0xf0000000-for-PCI-memory-start.patch
Patch02: 0002-Fix-PkgLength-calculation-for-the-SSDT.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: python
ExclusiveArch: %{ix86} x86_64

%description
SeaBIOS is an open-source legacy BIOS implementation which can be used as
a coreboot payload. It implements the standard BIOS calling interfaces
that a typical x86 proprietary BIOS implements.


%prep
%setup -q

%patch01 -p1
%patch02 -p1

# Makefile changes version to include date and buildhost
sed -i 's,VERSION=%{version}.*,VERSION=%{version},g' Makefile


%build
make


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/seabios
install -m 0644 out/bios.bin $RPM_BUILD_ROOT%{_datadir}/seabios


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%dir %{_datadir}/seabios/
%doc COPYING COPYING.LESSER README TODO
%{_datadir}/seabios/bios.bin



%changelog
* Wed Mar 03 2010 Justin M. Forbes <jforbes@redhat.com> 0.5.1-1
- Update to 0.5.1 stable release
- Pick up patches required for current qemu

* Thu Jan 07 2010 Justin M. Forbes <jforbes@redhat.com> 0.5.1-0.1.20100108git669c991
- Created initial package
