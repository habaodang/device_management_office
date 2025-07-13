from device_management import db

class DatabaseAccess:
    def __init__(self,model_class):
        self.model_class=model_class

    #ham lay tat ca du lieu cua doi tuong model_class
    def get_all(self):
        return self.model_class.query.all()

    #lay gia tri loc them id
    def get_by_id(self, obj_id):
        return self.model_class.query.get(obj_id)

    #loc them fiekd cua obj
    def get_by_field(self, field_name, value):
        """
        Tìm 1 bản ghi theo field bất kỳ
        """
        field = getattr(self.model_class, field_name)
        return self.model_class.query.filter(field == value).first()

    def get_by_field_all(self, field_name,value):
        field = getattr(self.model_class, field_name)
        return self.model_class.query.filter(field == value).all()

    def create(self, **kwargs):
        obj = self.model_class(**kwargs)
        db.session.add(obj)
        db.session.commit()
        return obj

    def delete(self, obj_id):
        obj = self.get_by_id(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return True
        return False
