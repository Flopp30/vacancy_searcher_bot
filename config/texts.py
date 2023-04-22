from config import VACANCY_TO_SHOW_COUNT

TEXT_GREETING = f"Привет! Я Job. Могу показать тебе вакансии с hh.ru по запросу.\n" \
                f"/search - для старта поиска по вакансиям\n" \
                f"/profile - для просмотра своего профиля и добавления резюме\n" \
                f"/help - справочная информация по командам\n"

TEXT_VACANCY_SEARCH = f"Для получения {VACANCY_TO_SHOW_COUNT} вакансий " \
                      f"просто отправь название своей специальности"

TEXT_SEARCH_WITHOUT_COMMAND = f"Для поиска по вакансиям предварительно " \
                              f"необходимо отправить команду /search"

TEXT_HELP = f"/search - для старта поиска по вакансиям\n" \
            f"/profile - для просмотра своего профиля и добавления резюме\n" \
            f"/help - справочная информация по командам\n"

TEXT_PROFILE_GET_NAME = f"Как я могу к тебе обращаться?"

TEXT_PROFILE_GET_PROF_ROLE = "Приятно познакомиться, {username}. Подскажи свою специальность"

TEXT_PROFILE_GET_EXPERIENCE = "Подскажи, какой у тебя опыт работы по специальности: {prof_role}"
