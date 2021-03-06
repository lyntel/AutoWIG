.. Copyright [2017-2018] UMR MISTEA INRA, UMR LEPSE INRA,                ..
..                       UMR AGAP CIRAD, EPI Virtual Plants Inria        ..
.. Copyright [2015-2016] UMR AGAP CIRAD, EPI Virtual Plants Inria        ..
..                                                                       ..
.. This file is part of the AutoWIG project. More information can be     ..
.. found at                                                              ..
..                                                                       ..
..     http://autowig.rtfd.io                                            ..
..                                                                       ..
.. The Apache Software Foundation (ASF) licenses this file to you under  ..
.. the Apache License, Version 2.0 (the "License"); you may not use this ..
.. file except in compliance with the License. You should have received  ..
.. a copy of the Apache License, Version 2.0 along with this file; see   ..
.. the file LICENSE. If not, you may obtain a copy of the License at     ..
..                                                                       ..
..     http://www.apache.org/licenses/LICENSE-2.0                        ..
..                                                                       ..
.. Unless required by applicable law or agreed to in writing, software   ..
.. distributed under the License is distributed on an "AS IS" BASIS,     ..
.. WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or       ..
.. mplied. See the License for the specific language governing           ..
.. permissions and limitations under the License.                        ..

Installation from binaries
==========================
    
In order to ease the installation of the **AutoWIG** software on multiple operating systems, the **Conda** package and environment management system is used.
To install **Conda**, please refers to its `documentation <http://conda.pydata.org/docs>`_ or follow the installation instructions given on the **StatisKit** `documentation <https://statiskit.rtfd.io>`_.
Once **Conda** is installed, you can install **AutoWIG** binaries into a special environment that will be used for wrapper generation by typing the following command line in your terminal:

.. code-block:: console

    conda create -n autowig python-autowig -c statiskit

.. warning::

    When compiling wrappers generated by **AutoWIG** in its environment some issues can be encountered at compile time or run time (from within the *Python* interpreter) due to compiler or dependency incompatibilies.
    This is why it is recommended to install **AutoWIG** in a separate environment that will only be used for wrappers' generation.
    If the problem persits, please refers to the **StatisKit** `documentation <http://statiskit.rtfd.io>`_ concerning the configuration of the development environment.
