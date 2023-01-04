import json
from dataclasses import dataclass

@dataclass
class AppResult:
    success: bool
    message: str
    data: list

    def toJSON(self):
        return json.loads(json.dumps(self, default=vars))

    @staticmethod
    def create_error_result(message):
        return AppResult(False, message, None)

    @staticmethod
    def create_true_result():
        return AppResult(True, "", None)