import Tkinter as Tk
import ttk
import tkMessageBox
import ValidatorManager


class MainWindow:
    # Tkinter Window class #

    def __init__(self, master):

        # Mainwindow #
        self.master = master
        self.frame = Tk.Frame(self.master, borderwidth=0)

        # Table of models #
        self.model_table = ttk.Treeview(self.master, height=9)
        self.model_table.grid(row=0, column=0, sticky="ne", padx=[5, 0], pady=5, rowspan=2, columnspan=3)
        self.model_table.heading('#0', text="PDBid")
        self.model_table.bind("<<TreeviewSelect>>", self.on_select_model_table)
        self.model_table.bind("<Delete>", lambda event, table=self.model_table: self.delete_option(table))
        self.model_table.column('#0', width=80, stretch=Tk.NO, minwidth=80)

        # Table of entries #
        self.entries_table_columns = ["Entry", "Missing Atoms", "Substitutions", "Chirality Mismatches",
                                                   "Name Mismatches", "Foreign Atoms"]
        self.entries_table = ttk.Treeview(self.master, height=9,
                                          columns=self.entries_table_columns)
        self.entries_table.grid(row=0, column=3, sticky="NW", padx=[3, 0], pady=[5, 0], columnspan=10)
        self.entries_table['show'] = 'headings'

        self.entries_table.heading('#1', text=self.entries_table_columns[0])
        self.entries_table.heading('#2', text=self.entries_table_columns[1])
        self.entries_table.heading('#3', text=self.entries_table_columns[2])
        self.entries_table.heading('#4', text=self.entries_table_columns[3])
        self.entries_table.heading('#5', text=self.entries_table_columns[4])
        self.entries_table.heading('#6', text=self.entries_table_columns[5])
        self.entries_table.column('#1', width=45, anchor=Tk.W)
        self.entries_table.column('#2', width=88, anchor="center")
        self.entries_table.column('#3', width=78, anchor="center")
        self.entries_table.column('#4', width=120, anchor="center")
        self.entries_table.column('#5', width=110, anchor="center")
        self.entries_table.column('#6', width=90, anchor="center")
        self.entries_table.bind("<<TreeviewSelect>>", self.on_select_entries_table)
        self.entries_table.bind("<Delete>", lambda event, table=self.entries_table: self.delete_option(table))

        # Enntries table scrollbar #
        self.entries_scrollbar = ttk.Scrollbar(self.master, orient=Tk.VERTICAL, command=self.entries_table.yview)
        self.entries_table['yscroll'] = self.entries_scrollbar.set
        self.entries_scrollbar.grid(row=0, column=14, sticky=Tk.NSEW, padx=[2, 5], pady=0)
        self.entries_table.bind("<<TreeviewSelect>>", self.on_select_entries_table)

        # Notebook, used for tabs #
        self.notebook = ttk.Notebook(self.master, width=350, height=180)
        self.notebook.grid(row=1, column=0, sticky="NW", columnspan=6, pady=[5, 5], padx=5)

        # Tabs, each tab has one table #
        self.tab_names = ['Entries', 'Missing', 'Substitutions', 'Name Mismatches', 'Chirality Mismatches',
                          'Foreign Atoms']

        self.missing_table = self.tab_maker(self.tab_names[1], ["Atoms"])

        self.substitution_table = self.tab_maker(self.tab_names[2], ["Model", "Motif"])

        self.name_mismatches_table = self.tab_maker(self.tab_names[3], ["Model", "Motif"])

        self.chirality_mismatches_table = self.tab_maker(self.tab_names[4], ["Model", "Motif"])

        self.foreign_atoms_table = self.tab_maker(self.tab_names[5], ["Model", "Motif"])

        # Entry label #
        self.entry_label = Tk.Label(self.master, text="PDBid", anchor=Tk.W)
        self.entry_label.grid(row=2, column=0, sticky=Tk.NW, padx=(5, 0))

        # String length control #
        self.input_text = Tk.StringVar()
        self.input_text.trace("w", lambda name, index, mode, sv=self.input_text: self.str_length(self.input_text))

        # Entry widget #
        self.entry = Tk.Entry(self.master, width=23, textvariable=self.input_text)
        self.entry.grid(row=2, column=1, sticky=Tk.NE, padx=(0, 5), columnspan=3)
        self.entry.bind("<Return>", lambda event, pdb_id=self.entry.get(): self.start_validation())

        # Start button #
        self.start_button = Tk.Button(self.master, text="Validate!", command=lambda: self.start_validation())
        self.start_button.grid(row=2, column=4, sticky=Tk.NW, padx=0, columnspan=2)

        # self.info_button = tk.Button(self.master, text="Help", command=self.help)
        # self.info_button.grid(row=2, column=5, sticky=tk.NE)

        # Status bar frame #
        self.status_bar_frame = Tk.Frame(self.master)
        self.status_bar_frame.configure(width=640, height=20)
        self.status_bar_frame.grid(column=0, columnspan=11)

        self.status_bar_label = Tk.Label(self.status_bar_frame)
        self.status_bar_label.grid(sticky="w", column=0, row=0)

    def str_length(self, input_text):
        """
        Control length of given string.
        :param input_text: text written into entry box
        :return: True, if it has right length
        """
        string = self.input_text.get()[0:4]
        self.input_text.set(string)
        return True

    def add_option(self, pdb_id):
        """
        Method, makes a PDBid option in model_table + makes it's children (Models)
        :param pdb_id: given PDBid
        :return:
        """
        try:
            self.model_table.insert("", 1, pdb_id.lower(), text=pdb_id.lower())
            for i in self.downloaded_object.protein_model_list:
                self.model_table.insert(pdb_id, 1, text=i["ModelName"])

        except Tk.TclError:
            tkMessageBox.showerror("Error", "PDB already downloaded. Please use another molecule.")
            return

    def help(self):
        """
        Run help window.
        :return:
        """
        tkMessageBox.showinfo("Help",
                              "Validator\nType PDBid, which you want to validate and the program will give you information about all models  in given PDB")

    def tab_maker(self, tab, column_names):
        """
        Method, makes tabs with given name
        :param tab: name of tab
        :param column_names: name of columns for table
        :return:
        """
        self.tab = Tk.Frame(self.master)

        self.tree = ttk.Treeview(self.tab, columns=column_names, height=18)

        self.tree['show'] = 'headings'
        for i in range(len(column_names)):
            self.tree.heading(i, text=column_names[i])
            self.tree.column(i, stretch=Tk.NO, width=435 / (len(column_names)))

        self.tree.column('#0', width=435 / (len(column_names)))

        self.tree.grid(row=0, columnspan=4, sticky="nsew", padx=2, pady=2)
        self.treeview = self.tree

        self.notebook.add(self.tab, text=tab)
        return self.treeview

    def on_select_model_table(self, event):
        """
        Method, called when is clicked on left table. Fills Entries table.
        :param event:
        :return:
        """

        clicked_item = self.model_table.focus()

        if self.model_table.parent(clicked_item) == '':
            return

        counter = 0

        pdb_id = self.model_table.parent(clicked_item)
        model_name = self.model_table.item(clicked_item, "text")

        self.entries_table.delete(*self.entries_table.get_children())

        while model_name not in ValidatorManager.validation_report[pdb_id]["Models"][counter]["ModelName"]:
            counter += 1

        if model_name in ValidatorManager.validation_report[pdb_id]["Models"][counter]["ModelName"]:
            current_model = ValidatorManager.validation_report[pdb_id]["Models"][counter]["Entries"]

            for entry, properties in enumerate(current_model):
                if current_model[entry]["MissingAtomCount"] != 0:
                    self.entries_table.insert('', 1, text=current_model[entry]["MainResidue"],
                                              values=(self.entries_table_fill(current_model, entry)),
                                              tags=('missing'))
                    self.entries_table.tag_configure('missing', background='red')


                elif current_model[entry]["SubstitutionCount"] != 0:
                    self.entries_table.insert('', 1, text=current_model[entry]["MainResidue"],
                                              values=(self.entries_table_fill(current_model, entry)),
                                              tags=('substitution'))
                    self.entries_table.tag_configure('substitution', background='#BDA429')


                elif current_model[entry]["MissingAtomCount"] == 0 and current_model[entry]["SubstitutionCount"] == 0 \
                        and current_model[entry]["ChiralityMismatchCount"] == 0 \
                        and current_model[entry]["NameMismatchCount"] == 0 \
                        and current_model[entry]["ForeignAtomCount"] == 0:

                    self.entries_table.insert('', 1, text=current_model[entry]["MainResidue"],
                                              values=(self.entries_table_fill(current_model, entry)),
                                              tags=('ok'))
                    self.entries_table.tag_configure('ok', foreground='green')


                else:
                    self.entries_table.insert('', 1, text=current_model[entry]["MainResidue"],
                                              values=(self.entries_table_fill(current_model, entry)))

    def entries_table_fill(self, current_model, entry):
        entry_name, res_id, chain = current_model[entry]["MainResidue"].split(" ")
        return (res_id, chain), current_model[entry]["MissingAtomCount"], current_model[entry]["SubstitutionCount"], \
               current_model[entry]["ChiralityMismatchCount"], current_model[entry]["NameMismatchCount"], \
               current_model[entry]["ForeignAtomCount"]

    def on_select_entries_table(self, event):
        """
        Method, is called when is clicked on entries table, fill properties tables.
        :param event:
        :return:
        """

        res_name = self.entries_table.item(self.entries_table.focus(), 'text')
        entry_count = 0
        pdb_id = self.model_table.parent(self.model_table.focus())
        model_name_id = self.model_table.focus()
        model_name = self.model_table.item(model_name_id, 'text')

        counter = 0

        self.missing_table.delete(*self.missing_table.get_children())

        while model_name not in ValidatorManager.validation_report[pdb_id]["Models"][counter]["ModelName"]:
            counter += 1

        while res_name not in ValidatorManager.validation_report[pdb_id]["Models"][counter]["Entries"][entry_count][
            "MainResidue"]:
            entry_count += 1

        # if model_name in ValidatorManager.validation_report[pdb_id]["Models"][counter]["ModelName"]:
        current_entry = ValidatorManager.validation_report[pdb_id]["Models"][counter]["Entries"][entry_count]

        for atom_index in current_entry["MissingAtoms"]:
            self.missing_table.insert('', 1, values=(
                ValidatorManager.validation_report[pdb_id]["Models"][counter]["ModelNames"][str(atom_index)]))

        self.table_fill(self.chirality_mismatches_table, "ChiralityMismatches")
        self.table_fill(self.substitution_table, "Substitutions")
        self.table_fill(self.foreign_atoms_table, "ForeignAtoms")
        self.table_fill(self.name_mismatches_table, "NameMismatches")

    def delete_option(self, table):
        """
        Delete option from tables
        :param table: table, form which will be option deleted
        :return:
        """
        selected_item = table.selection()
        table.delete(selected_item)

    def table_fill(self, table, property):
        """
        Fill given table with given properties
        :param table: Table, wchich will be filled
        :param property:
        :return:
        """
        counter = 0
        res_name = self.entries_table.item(self.entries_table.focus(), 'text')
        entry_count = 0
        pdb_id = self.model_table.parent(self.model_table.focus())
        model_name_id = self.model_table.focus()
        model_name = self.model_table.item(model_name_id, 'text')
        table.delete(*table.get_children())

        while model_name not in ValidatorManager.validation_report[pdb_id]["Models"][counter]["ModelName"]:
            counter += 1

        while res_name not in ValidatorManager.validation_report[pdb_id]["Models"][counter]["Entries"][entry_count][
            "MainResidue"]:
            entry_count += 1

        # if model_name in ValidatorManager.validation_report[pdb_id]["Models"][counter]["ModelName"]:

        current_entry = ValidatorManager.validation_report[pdb_id]["Models"][counter]["Entries"][entry_count]
        for atom_index, motiff in enumerate(current_entry[property]):
            table.insert('', 1, values=(ValidatorManager.validation_report[pdb_id]["Models"][counter]["ModelNames"]
                                        [str(motiff)], current_entry[property][str(motiff)]))

    def start_validation(self):
        """
        Method, calls validation from ValidatorManager class
        :return:
        """

        self.downloaded_object = ValidatorManager.ValidatorManager()

        if self.downloaded_object.error_check(self.entry.get()):
            tkMessageBox.showerror("Error", self.downloaded_object.error)
            return
        else:
            self.downloaded_object.scan_json(self.entry.get())
            self.add_option(self.entry.get())

        self.entry.delete('0', 'end')


def main():
    root = Tk.Tk()
    root.wm_title("Validator")
    root.resizable(width=False, height=False)
    root.geometry("640x480")
    app = MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()
