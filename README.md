# combattbmodel

[![Build Status](https://travis-ci.org/COMBAT-TB/combattbmodel.svg?branch=master)](https://travis-ci.org/COMBAT-TB/combattbmodel)

The COMBAT-TB graph model is a [Chado](https://github.com/GMOD/Chado)-derived graph model for genome annotation.

## Overview

The graph model is based on the following Chado modules:

* CV
* Sequence
* Publication

A diagram depicting the Graph model can be found [here,](docs/chado_based_graph_model.png) with the accompanying documentation [here](docs/genome_annotation_model.md).

## Installation

```sh
$ virtualenv envname
$ source envname/bin/activate
$ pip install -i https://test.pypi.org/simple/ combattbmodel
$ python
```

```python
>>> import combattbmodel
>>> combattbmodel.name
'combattbmodel'
>>> from combattbmodel.core import Gene
>>> gene = Gene()
>>> gene.so_id
u'SO:0000704'
>>>
```
