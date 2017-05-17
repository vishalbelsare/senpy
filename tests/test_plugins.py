#!/bin/env python

import os
import pickle
import shutil
import tempfile

from unittest import TestCase
from senpy.models import Results, Entry
from senpy.plugins import SentimentPlugin, ShelfMixin


class ShelfDummyPlugin(SentimentPlugin, ShelfMixin):
    def activate(self, *args, **kwargs):
        if 'counter' not in self.sh:
            self.sh['counter'] = 0
        self.save()

    def deactivate(self, *args, **kwargs):
        self.save()

    def analyse(self, *args, **kwargs):
        self.sh['counter'] = self.sh['counter'] + 1
        e = Entry()
        e.nif__isString = self.sh['counter']
        r = Results()
        r.entries.append(e)
        return r


class PluginsTest(TestCase):
    def tearDown(self):
        if os.path.exists(self.shelf_dir):
            shutil.rmtree(self.shelf_dir)

        if os.path.isfile(self.shelf_file):
            os.remove(self.shelf_file)

    def setUp(self):
        self.shelf_dir = tempfile.mkdtemp()
        self.shelf_file = os.path.join(self.shelf_dir, "shelf")

    def test_shelf_file(self):
        a = ShelfDummyPlugin(
            info={'name': 'default_shelve_file',
                  'version': 'test'})
        a.activate()
        assert os.path.isfile(a.shelf_file)
        os.remove(a.shelf_file)

    def test_shelf(self):
        ''' A shelf is created and the value is stored '''
        a = ShelfDummyPlugin(info={
            'name': 'shelve',
            'version': 'test',
            'shelf_file': self.shelf_file
        })
        assert a.sh == {}
        a.activate()
        assert a.sh == {'counter': 0}
        assert a.shelf_file == self.shelf_file

        a.sh['a'] = 'fromA'
        assert a.sh['a'] == 'fromA'

        a.save()

        sh = pickle.load(open(self.shelf_file, 'rb'))

        assert sh['a'] == 'fromA'

    def test_dummy_shelf(self):
        a = ShelfDummyPlugin(info={
            'name': 'DummyShelf',
            'shelf_file': self.shelf_file,
            'version': 'test'
        })
        a.activate()

        assert a.shelf_file == self.shelf_file
        res1 = a.analyse(input=1)
        assert res1.entries[0].nif__isString == 1
        res2 = a.analyse(input=1)
        assert res2.entries[0].nif__isString == 2

    def test_corrupt_shelf(self):
        ''' Reusing the values of a previous shelf '''

        emptyfile = os.path.join(self.shelf_dir, "emptyfile")
        invalidfile = os.path.join(self.shelf_dir, "invalid_file")
        with open(emptyfile, 'w+b'), open(invalidfile, 'w+b') as inf:
            inf.write(b'ohno')

        files = {emptyfile: ['empty file', (EOFError, IndexError)],
                 invalidfile: ['invalid file', (pickle.UnpicklingError, IndexError)]}

        for fn in files:
            with open(fn, 'rb') as f:
                msg, error = files[fn]
                a = ShelfDummyPlugin(info={
                    'name': 'shelve',
                    'version': 'test',
                    'shelf_file': f.name
                })
                assert os.path.isfile(a.shelf_file)
                print('Shelf file: %s' % a.shelf_file)
                with self.assertRaises(error):
                    a.sh['a'] = 'fromA'
                    a.save()
                del a._sh
                assert os.path.isfile(a.shelf_file)
                a.force_shelf = True
                a.sh['a'] = 'fromA'
                a.save()
                b = pickle.load(f)
                assert b['a'] == 'fromA'

    def test_reuse_shelf(self):
        ''' Reusing the values of a previous shelf '''
        a = ShelfDummyPlugin(info={
            'name': 'shelve',
            'version': 'test',
            'shelf_file': self.shelf_file
        })
        a.activate()
        print('Shelf file: %s' % a.shelf_file)
        a.sh['a'] = 'fromA'
        a.save()

        b = ShelfDummyPlugin(info={
            'name': 'shelve',
            'version': 'test',
            'shelf_file': self.shelf_file
        })
        b.activate()
        assert b.sh['a'] == 'fromA'
        b.sh['a'] = 'fromB'
        assert b.sh['a'] == 'fromB'

    def test_extra_params(self):
        ''' Should be able to set extra parameters'''
        a = ShelfDummyPlugin(info={
            'name': 'shelve',
            'version': 'test',
            'shelf_file': self.shelf_file,
            'extra_params': {
                'example': {
                    'aliases': ['example', 'ex'],
                    'required': True,
                    'default': 'nonsense'
                }
            }
        })
        assert 'example' in a.extra_params
