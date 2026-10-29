from services.general.base_service import BaseService
from services.university.helpers.grade_helper import GradeHelper
from services.university.helpers.group_helper import GroupHelper
from services.university.helpers.student_helper import StudentHelper
from services.university.helpers.teacher_helper import TeacherHelper
from services.university.group_service import GroupService
from services.university.student_service import StudentService
from services.university.teacher_service import TeacherService
from services.university.grade_service import GradeService
from utils.api_utils import ApiUtils


class UniversityService(BaseService):
    SERVICE_URL = "http://127.0.0.1:8001"

    def __init__(self, api_utils: ApiUtils):
        super().__init__(api_utils)

        self.group = GroupService(
            GroupHelper(self.api_utils)
        )
        self.student = StudentService(
            StudentHelper(self.api_utils)
        )
        self.teacher = TeacherService(
            TeacherHelper(self.api_utils)
        )
        self.grade = GradeService(
            GradeHelper(self.api_utils)
        )
