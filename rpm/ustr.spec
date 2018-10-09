# based on work by The Fedora Project (2017)
# Copyright (c) 1998, 1999, 2000 Thai Open Source Software Center Ltd
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

%define show_all_cmds       1
%define broken_fed_dbg_opts 0
%define multilib_inst       1

%if %{show_all_cmds}
%define policy_cflags_hide HIDE=
%else
%define policy_cflags_hide %{nil}
%endif

%if %{broken_fed_dbg_opts}
# Variable name explains itself.
%define policy_cflags_broken DBG_ONLY_BAD_POLICIES_HAVE_THIS_EMPTY_CFLAGS=
%else
%define policy_cflags_broken %{nil}
%endif

%define policy_cflags %{policy_cflags_hide}  %{policy_cflags_broken}

%if %{multilib_inst}
%define ustr_make_install install-multilib-linux
%else
%define ustr_make_install install
%endif


Name: ustr
Version: 0
Release: 1
Summary: String library, very low memory overhead, simple to import
Group: System Environment/Libraries
License: MIT or LGPLv2+ or BSD
URL: http://www.and.org/ustr/
Source: %{name}-%{version}.tar.gz
Patch0: c99-inline.patch
# BuildRequires: make gcc sed

%description
 Micro string library, very low overhead from plain strdup() (Ave. 44% for
0-20B strings). Very easy to use in existing C code. At it's simplest you can
just include a single header file into your .c and start using it.
 This package also distributes pre-built shared libraries.

%package devel
Summary: Development files for %{name}
Group: Development/Libraries
# This isn't required, but Fedora policy makes it so
Requires: pkgconfig >= 0.14
Requires: %{name} = %{version}-%{release}

%description devel
 Header files for the Ustr string library, and the .so to link with.
 Also includes a %{name}.pc file for pkg-config usage.
 Includes the ustr-import tool, for if you jsut want to include
the code in your projects ... you don't have to link to the shared lib.

%package static
Summary: Static development files for %{name}
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description static
 Static library for the Ustr string library.

%package debug
Summary: Development files for %{name}, with debugging options turned on
Group: Development/Libraries
# This isn't required, but Fedora policy makes it so
Requires: pkgconfig >= 0.14
Requires: %{name}-devel = %{version}-%{release}

%description debug
 Header files and dynamic libraries for a debug build of the Ustr string
library.
 Also includes a %{name}-debug.pc file for pkg-config usage.

%package debug-static
Summary: Static development files for %{name}, with debugging options turned on
Group: Development/Libraries
Requires: %{name}-debug = %{version}-%{release}

%description debug-static
 Static library for the debug build of the Ustr string library.

%prep
%setup -q -n %{name}-%{version}/upstream
%patch0 -p1

%build
make %{?_smp_mflags} all-shared CFLAGS="${CFLAGS:-%optflags}  -fgnu89-inline" %{policy_cflags}

%check
%if %{?chk}%{!?chk:1}
make %{?_smp_mflags} check CFLAGS="${CFLAGS:-%optflags}  -fgnu89-inline" %{policy_cflags}
%endif

%install
rm -rf $RPM_BUILD_ROOT
make $@ %{ustr_make_install} prefix=%{_prefix} \
                bindir=%{_bindir}         mandir=%{_mandir} \
                datadir=%{_datadir}       libdir=%{_libdir} \
                includedir=%{_includedir} libexecdir=%{_libexecdir} \
                DOCSHRDIR=%{_datadir}/doc/ustr-devel \
                DESTDIR=$RPM_BUILD_ROOT LDCONFIG=/bin/true HIDE=

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post debug -p /sbin/ldconfig

%postun debug -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libustr-1.0.so.*
%doc LICENSE*
%doc ChangeLog README NEWS

%files devel
%defattr(-,root,root,-)
%{_datadir}/ustr-*
%{_bindir}/ustr-import
%if %{multilib_inst}
%{_libexecdir}/ustr-*
%endif
%{_includedir}/ustr.h
%{_includedir}/ustr-*.h
%exclude %{_includedir}/ustr*debug*.h
%{_libdir}/pkgconfig/ustr.pc
%{_libdir}/libustr.so
%{_datadir}/doc/ustr-devel
%{_mandir}/man1/*
%{_mandir}/man3/*

%files static
%{_libdir}/libustr.a

%files debug
%defattr(-,root,root,-)
%{_libdir}/libustr-debug-1.0.so.*
%{_libdir}/libustr-debug.so
%{_includedir}/ustr*debug*.h
%{_libdir}/pkgconfig/ustr-debug.pc

%files debug-static
%{_libdir}/libustr-debug.a
