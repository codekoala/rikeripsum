# Maintainer: Josh VanderLinden <arch@cloudlery.com>
pkgname=python-treksum
pkgver=r32.e8564f4
pkgrel=1
pkgdesc="Library for generating lorem ipsum-like text from Star Trek: TNG scripts"
arch=('any')
url="https://github.com/codekoala/treksum"
license=('custom')
depends=('python')
makedepends=('git')

_gitroot=https://github.com/codekoala/treksum
_gitname=treksum

pkgver() {
  cd "${srcdir}/${_gitname}-build"
  printf "r%s.%s" "$(git rev-list --count HEAD)" "$(git rev-parse --short HEAD)"
}

build() {
  cd "${srcdir}"
  msg "Connecting to GIT server...."

  if [[ -d "${_gitname}" ]]; then
    cd "${_gitname}" && git pull origin
    msg "The local files are updated."
  else
    git clone "${_gitroot}" "${_gitname}"
  fi

  msg "GIT checkout done or server timeout"
  msg "Starting build..."

  rm -rf "${srcdir}/${_gitname}-build"
  git clone "${srcdir}/${_gitname}" "${srcdir}/${_gitname}-build"


  cd "${srcdir}/${_gitname}-build"
  mkdir -p treksum/data
  python treksum/strip.py
}

package() {
  cd "${srcdir}/${_gitname}-build"
  python setup.py install --root="${pkgdir}/" --optimize=1

  rm -f ${pkgdir}/usr/data/*.gzc

  install -Dm644 LICENSE.txt ${pkgdir}/usr/share/licenses/${pkgname}/LICENSE
}

# vim:set ts=2 sw=2 et:
