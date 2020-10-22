from typing import Generic, TypeVar

T = TypeVar('T')


class BaseRepository(Generic[T]):
    def __init__(self, model):
        self.model = model

    def get(self):
        return self.model.query.all()

    def getPaginated(self, per_page, page):
        return self.model.query.paginate(per_page=per_page, page=page)

    def getById(self, id):
        return self.model.query.filter(self.model.id == id).one_or_none()
