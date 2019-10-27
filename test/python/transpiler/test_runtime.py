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

"""Runtime pass testing"""

import unittest

from qiskit import QuantumCircuit
from qiskit.converters import circuit_to_dag
from qiskit.transpiler.passes import Runtime
from qiskit.test import QiskitTestCase
from qiskit.test.mock import FakeOurense


class TestRuntimePass(QiskitTestCase):
    """ Tests for Runtime analysis methods. """

    def test_empty_dag(self):
        """ Empty DAG has 0 size"""
        circuit = QuantumCircuit()
        dag = circuit_to_dag(circuit)

        backend_props = FakeOurense().properties()
        pass_ = Runtime(backend_props)
        _ = pass_.run(dag)

        self.assertEqual(pass_.property_set['runtime_ns'], 0)


if __name__ == '__main__':
    unittest.main()
