import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# ====== KẾT NỐI DATABASE ======
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Khanh@091025",  # thay bằng mật khẩu MySQL của bạn
        database="ql_diem_sinhvien"
    )

# ====== HÀM CHUYỂN FRAME ======
def show_frame(frame):
    frame.tkraise()

# ====== HÀM LOAD DỮ LIỆU CHUNG ======
def load_data(table_name, tree):
    for item in tree.get_children():
        tree.delete(item)
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(f"SHOW COLUMNS FROM {table_name}")
    col_names = [col[0] for col in cur.fetchall()]
    tree["columns"] = col_names
    for col in col_names:
        tree.heading(col, text=col.upper())
        tree.column(col, anchor="center", width=120)
    cur.execute(f"SELECT * FROM {table_name}")
    rows = cur.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)
    conn.close()

# ====== TẠO CỬA SỔ CHÍNH ======
root = tk.Tk()
root.title("🎓 Ứng dụng Quản lý điểm sinh viên")
root.geometry("1150x700")

# ====== TẠO MENU ======
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# ====== FRAME CHÍNH ======
frames = {}
for F in ("trang_chu", "sinhvien", "monhoc", "diem", "lop", "khoa", "giangvien"):
    frame = tk.Frame(root)
    frame.place(x=0, y=0, width=1150, height=700)
    frames[F] = frame

# ================== TRANG CHỦ ==================
# ================== TRANG CHỦ (QUẢN LÝ ĐIỂM) ==================
frame_home = frames["trang_chu"]

# ====== TIÊU ĐỀ ======
banner = tk.Frame(frame_home, bg="#2c3e50", height=80)
banner.pack(fill="x")
tk.Label(
    banner,
    text="📊 BẢNG ĐIỂM TỔNG HỢP",
    font=("Arial", 22, "bold"),
    bg="#2c3e50",
    fg="white"
).pack(pady=16)

# ====== THANH TÌM KIẾM ======
toolbar = tk.Frame(frame_home, bg="#ecf0f1", pady=8)
toolbar.pack(fill="x")

tk.Label(toolbar, text="🔍 Tìm kiếm:", font=("Arial", 12, "bold"), bg="#ecf0f1").pack(side="left", padx=(12,6))
search_var = tk.StringVar()
search_entry = tk.Entry(toolbar, textvariable=search_var, width=40, font=("Arial", 12))
search_entry.pack(side="left", padx=6)

def tim_kiem():
    key = search_var.get().strip().lower()
    for i in tree_home.get_children(): tree_home.delete(i)
    conn = connect_db(); cur = conn.cursor()
    cur.execute("""
        SELECT d.maSV, sv.hoTen, d.maMH, mh.tenMH, d.diemQT, d.diemThi,
               ROUND(d.diemQT*0.4 + d.diemThi*0.6,2) AS diemTB,
               CASE
                 WHEN (d.diemQT*0.4 + d.diemThi*0.6) >= 8 THEN 'Giỏi'
                 WHEN (d.diemQT*0.4 + d.diemThi*0.6) >= 6.5 THEN 'Khá'
                 WHEN (d.diemQT*0.4 + d.diemThi*0.6) >= 5 THEN 'TB'
                 ELSE 'Yếu'
               END AS XepLoai
        FROM diem d
        JOIN sinhvien sv ON d.maSV = sv.maSV
        JOIN monhoc mh ON d.maMH = mh.maMH
        WHERE LOWER(sv.hoTen) LIKE %s OR LOWER(mh.tenMH) LIKE %s OR LOWER(d.maSV) LIKE %s OR LOWER(d.maMH) LIKE %s
        ORDER BY d.maSV;
    """, (f"%{key}%", f"%{key}%", f"%{key}%", f"%{key}%"))
    for row in cur.fetchall():
        tree_home.insert("", tk.END, values=row)
    conn.close()

tk.Button(toolbar, text="🔎 Tìm kiếm", command=tim_kiem, font=("Arial",11,"bold"), bg="#3498db", fg="white").pack(side="left", padx=6)
tk.Button(toolbar, text="🔄 Làm mới", command=lambda: show_bang_diem(), font=("Arial",11,"bold"), bg="#27ae60", fg="white").pack(side="left", padx=6)

# ====== BẢNG DỮ LIỆU ======
table_frame = tk.Frame(frame_home, bg="white")
table_frame.pack(fill="both", expand=True, padx=12, pady=8)

columns = ["Mã SV", "Họ Tên", "Mã MH", "Môn học", "Điểm QT", "Điểm Thi", "Điểm TB", "Xếp loại"]
tree_home = ttk.Treeview(table_frame, columns=columns, show="headings")
for col in columns:
    tree_home.heading(col, text=col)
    tree_home.column(col, width=140, anchor="center")
tree_home.pack(fill="both", expand=True, side="left")

scrollbar_home = ttk.Scrollbar(table_frame, orient="vertical", command=tree_home.yview)
tree_home.configure(yscrollcommand=scrollbar_home.set)
scrollbar_home.pack(side="right", fill="y")

# ====== HÀM HIỂN THỊ DỮ LIỆU ======
def show_bang_diem():
    for i in tree_home.get_children(): tree_home.delete(i)
    conn = connect_db(); cur = conn.cursor()
    cur.execute("""
        SELECT d.maSV, sv.hoTen, d.maMH, mh.tenMH, d.diemQT, d.diemThi,
               ROUND(d.diemQT*0.4 + d.diemThi*0.6,2) AS diemTB,
               CASE
                 WHEN (d.diemQT*0.4 + d.diemThi*0.6) >= 8 THEN 'Giỏi'
                 WHEN (d.diemQT*0.4 + d.diemThi*0.6) >= 6.5 THEN 'Khá'
                 WHEN (d.diemQT*0.4 + d.diemThi*0.6) >= 5 THEN 'TB'
                 ELSE 'Yếu'
               END AS XepLoai
        FROM diem d
        JOIN sinhvien sv ON d.maSV = sv.maSV
        JOIN monhoc mh ON d.maMH = mh.maMH
        ORDER BY d.maSV;
    """)
    for row in cur.fetchall():
        tree_home.insert("", tk.END, values=row)
    conn.close()

show_bang_diem()

# ====== HỖ TRỢ LẤY TÊN SV / MH ======
def get_student_name(maSV):
    conn = connect_db(); cur = conn.cursor()
    cur.execute("SELECT hoTen FROM sinhvien WHERE maSV=%s", (maSV,))
    r = cur.fetchone(); conn.close()
    return r[0] if r else ""

def get_subject_name(maMH):
    conn = connect_db(); cur = conn.cursor()
    cur.execute("SELECT tenMH FROM monhoc WHERE maMH=%s", (maMH,))
    r = cur.fetchone(); conn.close()
    return r[0] if r else ""

# ====== HÀM MỞ FORM THÊM / SỬA ======
def open_form(mode="add"):
    # mode: "add" or "edit"
    selected = None
    if mode == "edit":
        sel = tree_home.selection()
        if not sel:
            messagebox.showwarning("Chú ý", "Chọn 1 bản ghi để sửa.")
            return
        selected = tree_home.item(sel[0], "values")

    form = tk.Toplevel(root)
    form.title("Nhập điểm" if mode=="add" else "Sửa điểm")
    form.geometry("420x320")
    form.transient(root)
    form.grab_set()

    # biến
    maSV_var = tk.StringVar(value=selected[0] if selected else "")
    hoTen_var = tk.StringVar(value=selected[1] if selected else "")
    maMH_var = tk.StringVar(value=selected[2] if selected else "")
    tenMH_var = tk.StringVar(value=selected[3] if selected else "")
    diemQT_var = tk.StringVar(value=selected[4] if selected else "")
    diemThi_var = tk.StringVar(value=selected[5] if selected else "")
    diemTong_var = tk.StringVar(value=selected[6] if selected else "")

    def update_names_from_codes(event=None):
        hoTen_var.set(get_student_name(maSV_var.get()))
        tenMH_var.set(get_subject_name(maMH_var.get()))
        try:
            qt = float(diemQT_var.get())
            thi = float(diemThi_var.get())
            tong = round(qt*0.4 + thi*0.6, 2)
            diemTong_var.set(str(tong))
        except:
            diemTong_var.set("")

    # layout
    lbls = [("Mã SV", maSV_var), ("Họ Tên", hoTen_var),
            ("Mã MH", maMH_var), ("Tên MH", tenMH_var),
            ("Điểm QT", diemQT_var), ("Điểm Thi", diemThi_var),
            ("Điểm TB", diemTong_var)]
    for i, (t, var) in enumerate(lbls):
        tk.Label(form, text=t+":", anchor="w").place(x=12, y=12+38*i, width=80)
        ent = tk.Entry(form, textvariable=var)
        ent.place(x=100, y=12+38*i, width=300)
        # bind updates
        if t == "Mã SV":
            ent.bind("<FocusOut>", update_names_from_codes)
        if t == "Mã MH":
            ent.bind("<FocusOut>", update_names_from_codes)
        if t in ("Điểm QT", "Điểm Thi"):
            ent.bind("<KeyRelease>", update_names_from_codes)

    # Save function inside form
    def save_from_form():
        maSV = maSV_var.get().strip()
        maMH = maMH_var.get().strip()
        try:
            diemQT = float(diemQT_var.get())
            diemThi = float(diemThi_var.get())
        except:
            messagebox.showerror("Lỗi", "Điểm phải là số.")
            return
        if not maSV or not maMH:
            messagebox.showwarning("Thiếu", "Mã SV và Mã MH không được để trống.")
            return
        if not (0 <= diemQT <= 10 and 0 <= diemThi <= 10):
            messagebox.showwarning("Sai giá trị", "Điểm nằm trong 0 - 10.")
            return
        diemTong = round(diemQT*0.4 + diemThi*0.6, 2)
        try:
            conn = connect_db(); cur = conn.cursor()
            # try insert/update (ON DUPLICATE KEY UPDATE) - cần PK (maSV,maMH)
            cur.execute("""
                INSERT INTO diem (maSV, maMH, diemQT, diemThi)
                VALUES (%s,%s,%s,%s)
                ON DUPLICATE KEY UPDATE diemQT=%s, diemThi=%s
            """, (maSV, maMH, diemQT, diemThi, diemQT, diemThi))

            conn.commit(); conn.close()
            show_bang_diem()
            form.destroy()
            messagebox.showinfo("Thành công", "Lưu dữ liệu thành công.")
        except Exception as e:
            # fallback: nếu DB không hỗ trợ ON DUPLICATE KEY, thử UPDATE/INSERT
            try:
                conn = connect_db(); cur = conn.cursor()
                cur.execute("SELECT * FROM diem WHERE maSV=%s AND maMH=%s", (maSV, maMH))
                if cur.fetchone():
                  cur.execute("""
                        INSERT INTO diem (maSV, maMH, diemQT, diemThi)
                        VALUES (%s,%s,%s,%s)
                        ON DUPLICATE KEY UPDATE diemQT=%s, diemThi=%s
                        """, (maSV, maMH, diemQT, diemThi, diemQT, diemThi))

                else:
                    cur.execute("""
                        INSERT INTO diem (maSV, maMH, diemQT, diemThi)
                        VALUES (%s,%s,%s,%s)
                        ON DUPLICATE KEY UPDATE diemQT=%s, diemThi=%s
                        """, (maSV, maMH, diemQT, diemThi, diemQT, diemThi))

                conn.commit(); conn.close()
                show_bang_diem()
                form.destroy()
                messagebox.showinfo("Thành công", "Lưu dữ liệu thành công.")
            except Exception as e2:
                messagebox.showerror("Lỗi", f"Lưu không thành công:\n{e2}")

    # Buttons
    tk.Button(form, text="Lưu", width=10, bg="#3498db", fg="white", command=save_from_form).place(x=110, y=275)
    tk.Button(form, text="Hủy", width=10, command=form.destroy).place(x=230, y=275)

# ====== NÚT CHỨC NĂNG ======
button_frame = tk.Frame(frame_home, bg="#dddddd", pady=10)
button_frame.pack(fill="x", padx=12, pady=(0,12))

def them_click():
    open_form("add")

def luu_click():
    # mở form lưu (tương tự Thêm) để nhập xong bấm Lưu
    open_form("add")

def sua_click():
    open_form("edit")

def xoa_click():
    sel = tree_home.selection()
    if not sel:
        messagebox.showwarning("Chú ý", "Vui lòng chọn bản ghi để xóa.")
        return
    vals = tree_home.item(sel[0], "values")
    maSV = vals[0]; maMH = vals[2]
    if messagebox.askyesno("Xác nhận", f"Xóa điểm của SV {maSV} - Môn {maMH}?"):
        try:
            conn = connect_db(); cur = conn.cursor()
            cur.execute("DELETE FROM diem WHERE maSV=%s AND maMH=%s", (maSV, maMH))
            conn.commit(); conn.close()
            show_bang_diem()
            messagebox.showinfo("Đã xóa", "Xóa thành công.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Xóa thất bại: {e}")

def huy_click():
    search_var.set("")
    show_bang_diem()

def thoat_click():
    root.destroy()

# buttons
tk.Button(button_frame, text="➕ Thêm", command=them_click, width=12, bg="#1abc9c", fg="white", font=("Arial",11,"bold")).pack(side="left", padx=8)
tk.Button(button_frame, text="💾 Lưu", command=luu_click, width=12, bg="#3498db", fg="white", font=("Arial",11,"bold")).pack(side="left", padx=8)
tk.Button(button_frame, text="✏️ Sửa", command=sua_click, width=12, bg="#f1c40f", fg="black", font=("Arial",11,"bold")).pack(side="left", padx=8)
tk.Button(button_frame, text="🗑️ Xóa", command=xoa_click, width=12, bg="#e74c3c", fg="white", font=("Arial",11,"bold")).pack(side="left", padx=8)
tk.Button(button_frame, text="↩️ Hủy", command=huy_click, width=12, bg="#95a5a6", fg="black", font=("Arial",11,"bold")).pack(side="left", padx=8)
tk.Button(button_frame, text="🚪 Thoát", command=thoat_click, width=12, bg="#7f8c8d", fg="white", font=("Arial",11,"bold")).pack(side="right", padx=8)


# ================== CÁC FRAME KHÁC ==================
frame_sv = frames["sinhvien"]
tk.Label(frame_sv, text="👨‍🎓 Quản lý Sinh viên", font=("Arial", 18, "bold")).pack(pady=10)
tree_sv = ttk.Treeview(frame_sv, show="headings")
tree_sv.pack(fill="both", expand=True, padx=10, pady=10)
tk.Button(frame_sv, text="🔄 Tải danh sách", command=lambda: load_data("sinhvien", tree_sv)).pack(pady=10)
load_data("sinhvien", tree_sv)

# ====== MENU ======
menu_bar.add_command(label="🏠 Trang chủ", command=lambda: show_frame(frames["trang_chu"]))
menu_bar.add_command(label="👨‍🎓 Sinh viên", command=lambda: show_frame(frames["sinhvien"]))
menu_bar.add_command(label="📚 Môn học", command=lambda: show_frame(frames["monhoc"]))
menu_bar.add_command(label="🧮 Điểm", command=lambda: show_frame(frames["diem"]))
menu_bar.add_command(label="🏫 Lớp", command=lambda: show_frame(frames["lop"]))
menu_bar.add_command(label="🏢 Khoa", command=lambda: show_frame(frames["khoa"]))
menu_bar.add_command(label="👩‍🏫 Giảng viên", command=lambda: show_frame(frames["giangvien"]))

# ====== KHỞI ĐỘNG ======
show_frame(frames["trang_chu"])
root.mainloop()
