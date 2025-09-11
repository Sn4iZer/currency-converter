import customtkinter as ctk
import unicodedata

class CurrencyPicker(ctk.CTkToplevel):
    def __init__(self, parent, currency_list, callback):
        super().__init__(parent)
        self.currency_list = sorted(currency_list)
        self.callback = callback
        self.geometry("300x400")
        self.resizable(False, False)
        self.title("Select currency")
        self.grab_set()          # modal

        # search box
        self.search = ctk.CTkEntry(self, placeholder_text="Type to filter…")
        self.search.pack(fill="x", padx=10, pady=10)
        self.search.bind("<KeyRelease>", self._filter)

        # scrollable frame
        self.container = ctk.CTkScrollableFrame(self)
        self.container.pack(fill="both", expand=True, padx=10, pady=10)

        # build labels once
        self.labels = []
        for code in self.currency_list:
            lbl = ctk.CTkLabel(self.container, text=code, anchor="w",
                               cursor="hand2", font=ctk.CTkFont(size=14))
            lbl.bind("<Button-1>", lambda e, c=code: self._select(c))
            lbl.pack(fill="x", pady=2)
            self.labels.append((code, lbl))

        # pre-select first
        self.after(100, lambda: self.search.focus())

    # ---------- helpers ----------
    def _filter(self, _=None):
        txt = self.search.get().strip().upper()
        for code, lbl in self.labels:
            lbl.pack(fill="x", pady=2) if txt in code else lbl.pack_forget()

    def _select(self, code):
        self.callback(code)
        self.destroy()