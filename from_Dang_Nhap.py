import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  
import mysql.connector

# ====== HÀM KẾT NỐI DATABASE ======
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Khanh@091025",
        database="quanly_diemsinhvien"
    )

# ====== HÀM ĐĂNG NHẬP ======
def check_login():
    username = entry_user.get().strip()
    password = entry_pass.get().strip()

    if not username or not password:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
        return

    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM giangvien WHERE hoTen=%s AND matKhau=%s", (username, password))
        result = cur.fetchone()
        conn.close()

        if result:
            messagebox.showinfo("Thành công", f"Xin chào {username}!")
            root.destroy()  # ✅ Đóng login hẳn
            import DoAn_Python_QL_DiemSinhVien
        else:
            messagebox.showerror("Thất bại", "Sai tên đăng nhập hoặc mật khẩu!")

    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

# ===== GIAO DIỆN LOGIN =====
root = tk.Tk()
root.title("Đăng nhập - Giảng viên")
root.geometry("700x500")
root.resizable(False, False)

# ===== CĂN GIỮA MÀN HÌNH =====
window_width = 700
window_height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")  

# ===== CHÈN ẢNH NỀN =====
bg_image = Image.open("anh_truong.jpg")
bg_image = bg_image.resize((window_width, window_height), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# ===== KHUNG LOGIN =====
login_frame = tk.Label(root,bg="#FBFBE2", width=450, height=300)  
login_frame.place(relx=0.5, rely=0.5, anchor="center")
# Label tiêu đề
tk.Label(login_frame, text="QUẢN LÝ ĐIỂM SINH VIÊN", font=("Arial", 14, "bold"),
         bg="#FBFBE2", fg="black").pack(pady=20)

# Frame chứa form
form_frame = tk.Label(login_frame, bg="#FBFBE2")
form_frame.pack(pady=10, padx=40, fill="x")

# ===== Tên đăng nhập =====
tk.Label(form_frame, text="Tên đăng nhập", bg="#FBFBE2", fg="black", anchor="w").pack(fill="x", pady=(0, 2))
entry_user = tk.Entry(form_frame, width=40)
entry_user.pack(fill="x", pady=(0, 10))

# ===== Mật khẩu =====
tk.Label(form_frame, text="Mật khẩu", bg="#FBFBE2", fg="black", anchor="w").pack(fill="x", pady=(0, 2))
entry_pass = tk.Entry(form_frame, width=40, show="*")
entry_pass.pack(fill="x", pady=(0, 10))

# Nút đăng nhập
btn_login = ttk.Button(login_frame, text="Đăng nhập", command=check_login)
btn_login.pack(pady=20)

root.mainloop()
