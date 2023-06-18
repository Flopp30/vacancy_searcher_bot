from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session, profile_crud, grade_types_crud, work_types_crud
from db.schemas import ProfileCreate
from .validators import validate_salary


router = APIRouter()
templates = Jinja2Templates(directory='app/templates')


@router.get('/{user_id}', response_class=HTMLResponse)
async def get_profile_form(
    request: Request,
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    returns profile template.
    """
    profile = await profile_crud.get_by_attribute(
        'user_id', user_id, session, is_deleted=False
    )
    if profile:
        return templates.TemplateResponse(
            'profile.html', {'request': request, 'profile': profile}
        )
    return templates.TemplateResponse('profile.html', {'request': request})


@router.post('/{user_id}')
async def create_or_update_profile(
    user_id: int,
    form: ProfileCreate = Depends(ProfileCreate.as_form),
    session: AsyncSession = Depends(get_async_session),
) -> dict[str: str | int | bool]:
    """
    creates new profile or updates existing.
    """
    data = form.dict()
    validate_salary(data['salary_from'], data['salary_to'])
    grade = await grade_types_crud.get_by_attribute('type', data.pop('grade'), session)
    work_type = await work_types_crud.get_by_attribute('type', data.pop('work_type'), session)
    data['grade_type_id'] = grade.id
    data['work_type_id'] = work_type.id
    data['user_id'] = user_id

    profile = await profile_crud.get_by_attribute(
        'user_id', user_id, session, is_deleted=False
    )
    if profile:
        await profile_crud.update(profile, data, session)
    else:
        await profile_crud.create(data, session)
    return data
