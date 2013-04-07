import unittest
import os
from os.path import dirname, isfile, isdir
import shutil

from sqlalchemy import create_engine
from sqlalchemy.sql import text

from context import tagi
from tagi import data
from tagi.data import Document, Tag, Tagi

import string
import random

def create_test_database():
    # if isfile('tagi_tests.db'):
    #     os.remove('tagi_tests.db')

    if not isfile('tagi_tests.db'):
        db = Tagi('tagi_tests.db')
        db.create_document('existing_document', tags = [])
        db.create_document('no_tags', tags = [])
        db.create_document('tags_a_e_i_o_u', tags = ['a','e','i','o','u'])
        
        db.create_document('three_docs_1', tags = ['three_docs'])
        db.create_document('three_docs_2', tags = ['three_docs'])
        db.create_document('three_docs_3', tags = ['three_docs','only_doc'])
        
        db.create_document('context_doc_a', tags = ['context_test_docs'], context = ['context_tag_a'])
        db.create_document('context_doc_b1', tags = ['context_test_docs'], context = ['context_tag_b'])
        db.create_document('context_doc_b2', tags = ['context_test_docs'], context = ['context_tag_b'])
        db.create_document('context_doc_bc', tags = ['context_test_docs'], context = ['context_tag_b', 'context_tag_c'])

        for i in xrange(20):
            # path = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
            # db.create_document("context_doc_%s" % path,['context_test_docs'])
            db.create_document("context_doc_extra_%s" % (i + 1),['context_test_docs'])

        db.create_document('link_doc_a', links = ['link_tag_a'])

    shutil.copyfile('tagi_tests.db','tagi.db')

    

class TestDbInit(unittest.TestCase):
    def setUp(self):
        if isfile('tagi.db'):
            os.remove('tagi.db')

        open('tagi.db', 'w').close()
        
    def tearDown(self):
        os.remove('tagi.db')

    def test_new_init(self):
        os.remove('tagi.db')
        Tagi('tagi.db')
        self.assertTrue(isfile('tagi.db'))
        

    # not actually possible to test. birth time is not usually recorded...
    # def test_existing_init(self):
    #     time = getctime('tagi.db')
    #     db.init('tagi.db')
    #     self.assertEqual(time,getctime('tagi.db'))

class TestWikiRoot(unittest.TestCase):
    
    def setUp(self):
        if(isdir('level1')):
            shutil.rmtree('level1')
            
        os.makedirs('level1/level2/level3')
        open('level1/level1.db','w').close()
        open('level1/level2/level2.db','w').close()
        open('level1/level2/level3/level3.db','w').close()

        open('level1/level2/level3.db','w').close()


    def tearDown(self):
        shutil.rmtree('level1')
    
    def test_database_name(self):
        original_dir = os.getcwd()

	os.chdir('level1/level2/level3')
        cwd = os.getcwd()
        db = Tagi('level3.db')
        self.assertEqual(cwd, db.wiki_root)
        
        db = Tagi('level2.db')
        self.assertEqual(dirname(cwd), db.wiki_root)

        db = Tagi('level1.db')
        self.assertEqual(dirname(dirname(cwd)), db.wiki_root)
        
        os.chdir(original_dir)
        

class TestDocuments(unittest.TestCase):

    def setUp(self):
        if (isfile('tagi.db')):
            os.remove('tagi.db')
            
        create_test_database()
        self.db = Tagi('tagi.db')
            
    def tearDown(self):
        os.remove('tagi.db')

    def test_can_find_document_by_path(self):
        existing = self.db.find_document(path = 'existing_document')
        self.assertTrue(existing.id == 1)
    
    def test_can_add_new_document(self):
        doc = self.db.create_document('new_document')

        new_id = doc.id
        found_doc = self.db.find_document(path = 'new_document')
        self.assertEqual(new_id, found_doc.id)
        
    def test_cannot_add_existing_document(self):
        existing = self.db.find_document(path = 'existing_document')
        new = self.db.create_document('existing_document')
        self.assertTrue(existing.id == new.id)

    def test_can_read_tags(self):
        doc = self.db.find_document(path='tags_a_e_i_o_u')
        self.assertEqual([tag.keyword.name for tag in doc.tags], ['a','e','i','o','u'])
        
    def test_can_add_tags(self):
        orig = self.db.find_document(path='no_tags')
        self.db.add_tags(orig,['a','b','c'])

        doc = self.db.find_document(path='no_tags')
        self.assertEqual([tag.keyword.name for tag in doc.tags], ['a','b','c'])

    def test_cannot_add_duplicate_tags(self):
        doc = self.db.find_document(path='tags_a_e_i_o_u')
        self.db.add_tags(doc, ['a','e'])

        doc = self.db.find_document(path='tags_a_e_i_o_u')
        self.assertEqual([tag.keyword.name for tag in doc.tags], ['a','e','i','o','u'])

    def test_can_remove_tags(self):
        doc = self.db.find_document(path='tags_a_e_i_o_u')
        self.db.remove_tags(doc,['a','b','c'])

        doc = self.db.find_document(path='tags_a_e_i_o_u')
        self.assertEqual([tag.keyword.name for tag in doc.tags], ['e','i','o','u'])
        
    def test_can_read_context(self):
        doc = self.db.find_document(path='context_doc_bc')
        self.assertEqual([tag.keyword.name for tag in doc.context], ['context_tag_b','context_tag_c'])

    def test_can_change_context(self):
        doc = self.db.find_document(path='context_doc_bc')
        self.db.set_context(doc,['context_tag_a'])

        doc = self.db.find_document(path='context_doc_bc')
        self.assertEqual([tag.keyword.name for tag in doc.context], ['context_tag_a'])
        
    def test_can_read_link_tags(self):
        doc = self.db.find_document(path='link_doc_a')
        self.assertEqual([tag.keyword.name for tag in doc.links], ['link_tag_a'])

    def test_can_change_link_tags(self):
        doc = self.db.find_document(path='link_doc_a')
        self.db.set_links(doc,['link_doc_b'])

        doc = self.db.find_document(path='link_doc_a')
        self.assertEqual([tag.keyword.name for tag in doc.links], ['link_doc_b'])

    def test_can_find_documents_with_tag(self):
        docs = self.db.find_documents(tags = ['three_docs'])
        self.assertTrue(len(docs) == 3) #1

        docs = self.db.find_documents(tags = ['only_doc'])
        self.assertTrue(len(docs) == 1) #2

        docs = self.db.find_documents(tags = ['three_docs', 'only_doc'])
        self.assertTrue(len(docs) == 1) #3

    def test_can_find_document_using_tags_and_context(self):
        # uses both the context and tags when filtering
        context_a = self.db.find_documents(tags = ['context_test_docs'],context = ['context_tag_a'])
        context_doc_a = self.db.find_document(path = 'context_doc_a')
        self.assertEqual(context_a[0].id, context_doc_a.id)

        # returns a list of documents with the most appropriate at the top
        context_bc = self.db.find_documents(tags = ['context_test_docs'], context = ['context_tag_b','context_tag_c'])
        context_doc_bc = self.db.find_document(path = 'context_doc_bc')
        self.assertEqual(context_bc[0].id, context_doc_bc.id)
        self.assertEqual(len(context_bc), 24)

        # if nothing exits with the context, return all
        nonexistant_context = self.db.find_documents(tags = ['context_test_docs'], context = ['nonexistant_context'])
        self.assertEqual(len(nonexistant_context), 24)
 
if __name__ == '__main__':
    unittest.main()

