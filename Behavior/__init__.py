from .Meta.Behavior import *

from .Listable import *
from .Indexable import *
from .Deleteable import *
from .Postable import *
from .Updateable import *
from .Pageable import *
from .Login import *

mapper = {
    Listable.__name__: Listable,
    Indexable.__name__: Indexable,
    Deleteable.__name__: Deleteable,
    Postable.__name__: Postable,
    Updateable.__name__: Updateable,
    Pageable.__name__: Pageable,
    Login.__name__: Login
}
