Summary: Library and utilities for automated guest OS installs
Name: oz
Version: 0.9.0
Release: 0.20120601084324git7e0b0a9%{?dist}
License: LGPLv2
Group: Development/Libraries
URL: http://aeolusproject.org/oz.html
Source0: http://repos.fedorapeople.org/repos/aeolus/oz/%{version}/tarball/%{name}-%{version}.tar.gz
BuildArch: noarch
Requires: python >= 2.5
Requires: gvnc-tools
Requires: python-libguestfs
Requires: libxml2-python
Requires: libvirt-python
# in theory, oz doesn't really require libvirtd to be local to operate
# properly.  However, because of the libguestfs manipulations, in practice
# it really does.  Make it depend on libvirt (so we get libvirtd) for now,
# unless/until we are able to make it really be remote.
Requires: libvirt
Requires: python-pycurl
Requires: genisoimage
Requires: numpy
Requires: mtools
Requires: python-uuid
Requires: openssh-clients
Requires: m2crypto
Requires: pyparted

BuildRequires: python

%description
Oz is a set of libraries and utilities for doing automated guest OS
installations, with minimal input from the user.

%prep
%setup -q

%build
python setup.py build

%install
# generate the oz-examples man page
python setup.py install --root=$RPM_BUILD_ROOT --skip-build

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/oz/
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/oz/isocontent/
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/oz/isos/
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/oz/floppycontent/
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/oz/floppies/
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/oz/icicletmp/
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/oz/jeos/
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/oz/kernels/

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/oz
cp oz.cfg $RPM_BUILD_ROOT%{_sysconfdir}/oz

# generate the oz-examples.1 man page and copy it into place
make examples-manpage
cp man/oz-examples.1 $RPM_BUILD_ROOT%{_mandir}/man1
gzip $RPM_BUILD_ROOT%{_mandir}/man1/oz-examples.1

%post
if [ ! -f %{_sysconfdir}/oz/id_rsa-icicle-gen ]; then
   ssh-keygen -t rsa -b 2048 -N "" -f %{_sysconfdir}/oz/id_rsa-icicle-gen >& /dev/null
fi

%files
%doc README COPYING examples docs
%dir %attr(0755, root, root) %{_sysconfdir}/oz/
%config(noreplace) %{_sysconfdir}/oz/oz.cfg
%dir %attr(0755, root, root) %{_localstatedir}/lib/oz/
%dir %attr(0755, root, root) %{_localstatedir}/lib/oz/isocontent/
%dir %attr(0755, root, root) %{_localstatedir}/lib/oz/isos/
%dir %attr(0755, root, root) %{_localstatedir}/lib/oz/floppycontent/
%dir %attr(0755, root, root) %{_localstatedir}/lib/oz/floppies/
%dir %attr(0755, root, root) %{_localstatedir}/lib/oz/icicletmp/
%dir %attr(0755, root, root) %{_localstatedir}/lib/oz/jeos/
%dir %attr(0755, root, root) %{_localstatedir}/lib/oz/kernels/
%{python_sitelib}/oz
%{_bindir}/oz-install
%{_bindir}/oz-generate-icicle
%{_bindir}/oz-customize
%{_bindir}/oz-cleanup-cache
%{python_sitelib}/oz-*.egg-info
%{_mandir}/man1/*

%changelog
* Wed Jan 11 2012 Chris Lalancette <clalancette@gmail.om> - 0.8.0-1
- Release 0.8.0

* Mon Sep 12 2011 Chris Lalancette <clalance@redhat.com> - 0.7.0-1
- Release 0.7.0

* Wed Aug 17 2011 Chris Lalancette <clalance@redhat.com> - 0.6.0-1
- Release 0.6.0

* Wed Jun 29 2011 Chris Lalancette <clalance@redhat.com> - 0.5.0-1
- Release 0.5.0

* Wed Jun 20 2011 Pádraig Brady <P@draigBrady.com> - 0.4.0-4
- Include examples/.

* Wed Jun 15 2011 Pádraig Brady <P@draigBrady.com> - 0.4.0-3
- Address rpmlint issues.

* Fri Jun 10 2011 Pádraig Brady <P@draigBrady.com> - 0.4.0-2
- Change to noarch.

* Tue May 24 2011 Chris Lalancette <clalance@redhat.com> - 0.4.0-1
- Release 0.4.0.

* Wed Mar 30 2011 Chris Lalancette <clalance@redhat.com> - 0.3.0-1
- Release 0.3.0.

* Wed Mar 16 2011 Chris Lalancette <clalance@redhat.com> - 0.2.0-1
- Release 0.2.0.

* Fri Feb  3 2011 Chris Lalancette <clalance@redhat.com> - 0.1.0-1
- Initial public release of Oz.

* Wed Nov  3 2010 Chris Lalancette <clalance@redhat.com> - 0.0.4-1
- Initial build.

