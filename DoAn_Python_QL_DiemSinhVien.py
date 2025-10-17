import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from tkcalendar import DateEntry

# ===== HÀM KẾT NỐI DATABASE =====
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Khanh@091025",  
        database="ql_diemsinhvien"
        #hàm này để mở kết nối đến database ql_diemsinhvien.
    )
 
# ===== HÀM CHUYỂN FRAME =====
def show_frame(name):
    for f in frames.values():
        f.pack_forget()  #n frame khỏi cửa sổ — nhưng không xóa nội dung.
    frames[name].pack(fill="both", expand=True) #làm frame giãn đầy vùng chứa.
    #Hàm này ẩn tất cả các frame, sau đó hiển thị frame có tên name.

# ===== HÀM TẢI DỮ LIỆU =====
def load_data(table_name, tree):
    for item in tree.get_children(): #xóa toàn bộ hàng hiện có trong Treeview để tránh chồng dữ liệu khi tải lại.
        tree.delete(item)
    conn = connect_db() #mở kết nối database
    cursor = conn.cursor() #tạo cursor để chạy truy vấn.

    query_map = { #là dict ánh xạ tên logical (vd "sinhvien") sang câu SQL tương ứng. Giúp hàm chung xử lý nhiều bảng.
        "khoa": "SELECT maKhoa AS 'Mã Khoa', tenKhoa AS 'Tên Khoa' FROM khoa",
        "lop": "SELECT maLop AS 'Mã Lớp', tenLop AS 'Tên Lớp', maKhoa AS 'Mã Khoa' FROM lop",
        "giangvien": "SELECT  maGV AS 'Mã Giảng Viên', hoTen AS 'Họ Tên Giảng Viên', maKhoa AS 'Mã Khoa' FROM giangvien",
        "sinhvien": "SELECT maSV AS 'Mã Số Sinh Viên', hoTen AS 'Họ Tên', ngaySinh AS 'Ngày Sinh', gioiTinh AS 'Giới Tính', diaChi AS 'Địa Chỉ', maLop AS 'Mã Lớp' FROM sinhvien",
        "monhoc": "SELECT maMH AS 'Mã Môn Học', tenMH AS 'Tên Môn Học', soTinChi AS 'Số Tín Chỉ', maGV AS 'Giảng Viên Phụ Trách' FROM monhoc",
        "diem": "SELECT maSV AS 'Mã Số Sinh Viên', maMH AS 'Mã Môn Học', diemQT AS 'Điểm Quá Trình', diemThi AS 'Điểm Thi', diemTong AS 'Điểm Tổng' FROM diem"
    }

    cursor.execute(query_map[table_name])
    rows = cursor.fetchall()
    #Thực hiện truy vấn và lấy toàn bộ dữ liệu về.

    columns = [desc[0] for desc in cursor.description] #ấy tên cột (để gán header cho Treeview).
    tree["columns"] = columns #đặt cấu hình cột cho Treeview.
    for col in columns:
        tree.heading(col, text=col) #đặt tiêu đề hiển thị.
        tree.column(col, width=150, anchor="center") #đặt chiều rộng và căn giữa nội dung cột.

    for row in rows:
        tree.insert("", "end", values=row) #thêm từng hàng vào Treeview.
    conn.close() #đóng kết nối (rất quan trọng để giải phóng tài nguyên). 

# ===== HÀM TÍNH ĐIỂM TB & XẾP LOẠI =====
def calc_average(tree):
    for item in tree.get_children():
        tree.delete(item)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sv.maSV, sv.hoTen, AVG(d.diemTong) AS diemTB,
        CASE
            WHEN AVG(d.diemTong) >= 8 THEN 'Giỏi'
            WHEN AVG(d.diemTong) >= 6.5 THEN 'Khá'
            WHEN AVG(d.diemTong) >= 5 THEN 'Trung bình'
            ELSE 'Yếu'
        END AS xepLoai
        FROM diem d
        JOIN sinhvien sv ON d.maSV = sv.maSV
        GROUP BY sv.maSV, sv.hoTen
    """)
    rows = cursor.fetchall()
    columns = ["Mã SV", "Họ Tên", "Điểm TB", "Xếp loại"]
    tree["columns"] = columns
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")
    for row in rows:
        diem_tb = round(row[2], 2) if row[2] is not None else 0  # làm tròn 2 chữ số thập phân (đã chỉnh theo yêu cầu trước). và tránh lỗi với sinh viên không có điểm.
        tree.insert("", "end", values=(row[0], row[1], diem_tb, row[3]))
    conn.close()

# ====== TẠO CỬA SỔ CHÍNH ======
root = tk.Tk()
root.title("Quản lý điểm sinh viên")
root.geometry("700x500")
root.config(bg="#f7f7f7")
root.resizable(False, False)

# ===== CĂN GIỮA MÀN HÌNH =====
window_width = 700
window_height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

root.geometry(f"{window_width}x{window_height}+{x}+{y}")  # 👈 đặt vị trí giữa màn hình
root.config(bg="#f7f7f7")
root.resizable(False, False)

# ===== MENU =====
menu = tk.Menu(root) #Tạo menu để thêm submenu cho chuyển trang.
root.config(menu=menu)

frames = {} #frames dict lưu Frame cho mỗi bảng.
tables = ["diem", "sinhvien", "lop", "khoa", "giangvien", "monhoc"] #tables danh sách tên dùng để tạo frames theo vòng lặp.
titles = {
    "diem": "QUẢN LÝ ĐIỂM SINH VIÊN",
    "sinhvien": "DANH SÁCH SINH VIÊN",
    "lop": "DANH SÁCH LỚP",
    "khoa": "DANH SÁCH KHOA",
    "giangvien": "DANH SÁCH GIẢNG VIÊN",
    "monhoc": "DANH SÁCH MÔN HỌC"
}

# ===== FONT CHUNG =====
title_font = ("Arial", 18, "bold")
# ===== TẠO FRAME =====
for t in tables: #Vòng lặp tạo frame cho từng bảng
    frames[t] = tk.Frame(root, bg="#fff")
    # ===== TIÊU ĐỀ =====
    title_label = tk.Label(
        frames[t],
        text=titles[t],
        font=title_font,
        fg="#333",
        bg="#fff"
    )
    title_label.pack(pady=(20, 5))
    
    # ==== TRANG QUẢN LÝ ĐIỂM ====
    if t == "diem":
        # --- FORM NHẬP LIỆU ---
        form = tk.Frame(frames[t], bg="#fff")
        form.pack(pady=20, padx=100, fill="x") #fill="x" cho form giúp giãn ngang.
        # Text mã số sinh viên
        tk.Label(form, text="Mã số sinh viên:", bg="#fff").grid(row=0, column=0, padx=10, pady=5,sticky="w") #Sử dụng grid để điều chỉnh vị trí label + entry theo hàng/cột.
        maSV_entry = tk.Entry(form, width=20)
        maSV_entry.grid(row=0, column=1, padx=5, pady=5,sticky="w")
        # Text nã môn học
        tk.Label(form, text="Mã môn học:", bg="#fff").grid(row=0, column=2, padx=10, pady=5,sticky="w")
        maMH_entry = tk.Entry(form, width=20)
        maMH_entry.grid(row=0, column=3, padx=5, pady=5,sticky="w")
        # Text điểm quá trình
        tk.Label(form, text="Điểm quá trình:", bg="#fff").grid(row=1, column=0, padx=10, pady=5,sticky="w")
        diemQT_entry = tk.Entry(form, width=20)
        diemQT_entry.grid(row=1, column=1, padx=5, pady=5)
        # Text điểm thi
        tk.Label(form, text="Điểm thi:", bg="#fff").grid(row=1, column=2, padx=10, pady=5,sticky="w")
        diemThi_entry = tk.Entry(form, width=20)
        diemThi_entry.grid(row=1, column=3, padx=5, pady=5)

        # ====== HÀM RESET ======
        def reset_fields():
            maSV_entry.delete(0, tk.END)
            maMH_entry.delete(0, tk.END)
            diemQT_entry.delete(0, tk.END)
            diemThi_entry.delete(0, tk.END)
        # --- NÚT CHỨC NĂNG ---
        btn_frame = tk.Frame(frames[t], bg="#fff")
        btn_frame.pack(pady=2)

        ttk.Button(btn_frame, text="Thêm điểm", width=15, command=lambda: add_diem()).grid(row=0, column=0, padx=8, pady=8)
        ttk.Button(btn_frame, text="Sửa điểm", width=15, command=lambda: update_diem()).grid(row=0, column=1, padx=8, pady=8)
        ttk.Button(btn_frame, text="Xóa điểm", width=15, command=lambda: delete_diem()).grid(row=0, column=2, padx=8, pady=8)
        ttk.Button(btn_frame, text="Tính điểm TB & Xếp loại", width=25, command=lambda tr=None: calc_average(tree_diem)).grid(row=0, column=3, padx=8, pady=8)
        ttk.Button(btn_frame, text="Tải danh sách", width=15, command=lambda n=t: load_data("diem", tree_diem)).grid(row=0, column=4, padx=8, pady=8)
        
        btn_frame2 = tk.Frame(frames[t], bg="#fff")
        btn_frame2.pack(pady=2)
    
        ttk.Button(btn_frame2, text="Reset", width=18, command=reset_fields).pack(side="left", padx=10, pady=5)
        ttk.Button(btn_frame2, text="Thoát", width=18, style="Accent.TButton", command=root.destroy).pack(side="left", padx=10 ,pady=5)#Sử dụng grid cho hàng 1, dùng pack(side="left") cho hàng 2 để căn giữa.
        # --- BẢNG DỮ LIỆU ---
        tree_diem = ttk.Treeview(frames[t], show="headings") #show="headings" tắt cột mặc định (tree icon) — chỉ hiển thị cột bạn đặt bằng tree["columns"].
        tree_diem.pack(fill="both", expand=True, padx=10, pady=10) #pack(fill="both", expand=True) cho bảng giãn chiếm toàn bộ vùng còn lại.

        def select_item(event):
            selected = tree_diem.focus()
            if not selected:
                return
            values = tree_diem.item(selected, "values")
            if len(values) >= 4:
                maSV_entry.delete(0, tk.END)
                maSV_entry.insert(0, values[0])
                maMH_entry.delete(0, tk.END)
                maMH_entry.insert(0, values[1])
                diemQT_entry.delete(0, tk.END)
                diemQT_entry.insert(0, values[2])
                diemThi_entry.delete(0, tk.END)
                diemThi_entry.insert(0, values[3])
        tree_diem.bind("<ButtonRelease-1>", select_item)
        #Khi nhả chuột trên một hàng, lấy id của dòng đang focus, rồi lấy values.
        #Điền giá trị vào các Entry để sửa hoặc xóa thuận tiện.
        
        # ==== HÀM THÊM ====
        def add_diem():
            try:
                maSV = maSV_entry.get()
                maMH = maMH_entry.get()
                diemQT = float(diemQT_entry.get()) #Lấy dữ liệu từ Entry, ép kiểu float cho điểm.
                diemThi = float(diemThi_entry.get())
                diemTong = diemQT * 0.4 + diemThi * 0.6

                conn = connect_db()
                cur = conn.cursor()
                cur.execute("INSERT INTO diem (maSV, maMH, diemQT, diemThi) VALUES (%s, %s, %s, %s)", (maSV, maMH, diemQT, diemThi))
                conn.commit()
                conn.close()
                messagebox.showinfo("Thành công", "Đã thêm điểm!")
                load_data("diem", tree_diem) #Gọi load_data("diem", tree_diem) để refresh bảng hiển thị sau khi thao tác.
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))
                
        # ==== HÀM SỬA ====
        def update_diem(): #dùng UPDATE ... WHERE maSV=%s AND maMH=%s để cập nhật điểm.
            try:
                maSV = maSV_entry.get()
                maMH = maMH_entry.get()
                diemQT = float(diemQT_entry.get())
                diemThi = float(diemThi_entry.get())
                diemTong = diemQT * 0.4 + diemThi * 0.6
                conn = connect_db()
                cur = conn.cursor()
                cur.execute("UPDATE diem SET diemQT=%s, diemThi=%s WHERE maSV=%s AND maMH=%s",(diemQT, diemThi, maSV, maMH))
                conn.commit()
                conn.close()
                messagebox.showinfo("Thành công", "Đã cập nhật điểm!")
                load_data("diem", tree_diem) #gọi load_data sau khi commit để cập nhật UI.
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))
        
        # ==== HÀM XÓA ====
        def delete_diem(): #dùng DELETE FROM diem WHERE maSV=%s AND maMH=%s để xóa.
            try:
                maSV = maSV_entry.get()
                maMH = maMH_entry.get()
                conn = connect_db()
                cur = conn.cursor()
                cur.execute("DELETE FROM diem WHERE maSV=%s AND maMH=%s", (maSV, maMH))
                conn.commit()
                conn.close()
                messagebox.showinfo("Thành công", "Đã xóa điểm!")
                load_data("diem", tree_diem) #gọi load_data sau khi commit để cập nhật UI.
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))
    else:
        
        # === Các trang khác ===
        tree = ttk.Treeview(frames[t], show="headings")
        tree.pack(fill="both", expand=True, padx=10, pady=10)
        ttk.Button(frames[t], text="Tải danh sách", command=lambda n=t, tr=tree: load_data(n, tr)).pack(pady=5)

# ===== MENU CHUYỂN TRANG =====
submenu = tk.Menu(menu, tearoff=0) #Tạo một submenu trong thanh menu chính.
menu.add_cascade(label=" Trang chính", menu=submenu)
for t in tables:
    submenu.add_command(label=titles[t], command=lambda n=t: show_frame(n)) #add_command(..., command=lambda n=t: show_frame(n)) — dùng lambda n=t để giữ giá trị t chính xác trong vòng lặp (important).

root.update() #cập nhật giao diện trước khi lấy kích thước.
root.minsize(root.winfo_width(), root.winfo_height()) #đặt kích thước tối thiểu ứng dụng bằng kích thước hiện tại, tránh bị thu nhỏ quá.

show_frame("diem") #hiển thị trang mặc định.
root.mainloop() #bắt đầu vòng lặp sự kiện Tkinter — GUI phản hồi người dùng cho đến khi đóng.
