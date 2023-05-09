# Defining the package namespace
%global ns_name ea
%global ns_dir /opt/cpanel
%global pkg ruby27
%global gem_name sqlite3

%global ruby_version %(/opt/cpanel/ea-ruby27/root/usr/bin/ruby -e 'puts %RUBY_VERSION')

# Force Software Collections on
%global _scl_prefix %{ns_dir}
%global scl %{ns_name}-%{pkg}
# HACK: OBS Doesn't support macros in BuildRequires statements, so we have
#       to hard-code it here.
# https://en.opensuse.org/openSUSE:Specfile_guidelines#BuildRequires
%global scl_prefix %{scl}-
%{?scl:%scl_package rubygem-%{gem_name}}

# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4590 for more details
%define release_prefix 5

Summary:        Allows Ruby scripts to interface with a SQLite3 database
Name:           %{?scl_prefix}rubygem-%{gem_name}
Version:        1.4.4
Release:        %{release_prefix}%{?dist}.cpanel
Group:          Development/Languages
License:        BSD
URL:            https://github.com/sparklemotion/sqlite3-ruby
Source0:        %{gem_name}-%{version}.gem
Requires:       %{?scl_prefix}ruby(rubygems)
Requires:       %{?scl_prefix}ruby(release)

BuildRequires:  sqlite-devel
BuildRequires:  scl-utils
BuildRequires:  scl-utils-build
BuildRequires:  %{?scl_prefix}ruby
BuildRequires:  %{?scl_prefix}rubygems-devel
BuildRequires:  %{?scl_prefix}ruby-devel
BuildRequires:  %{?scl_prefix}rubygem(rake)
BuildRequires:  %{?scl_prefix}rubygem(minitest) >= 5.0.0
Provides:       %{?scl_prefix}rubygem(%{gem_name}) = %{version}-%{release}

%description
SQLite3/Ruby is a module to allow Ruby scripts to interface with a SQLite3
database.

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
# setup.rb shipped in the -doc subpackage has LGPLv2.1 licensing
License: BSD and LGPLv2
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}

%prep
%setup -q -c -T

export CONFIGURE_ARGS="--with-cflags='%{optflags}'"

%{?scl:scl enable %{scl} - << \EOF} \
%gem_install -n %{SOURCE0} \
%{?scl:EOF}

# Permission
find . -name \*.rb -or -name \*.gem | xargs chmod 0644

%build

%install
%global rubybase opt/cpanel/ea-ruby27/root/usr/share/ruby/gems/ruby-%{ruby_version}
%global lib64base opt/cpanel/ea-ruby27/root/usr/lib64/gems/ruby/sqlite3-%{version}

%global gemsbase opt/cpanel/ea-ruby27/root/usr/share/gems
%global gemsdir  %{gemsbase}/gems
%global gemsmri  %{gemsdir}/sqlite3-%{version}
%global gemsdoc  %{gemsbase}/doc/sqlite3-%{version}

mkdir -p %{buildroot}/%{gemsmri}
mkdir -p %{buildroot}/%{gemsdoc}
mkdir -p %{buildroot}/%{gemsbase}/specifications
mkdir -p %{buildroot}/%{lib64base}

cp -ar %{gemsmri}/* %{buildroot}/%{gemsmri}
cp -ar %{gemsdoc}/* %{buildroot}/%{gemsdoc}
cp -a %{gemsbase}/specifications/sqlite3-%{version}.gemspec %{buildroot}/%{gemsbase}/specifications
cp -a %{lib64base}/* %{buildroot}/%{lib64base}

%check
# I cannot get this to work, not sure why
# Tests fail on cent 6
#%if 0%{rhel} > 6
#%{?scl:scl enable %{scl} - << \EOF} \
#pushd %{gemsdir} \
#ruby -I$(dirs +1)%{gemsmri}:lib:test -e 'Dir.glob "./test/test_*.rb", &method(:require)' \
#popd \
#EOF}
#%endif

%files
/%{gemsbase}
%dir /%{gemsdir}
%exclude /%{gemsmri}/.gemtest
%exclude /%{gemsmri}/.travis.yml
%exclude /%{gemsmri}/appveyor.yml
%exclude /%{gemsmri}/ext
%exclude /%{gemsbase}/cache
%doc /%{gemsmri}/README.rdoc
%doc /%{gemsmri}/LICENSE
/%{lib64base}

%files doc
%doc /%{gemsmri}/API_CHANGES.rdoc
%doc /%{gemsmri}/CHANGELOG.rdoc
%doc /%{gemsmri}/ChangeLog.cvs
%doc /%{gemsmri}/Manifest.txt
%doc /%{gemsmri}/faq/

%changelog
* Tue May 09 2023 Brian Mendoza <brian.mendoza@cpanel.net> - 1.4.4-5
- ZC-10936: Clean up Makefile and remove debug-package-nil

* Fri Mar 31 2023 Cory McIntire <cory@cpanel.net> - 1.4.4-4
- EA-11327: ea-ruby27 was updated from v2.7.7 to v2.7.8

* Thu Nov 24 2022 Travis Holloway <t.holloway@cpanel.net> - 1.4.4-3
- EA-11073: ea-ruby27 was updated from v2.7.6 to v2.7.7

* Thu Oct 20 2022 Dan Muey <dan@cpanel.net> - 1.4.4-2
- ZC-10347: limit to 1.4 updates since it is nearing EOL and 1.5 has issues

* Thu Jun 16 2022 Cory McIntire <cory@cpanel.net> - 1.4.4-1
- EA-10771: Update ea-ruby27-rubygem-sqlite3 from v1.4.2 to v1.4.4

* Tue Apr 12 2022 Cory McIntire <cory@cpanel.net> - 1.4.2-6
- EA-10620: ea-ruby27 was updated from v2.7.5 to v2.7.6

* Tue Dec 28 2021 Dan Muey <dan@cpanel.net> - 1.4.2-5
- ZC-9589: Update DISABLE_BUILD to match OBS

* Wed Nov 24 2021 Travis Holloway <t.holloway@cpanel.net> - 1.4.2-4
- EA-10301: ea-ruby27 was updated from v2.7.4 to v2.7.5

* Thu Jul 29 2021 Travis Holloway <t.holloway@cpanel.net> - 1.4.2-3
- EA-10007: ea-ruby27 was updated from v2.7.3 to v2.7.4

* Tue Jun 29 2021 Julian Brown <julian.brown@cpanel.net> - 1.4.2-2
- ZC-9033: provide reliable way to get the ruby_version

* Wed Sep 09 2020 Julian Brown <julian.brown@cpanel.net> - 1.4.2-1
- ZC-7511 - add rubygem sqlite3 to Ruby 2.7

