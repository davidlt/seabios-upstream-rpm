%define githead 669c991

Name:           seabios
Version:        0.5.1
Release:        0.1.20100108git%{githead}%{?dist}
Summary:        Open-source legacy BIOS implementation

Group:          Applications/Emulators
License:        LGPLv3
URL:            http://www.coreboot.org/SeaBIOS
# Source0:        http://linuxtogo.org/~kevin/SeaBIOS/%{name}-%{version}.tar.gz
# The source for this package was pulled from upstream's git.  Use the
# following commands to generate the tarball:
# git archive --format=tar --prefix=seabios-0.5.1/ 669c991 | gzip > seabios-0.5.1-669c991.tar.gz
Source0:        %{name}-%{version}-%{githead}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: python
ExclusiveArch: %{ix86} x86_64

%description
SeaBIOS is an open-source legacy BIOS implementation which can be used as
a coreboot payload. It implements the standard BIOS calling interfaces
that a typical x86 proprietary BIOS implements.


%prep
%setup -q
# Makefile on pre releases changes version to include date and buildhost
sed -i 's,VERSION=pre-%{version}.*,VERSION=pre-%{version}-%{githead},g' Makefile


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
* Thu Jan 07 2010 Justin M. Forbes <jforbes@redhat.com> 0.5.1-0.1.20100108git669c991
- Created initial package
