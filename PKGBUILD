# Maintainer: Josh VanderLinden <arch@cloudlery.com>
pkgname=python-treksum
pkgver=r33.e8a3d28
pkgrel=1
pkgdesc="Library for generating lorem ipsum-like text from Star Trek: TNG scripts"
arch=('any')
url="https://github.com/codekoala/treksum"
license=('custom')
depends=('python')
makedepends=('git')
source=("treksum-git::git+https://github.com/codekoala/treksum")
md5sums=('SKIP')

pkgver() {
  cd "${srcdir}/treksum-git"
  printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

build() {
  cd "${srcdir}/treksum-git"

  mkdir -p treksum/data
  python treksum/strip.py
}

package() {
  cd "${srcdir}/treksum-git"
  python setup.py install --root="${pkgdir}/" --optimize=1

  rm -f ${pkgdir}/usr/data/*.gzc

  install -Dm644 LICENSE.txt ${pkgdir}/usr/share/licenses/${pkgname}/LICENSE
}

# vim:set ts=2 sw=2 et:
