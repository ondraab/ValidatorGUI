import Tkinter as tk
import ttk
import tkMessageBox
import ValidatorManager
import pprint


class MainWindow():
    def __init__(self, master):


        self.master = master
        self.frame = tk.Frame(self.master, borderwidth=0)

        self.model_table = ttk.Treeview(self.master, height=9)
        self.model_table.grid(row=0, column=0, sticky="ne", padx=[5,0], pady=5, rowspan = 2, columnspan = 3)
        self.model_table.heading('#0', text="PDBid")


        self.model_table.bind("<<TreeviewSelect>>", self.on_select_model_table)
        #self.model_scrollbar = ttk.Scrollbar(self.upper_frame, orient = tk.VERTICAL, command = self.model_table.yview)
        #self.model_table['yscroll'] = self.model_scrollbar.set
        self.model_table.column('#0', width = 80, stretch = tk.NO, minwidth = 80)
        #self.model_scrollbar.grid(row = 0, column = 1, sticky = tk.NSEW, padx = [2,0], pady = 5)


        self.entries_table = ttk.Treeview(self.master, height =9, columns = ["Entry", "Missing Atoms", "Substitutions","Chirality Mismatches", "Name Mismatches", "Foreign Atoms"])
        self.entries_table.grid(row=0, column=3, sticky="NW", padx=[3,0], pady=[5,0], columnspan = 10)
        self.entries_table['show'] = 'headings'
        self.entries_table.heading('#1', text="Entry")
        self.entries_table.heading('#2', text="Missing Atoms")
        self.entries_table.heading('#3', text="Substitutions")
        self.entries_table.heading('#4', text="Chirality Mismatches")
        self.entries_table.heading('#5', text="Name Mimsatches")
        self.entries_table.heading('#6', text="Foreign Atoms")
        self.entries_table.column('#1', width = 38, anchor = tk.W)
        self.entries_table.column('#2', width=88)
        self.entries_table.column('#3', width=78)
        self.entries_table.column('#4', width=120, anchor=tk.W)
        self.entries_table.column('#5', width=110)
        self.entries_table.column('#6', width=90)


        self.entries_table.bind("<<TreeviewSelect>>", self.on_select_entries_table)

        self.entries_scrollbar = ttk.Scrollbar(self.master, orient=tk.VERTICAL, command=self.entries_table.yview)
        self.entries_table['yscroll'] = self.entries_scrollbar.set
        self.entries_scrollbar.grid(row=0, column=14, sticky=tk.NSEW, padx=[2, 5], pady=0)
        self.entries_table.bind("<<TreeviewSelect>>", self.on_select_entries_table)


        self.notebook = ttk.Notebook(self.master, width=350, height=180)
        self.notebook.grid(row=1, column=0, sticky="NW", columnspan=6, pady=[5,5], padx = 5)

        self.tab_names = ['Entries', 'Missing', 'Name Mismatches', 'Chirality Mismatches', 'Foreign Atoms']

        self.missing_table = self.tab_maker(self.tab_names[1], ["Atoms", "Rings"])

        self.name_mismatches_table = self.tab_maker(self.tab_names[2], ["Model", "Motif"])

        self.chirality_mismatches_table = self.tab_maker(self.tab_names[3], ["Model", "Motif"])

        self.foreign_atoms_table = self.tab_maker(self.tab_names[4], ["Model", "Motif"])

        self.entry_label = tk.Label(self.master, text="PDBid", anchor=tk.W)
        self.entry_label.grid(row=2, column=0, sticky=tk.NW, padx=(5, 0))

        self.input_text = tk.StringVar()
        self.input_text.trace("w", lambda name, index, mode, sv=self.input_text: self.str_length(self.input_text))

        self.entry = tk.Entry(self.master, width=23, textvariable=self.input_text)
        self.entry.grid(row=2, column=1, sticky=tk.NE, padx=(0, 5), columnspan = 3)

        self.start_button = tk.Button(self.master, text="Validate!", command=lambda: self.start_validation())
        self.start_button.grid(row=2, column=4, sticky=tk.NW, padx=0, columnspan = 2)

        #self.info_button = tk.Button(self.master, text="Help", command=self.help)
        #self.info_button.grid(row=2, column=5, sticky=tk.NE)

        self.status_bar_frame = tk.Frame(self.master)
        self.status_bar_frame.configure(width=640, height=20)
        self.status_bar_frame.grid(column=0, columnspan=11)

        self.status_bar_label = tk.Label(self.status_bar_frame)
        self.status_bar_label.grid(sticky="w", column=0, row = 0)

    def str_length(self, input_text):
        """
        Control length of given string.
        :param input_text: text written into entry box
        :return: True, if it has right length
        """
        c = self.input_text.get()[0:4]
        self.input_text.set(c)
        return True

    def add_option(self, pdb_id):
        """
        Method, makes a PDBid option in left panel + makes it's children (Models)
        :param pdb_id: given PDBid
        :return:
        """
        try:
            self.model_table.insert("", 1, pdb_id.lower(), text=pdb_id.lower())
            for i in self.downloaded_object.protein_model_list:
                self.model_table.insert(pdb_id, 1, text=i["ModelName"])

        except tk.TclError:
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
        :param name: name of tab
        :param columnames: name of columns for table
        :return:
        """
        self.tab = tk.Frame(self.master)

        self.tree = ttk.Treeview(self.tab, columns=column_names, height=18)

        self.tree['show'] = 'headings'
        for i in range(len(column_names)):
            self.tree.heading(i, text=column_names[i])
            self.tree.column(i, stretch=tk.NO, width=357 / (len(column_names)))

        self.tree.column('#0', width = 357 / (len(column_names)))


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
            counter +=1

        if model_name in ValidatorManager.validation_report[pdb_id]["Models"][counter]["ModelName"]:
            current_model = ValidatorManager.validation_report[pdb_id]["Models"][counter]["Entries"]

            for entry, properties in enumerate(current_model):
                if current_model[entry]["MissingAtomCount"] != 0:
                    self.entries_table.insert('', 1, text = current_model[entry]["MainResidue"],
                                              values = (current_model[entry]["MainResidue"],
                                                        current_model[entry]["MissingAtomCount"],
                                                        current_model[entry]["SubstitutionCount"],
                                                        current_model[entry]["ChiralityMismatchCount"],
                                                        current_model[entry]["NameMismatchCount"],
                                                        current_model[entry]["ForeignAtomCount"]),
                                              tags = ('missing'))
                    self.entries_table.tag_configure('missing', background='red')

                elif current_model[entry]["SubstitutionCount"] != 0:
                    self.entries_table.insert('', 1, text=current_model[entry]["MainResidue"],
                                              values=(current_model[entry]["MainResidue"],
                                                      current_model[entry]["MissingAtomCount"],
                                                      current_model[entry]["SubstitutionCount"],
                                                      current_model[entry]["ChiralityMismatchCount"],
                                                      current_model[entry]["NameMismatchCount"],
                                                      current_model[entry]["ForeignAtomCount"]),
                                              tags=('substitution'))
                    self.entries_table.tag_configure('substitution', background ='orange')


                else:
                    self.entries_table.insert('', 1, text=current_model[entry]["MainResidue"],
                                              values=(current_model[entry]["MainResidue"],
                                                      current_model[entry]["MissingAtomCount"],
                                                      current_model[entry]["SubstitutionCount"],
                                                      current_model[entry]["ChiralityMismatchCount"],
                                                      current_model[entry]["NameMismatchCount"],
                                                      current_model[entry]["ForeignAtomCount"]))


    def on_select_entries_table(self, event):
        """
        Method, is called when is clicked on entries table, fill properties tables.
        :param event:
        :return:
        """

        res_name = self.entries_table.item(self.entries_table.focus(),'text')
        entry_count = 0
        pdb_id = self.model_table.parent(self.model_table.focus())
        model_name_id = self.model_table.focus()
        model_name = self.model_table.item(model_name_id, 'text')



        counter = 0

        self.missing_table.delete(*self.missing_table.get_children())

        while model_name not in ValidatorManager.validation_report[pdb_id]["Models"][counter]["ModelName"]:
            counter +=1

        while res_name not in ValidatorManager.validation_report[pdb_id]["Models"][counter]["Entries"][entry_count]["MainResidue"]:
            entry_count +=1


        #if model_name in ValidatorManager.validation_report[pdb_id]["Models"][counter]["ModelName"]:
        current_entry = ValidatorManager.validation_report[pdb_id]["Models"][counter]["Entries"][entry_count]

        for atom_index in current_entry["MissingAtoms"]:
            self.missing_table.insert('', 1, values = (ValidatorManager.validation_report[pdb_id]["Models"][counter]["ModelNames"][str(atom_index)]))


        self.table_fill(self.chirality_mismatches_table, "ChiralityMismatches")
        self.table_fill(self.foreign_atoms_table, "ForeignAtoms")
        self.table_fill(self.name_mismatches_table, "NameMismatches")



    def table_fill(self, table, property):
        counter = 0
        res_name = self.entries_table.item(self.entries_table.focus(), 'text')
        entry_count = 0
        pdb_id = self.model_table.parent(self.model_table.focus())
        model_name_id = self.model_table.focus()
        model_name = self.model_table.item(model_name_id, 'text')
        table.delete(*table.get_children())


        while model_name not in ValidatorManager.validation_report[pdb_id]["Models"][counter]["ModelName"]:
            counter +=1

        while res_name not in ValidatorManager.validation_report[pdb_id]["Models"][counter]["Entries"][entry_count]["MainResidue"]:
                entry_count += 1

        #if model_name in ValidatorManager.validation_report[pdb_id]["Models"][counter]["ModelName"]:

        current_entry = ValidatorManager.validation_report[pdb_id]["Models"][counter]["Entries"][entry_count]
        for atom_index, motiff in enumerate(current_entry[property]):
            table.insert('', 1, values = (ValidatorManager.validation_report[pdb_id]["Models"][counter]["ModelNames"]
                                          [str(motiff)], current_entry[property][str(motiff)]))


    def start_validation(self):
        """
        Method, calls validation from RESIDUE class
        :return:
        """
        self.downloaded_object = ValidatorManager.ValidatorManager()

        if self.downloaded_object.error_check(self.entry.get()):
            tkMessageBox.showerror("Error", self.downloaded_object.error)
            return
        else:
            self.downloaded_object.download_entry(self.entry.get())
            self.add_option(self.entry.get())


            # for i in range(self.entry_count):
            # self.entries_table.insert('', 'end', values = (self.main_res[i][0], self.state[i], self.main_res[i]))

            # for key, value in enumerate(self.missing_atoms_dict):
            # self.missing_table.insert('', 'end', values = (self.missing_atoms_dict[value]) )

            # for key, value in self.missing_atoms_dict.iteritems():
            # self.table4.insert('', 'end', values = (value))


            # for key, value in self.foreign_atoms.iteritems():
            # self.foreign_atoms_table.insert('', 'end', values = (key , value))


def main():
    root = tk.Tk()
    root.wm_title("Validator")
    root.resizable(width=False, height=False)
    root.geometry("640x480")
    app = MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()
