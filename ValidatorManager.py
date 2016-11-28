import json
import urllib2
import Model

# Global variable, used for display values in treeview #
validation_report = {}


class ValidatorManager:
    # Manage validation, Checks internet connection, checks for errors in PDBs #

    def __init__(self):
        self.error = ""
        self.protein_model_list = []
        # self.downloaded_json = json.load(open('3d11.json', mode='r'))             # uncomment when internet connection
        self.downloaded_json = {}
        self.validation_report = {}

    def error_check(self, pdb_id):
        """
        Method, checks if internet connection is ok download JSON from web and if PDB is valid
        :param pdb_id: PDBid which will be downloaded
        :return: bool, True for Error, False for success
        """

        try:
            self.downloaded_json = json.load(
                urllib2.urlopen("https://webchemdev.ncbr.muni.cz/API/Validation/Protein/" + pdb_id))
            # self.downloaded_json = json.load(self.downloaded_json)

        except urllib2.URLError:
            self.error = "Could not load page. Check your internet connection."
            return True

        if 'Error' in self.downloaded_json:
            self.error = self.downloaded_json['Error']
            return True


        elif self.downloaded_json['MotiveCount'] == 0:
            self.error = "No models to validate! Please use another molecule."
            return True

        else:
            return False

    def scan_json(self, pdb_id):
        """
        Scan the JSON file, add PDB to global variable validation_report and split PDB to models.
        :param pdb_id: PDBid which will be downloaded
        :return: List of models of given PDBid
        """

        global validation_report
        validation_report[pdb_id] = self.downloaded_json

        for item, value in enumerate(self.downloaded_json["Models"]):
            pdb_entry = self.downloaded_json["Models"][item]
            self.protein_model_list.append(pdb_entry)
            Model.Model(pdb_entry)

        return self.protein_model_list
