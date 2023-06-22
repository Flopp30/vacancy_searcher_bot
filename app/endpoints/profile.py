from fastapi import APIRouter, Request, Depends, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session, profile_crud, grade_types_crud, work_types_crud
from db.schemas import ProfileForm
from app.settings import app_logger

router = APIRouter()
templates = Jinja2Templates(directory='app/templates')


@router.get('/profile/{user_id}', response_class=HTMLResponse)
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
        url = router.url_path_for('update_profile', user_id=user_id)
        return templates.TemplateResponse(
            'profile.html', {'request': request, 'profile': profile, 'url': url}
        )
    url = router.url_path_for('create_profile', user_id=user_id)
    return templates.TemplateResponse(
        'profile.html', {'request': request, 'user_id': user_id, 'url': url}
    )


@router.post('/profile/create/{user_id}')
async def create_profile(
    user_id: int,
    profile_form: ProfileForm = Body(...),
    session: AsyncSession = Depends(get_async_session),
) -> JSONResponse:
    """
    creates new profile.
    """
    profile = await profile_crud.get_by_attribute(
        'user_id', user_id, session, is_deleted=False
    )
    if profile is None:
        data = profile_form.dict()

        grade = await grade_types_crud.get_by_attribute('type', data.pop('grade'), session)
        work_type = await work_types_crud.get_by_attribute('type', data.pop('work_type'), session)

        data['grade_type_id'] = grade.id
        data['work_type_id'] = work_type.id
        data['user_id'] = user_id

        try:
            await profile_crud.create(data, session)
            content = "Профиль успешно создан"
            app_logger.info(f"Created profile for user : {user_id}")
            status_code = 200

        except Exception as e:
            app_logger.error(f"An error occurred while updating the profile with user id {user_id} -- {e}")
            content = f"Произошла ошибка во время обновления профиля: {e}"
            status_code = 500

    else:
        content = "Профиль уже существует"
        status_code = 400

    response = JSONResponse(content=content, status_code=status_code)
    return response


@router.post('/profile/update/{user_id}')
async def update_profile(
    user_id: int,
    profile_form: ProfileForm = Body(...),
    session: AsyncSession = Depends(get_async_session),
) -> JSONResponse:
    """
    updates profile.
    """
    profile = await profile_crud.get_by_attribute(
        'user_id', user_id, session, is_deleted=False
    )
    if profile:
        data = profile_form.dict()

        grade = await grade_types_crud.get_by_attribute('type', data.pop('grade'), session)
        work_type = await work_types_crud.get_by_attribute('type', data.pop('work_type'), session)

        data['grade_type_id'] = grade.id
        data['work_type_id'] = work_type.id
        data['user_id'] = user_id

        try:
            await profile_crud.update(profile, data, session)
            content = "Профиль успешно обновлен"
            app_logger.info(f"Updated profile for user : {user_id}")
            status_code = 200

        except Exception as e:
            app_logger.error(f"An error occurred while updating the profile with user id {user_id} -- {e}")
            content = f"Произошла ошибка во время обновления профиля: {e}"
            status_code = 500

    else:
        content = "Для редактирования профиля необходимо сначала создать его"
        status_code = 400

    response = JSONResponse(content=content, status_code=status_code)
    return response
