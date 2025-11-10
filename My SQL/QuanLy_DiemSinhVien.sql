-- tạo database
CREATE DATABASE QuanLy_DiemSinhVien CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- sử dụng database vừa tạo 
use QuanLy_DiemSinhVien;

-- tạo bảng 
-- bảng khoa 
create table khoa(
	maKhoa char(10) primary key,
    tenKhoa varchar(100) not null
);  
INSERT INTO khoa VALUES ('CNTT', 'Công nghệ thông tin'),
						('KT', 'Kinh tế'),
                        ('NN','Nông Nghiệp'),
                        ('SP','Sư Phạm');
-- bảng lớp 
create table lop(
	maLop char(10) primary key,
    tenLop varchar(100) not null,
    maKhoa char(10),
    foreign key (maKhoa) references khoa(maKhoa)
); 
INSERT INTO lop VALUES ('DH24TH2', 'Công nghệ thông tin - 02', 'CNTT'),
						('DH24PM1', 'Kỹ thuật phần mền - 01', 'CNTT'),
                        ('DH24PM2', 'Kỹ thuật phần mền - 02', 'CNTT'),
						('DH24MK1','Marketing - 01','KT'),
						('DH24MK2', 'Marketing - 02', 'KT'),
                        ('DH24BT1','Bảo vệ thực vật - 01','NN'),
                        ('DH24BT2', 'Bảo vệ thực vật - 02', 'NN'),
                        ('DH24AV1','Sử phạm tiếng anh - 01','SP'),
                        ('DH24AV2', 'Sử phạm tiếng anh - 02', 'SP'),
                        ('DH24TY', 'Thú y ', 'NN'),
                        ('DH24KT', 'Kế toán ', 'KT'),
                        ('DH24GT', 'Giáo dục tiểu học', 'SP');

-- bảng sinh viên 
create table sinhvien (
	maSV char(10) primary key,
    hoTen varchar(100) not null,
    ngaySinh date,
    gioiTinh enum ( 'Nam','Nữ'),
    diaChi varchar(200),
    maLop char(10),
    foreign key (maLop) references lop(maLop)
);
INSERT INTO sinhvien VALUES ('DTH235677', 'Trần Duy Khánh', '2005-09-10', 'Nam', 'An Giang', 'DH24TH2'),
							('DTH237612', 'Bùi Thành Nhơn', '2005-06-06', 'Nam', 'An Giang', 'DH24PM2'),
							('DPM236537', 'Trần Hoài Phương', '2005-05-16', 'Nam', 'TP.Hồ Chí Minh', 'DH24PM1'),
                            ('DMK237859', 'Nguyễn Trọng Nghĩa', '2005-11-6', 'Nam', 'Hà Nội', 'DH24MK1'),
                            ('DMK236120', 'Nguyễn Minh Trường', '2005-09-08', 'Nam', 'Vĩnh Long ', 'DH24MK2'),
                            ('DAV235696', 'Nguyễn Hữu Chương', '2005-01-01', 'Nam', 'An Giang', 'DH24AV2'),
                            ('DAV237847', 'Nguyễn Trí Tài', '2005-01-28', 'Nam', 'An Giang', 'DH24AV1'),
                            ('DKT239858', 'Nguyễn Bảo Minh', '2005-12-25', 'Nam', 'Kiên Giang', 'DH24KT'),
							('DBT233295', 'Đỗ Thanh Vy', '2005-06-08', 'Nữ', 'Đồng Tháp', 'DH24BT1'),
                            ('DTY239270', 'Diệp Yến Vy', '2005-01-28', 'Nữ', 'TP.Hồ Chí Minh', 'DH24TY'),
                            ('DGT237096', 'Nguyễn Hoàng Nam', '2005-01-12', 'Nam', 'Lạng Sơn', 'DH24GT');
                            

-- bảng giảng viên
CREATE TABLE giangvien (
    maGV VARCHAR(10) PRIMARY KEY,
    hoTen VARCHAR(100) NOT NULL,
    maKhoa VARCHAR(10),
    matKhau VARCHAR(50) NOT NULL,
    FOREIGN KEY (maKhoa) REFERENCES khoa(maKhoa)
);
INSERT INTO giangvien VALUES ('GV001', 'Trần Duy Khánh', 'CNTT', '091025'),
							 ('GV002', 'Đỗ Thị Vy', 'NN', '080603'),
							 ('GV003', 'Bùi Thành Nhơn', 'KT', '123456');

-- bảng môn học
CREATE TABLE monhoc (
    maMH CHAR(10) PRIMARY KEY,
    tenMH VARCHAR(100) NOT NULL,
    soTinChi INT NOT NULL,
    maGV CHAR(10),
    FOREIGN KEY (maGV) REFERENCES giangvien(maGV)
);
INSERT INTO monhoc VALUES ('MH01', 'Cơ sở dữ liệu', 3, 'GV001'),
						  ('MH02', 'Tuyến trùng', 4, 'GV002'),
                          ('MH03', 'Toán c', 2, 'GV002'),
                          ('MH04', 'Kinh tế chính trị', 3, 'GV003'),
                          ('MH05', 'Kỹ năng giảng dạy', 4, 'GV003'),
                          ('MH06', 'Kiến trúc máy tính', 3, 'GV001'),
                          ('MH07', 'Lý thuyết đò thị', 3, 'GV001'),
                          ('MH08', 'Cây ăn quả', 4, 'GV002'),
                          ('MH09', 'Ngữ pháp', 2, 'GV003'),
                          ('MH10', 'Xác xuất thông kê', 3, 'GV001'),
                          ('MH11', 'Lập trình cân bảng ', 4, 'GV001'),
						  ('MH12', 'Sinh học đại cương ', 4, 'GV002'),
                          ('MH13', 'Tài chính ngân hàng ', 3, 'GV003');

-- bảng điểm
CREATE TABLE diem (
    maSV CHAR(10),
    maMH CHAR(10),
    diemQT FLOAT CHECK (diemQT BETWEEN 0 AND 10),
    diemThi FLOAT CHECK (diemThi BETWEEN 0 AND 10),
    diemTong FLOAT GENERATED ALWAYS AS ((diemQT * 0.4) + (diemThi * 0.6)) STORED,
    PRIMARY KEY (maSV, maMH),
    FOREIGN KEY (maSV) REFERENCES sinhvien(maSV),
    FOREIGN KEY (maMH) REFERENCES monhoc(maMH)
);
INSERT INTO diem (maSV, maMH, diemQT, diemThi) VALUES 
							('DTH235677', 'MH01', 8.0, 9.0),
                            ('DTH235677', 'MH06', 8.0, 7.0),
                            ('DPM236537', 'MH07', 8.5, 7.0),
                            ('DMK237859', 'MH13', 7.0, 6.0),
                            ('DMK237859', 'MH03', 7.0, 9.0),
                            ('DBT233295', 'MH02', 6.0, 9.5),
                            ('DBT233295', 'MH08', 8.0, 9.5),
                            ('DTH237612', 'MH11', 5.5, 9.0),
                            ('DKT239858', 'MH04', 6.0, 8.0),
                            ('DMK236120', 'MH10', 8.0, 9.0),
                            ('DTY239270', 'MH12', 5.0, 8.0),
                            ('DGT237096', 'MH05', 9.0, 9.5),
                            ('DAV235696', 'MH09', 7.0, 8.7),
                            ('DAV237847', 'MH05', 7.0, 6.5);
                            
-- hiển thị bảng khoa
SELECT 
    maKhoa AS 'Mã Khoa',
    tenKhoa AS 'Tên Khoa'
FROM khoa;

-- hiển thị bảng điểm
SELECT 
    maSV AS 'Mã Sinh Viên',
    maMH AS 'Mã Môn Học',
    diemQT AS 'Điểm Quá Trình',
    diemThi AS 'Điểm Thi'
FROM diem;

-- hiển thị bảng lớp
SELECT 
    maLop AS 'Mã Lớp',
    tenLop AS 'Tên Lớp',
    maKhoa AS 'Mã Khoa'
FROM lop;

-- hiển thị bảng môn học
SELECT 
    maMH AS 'Mã Môn Học',
    tenMH AS 'Tên Môn Học',
    soTinChi AS 'Số Tín Chỉ',
    maGV AS 'Giảng Viên Phụ Trách'
FROM monhoc;

-- hiển thị bảng sinh viên 
SELECT 
    maSV AS 'Mã Sinh Viên',
    hoTen AS 'Họ Tên',
    ngaySinh AS 'Ngày Sinh',
    gioiTinh AS 'Giới Tính',
    diaChi AS 'Địa Chỉ',
    maLop AS 'Mã Lớp'
FROM sinhvien;

-- hiển thị bảng giảng viên 
SELECT 
    maGV AS 'Mã Giảng Viên',
    hoTen AS 'Họ Tên Giảng Viên',
    maKhoa AS 'Mã Khoa'
FROM giangvien;

-- hiển thị kết quả 
SELECT 
    sv.maSV AS 'Mã Sinh Viên',
    sv.hoTen AS 'Họ Tên Sinh Viên',
    mh.tenMH AS 'Tên Môn Học',
    d.diemQT AS 'Điểm Quá Trình',
    d.diemThi AS 'Điểm Thi'
FROM diem d
JOIN sinhvien sv ON d.maSV = sv.maSV
JOIN monhoc mh ON d.maMH = mh.maMH;

-- kết quả tổng điểm
SELECT 
    sv.hoTen AS 'Họ Tên Sinh Viên',
    mh.tenMH AS 'Tên Môn Học',
    d.diemQT AS 'Điểm Quá Trình',
    d.diemThi AS 'Điểm Thi',
    d.diemTong AS 'Điểm Tổng'
FROM diem d
JOIN sinhvien sv ON d.maSV = sv.maSV
JOIN monhoc mh ON d.maMH = mh.maMH;

-- Xóa bảng 
USE ql_diemsinhvien;

DROP TABLE IF EXISTS diem;
DROP TABLE IF EXISTS sinhvien;
DROP TABLE IF EXISTS monhoc;
DROP TABLE IF EXISTS giangvien;
DROP TABLE IF EXISTS lop;
DROP TABLE IF EXISTS khoa;







