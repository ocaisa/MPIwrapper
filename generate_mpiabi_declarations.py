#!/usr/bin/env python3

import re
from string import Template

from mpi_constants import constants
from mpi_functions import functions
from mpi_constants_fortran import constants_fortran
from mpi_functions_fortran import functions_fortran

print()
print("// C constants")
for (tp, nm) in constants:
    subs = {'abi_tp': re.sub(r"MPI(X?)_", r"MPI\1ABI_", tp),
            'abi_nm': re.sub(r"MPI(X?)_", r"MPI\1ABI_", nm)}
    print(Template("extern $abi_tp const $abi_nm;").substitute(subs))

print()
print("// C functions")
for (tp, nm, args, flags) in functions:
    subs = {'abi_tp': re.sub(r"MPI(X?)_", r"MPI\1ABI_", tp),
            'abi_nm': re.sub(r"MPI(X?)_", r"MPI\1ABI_", nm)}
    for (i, (atp, anm)) in enumerate(args):
        subs['abi_atp{0}'.format(i)] = re.sub(r"MPI(X?)_", r"MPI\1ABI_", atp)
        subs['anm{0}'.format(i)] = anm
    tmpl = ["$abi_tp $abi_nm("]
    for (i, (atp, anm)) in enumerate(args):
        tmpl.append("  $abi_atp{0} $anm{0},".format(i))
    tmpl[-1] = re.sub(r",?$", "", tmpl[-1])  # remove trailing comma of last argument
    tmpl.append(");")
    print(Template("\n".join(tmpl)).substitute(subs))

print()
print("// Fortran constants")
for (tp, nm) in constants_fortran:
    subs = {'abi_tp': re.sub(r"MPI(X?)_\w+", r"MPI\1ABI_Fint", tp),
            'abi_nm': re.sub(r"MPI(X?)_", r"MPI\1ABI_", nm).lower() + "_"}
    print(Template("extern $abi_tp const $abi_nm;").
          substitute(subs))

print()
print("// Fortran functions")
for (tp, nm, args) in functions_fortran:
    subs = {'abi_tp': re.sub(r"MPI(X?)_\w+", r"MPI\1ABI_Fint", tp),
            'abi_nm': re.sub(r"MPI(X?)_", r"MPI\1ABI_", nm).lower() + "_"}
    for (i, (atp, anm)) in enumerate(args):
        subs['abi_atp{0}'.format(i)] = re.sub(r"MPI(X?)_\w+", r"MPI\1ABI_Fint", atp)
        subs['anm{0}'.format(i)] = anm
    tmpl = ["$abi_tp $abi_nm("]
    for (i, (atp, anm)) in enumerate(args):
        tmpl.append("  $abi_atp{0} $anm{0},".format(i))
    tmpl[-1] = re.sub(r",?$", "", tmpl[-1])  # remove trailing comma of last argument
    tmpl.append(");")
    # tmpl = ["extern $abi_tp (* const $abi_nm)("]
    # for (i, (atp, anm)) in enumerate(args):
    #     tmpl.append("  $abi_atp{0} $anm{0},".format(i))
    # tmpl[-1] = re.sub(r",?$", "", tmpl[-1])  # remove trailing comma of last argument
    # tmpl.append(");")
    print(Template("\n".join(tmpl)).substitute(subs))
