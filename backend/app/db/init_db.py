from .models import Base, engine

def init_db():
    print('here')
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
