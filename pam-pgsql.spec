Summary:	Postgresql authentication for PAM
Name:		pam-pgsql
Version:	0.7.3.1
Release:	2
Epoch:		1
License:	GPLv2+
Group:		System/Libraries
Url:		https://sourceforge.net/projects/pam-pgsql
Source0:	http://ovh.dl.sourceforge.net/sourceforge/pam-pgsql/%{name}-%{version}.tar.gz
BuildRequires:	mhash-devel
BuildRequires:	pam-devel
BuildRequires:	postgresql-devel
BuildRequires:	pkgconfig(libgcrypt)
Requires:	pam

%description
This is a module that allows people to login to PAM-aware applications by
authenticating to a Postgresql database.

%files
%doc CREDITS README CHANGELOG COPYRIGHT sample.sql
%{_libdir}/security/pam_pgsql.*
%attr(600, root, root) %config(noreplace) %{_sysconfdir}/pam_pgsql.conf

#----------------------------------------------------------------------------

%prep
%setup -q

%build
autoreconf -fi
%configure2_5x
%make

%install
%makeinstall_std

mkdir -p %{buildroot}%{_sysconfdir}
cat > %{buildroot}%{_sysconfdir}/pam_pgsql.conf <<EOF
# PAM pgsql configuration files
# Olivier Thauvin <nanardon@nanardon.zarb.org>

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

