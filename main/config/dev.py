from main.config.base_config import BaseConfig


class DevConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:mathefuka1@localhost:3306/gotit_finalproject_dev"


config = DevConfig
