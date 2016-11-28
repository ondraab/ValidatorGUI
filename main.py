import ValidatorManager
import sys
import argparse
import Entry

print "ValidatorAPI - This program validates PDBs from ValidatorDB database\n"

##ArgParser##
parser = argparse.ArgumentParser()
parser.add_argument("pdbid", help = "PDB which you want validate")
args = parser.parse_args()
#print args.pdbid


download = ValidatorManager.JSONParser()
res = dict
#check = JSON_manager.JSONParser()
#check.ArgValid(args.pdbid)
#download.DownloadEntry(args.pdbid)

#ResParse = models.models()
#ResParse.ModelParser()

#ResParse = residue.RESIDUE()
#ResParse.ResParser()


