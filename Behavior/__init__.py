from .Meta.Behavior import *

from .Listable import *
from .Indexable import *
from .Deleteable import *
from .Postable import *
from .Updateable import *
from .Singleton import *
from .Pageable import *

mapper = {
    Listable.__name__: Listable,
    Indexable.__name__: Indexable,
    Deleteable.__name__: Deleteable,
    Postable.__name__: Postable,
    Updateable.__name__: Updateable,
    Singleton.__name__: Singleton,
    Pageable.__name__: Pageable
}
