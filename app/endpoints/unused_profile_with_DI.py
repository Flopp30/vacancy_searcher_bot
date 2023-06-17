# from fastapi import APIRouter, Depends, Form, Request
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# from sqlalchemy.ext.asyncio import AsyncSession

# from db import get_async_session, profile_crud
# from db import grade_types_crud, work_types_crud
# from .validators import validate_salary


# router = APIRouter()
# templates = Jinja2Templates(directory='app/templates')


# @router.get('/{user_id}')
# async def get_profile_form(
#     request: Request,
#     user_id: int,
#     session: AsyncSession = Depends(get_async_session),
# ):
#     profile = await profile_crud.get_by_attribute(
#        'user_id', user_id, session, is_deleted=False)
#     if profile:
#         return templates.TemplateResponse(
#             'profile.html', {'request': request, 'profile': profile}
#         )
#     return templates.TemplateResponse('profile.html', {'request': request})


# @router.post('/{user_id}', response_class=HTMLResponse)
# async def create_or_update_profile(
#     user_id: int,
#     professional_role: str = Form(..., min_length=1, max_length=32),
#     grade: str = Form(...),
#     work_type: str = Form(...),
#     region: str = Form(..., min_length=1, max_length=32),
#     salary_from: int = Form(..., gt=0),
#     salary_to: int = Form(..., gt=0),
#     ready_for_relocation: bool = Form(False),
#     session: AsyncSession = Depends(get_async_session),
# ):
#     validate_salary(salary_from, salary_to)
#     grade = await grade_types_crud.get_by_attribute('type', grade, session)
#     work_type = await work_types_crud.get_by_attribute(
#        'type', work_type, session)
#     data = {
#         "professional_role": professional_role,
#         "grade_type_id": grade.id,
#         "work_type_id": work_type.id,
#         "region": region,
#         "salary_from": salary_from,
#         "salary_to": salary_to,
#         "ready_for_relocation": ready_for_relocation,
#         "user_id": user_id,
#     }

#     profile = await profile_crud.get_by_attribute(
#        'user_id', user_id, session, is_deleted=False
#    )

#     if profile:
#         await profile_crud.update(profile, data, session)
#     else:
#         await profile_crud.create(data, session)
#     return data
