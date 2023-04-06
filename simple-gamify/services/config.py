import yaml
from jsonschema import validate
from schemas.config_schemas import actionConfigSchema, challengeConfigSchema, levelConfigSchema, pointSystemConfigSchema

class Config:
    def __init__(self, route):
        try:
            with open(route + '/actions.yml', 'r') as file:
                self.actions = yaml.safe_load(file)
            with open(route + '/challenges.yml', 'r') as file:
                self.challenges = yaml.safe_load(file)
            with open(route + '/levels.yml', 'r') as file:
                self.levels = yaml.safe_load(file)
            with open(route + '/points-systems.yml', 'r') as file:
                self.points_systems = yaml.safe_load(file)
        except EnvironmentError:
            print("Something went wrong then loading config files!")

    def validate(self, required = False):
        validate(instance=self.actions, schema=actionConfigSchema) if required or self.actions else None
        validate(instance=self.challenges, schema=challengeConfigSchema) if required or self.challenges else None
        validate(instance=self.levels, schema=levelConfigSchema) if required or self.levels else None
        validate(instance=self.points_systems, schema=pointSystemConfigSchema) if required or self.points_systems else None