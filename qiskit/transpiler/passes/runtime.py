# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

""" An analysis pass for calculating the esimtated runtime of a circuit
"""

from qiskit.transpiler.basepasses import AnalysisPass
from qiskit.exceptions import QiskitError


class Runtime(AnalysisPass):
    """ An analysis pass for calculating the esimtated runtime of a circuit
    """

    def __init__(self, backend_props):
        super().__init__()
        self.gate_dict = {
            gate.name.lower(): gate for gate in backend_props.gates}

    def run(self, dag):
        runtime = 0
        # should we ennumerate all paths instead of just longest
        # b/c some shorter paths might have lengthier gates
        for node in dag.longest_path():
            if node.data_dict["type"] == "op":
                # find the qubits going into this
                op_qubits = [str(qubit.index)
                             for qubit in node.data_dict["qargs"]]
                # find the name of the gate note
                op_name = node.data_dict["name"]
                if op_name == "measure":
                    # do any backends have measure data?
                    # i cant find measure data
                    continue
                # construct the gate name based off of this
                gate_name = op_name
                if len(op_qubits) == 2:
                    gate_name = gate_name + op_qubits[0] + "_" + op_qubits[1]
                elif len(op_qubits) == 1:
                    gate_name = gate_name + "_" + op_qubits[0]
                else:
                    # new future qc with bigger than two inputs on a gate?
                    raise QiskitError()

                gate = self.gate_dict[gate_name]
                # look for 'gate_length' property
                # need to take into account unit
                runtime += gate.parameters[1].value
        self.property_set['runtime_ns'] = runtime
        return dag
