from main.config.base_config import BaseConfig


class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:mathefuka1@localhost:3306/gotit_finalproject_test"
    TESTING = True


config = TestConfig