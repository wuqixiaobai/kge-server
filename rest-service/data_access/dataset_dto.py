#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# coding:utf-8
#
# dataset_dto.py: Contains the DTO for Datasets
# Copyright (C) 2016 - 2017 Víctor Fernández Rico <vfrico@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import os
import copy
import data_access.data_access_base as data_access_base
import kgeserver.dataset as dataset
from data_access.algorithm_dao import AlgorithmDAO
# from data_access.dataset_dao import DatasetDAO

RUNNING_TASK_MASK = 0b0001
TRAINED_MASK = 0b0010
INDEXED_MASK = 0b0100
SEARCHINDEXED_MASK = 0b1000


class DatasetDTO(data_access_base.DTOClass):
    id = None
    status = None
    entities = None
    relations = None
    triples = None
    algorithm = None
    name = None
    description = None
    dataset_type = None
    error = None
    task = None

    _binary_dataset = None
    _binary_model = None
    _binary_index = None

    _base = data_access_base._CONFIG_get_dataset_path()

    def from_dict(self, result_dict, use_cache=True):
        """Given a result dict, with proper fields, builds a datasetDTO

        :param dict result_dict: A dict with all fields required
        :return: A dataset dictionary or None
        :rtype: dict
        """  # INFO:This method is intended ONLY to fill a dataset dict.
        # Query has an object
        self._binary_dataset = result_dict['binary_dataset']
        self._binary_model = result_dict['binary_model']
        self._binary_index = result_dict['binary_index']
        self.status = result_dict['status']
        self.name = result_dict['name']
        self.description = result_dict['description']
        self.id = int(result_dict['id'])
        self.dataset_type = result_dict['dataset_type']
        self.task = result_dict['task']

        if result_dict['triples'] is not None and\
           result_dict['relations'] is not None and\
           result_dict['entities'] is not None and use_cache:
            # These fields are filled and can be readable
            print("Using cached values")
            self.triples = result_dict['triples']
            self.entities = result_dict['entities']
            self.relations = result_dict['relations']
        else:
            # Fields should be readed from file
            print("Without cache")
            dtst = dataset.Dataset()
            dtst_path = os.path.join(self._base, self._binary_dataset)
            try:
                dtst.load_from_binary(dtst_path)
            except OSError as err:
                self.error = "Dataset not found: "+str(err)
                self.is_error_dto()
            self.triples = len(dtst.subs)
            self.entities = len(dtst.entities)
            self.relations = len(dtst.relations)

        alg_dao = AlgorithmDAO()
        algorithm, err = alg_dao.get_algorithm_by_id(result_dict['algorithm'])
        if algorithm is None:
            raise LookupError(err)
        self.algorithm = algorithm

        return None

    def is_error_dto(self):
        for key in copy.copy(self.__dict__):
            if key != "id":
                self.key = None
        return

    def is_untrained(self):
        """Check if dataset is in untrained state

        Returns true if 0b0010 bit is 0 from the dataset status.

        :return: True if dataset is in untrained state
        :rtype: boolean
        """
        if self.status is None:
            return None
        elif self.status & TRAINED_MASK == 0:
            return True
        else:
            return False

    def is_trained(self):
        """Check if dataset is in untrained state

        Return True if status has bit 0b0010 on.

        :return: True if dataset is in untrained state
        :rtype: boolean
        """
        if self.status is None:
            return None
        elif self.status & TRAINED_MASK == TRAINED_MASK:
            return True
        else:
            return False

    def get_binary_index(self):
        """Returns the path to the binary index file.
        """
        return os.path.join(self._base, self._binary_index)

    def get_binary_dataset(self):
        """Return the path to the binary dataset file
        """
        return os.path.join(self._base, self._binary_dataset)

    def get_binary_model(self):
        """Return the path of the binary model file
        """
        return os.path.join(self._base, self._binary_model)
