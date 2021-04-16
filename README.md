# LinkedOutServer

Backend server dùng cho [LinkedOutApp](https://github.com/tacbliw/LinkedOutApp) (Bài tập lớn môn Phát triển ứng dụng di động (INT3120 1))

## Cài đặt và chuẩn bị môi trường

### 1. Cài đặt dependencies

```bash
python -m pip install -r requirements.txt
```

### 2. Chuẩn bị cơ sở dữ liệu (MySQL)

Cài đặt MySQL, sau đó tạo cơ sở dữ liệu và cấp quyền.

```sql
CREATE DATABASE backend CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
CREATE USER 'backend'@'%' IDENTIFIED BY 'backend';
GRANT ALL PRIVILEGES ON backend.* TO 'backend'@'%';
FLUSH PRIVILEGES;
```

### 3. Chuẩn bị môi trường

On Linux

```bash
export DJANGO_DATABASE_HOST="localhost"
export DJANGO_DATABASE_NAME="backend"
export DJANGO_DATABASE_USER="backend"
export DJANGO_DATABASE_PASSWORD="backend"
export DJANGO_CONFIG_SECRETKEY="ihateyou"
```

On Windows

Thêm 5 environment variables ở trên theo [hướng dẫn](https://www.architectryan.com/2018/08/31/how-to-change-environment-variables-on-windows-10/).

## Run

### 1. Migrate database

```bash
python manage.py makemigrations
python manage.py migrate
```

### 2. Chạy server

```bash
python manage.py runserver
```

## Dữ liệu mẫu
Có thể sử dụng dữ liệu mẫu ở [đây](https://drive.google.com/file/d/1cNSVeVk8bPR3z8l2FUc8r4v4HPm9esHK/view?usp=sharing)

Trong bộ dữ liệu mẫu có:
- 6 tài khoản người dùng: `user0001` - `user0006`, mật khẩu giống tên tài khoản.
- 3 tài khoản doanh nghiệp: `company01` - `company03`, mật khẩu giống tên tài khoản.
- Các tags về `Kỹ năng`, `Địa điểm`, `Trường Đại học`.
- Có sẵn một số bài đăng, công việc, bình luận, thông báo và tin nhẵn.
- Tài khoản quản trị: `admin:profNPT123` (Đăng nhập tại localhost:8000/admin)
