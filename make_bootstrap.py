import tarfile
import subprocess
import os
import platform

if platform.system() == "Windows":
    os.chdir(os.environ['USERPROFILE'])
else:
    os.chdir(os.environ['HOME'])
if os.path.exists("bootstramp.tar"):
    os.unlink("bootstrap.tar")
tar = tarfile.open("bootstrap.tar", "w")
for name in [".gnupg/private.key", ".gnupg/public.key", ".ssh/id_rsa", ".ssh/id_rsa.pub"]:
    tar.add(name)
tar.close()
subprocess.call(["openssl",  "des3", "-in", "bootstrap.tar", "-out", "bootstrap.tar.des3"])
os.unlink("bootstrap.tar")

