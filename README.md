# CS106.K21

### Thành viên nhóm DTL:
1. Trần Tuấn Vĩ 
2. Phạm Xuân Thiên
3. Vũ Ngọc Tú
4. Trịnh Quang Trường
5. Tăng Năng Chung

## Hướng dẫn cài đặt

### Yêu cầu:
Hệ điều hành Ubuntu 18.04 trở lên (Đã test trên 20.04) 

Python phiên bản >= 3.6
```
sudo apt-get update
sudo apt install python3
python3 --version
```

Java phiên bản 1.8.0_242
```
sudo apt-get update
sudo apt-get install openjdk-8-jdk
java --version
```

Virtualenv
```
sudo apt install python3-venv
```

Pip3 (Trình quản lí package của Python)
```
sudo apt install python3-pip
```

### Tải về

Cách 1: Sử dụng git
```
git clone 'https://github.com/UITTrinhQuangTruong/CS106.K21.git'
```

Cách 2: Tải file .zip về giải nén với lệnh
```
unzip your/path/file.zip your/path/file 
```

### Tạo máy ảo
```
cd /your/path/file
python3 -m venv myenv
source myenv/bin/activate
```

### Cài đặt các thư viện hỗ trợ

Cài đặt các thư viện cần thiết
```
pip3 install -r requirements.txt
```

### Chạy ứng dụng với lệnh
```
flask run
```

### Link hướng dẫn:
https://youtu.be/zRe7vLa6WB4
