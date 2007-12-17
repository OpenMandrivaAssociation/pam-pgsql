%define name	pam-pgsql
%define version 0.6.1
%define release %mkrel 4

Summary:	Postgresql authentication for PAM
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:      1
License:	GPL
Group:		System/Libraries
URL:		http://sourceforge.net/projects/pam-pgsql
Source:		http://ovh.dl.sourceforge.net/sourceforge/pam-pgsql/lib%name-%{version}.tar.bz2
Patch0:     pam-pgsql.null.patch
Requires:	pam
BuildRequires:	pam-devel, postgresql-devel, libmhash-devel

%description
This is a module that allows people to login to PAM-aware applications by
authenticating to a Postgresql database.

%prep
%setup -q
%patch -p0 -b .null

%build
%configure --with-postgres=%_includedir/pgsql --libdir=/%_lib/security
%make

%install
mkdir -p %buildroot/%_lib/security/

install -c -m 644 pam_pgsql.so %buildroot/%_lib/security/

mkdir -p %buildroot/%_sysconfdir
cat > %buildroot/%_sysconfdir/pam_pgsql.conf <<EOF
# PAM pgsql configuration files
# Olivier Thauvin <nanardon@mandriva.org>

# connect - the database connection string
# (see http://www.postgresql.org/docs/7.4/interactive/libpq.html#LIBPQ-CONNECT)

# auth_query      - authentication query (should return one column -- password)
# auth_succ_query - query to be executed after successful authentication
# auth_fail_query - query to be executed after failed authentication
# acct_query      - account options query (should return 3 boolean columns -- expired, new password required and password is null)
# pwd_query       - query to be executed for password changing

# You can use %u as username, %p as (new) password, %h for hostname of client
# as specified by PAM subsystem, %i for IP got by gethostbyname(%h) and %s as
# pa service name in any query. Please don't forget to specify pw_type as %p
# is replaced by password of pw_type form.

connect = dbname=sysdb user=ljb password=sth connect_timeout=15
auth_query = select user_password from account where user_name = %u
acct_query = select (acc_expired = 'y' OR acc_expired = '1'), (acc_new_pwreq = 'y' OR acc_new_pwreq = '1'), (user_password
 IS NULL OR user_password = '') from account where user_name = %u
pwd_query = update account set user_password = %p where user_name = %u
pw_type = crypt_md5

EOF


%clean
rm -rf %buildroot

%files
%defattr(-, root, root)
%doc CREDITS README
/%_lib/security/pam_pgsql.*
%attr(600, root, root) %config(noreplace) %_sysconfdir/pam_pgsql.conf


