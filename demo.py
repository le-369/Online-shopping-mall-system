import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import pymysql
import tkinter.font as tkFont
from ttkbootstrap import Style

style = Style()
style = Style(theme='litera')

class DatabaseManager:
    def __init__(self, host="localhost", user="root", password="123456", database="shopping"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        return pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, charset="utf8")

    def execute_query(self, query, params=None):
        try:
            conn = self.connect()
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchall()
                conn.commit()
            return result
        except pymysql.Error as e:
            messagebox.showerror("Database Error", f"Database error: {e}")
            return None
        finally:
            conn.close()

    def insert_user(self, name, password):
        query = "INSERT INTO user (name, password) VALUES (%s, %s)"
        self.execute_query(query, (name, password))

    def get_user(self, name):
        query = "SELECT name, password FROM user WHERE name = %s"
        return self.execute_query(query, (name,))

    def get_all_users(self):
        query = "SELECT name, password FROM user"
        return self.execute_query(query)

    def get_all_products(self):
        query = "SELECT cid, cname, cprice, cbrand FROM product"
        return self.execute_query(query)

    def get_all_orders(self):
        query = "SELECT oid, id, type, cid, price, calls, btime FROM orders"
        return self.execute_query(query)

    def update_order(self, oid, new_id, new_type, new_cid, new_price, new_calls, new_btime):
        query = """
        UPDATE orders
        SET id = %s, type = %s, cid = %s, price = %s, calls = %s, btime = %s
        WHERE oid = %s
        """
        self.execute_query(query, (new_id, new_type, new_cid, new_price, new_calls, new_btime, oid))

class GUI:
    def __init__(self, root):
        self.root = root
        self.root = style.master
        self.root.title('网上商城系统')
        self.root.geometry('1100x700')
        self.root.iconbitmap('logo.ico')

        # Background image
        self.canvas = tk.Canvas(self.root, height=700, width=1100)
        self.login_background = ImageTk.PhotoImage(Image.open('welcome.jpg').resize((1100, 700)))
        self.login_image = self.canvas.create_image(0, 0, anchor='nw', image=self.login_background)
        self.canvas.pack(side='top')

        # Fonts
        self.font_style = tkFont.Font(size=14)
        self.font_style2 = tkFont.Font(size=12)
        self.font_style_m = ('Helvetica', 16, 'bold')

        # Username and Password Labels
        tk.Label(self.root, text='用户名:', bg='white', font=self.font_style_m, width=8, height=1).place(x=380, y=250)
        tk.Label(self.root, text='密   码:', bg='white', font=self.font_style_m, width=8, height=1).place(x=380, y=300)

        # Username Entry
        self.var_user_name = tk.StringVar()
        self.entry_user_name = tk.Entry(self.root, textvariable=self.var_user_name, width=25, font=self.font_style_m)
        self.entry_user_name.place(x=500, y=250)

        # Password Entry
        self.var_user_pwd = tk.StringVar()
        self.entry_user_pwd = tk.Entry(self.root, textvariable=self.var_user_pwd, show='*', width=25, font=self.font_style_m)
        self.entry_user_pwd.place(x=500, y=300)

        # Register and Login Buttons
        tk.Button(self.root, bg='white', text='注册', command=self.user_register, width=8, height=1, font=self.font_style_m).place(x=500, y=340)
        tk.Button(self.root, bg='white', text='登录', command=self.user_login, width=8, height=1, font=self.font_style_m).place(x=680, y=340)

        # Database Manager
        self.db_manager = DatabaseManager()

    def user_login(self):
        user_name = self.var_user_name.get()
        user_password = self.var_user_pwd.get()

        if not (user_name and user_password):
            messagebox.showwarning(title='警告', message='用户名或密码不能为空')
            return

        result = self.db_manager.get_user(user_name)

        if result is None:
            messagebox.showerror(title='错误', message='数据库查询失败')
            return

        if not result:
            is_signup = messagebox.askyesno(title='提示', message='该账号不存在，是否现在注册？')
            if is_signup:
                self.user_register()
        else:
            if user_password == result[0][1]:
                messagebox.showinfo(title='欢迎您', message='登录成功！\n当前登录账号为：' + user_name)
                self.operation()
            else:
                messagebox.showerror(title='错误', message='密码输入错误')

    def user_register(self):
        def register_confirm():
            name = new_name.get()
            password = new_password.get()
            password_confirm = new_password_confirm.get()

            if not (name and password):
                messagebox.showwarning(title='警告', message='注册账号或密码不能为空')
            elif password != password_confirm:
                messagebox.showwarning(title='警告', message='两次密码输入不一致，请重新输入')
            else:
                if self.db_manager.get_user(name):
                    messagebox.showwarning(title='警告', message='该注册账号已存在')
                else:
                    self.db_manager.insert_user(name, password)
                    messagebox.showinfo(title='恭喜您', message='注册成功！\n注册账号为：' + name)
                    window_sign_up.destroy()

        window_sign_up = tk.Toplevel(self.root)
        window_sign_up.geometry('350x200')
        window_sign_up.title('欢迎注册')

        new_name = tk.StringVar()
        tk.Label(window_sign_up, bg='green', text='注册账号：').place(x=50, y=10)
        tk.Entry(window_sign_up, textvariable=new_name).place(x=150, y=10)

        new_password = tk.StringVar()
        tk.Label(window_sign_up, bg='green', text='密      码：').place(x=50, y=50)
        tk.Entry(window_sign_up, textvariable=new_password, show='*').place(x=150, y=50)

        new_password_confirm = tk.StringVar()
        tk.Label(window_sign_up, bg='green', text='确认密码：').place(x=50, y=90)
        tk.Entry(window_sign_up, textvariable=new_password_confirm, show='*').place(x=150, y=90)

        bt_confirm_sign_up = tk.Button(window_sign_up, bg='green', text='确认注册', command=register_confirm)
        bt_confirm_sign_up.place(x=150, y=130)

    def operation(self):
        op_window = tk.Toplevel(self.root)
        op_window.title('网上商城系统')
        op_window.geometry('900x600')
        op_window.iconbitmap('logo.ico')
        self.root.withdraw()

        notebook = ttk.Notebook(op_window)
        notebook.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        frame_goods_select = ttk.Frame(notebook)
        frame_goods_add_delete = ttk.Frame(notebook)
        frame_order_select = ttk.Frame(notebook)
        frame_order_revise = ttk.Frame(notebook)

        notebook.add(frame_goods_select, text="商品查询")
        notebook.add(frame_goods_add_delete, text="商品增删")
        notebook.add(frame_order_select, text="订单查询")
        notebook.add(frame_order_revise, text="订单修改")

        self.function1(frame_goods_select)
        self.function2(frame_goods_add_delete)
        self.function3(frame_order_select)
        self.function4(frame_order_revise)

        # 添加窗口关闭事件处理
        op_window.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self):
        if messagebox.askyesno("关闭系统", "你确定要关闭系统吗？"):
            
            self.root.destroy()

    def load_product_data(self, tree):
        for item in tree.get_children():
            tree.delete(item)

        rows = self.db_manager.get_all_products()
        for i, row in enumerate(rows):
            if i % 2 == 0:
                tree.insert("", tk.END, values=row, tags=('evenrow',))
            else:
                tree.insert("", tk.END, values=row, tags=('oddrow',))

    def function1(self, frame_goods_select):
        tree = ttk.Treeview(frame_goods_select, columns=("cid", "cname", "cprice", "cbrand"), show="headings")
        tree.heading("cid", text="商品编码")
        tree.heading("cname", text="商品名称")
        tree.heading("cprice", text="商品价格")
        tree.heading("cbrand", text="商品品牌")
        tree.pack(fill=tk.BOTH, expand=True)

        tree.column("cid", width=225, anchor='center')
        tree.column("cname", width=225, anchor='center')
        tree.column("cprice", width=225, anchor='center')
        tree.column("cbrand", width=225, anchor='center')

         # 定义两种不同的标签
        tree.tag_configure('evenrow', background='#BA9BC9')  # 偶数行颜色
        tree.tag_configure('oddrow', background='#e6e6fa')   # 奇数行颜色

        self.load_product_data(tree)
        # 添加更新按钮
        update_button = tk.Button(frame_goods_select, text="更新商品", command=lambda: self.load_product_data(tree))
        update_button.pack(side=tk.BOTTOM, pady=10)


        rows = self.db_manager.get_all_products()
        for i, row in enumerate(rows):
            if i % 2 == 0:
                tree.insert("", tk.END, values=row, tags=('evenrow',))
            else:
                tree.insert("", tk.END, values=row, tags=('oddrow',))

    def function2(self, frame_goods_add_delete):

        tk.Label(frame_goods_add_delete, text="商品编码:",font=self.font_style).pack(pady=5)
        entry_cid = tk.Entry(frame_goods_add_delete, width=25, font=self.font_style)
        entry_cid.pack(pady=5)

        tk.Label(frame_goods_add_delete,text="商品名称:",font=self.font_style).pack(pady=5)
        entry_cname = tk.Entry(frame_goods_add_delete, width=25, font=self.font_style)
        entry_cname.pack(pady=5)

        tk.Label(frame_goods_add_delete, text="商品价格:",font=self.font_style).pack(pady=5)
        entry_cprice = tk.Entry(frame_goods_add_delete, width=25, font=self.font_style)
        entry_cprice.pack(pady=5)

        tk.Label(frame_goods_add_delete,text="商品品牌:",font=self.font_style).pack(pady=5)
        entry_cbrand = tk.Entry(frame_goods_add_delete, width=25, font=self.font_style)
        entry_cbrand.pack(pady=5)

        def add_product():
            cid = entry_cid.get()
            cname = entry_cname.get()
            cprice = entry_cprice.get()
            cbrand = entry_cbrand.get()

            if not (cid and cname and cprice and cbrand):
                messagebox.showwarning(title='警告', message='所有字段均为必填项')
                return
            try:
                query = "INSERT INTO product (cid, cname, cprice, cbrand) VALUES (%s, %s, %s, %s)"
                self.db_manager.execute_query(query, (cid, cname, cprice, cbrand))
                messagebox.showinfo(title='成功', message='商品添加成功')

                entry_cid.delete(0, tk.END)
                entry_cname.delete(0, tk.END)
                entry_cprice.delete(0, tk.END)
                entry_cbrand.delete(0, tk.END)
            except pymysql.Error as e:
                messagebox.showerror(title='错误', message=f'数据库错误: {e}')

        def delete_product():
            cid = entry_cid.get()

            if not cid:
                messagebox.showwarning(title='警告', message='商品编码为必填项')
                return

            try:
                query = "DELETE FROM product WHERE cid = %s"
                result = self.db_manager.execute_query(query, (cid,))

                if result is None:
                    messagebox.showwarning(title='警告', message='未找到对应的商品')
                
                else:
                    messagebox.showinfo(title='成功', message='商品删除成功')

                    # 清空输入框
                    entry_cid.delete(0, tk.END)
                    entry_cname.delete(0, tk.END)
                    entry_cprice.delete(0, tk.END)
                    entry_cbrand.delete(0, tk.END)
            except pymysql.Error as e:
                messagebox.showerror(title='错误', message=f'数据库错误: {e}')


        add_button = tk.Button(frame_goods_add_delete, text="添加商品", font=self.font_style, command=add_product)
        add_button.pack(pady=10)

        delete_button = tk.Button(frame_goods_add_delete, text="删除商品", font=self.font_style, command=delete_product)
        delete_button.pack(pady=10)

    def load_order_data(self, tree):
        for item in tree.get_children():
            tree.delete(item)

        rows = self.db_manager.get_all_orders()
        for i, row in enumerate(rows):
            if i % 2 == 0:
                tree.insert("", tk.END, values=row, tags=('evenrow',))
            else:
                tree.insert("", tk.END, values=row, tags=('oddrow',))

    def function3(self, frame_order_select):
        tree = ttk.Treeview(frame_order_select, columns=("oid", "id", "type", "cid", "price", "calls", "btime"), show="headings")
        tree.heading("oid", text="订单编码")
        tree.heading("id", text="用户ID")
        tree.heading("type", text="商品种类")
        tree.heading("cid", text="商品编码")
        tree.heading("price", text="价格")
        tree.heading("calls", text="电话号码")
        tree.heading("btime", text="订单时间")

        tree.column("oid", width=100, anchor='center')
        tree.column("id", width=100, anchor='center')
        tree.column("type", width=100, anchor='center')
        tree.column("cid", width=100, anchor='center')
        tree.column("price", width=100, anchor='center')
        tree.column("calls", width=200, anchor='center')  
        tree.column("btime", width=200, anchor='center')

        tree.pack(fill=tk.BOTH, expand=True)
        
        # 定义两种不同的标签
        tree.tag_configure('evenrow', background='#BA9BC9')  
        tree.tag_configure('oddrow', background='#e6e6fa')

        self.load_order_data(tree)

        update_button = tk.Button(frame_order_select, text="更新订单", command=lambda: self.load_order_data(tree))
        update_button.pack(side=tk.BOTTOM, pady=10)

        return tree

    def perform_update(self):
        oid = entry_oid.get()
        new_id = entry_id.get()
        new_type = entry_type.get()
        new_cid = entry_cid.get()
        new_price = entry_price.get()
        new_calls = entry_calls.get()
        new_btime = entry_btime.get()

        if not all([oid, new_id, new_type, new_cid, new_price, new_calls, new_btime]):
            messagebox.showerror("错误", "所有字段都是必填项")
            return

        try:
            self.db_manager.update_order(oid, new_id, new_type, new_cid, new_price, new_calls, new_btime)
            messagebox.showinfo("成功", "订单更新成功")
        except pymysql.Error as e:
            messagebox.showerror("错误", f"错误: {e}")

    def function4(self, frame_order_revise):
        tk.Label(frame_order_revise, text="更新的订单编码",font=self.font_style2).pack(pady=5)
        global entry_oid
        entry_oid = tk.Entry(frame_order_revise, width=30,font=self.font_style2)
        entry_oid.pack(pady=5)

        tk.Label(frame_order_revise, text="更新用户ID",font=self.font_style2).pack(pady=5)
        global entry_id
        entry_id = tk.Entry(frame_order_revise, width=30,font=self.font_style2)
        entry_id.pack(pady=5)

        tk.Label(frame_order_revise, text="更新商品种类",font=self.font_style2).pack(pady=5)
        global entry_type
        entry_type = tk.Entry(frame_order_revise, width=30,font=self.font_style2)
        entry_type.pack(pady=5)

        tk.Label(frame_order_revise, text="更新商品编码",font=self.font_style2).pack(pady=5)
        global entry_cid
        entry_cid = tk.Entry(frame_order_revise, width=30,font=self.font_style2)
        entry_cid.pack(pady=5)

        tk.Label(frame_order_revise, text="更新价钱",font=self.font_style2).pack(pady=5)
        global entry_price
        entry_price = tk.Entry(frame_order_revise, width=30,font=self.font_style2)
        entry_price.pack(pady=5)

        tk.Label(frame_order_revise, text="更新电话号码",font=self.font_style2).pack(pady=5)
        global entry_calls
        entry_calls = tk.Entry(frame_order_revise, width=30,font=self.font_style2)
        entry_calls.pack(pady=5)

        tk.Label(frame_order_revise, text="更新订单时间",font=self.font_style2).pack(pady=5)
        global entry_btime
        entry_btime = tk.Entry(frame_order_revise, width=30,font=self.font_style2)
        entry_btime.pack(pady=5)

        update_button = tk.Button(frame_order_revise, text="更新订单",font=self.font_style2, command=self.perform_update)
        update_button.pack(pady=20)

if __name__ == "__main__":
    window = tk.Tk()
    app = GUI(window)
    window.mainloop()
