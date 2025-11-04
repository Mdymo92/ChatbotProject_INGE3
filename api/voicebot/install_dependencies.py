import os

def install_dependencies_dnf():
  os.system('sudo dnf install -y espeak')
  os.system('sudo dnf distro-sync -y')
  os.system('sudo dnf install -y alsa-utils')
  os.system('sudo dnf install -y ffmpeg')

def install_dependencies_apt():
  os.system('sudo apt-get update')
  os.system('sudo apt-get install -y espeak')
  os.system('sudo apt-get install -y alsa-utils')
  os.system('sudo apt-get install -y ffmpeg')
  

os_release = os.popen('cat /etc/os-release | grep -oP "ID=\K\w+"').read().strip()
first_item = os_release.splitlines()[0]
print('Detected OS Release:', first_item)

if first_item == 'fedora':
  print('Installing dependencies with DNF...')
  install_dependencies_dnf()
else:
  print('Installing dependencies with APT...')
  install_dependencies_apt()


  