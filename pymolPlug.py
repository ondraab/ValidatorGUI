from pymol import cmd

cmd.fetch("1tqn")
cmd.select("Selection1", "resn ASN")
cmd.hide("lines", "all")
cmd.show("sphere", "Selection1")
cmd.color("red", "Selection1")
