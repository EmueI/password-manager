![Project downloads](https://img.shields.io/github/downloads/EmueI/password-manager/total)

# About the project
 A password manager written entirely in Python with the PySide6 module. 



# Demo
Here is a quick demo of adding a password with the application. 


![linked-banner](https://i.ibb.co/4JBRMt7/Screenshot-2022-03-11-162837.png)



# Setup

### Install the required Python libraries

```sh
pip -r install requirements.txt
```

### Install FindBin and IPC-Cmd
```sh
sudo apt install perl-FindBin
sudo apt install perl-IPC-Cmd
sudo apt install perl-File-Copy
sudo apt install perl-File-Compare
```

### Install and Configure OpenSSL

Download OpenSSL 3.0.2 using wget:
```sh
cd /usr/local/src/
sudo wget https://www.openssl.org/source/openssl-3.0.2.tar.gz
sudo tar -xf openssl-3.0.2.tar.gz
cd openssl-3.0.2
```
Configure and compile OpenSSL:
```sh
sudo ./config --prefix=/usr/local/ssl --openssldir=/usr/local/ssl shared zlib
sudo make
sudo make test
sudo make install
```

### Install SQLCipher and pysqlcipher3
```sh 
sudo apt install sqlcipher libsqlcipher0 libsqlcipher-dev
sudo -H pip3 install pysqlcipher3
```


# Features
* Encrypted Database
* Random Password Generator 
* Password Health Dashboard



# Built with
* [PySide6](https://pypi.org/project/PySide6/)
* [Qt Designer](https://doc.qt.io/qt-5/qtdesigner-manual.html)
* [SQLCipher](https://github.com/sqlcipher/sqlcipher)



# ⚠️ Disclaimer

This project has not been extensively tested for any security issues.

It is not recommended to enter any personal account information. 
