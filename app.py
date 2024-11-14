import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

# Koneksi ke database MySQL
def connect_to_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="db_buku",
            port=3300
        )
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Koneksi gagal: {err}")
        return None

# Fungsi untuk menambah data buku
def add_book():
    judul = entry_judul.get()
    penulis = entry_penulis.get()
    tahun = entry_tahun.get()

    if judul and penulis and tahun:
        try:
            db = connect_to_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO buku (judul, penulis, tahun) VALUES (%s, %s, %s)", (judul, penulis, tahun))
            db.commit()
            db.close()
            messagebox.showinfo("Sukses", "Data buku berhasil ditambahkan")
            display_books()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Input Error", "Semua kolom harus diisi")

# Fungsi untuk menampilkan data buku
def display_books():
    for row in tree.get_children():
        tree.delete(row)
    
    db = connect_to_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM buku")
    books = cursor.fetchall()
    db.close()

    for book in books:
        tree.insert("", "end", values=book)

# Fungsi untuk menghapus data buku
def delete_book():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Pilih Buku", "Pilih buku yang akan dihapus")
        return
    
    book_id = tree.item(selected_item[0])["values"][0]
    try:
        db = connect_to_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM buku WHERE id=%s", (book_id,))
        db.commit()
        db.close()
        messagebox.showinfo("Sukses", "Data buku berhasil dihapus")
        display_books()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Fungsi untuk mengedit data buku
def edit_book():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Pilih Buku", "Pilih buku yang akan diedit")
        return

    book_id = tree.item(selected_item[0])["values"][0]
    new_judul = entry_judul.get()
    new_penulis = entry_penulis.get()
    new_tahun = entry_tahun.get()

    if new_judul and new_penulis and new_tahun:
        try:
            db = connect_to_db()
            cursor = db.cursor()
            cursor.execute("UPDATE buku SET judul=%s, penulis=%s, tahun=%s WHERE id=%s", (new_judul, new_penulis, new_tahun, book_id))
            db.commit()
            db.close()
            messagebox.showinfo("Sukses", "Data buku berhasil diedit")
            display_books()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Input Error", "Semua kolom harus diisi")

# GUI Tkinter
root = tk.Tk()
root.title("CRUD Buku")

# Input Fields
tk.Label(root, text="Judul").grid(row=0, column=0)
entry_judul = tk.Entry(root)
entry_judul.grid(row=0, column=1)

tk.Label(root, text="Penulis").grid(row=1, column=0)
entry_penulis = tk.Entry(root)
entry_penulis.grid(row=1, column=1)

tk.Label(root, text="Tahun").grid(row=2, column=0)
entry_tahun = tk.Entry(root)
entry_tahun.grid(row=2, column=1)

# Buttons
btn_add = tk.Button(root, text="Tambah Buku", command=add_book)
btn_add.grid(row=3, column=0)

btn_edit = tk.Button(root, text="Edit Buku", command=edit_book)
btn_edit.grid(row=3, column=1)

btn_delete = tk.Button(root, text="Hapus Buku", command=delete_book)
btn_delete.grid(row=3, column=2)

# Treeview for displaying books
tree = tk.ttk.Treeview(root, columns=("ID", "Judul", "Penulis", "Tahun"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Judul", text="Judul")
tree.heading("Penulis", text="Penulis")
tree.heading("Tahun", text="Tahun")
tree.grid(row=4, column=0, columnspan=3)

display_books()  # Load initial data

root.mainloop()
