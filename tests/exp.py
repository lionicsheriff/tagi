from context import tagi
import tagi.db
from tagi.db import Document,Tag, Session

tagi.db.init()

s = Session()
d = Document('doc_a')
t = Tag('tag_a')

