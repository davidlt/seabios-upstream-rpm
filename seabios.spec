Name:           seabios
Version:        1.7.3
Release:        1%{?dist}
Summary:        Open-source legacy BIOS implementation

Group:          Applications/Emulators
License:        LGPLv3
URL:            http://www.coreboot.org/SeaBIOS

Source0:        http://code.coreboot.org/p/seabios/downloads/get/%{name}-%{version}.tar.gz

Source10:       config.vga.cirrus
Source11:       config.vga.isavga
Source12:       config.vga.qxl
Source13:       config.vga.stdvga
Source14:       config.vga.vmware

BuildRequires: python iasl
BuildRequires: binutils-x86_64-linux-gnu gcc-x86_64-linux-gnu

Requires: %{name}-bin = %{version}-%{release}
Requires: seavgabios-bin = %{version}-%{release}
Buildarch: noarch

# Seabios is noarch, but required on architectures which cannot build it.
# Disable debuginfo because it is of no use to us.
%global debug_package %{nil}

# You can build a debugging version of the BIOS by setting this to a
# value > 1.  See src/config.h for possible values, but setting it to
# a number like 99 will enable all possible debugging.  Note that
# debugging goes to a special qemu port that you have to enable.  See
# the SeaBIOS top-level README file for the magic qemu invocation to
# enable this.
%global debug_level 1


%description
SeaBIOS is an open-source legacy BIOS implementation which can be used as
a coreboot payload. It implements the standard BIOS calling interfaces
that a typical x86 proprietary BIOS implements.


%package bin
Summary: Seabios for x86
Buildarch: noarch


%description bin
SeaBIOS is an open-source legacy BIOS implementation which can be used as
a coreboot payload. It implements the standard BIOS calling interfaces
that a typical x86 proprietary BIOS implements.


%package -n seavgabios-bin
Summary: Seavgabios for x86
Buildarch: noarch
Obsoletes: vgabios

%description -n seavgabios-bin
SeaVGABIOS is an open-source VGABIOS implementation.


%prep
%setup -q

# Makefile changes version to include date and buildhost
sed -i 's,VERSION=%{version}.*,VERSION=%{version},g' Makefile


%build
make .config V=1
sed -i 's,CONFIG_DEBUG_LEVEL=.*,CONFIG_DEBUG_LEVEL=%{debug_level},g' .config

export CFLAGS="$RPM_OPT_FLAGS"
mkdir binaries

# seabios
make V=1 \
	HOSTCC=gcc \
	CC=x86_64-linux-gnu-gcc \
	AS=x86_64-linux-gnu-as \
	LD=x86_64-linux-gnu-ld \
	OBJCOPY=x86_64-linux-gnu-objcopy \
	OBJDUMP=x86_64-linux-gnu-objdump \
	STRIP=x86_64-linux-gnu-strip
cp out/bios.bin binaries

# seavgabios
for config in %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14}; do
	name=${config#*config.vga.}
	make clean distclean
	cp ${config} .config
	echo "CONFIG_DEBUG_LEVEL=%{debug_level}" >> .config
	make oldnoconfig
	make V=1 \
		HOSTCC=gcc \
		CC=x86_64-linux-gnu-gcc \
		AS=x86_64-linux-gnu-as \
		LD=x86_64-linux-gnu-ld \
		OBJCOPY=x86_64-linux-gnu-objcopy \
		OBJDUMP=x86_64-linux-gnu-objdump \
		STRIP=x86_64-linux-gnu-strip \
		out/vgabios.bin
	cp out/vgabios.bin binaries/vgabios-${name}.bin
done


%install
mkdir -p $RPM_BUILD_ROOT%{_datadir}/seabios
mkdir -p $RPM_BUILD_ROOT%{_datadir}/seavgabios
install -m 0644 binaries/bios.bin $RPM_BUILD_ROOT%{_datadir}/seabios
install -m 0644 binaries/vgabios*.bin $RPM_BUILD_ROOT%{_datadir}/seavgabios


%files
%doc COPYING COPYING.LESSER README TODO


%files bin
%dir %{_datadir}/seabios/
%{_datadir}/seabios/bios.bin

%files -n seavgabios-bin
%dir %{_datadir}/seavgabios/
%{_datadir}/seavgabios/vgabios*.bin


%changelog
* Mon Jul 08 2013 Cole Robinson <crobinso@redhat.com> - 1.7.3-1
- Rebased to version 1.7.3
- Initial support for using SeaBIOS as a UEFI CSM
- Support for detecting and using ACPI reboot ports.
- Non-standard floppy sizes now work again with recent QEMU versions.
- Several bug fixes and code cleanups
- Again fix vgabios obsoletes (bz #981147)

* Mon May 27 2013 Cole Robinson <crobinso@redhat.com> - 1.7.2.2-1
- Update to seabios stable 1.7.2.2
- Obsolete vgabios (bz #967315)

* Thu Jan 24 2013 Cole Robinson <crobinso@redhat.com> - 1.7.2-1
- Rebased to version 1.7.2
- Support for ICH9 host chipset ("q35") on emulators
- Support for booting from LSI MegaRAID SAS controllers
- Support for using the ACPI PM timer on emulators
- Improved Geode VGA BIOS support.
- Several bug fixes

* Thu Dec  6 2012 Peter Robinson <pbrobinson@fedoraproject.org> 1.7.1-4
- Root seabios package is noarch too because it only contains docs

* Fri Oct 19 2012 Cole Robinson <crobinso@redhat.com> - 1.7.1-3
- Add seavgabios subpackage

* Wed Oct 17 2012 Paolo Bonzini <pbonzini@redhat.com> - 1.7.1-2
- Build with cross compiler.  Resolves: #866664.

* Wed Sep 05 2012 Cole Robinson <crobinso@redhat.com> - 1.7.1-1
- Rebased to version 1.7.1
- Initial support for booting from USB attached scsi (USB UAS) drives
- USB EHCI 64bit controller support
- USB MSC multi-LUN device support
- Support for booting from LSI SCSI controllers on emulators
- Support for booting from AMD PCscsi controllers on emulators

* Mon Aug 13 2012 Richard W.M. Jones <rjones@redhat.com> - 1.7.0-4
- Modernise and tidy up the RPM.
- Allow debug versions of SeaBIOS to be built easily.

* Mon Aug 06 2012 Cole Robinson <crobinso@redhat.com> - 1.7.0-3
- Enable S3/S4 support for guests (it's an F18 feature after all)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 28 2012 Cole Robinson <crobinso@redhat.com> - 1.7.0-1
- Rebased to version 1.7.0
- Support for virtio-scsi
- Improved USB drive support
- Several USB controller bug fixes and improvements

* Wed Mar 28 2012 Paolo Bonzini <pbonzini@redhat.com> - 1.6.3-2
- Fix bugs in booting from host (or redirected) USB pen drives

* Wed Feb 08 2012 Justin M. Forbes <jforbes@redhat.com> - 1.6.3-1
- Update to 1.6.3 upstream
- Add virtio-scsi

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
