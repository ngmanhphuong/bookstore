from sqlalchemy import Column, Integer, String, Text, Boolean, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from banhang import db, app
from enum import Enum as UserEnum
from flask_login import UserMixin
from datetime import datetime


class UserRole(UserEnum):
    USER = 2
    ADMIN = 1


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class Category(BaseModel):
    __tablename__ = 'category'

    name = Column(String(50), nullable=False)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


prod_tag = db.Table('prod_tag',
                    Column('product_id', Integer, ForeignKey('product.id'), primary_key=True),
                    Column('tag_id', Integer, ForeignKey('tag.id'), primary_key=True))


class Product(BaseModel):
    name = Column(String(50), nullable=False)
    description = Column(Text)
    price = Column(Float, default=0)
    image = Column(String(100))
    active = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    receipt_details = relationship('ReceiptDetails', backref='product', lazy=True)
    tags = relationship('Tag', secondary='prod_tag', lazy='subquery',
                        backref=backref('products', lazy=True))
    comments = relationship('Comment', backref='product', lazy=True)

    def __str__(self):
        return self.name


class Tag(BaseModel):
    name = Column(String(50), nullable=False, unique=True)

    def __str__(self):
        return self.name


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100), nullable=False)
    active = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    receipts = relationship('Receipt', backref='user', lazy=True)
    comments = relationship('Comment', backref='user', lazy=True)

    def __str__(self):
        return self.name


class Receipt(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetails', backref='receipt', lazy=True)


class ReceiptDetails(BaseModel):
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)


class Comment(BaseModel):
    content = Column(String(255), nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        c1 = Category(name='Sách bán chạy')
        c2 = Category(name='Sách mới nhập')

        db.session.add_all([c1, c2])
        db.session.commit()

        p1 = Product(name='Mắt biếc', description='Truyện dài', price=110000,
                     image='https://upload.wikimedia.org/wikipedia/vi/9/92/Mat_Biec.gif',
                     category_id=1)
        p2 = Product(name='Út Quyên và tôi', description='Tập truyện', price=72250,
                     image='https://www.nxbtre.com.vn/Images/Book/copy_21_NXBTreStoryFull_04112014_021101.jpg',
                     category_id=2)
        p3 = Product(name='Trước vòng chung kết', description='Truyện dài', price=102000,
                     image='https://quang.name.vn/wp-content/uploads/2020/05/truoc-vong-chung-ket.jpg',
                     category_id=1)
        p4 = Product(name='Nữ sinh', description='Truyện dài', price=72250,
                     image='https://isach.info/images/story/cover/nu_sinh__nguyen_nhat_anh.jpg',
                     category_id=2)
        p5 = Product(name='Thằng quỷ nhỏ', description='Truyện dài', price=93500,
                     image='https://nhungcuonsachhay.com/wp-content/uploads/2021/05/Thang-quy-nho-Nguyen-Nhat-Anh.jpg',
                     category_id=1)
        p6 = Product(name='Chú bé rắc rối', description='Truyện dài', price=70300,
                     image='http://isach.info/images/story/cover/chu_be_rac_roi__nguyen_nhat_anh.jpg',
                     category_id=2)
        p7 = Product(name='Kính vạn hoa 2', description='Tập truyện', price=88000,
                     image='https://salt.tikicdn.com/media/catalog/product/k/v/kvh_18tap_2.jpg',
                     category_id=2)
        p8 = Product(name='Kính vạn hoa 6', description='Tập truyện', price=76500,
                     image='https://salt.tikicdn.com/media/catalog/product/k/v/kvh_18tap_6.jpg',
                     category_id=2)

        db.session.add_all([p1, p2, p3, p4, p5, p6, p7, p8])
        db.session.commit()

        import hashlib

        password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        u = User(name='', username='admin', password=password,
                 user_role=UserRole.ADMIN,
                 avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1647248722/r8sjly3st7estapvj19u.jpg')
        db.session.add(u)
        db.session.commit()

        c1 = Comment(content='Good', user_id=1, product_id=1)
        c2 = Comment(content='Nice', user_id=1, product_id=1)
        db.session.add_all([c1, c2])
        db.session.commit()
