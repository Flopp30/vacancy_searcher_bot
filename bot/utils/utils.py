from urllib.parse import quote
from db import Profile
from bot.utils.hh_parser import get_area_id_by_area_name


async def make_get_params_from_profile(profile: Profile) -> str:
    unexpected_attrs = [
        "user_id",
        "id",
        "created_at",
        "updated_at",
        "is_deleted",
        "firstname",
        "lastname",
        "email",
        "work_type_id",
        "grade_type_id",
        "_sa_instance_state",
    ]
    attrs_ = profile.__dict__
    get_params = ""
    for attr_ in attrs_:
        if attr_ not in unexpected_attrs:
            value = getattr(profile, attr_)
            if value:
                match attr_:
                    case "professional_role":
                        get_params += f"text={quote(value)}&"
                    case "grade_type":
                        match value.type:
                            case "trainee":
                                get_params += "experience=noExperience&"
                            case "junior":
                                get_params += "experience=noExperience&experience=between1And3&"
                            case "middle":
                                get_params += "experience=between1And3&"
                            case "senior":
                                get_params += "experience=between3And6&moreThan6&"
                    case "work_type":
                        match value.type:
                            case "Полная занятость":
                                get_params += "employment=full&"
                            case "Частичная занятость":
                                get_params += "employment=part&"
                            case "Стажировка":
                                get_params += "employment=probation&"
                            case "Проектная работа":
                                get_params += "employment=project&"
                    case "region":
                        reloc_status = getattr(profile, "ready_for_relocation")
                        if not reloc_status:
                            area_id = await get_area_id_by_area_name(value)
                            get_params += f"area={area_id}&"
                        else:
                            get_params += "area=1&area=2&"
                    case "salary_from":
                        salary = value
                        salary_to = getattr(profile, "salary_to")
                        if salary_to:
                            salary = (salary_to + value) // 2
                        get_params += f"salary{salary}&only_with_salary=True&"
    get_params += "period=5&search_field=name&search_field=description&"
    return get_params
