from typing import Generic, TypeVar

T = TypeVar('T')


class BaseRepository(Generic[T]):
    def __init__(self, model):
        self.model = model

    def get(self):
        return self.model.query.limit(25).all()

    def getPaginated(self, per_page, page):
        return self.model.query.paginate(per_page=per_page, page=page)

    def getById(self, id):
        return self.model.query.filter(self.model.id == id).one_or_none()

    def executeQuery(self, limit, orderBy, descending=False):
        if descending:
            return self.model.query.order_by(orderBy.desc()).limit(limit).all()
        return self.model.query.order_by(orderBy).limit(limit).all()
