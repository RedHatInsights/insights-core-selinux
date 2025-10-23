set -euxo pipefail

rpmbuild_dir="$(mktemp -d)"
distgit_dir="$rpmbuild_dir/SOURCES"
mkdir -p "$distgit_dir"

version=`grep "Version:" scripts/insights-core-selinux.spec | awk '{print $2}'`
mkdir -p "$distgit_dir/insights-core-selinux-$version"
cp insights_core.* Makefile LICENSE "$distgit_dir/insights-core-selinux-$version"

(cd "$distgit_dir/insights-core-selinux-$version" && make )
(cd "$distgit_dir" && tar zcf "$distgit_dir/insights-core-selinux-$version.tar.gz" "insights-core-selinux-$version")

rpmbuild --define "_topdir $rpmbuild_dir" -ba "scripts/insights-core-selinux.spec"

cp $rpmbuild_dir/RPMS/noarch/*.rpm $rpmbuild_dir/SRPMS/*.rpm "./"
