import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from tkcalendar import DateEntry

# ===== KẾT NỐI DATABASE =====
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Khanh@091025",  # đổi theo máy bạn
        database="ql_diemsinhvien"
    )
 
# ===== HÀM CHUYỂN FRAME =====
def show_frame(name):
    for f in frames.values():
        f.pack_forget()   
    frames[name].pack(fill="both", expand=True)

# ===== HÀM TẢI DỮ LIỆU =====
def load_data(table_name, tree):
    for item in tree.get_children():
        tree.delete(item)
    conn = connect_db()
    cursor = conn.cursor()

    query_map = {
        "khoa": "SELECT maKhoa AS 'Mã Khoa', tenKhoa AS 'Tên Khoa' FROM khoa",
        "lop": "SELECT maLop AS 'Mã Lớp', tenLop AS 'Tên Lớp', maKhoa AS 'Mã Khoa' FROM lop",
        "giangvien": "SELECT  maGV AS 'Mã Giảng Viên', hoTen AS 'Họ Tên Giảng Viên', maKhoa AS 'Mã Khoa' FROM giangvien",
        "sinhvien": "SELECT maSV AS 'Mã Số Sinh Viên', hoTen AS 'Họ Tên', ngaySinh AS 'Ngày Sinh', gioiTinh AS 'Giới Tính', diaChi AS 'Địa Chỉ', maLop AS 'Mã Lớp' FROM sinhvien",
        "monhoc": "SELECT maMH AS 'Mã Môn Học', tenMH AS 'Tên Môn Học', soTinChi AS 'Số Tín Chỉ', maGV AS 'Giảng Viên Phụ Trách' FROM monhoc",
        "diem": "SELECT maSV AS 'Mã Số Sinh Viên', maMH AS 'Mã Môn Học', diemQT AS 'Điểm Quá Trình', diemThi AS 'Điểm Thi', diemTong AS 'Điểm Tổng' FROM diem"
    }

    cursor.execute(query_map[table_name])
    rows = cursor.fetchall()

    columns = [desc[0] for desc in cursor.description]
    tree["columns"] = columns
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")

    for row in rows:
        tree.insert("", "end", values=row)
    conn.close()

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
        tree.insert("", "end", values=row)
    conn.close()

# ====== TẠO CỬA SỔ CHÍNH ======
root = tk.Tk()
root.title("Quản lý điểm sinh viên")
root.geometry("700x500")
root.config(bg="#f7f7f7")
root.resizable(False, False)

# ===== MENU =====
menu = tk.Menu(root)
root.config(menu=menu)

frames = {}
tables = ["diem", "sinhvien", "lop", "khoa", "giangvien", "monhoc"]
titles = {
    "diem": "QUẢN LÝ ĐIỂM SINH VIÊN",
    "sinhvien": "QUẢN LÝ SINH VIÊN",
    "lop": "QUẢN LÝ LỚP",
    "khoa": "QUẢN LÝ KHOA",
    "giangvien": "QUẢN LÝ GIẢNG VIÊN",
    "monhoc": "QUẢN LÝ MÔN HỌC"
}

# ===== FONT CHUNG =====
title_font = ("Arial", 18, "bold")
# ===== TẠO FRAME =====
for t in tables:
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
        form.pack(pady=20, padx=100, fill="x")
        # Text mã số sinh viên
        tk.Label(form, text="Mã số sinh viên:", bg="#fff").grid(row=0, column=0, padx=10, pady=5,sticky="w")
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

        # --- NÚT CHỨC NĂNG ---
        btn_frame = tk.Frame(frames[t], bg="#fff")
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Thêm điểm",width=15, command=lambda: add_diem()).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Sửa điểm",width=15, command=lambda: update_diem()).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Xóa điểm",width=15, command=lambda: delete_diem()).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Tính điểm TB & Xếp loại",width=30, command=lambda tr=None: calc_average(tree_diem)).grid(row=0, column=3, padx=5)
        ttk.Button(btn_frame, text="Tải danh sách",width=15, command=lambda n=t: load_data("diem", tree_diem)).grid(row=0, column=4, padx=5)

        # --- BẢNG DỮ LIỆU ---
        tree_diem = ttk.Treeview(frames[t], show="headings")
        tree_diem.pack(fill="both", expand=True, padx=10, pady=10)

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
        
        # ==== HÀM THÊM ====
        def add_diem():
            try:
                maSV = maSV_entry.get()
                maMH = maMH_entry.get()
                diemQT = float(diemQT_entry.get())
                diemThi = float(diemThi_entry.get())
                diemTong = diemQT * 0.4 + diemThi * 0.6

                conn = connect_db()
                cur = conn.cursor()
                cur.execute("INSERT INTO diem (maSV, maMH, diemQT, diemThi) VALUES (%s, %s, %s, %s)",
                            (maSV, maMH, diemQT, diemThi))
                conn.commit()
                conn.close()
                messagebox.showinfo("Thành công", "Đã thêm điểm!")
                load_data("diem", tree_diem)
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))
                
        # ==== HÀM SỬA ====
        def update_diem():
            try:
                maSV = maSV_entry.get()
                maMH = maMH_entry.get()
                diemQT = float(diemQT_entry.get())
                diemThi = float(diemThi_entry.get())
                diemTong = diemQT * 0.4 + diemThi * 0.6
                conn = connect_db()
                cur = conn.cursor()
                cur.execute("UPDATE diem SET diemQT=%s, diemThi=%s WHERE maSV=%s AND maMH=%s",
                        (diemQT, diemThi, maSV, maMH))
                conn.commit()
                conn.close()
                messagebox.showinfo("Thành công", "Đã cập nhật điểm!")
                load_data("diem", tree_diem)
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))
                
        # ==== HÀM XÓA ====
        def delete_diem():
            try:
                maSV = maSV_entry.get()
                maMH = maMH_entry.get()
                conn = connect_db()
                cur = conn.cursor()
                cur.execute("DELETE FROM diem WHERE maSV=%s AND maMH=%s", (maSV, maMH))
                conn.commit()
                conn.close()
                messagebox.showinfo("Thành công", "Đã xóa điểm!")
                load_data("diem", tree_diem)
            except Exception as e:
                messagebox.showerror("Lỗi", str(e))
    else:
        
        # === Các trang khác ===
        tree = ttk.Treeview(frames[t], show="headings")
        tree.pack(fill="both", expand=True, padx=10, pady=10)
        ttk.Button(frames[t], text="Tải danh sách", command=lambda n=t, tr=tree: load_data(n, tr)).pack(pady=5)

# ===== MENU CHUYỂN TRANG =====
submenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label=" Trang chính", menu=submenu)
for t in tables:
    submenu.add_command(label=titles[t], command=lambda n=t: show_frame(n))

root.update()
root.minsize(root.winfo_width(), root.winfo_height())

show_frame("diem")
root.mainloop()
