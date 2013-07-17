Name:		spaceclone
Version:	0.1
Release: 1373990456
Summary:	Tool for managing RHN Satellite Channels

BuildArch:  noarch

Group:	    Applications/System	
License:	MIT
URL:		https://github.com/stbenjam/spaceclone
Source0:	spaceclone.tar.gz

Requires:	python python-prettytable

%description
Tool for managing RHN Satellite Channels

%prep
%setup -n src

%build
%{__python} setup.py build

%install
test "x$RPM_BUILD_ROOT" != "x" && rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --optimize=1 --root=$RPM_BUILD_ROOT $PREFIX
mkdir -p ${RPM_BUILD_ROOT}/usr/bin
mkdir -p ${RPM_BUILD_ROOT}/etc
install -m 0755 bin/spaceclone ${RPM_BUILD_ROOT}/usr/bin

%files
%defattr(-,root,root,-)
%{python_sitelib}/spaceclone
/usr/bin/spaceclone
%if 0%{?fedora} >= 9 || 0%{?rhel} > 5
%{python_sitelib}/spaceclone*.egg-info
%endif

%changelog
* Fri Jun 1 2013 Stephen Benjamin <stephen@bitbin.de>
- Initial creation
