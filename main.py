import customtkinter as ctk
from tkinter import messagebox
from converter.logic import exchange, currencies
import threading, queue, time
from converter.logic import _singleton   # the client instance
from datetime import datetime, timedelta
from converter import api
from currency_picker import CurrencyPicker

ctk.set_appearance_mode("System")   # Dark/Light
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Currency Converter")
        self.geometry("380x360")
        self.resizable(False, False)

        # data
        self.currencies = currencies()

        # widgets
        self.create_widgets()
        self.bind("<Return>", lambda e: self.convert())

        ts = api.last_fetch_time()
        self.status.configure(text=f"Last updated {ts:%Y-%m-%d %H:%M}")

        self.refresh_q = queue.Queue()
        self.after(200, self._poll_refresh)   # tkinter after loop
        threading.Thread(target=self._background_refresh, daemon=True).start()

    # --------------------------------------------------
    def create_widgets(self):
        self.grid_columnconfigure(1, weight=1)

        pad = {"padx": 15, "pady": 12}

        # title
        ctk.CTkLabel(self, text="💱 Currency Converter", font=ctk.CTkFont(size=22, weight="bold"))\
            .grid(row=0, column=0, columnspan=3, **pad)

        # amount
        self.amount_var = ctk.StringVar(value="1.0")
        self.amount_var.trace_add("write", self._validate_amount)
        ctk.CTkLabel(self, text="Amount").grid(row=1, column=0, sticky="w", **pad)
        self.amount_entry = ctk.CTkEntry(self, textvariable=self.amount_var)
        self.amount_entry.grid(row=1, column=1, columnspan=2, sticky="ew", **pad)

        # from
        self.from_var = ctk.StringVar(value="USD")
        ctk.CTkLabel(self, text="From").grid(row=2, column=0, sticky="w", **pad)
        self.from_btn = ctk.CTkButton(self, textvariable=self.from_var,
                              command=lambda: self._pick_currency(self.from_var))
        self.from_btn.grid(row=2, column=1, sticky="ew", **pad)

        # swap button
        self.swap_btn = ctk.CTkButton(self, text="⇄", width=40, command=self._swap)
        self.swap_btn.grid(row=2, column=2, **pad)

        # to
        self.to_var = ctk.StringVar(value="EUR")
        ctk.CTkLabel(self, text="To").grid(row=3, column=0, sticky="w", **pad)
        self.to_btn = ctk.CTkButton(self, textvariable=self.to_var,
                            command=lambda: self._pick_currency(self.to_var))
        self.to_btn.grid(row=3, column=1, sticky="ew", **pad)

        # result
        self.result_lbl = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=20, weight="bold"))
        self.result_lbl.grid(row=4, column=0, columnspan=3, **pad)

        # status bar
        self.status = ctk.CTkLabel(self, text="Ready", anchor="w", font=ctk.CTkFont(size=12))
        self.status.grid(row=5, column=0, columnspan=3, sticky="ew", padx=10, pady=(0,5))

        # appearance switch
        self.appearance_menu = ctk.CTkOptionMenu(self, values=["System","Dark","Light"],
                                                command=ctk.set_appearance_mode)
        self.appearance_menu.grid(row=6, column=2, padx=10, pady=10, sticky="e")

    # --------------------------------------------------
    def _pick_currency(self, stringvar):
        CurrencyPicker(self, self.currencies, lambda code: (stringvar.set(code), self.convert()))

    
    def convert(self):
        try:
            amt = float(self.amount_var.get())
            if amt <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Input error", "Please enter a positive number")
            return

        frm = self.from_var.get()
        to  = self.to_var.get()
        if frm == to:
            messagebox.showinfo("Info", "Source and target currencies are identical")
            return

        try:
            result = exchange(frm, to, amt)
        except Exception as e:
            messagebox.showerror("API error", str(e))
            return

        self.result_lbl.configure(text=f"{amt}  {frm}  =  {result}  {to}")
    # ----------------------------------
    def _validate_amount(self, *_, **__):
        try:
            float(self.amount_var.get())
            self.amount_entry.configure(border_color=["gray60","gray40"])
        except ValueError:
            self.amount_entry.configure(border_color="red")

    def _swap(self):
        f, t = self.from_var.get(), self.to_var.get()
        self.from_var.set(t)
        self.to_var.set(f)
        self.convert()

    def _background_refresh(self):
        while True:
            time.sleep(30*60)          # 30 minutes
            try:
                _singleton.get_rates.__wrapped__()  # force refresh
                self.refresh_q.put("updated")
            except Exception as e:
                self.refresh_q.put(f"error: {e}")

    def _poll_refresh(self):
        try:
            msg = self.refresh_q.get_nowait()
            if msg == "updated":
                self.status.configure(text=f"Rates refreshed · {datetime.now():%H:%M}")
                self.convert()          # update result with new rates
            elif msg.startswith("error"):
                self.status.configure(text=msg)
        except queue.Empty:
            pass
        self.after(200, self._poll_refresh)

# ------------------------------------------------------
if __name__ == "__main__":
    App().mainloop()