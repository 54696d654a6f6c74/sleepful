from Behavior import Indexable
from Behavior import Listable
from Behavior import Pageable

from Behavior import Postable
from Behavior import Updateable
from Behavior import Deleteable


class PostView(Postable, Deleteable, Updateable, Pageable):
    def bind(self, bp):
        Indexable.bind(self, bp)
        Listable.bind(self, bp)
        Postable.bind(self, bp)
        Deleteable.bind(self, bp)
        Updateable.bind(self, bp)
