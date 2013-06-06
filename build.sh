#!/bin/bash

RPM_SPEC="spaceclone.spec"
RPM_TGZ="spaceclone.tar.gz"

LOCKFILE="/tmp/${RPM_SPEC}.lock"
BASEDIR=`pwd`

cleanup()
{
	rm -f $LOCKFILE
	cd $BASEDIR
	exit 0
}
ctrl_c()
{
    echo "Caught CTRL+C, cleaning up"
    cleanup
}

trap ctrl_c SIGINT

if [[ -e $LOCKFILE ]]
then
    echo "$LOCKFILE exists"
    cat $LOCKFILE
    echo "Verify this user is not building and clean up before you continue"
    exit 1
else
    echo $USER > $LOCKFILE
fi

mkdir -p rpms/

revision=$(date +%s)
echo "Revision: $revision"
sed -i -r "s/Release:.*/Release: $revision/g" ${RPM_SPEC}
cd $(dirname $0)
tarball=$(rpm -E '%_sourcedir')/${RPM_TGZ}

tar zvcf $tarball --exclude git --exclude .svn src/

cp ${RPM_TGZ} $(rpm -E '%_sourcedir')/

[ ! -d $(dirname $tarball/../SRPMS) ] && mkdir -p $(dirname $tarball)/../SRPMS
[ ! -d $(dirname $tarball/../RPMS) ] && mkdir -p $(dirname $tarball)/../RPMS

rm *.rpm >/dev/null 2>&1
rm -rf build

echo Creating source rpm
srpm=$(rpmbuild -bs ${RPM_SPEC} | sed "s/Wrote: //")

echo Building RPM in mock
/usr/bin/mock -r default $srpm
cp /var/lib/mock/*/result/*.rpm rpms/

cleanup
