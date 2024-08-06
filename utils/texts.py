from data.models import Booking

about_us = ('Жилье и отдых Сочи, Вардане Гостевой дом "Удача"\n'
            '🏖 ДО ПЛЯЖА 5-7 МИНУТ ПЕШКОМ\n'
            '💥СЕМЕЙНЫЙ ОТДЫХ в УЮТНОМ МИНИ-ОТЕЛЕ "Удача"💥#СОЧИ💥\
            посёлок #Вардане, Лазаревский район, ул. Львовская 7к\n'
            '🏖До пляжа 5 минут пешком по ровной дороге без подъемов и спусков'
            '🔥удивит доступными ценами на #номерасудобствами и индивидуальным '
            'подходом к каждому гостю💯\n'
            '✅Кафе, столовые, минимаркеты, аптеки, остановка общественного'
            'транспорта, жд станция Вардане - 5-7 минут пешком.\n'
            )


def moderator_text(data: Booking) -> str:
    return (
        f"Имя: {data.user_first_name}\n"
        f"Количкство гостей: {data.guests}\n"
        f"Номер: {data.room}\n"
        f"Дата заезда: {data.check_in_date}\n"
        f"Дата выезда: {data.departure_date}\n"
        f"Статус бронирования: {data.status}\n"
    )
