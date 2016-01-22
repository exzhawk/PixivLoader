# -*- encoding: utf-8 -*-
# Author: Epix
import pickle


class CacheDb:
    def __init__(self, db_file_name):
        self.db_file_name = db_file_name
        self.data = {}
        self.load()

    def load(self):
        try:
            self.data = pickle.load(open(self.db_file_name, 'rb'))
        except IOError:
            self.data = {}

    def save(self):
        pickle.dump(self.data, open(self.db_file_name, 'wb'))

    def get(self, key):
        return self.data.get(key, None)

    def set(self, key, value):
        self.data[key] = value
        self.save()
