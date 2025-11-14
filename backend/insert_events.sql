-- ============================================================================
-- SQL скрипт для вставки 10 событий в таблицу events
-- ============================================================================
--
-- ИНСТРУКЦИЯ ПО ИСПОЛЬЗОВАНИЮ:
--
-- 1. Убедитесь, что таблицы events, event_participations и qr_scans существуют
-- 2. Скрипт автоматически очистит все данные о мероприятиях перед вставкой
-- 3. Выполните скрипт через psql или другой PostgreSQL клиент:
--
--    psql -U <username> -d <database> -f insert_events.sql
--
--    или через psql интерактивно:
--    \i insert_events.sql
--
-- ВАЖНО:
-- - Скрипт очищает все данные из таблиц qr_scans, event_participations и events
-- - Все события создаются с фиксированным creator_id: 7a25a307-c3d5-4087-bd23-406f9213725b
-- - Все даты указаны после 15 ноября 2025 года (текущая дата)
-- - Теги соответствуют доступным в системе: 'Лекция', 'Музей', 'Спорт', 'Музыка', 'Природа'
--
-- ============================================================================

-- Очистка всех данных, связанных с мероприятиями
-- Порядок важен из-за внешних ключей: сначала зависимые таблицы, потом основная

DO $$
BEGIN
    -- Удаляем все QR сканы (зависят от event_participations)
    DELETE FROM qr_scans;

    -- Удаляем все записи об участии (зависят от events)
    DELETE FROM event_participations;

    -- Удаляем все события
    DELETE FROM events;

    RAISE NOTICE 'Все данные о мероприятиях очищены.';
END $$;

-- ============================================================================
-- Вставка 10 событий
-- ============================================================================

DO $$
DECLARE
    creator_id TEXT := '7a25a307-c3d5-4087-bd23-406f9213725b';
    event_id_1 TEXT;
    event_id_2 TEXT;
    event_id_3 TEXT;
    event_id_4 TEXT;
    event_id_5 TEXT;
    event_id_6 TEXT;
    event_id_7 TEXT;
    event_id_8 TEXT;
    event_id_9 TEXT;
    event_id_10 TEXT;
BEGIN
    -- 1. Хакатон VK x MAX: Campus Future
    event_id_1 := 'dab0c4f7-ac8d-404b-8f03-fdda0542894c';
    INSERT INTO events (
        id, title, body, photo, tags, place, start_date, end_date,
        max_participants, registration_start_date, registration_end_date,
        creator, status, created_at
    ) VALUES (
        event_id_1,
        'Хакатон VK x MAX: Campus Future',
        '24-часовой студенческий хакатон по созданию мини-приложений для VK: сервисы для кампуса, мероприятия, клубы, лайфстайл. Формат: офлайн + онлайн-трек, команды по 3–5 человек, менторы от VK и MAX. Темы: IT, продуктовая разработка, карьерный рост.',
        NULL,
        ARRAY['Лекция']::text[],
        'Главный корпус университета, аудитория 101',
        '2025-11-22'::date,
        '2025-11-23'::date,
        50,
        '2025-11-16 10:00:00'::timestamp,
        '2025-11-20 23:59:59'::timestamp,
        creator_id,
        'A',
        NOW()
    );
    INSERT INTO event_participations (id, user_id, event_id, participation_type, created_at)
    VALUES (gen_random_uuid()::TEXT, creator_id, event_id_1, 'C', NOW());

    -- 2. Экскурсия в офис VK + Q&A с разработчиками
    event_id_2 := 'f299c515-ef0e-4f06-b341-e11c480ffad3';
    INSERT INTO events (
        id, title, body, photo, tags, place, start_date, end_date,
        max_participants, registration_start_date, registration_end_date,
        creator, status, created_at
    ) VALUES (
        event_id_2,
        'Экскурсия в офис VK + Q&A с разработчиками',
        'Организованная экскурсия в штаб-квартиру VK: тур по офису, мини-лекция про экосистему и карьерные треки, живая сессия вопросов к разработчикам и продактам. Формат: экскурсия + митап, 2–3 часа. Темы: карьерный рост, IT, нетворкинг.',
        NULL,
        ARRAY['Лекция']::text[],
        'Офис VK, Москва',
        '2025-12-05'::date,
        '2025-12-05'::date,
        30,
        '2025-11-16 10:00:00'::timestamp,
        '2025-12-01 23:59:59'::timestamp,
        creator_id,
        'A',
        NOW()
    );
    INSERT INTO event_participations (id, user_id, event_id, participation_type, created_at)
    VALUES (gen_random_uuid()::TEXT, creator_id, event_id_2, 'C', NOW());

    -- 3. MAX Product Night: разбор топовых кейсов
    event_id_3 := 'a2963ceb-24d4-4fad-abbf-5bc60dde1a21';
    INSERT INTO events (
        id, title, body, photo, tags, place, start_date, end_date,
        max_participants, registration_start_date, registration_end_date,
        creator, status, created_at
    ) VALUES (
        event_id_3,
        'MAX Product Night: разбор топовых кейсов',
        'Вечерний митап, где продуктовые менеджеры MAX и приглашённые спикеры разбирают реальные кейсы: рост метрик, провальные фичи, работа с гипотезами. Формат: 2–3 коротких доклада + панельная дискуссия + неформальный нетворкинг. Темы: продуктовая аналитика, IT, soft skills.',
        NULL,
        ARRAY['Лекция']::text[],
        'Коворкинг университета, конференц-зал',
        '2025-12-12'::date,
        '2025-12-12'::date,
        40,
        '2025-11-16 10:00:00'::timestamp,
        '2025-12-08 23:59:59'::timestamp,
        creator_id,
        'A',
        NOW()
    );
    INSERT INTO event_participations (id, user_id, event_id, participation_type, created_at)
    VALUES (gen_random_uuid()::TEXT, creator_id, event_id_3, 'C', NOW());

    -- 4. VK Clips Challenge: студенческий контент-баттл
    event_id_4 := '8a1daea4-5d9f-40aa-901e-855f705392a9';
    INSERT INTO events (
        id, title, body, photo, tags, place, start_date, end_date,
        max_participants, registration_start_date, registration_end_date,
        creator, status, created_at
    ) VALUES (
        event_id_4,
        'VK Clips Challenge: студенческий контент-баттл',
        'Конкурс клипов в VK на тему студенческой жизни: учеба, общага, хакатоны, любовь, спорт. Лучшие клипы попадают в официальное сообщество универа и партнёров. Формат: онлайн-активность + офлайн награждение. Темы: креатив, медиа, коммьюнити, развлечение.',
        NULL,
        ARRAY['Музыка']::text[],
        'Онлайн + церемония награждения в главном корпусе',
        '2025-11-20'::date,
        '2025-12-20'::date,
        100,
        '2025-11-16 10:00:00'::timestamp,
        '2025-12-15 23:59:59'::timestamp,
        creator_id,
        'A',
        NOW()
    );
    INSERT INTO event_participations (id, user_id, event_id, participation_type, created_at)
    VALUES (gen_random_uuid()::TEXT, creator_id, event_id_4, 'C', NOW());

    -- 5. Патриотический квиз «Россия: люди, идеи, технологии»
    event_id_5 := '72ff3eb5-3cc6-44cb-b1e0-066af8f2af1b';
    INSERT INTO events (
        id, title, body, photo, tags, place, start_date, end_date,
        max_participants, registration_start_date, registration_end_date,
        creator, status, created_at
    ) VALUES (
        event_id_5,
        'Патриотический квиз «Россия: люди, идеи, технологии»',
        'Командная интеллектуальная игра о современной России: культура, наука, технологические прорывы, добровольчество, историческая память. Формат: квиз на 10–15 раундов, команды по 4–6 человек. Темы: патриотизм, история, культура, образование.',
        NULL,
        ARRAY['Музей', 'Лекция']::text[],
        'Актовый зал университета',
        '2025-11-28'::date,
        '2025-11-28'::date,
        60,
        '2025-11-16 10:00:00'::timestamp,
        '2025-11-25 23:59:59'::timestamp,
        creator_id,
        'A',
        NOW()
    );
    INSERT INTO event_participations (id, user_id, event_id, participation_type, created_at)
    VALUES (gen_random_uuid()::TEXT, creator_id, event_id_5, 'C', NOW());

    -- 6. Киноклуб VK Видео: вечер современного российского кино
    event_id_6 := '479da977-1063-48b2-82d9-cc306f61559e';
    INSERT INTO events (
        id, title, body, photo, tags, place, start_date, end_date,
        max_participants, registration_start_date, registration_end_date,
        creator, status, created_at
    ) VALUES (
        event_id_6,
        'Киноклуб VK Видео: вечер современного российского кино',
        'Просмотр фильма/подборки короткого метра о современных героях, волонтёрах, учёных и предпринимателях, + обсуждение с модератором. Формат: офлайн-показ + обсуждение, можно вести трансляцию в VK Видео. Темы: патриотизм, культура, осознанность.',
        NULL,
        ARRAY['Музей']::text[],
        'Кинозал университета',
        '2025-12-10'::date,
        '2025-12-10'::date,
        50,
        '2025-11-16 10:00:00'::timestamp,
        '2025-12-05 23:59:59'::timestamp,
        creator_id,
        'A',
        NOW()
    );
    INSERT INTO event_participations (id, user_id, event_id, participation_type, created_at)
    VALUES (gen_random_uuid()::TEXT, creator_id, event_id_6, 'C', NOW());

    -- 7. Добровольческий выезд «VK Добро»
    event_id_7 := 'a295cb44-d07d-40e7-8a41-7d9d282f75b3';
    INSERT INTO events (
        id, title, body, photo, tags, place, start_date, end_date,
        max_participants, registration_start_date, registration_end_date,
        creator, status, created_at
    ) VALUES (
        event_id_7,
        'Добровольческий выезд «VK Добро»',
        'Студенческий выезд в приют / на благоустройство парка / социальную акцию, с последующей медиа-отчётностью в VK (фото, сторис, посты). Формат: 1-дневная волонтёрская акция. Темы: патриотизм, волонтёрство, коммьюнити.',
        NULL,
        ARRAY['Природа']::text[],
        'Городской парк / Приют для животных (уточняется)',
        '2025-12-14'::date,
        '2025-12-14'::date,
        25,
        '2025-11-16 10:00:00'::timestamp,
        '2025-12-10 23:59:59'::timestamp,
        creator_id,
        'A',
        NOW()
    );
    INSERT INTO event_participations (id, user_id, event_id, participation_type, created_at)
    VALUES (gen_random_uuid()::TEXT, creator_id, event_id_7, 'C', NOW());

    -- 8. Cyber Night: турнир по играм от VK Play
    event_id_8 := '1b46da94-027a-4d99-9801-22f0380c4657';
    INSERT INTO events (
        id, title, body, photo, tags, place, start_date, end_date,
        max_participants, registration_start_date, registration_end_date,
        creator, status, created_at
    ) VALUES (
        event_id_8,
        'Cyber Night: турнир по играм от VK Play',
        'Ночной киберспортивный мини-турнир (CS2/Valorant/Dota / VK Play игры), укрепление студенческого коммьюнити, плюсом — мини-лекция про геймдев и киберспорт. Формат: LAN-турнир + стрим в VK. Темы: киберспорт, развлечения, IT.',
        NULL,
        ARRAY['Спорт', 'Лекция']::text[],
        'Компьютерный класс университета',
        '2025-12-28'::date,
        '2025-12-29'::date,
        32,
        '2025-11-16 10:00:00'::timestamp,
        '2025-12-23 23:59:59'::timestamp,
        creator_id,
        'A',
        NOW()
    );
    INSERT INTO event_participations (id, user_id, event_id, participation_type, created_at)
    VALUES (gen_random_uuid()::TEXT, creator_id, event_id_8, 'C', NOW());

    -- 9. Career Boost Day с VK и партнёрами
    event_id_9 := 'fe9ecdef-9566-4ca9-ade0-ce93cf061d71';
    INSERT INTO events (
        id, title, body, photo, tags, place, start_date, end_date,
        max_participants, registration_start_date, registration_end_date,
        creator, status, created_at
    ) VALUES (
        event_id_9,
        'Career Boost Day с VK и партнёрами',
        'День карьерных консультаций: разбор резюме, микрособеседования, стенды компаний-партнёров, мини-лекции «Как попасть в стажировку VK/MAX». Формат: карьерный день + стенды + лекции. Темы: карьерный рост, образование, нетворкинг.',
        NULL,
        ARRAY['Лекция']::text[],
        'Выставочный зал университета',
        '2026-01-18'::date,
        '2026-01-18'::date,
        80,
        '2025-11-16 10:00:00'::timestamp,
        '2026-01-15 23:59:59'::timestamp,
        creator_id,
        'A',
        NOW()
    );
    INSERT INTO event_participations (id, user_id, event_id, participation_type, created_at)
    VALUES (gen_random_uuid()::TEXT, creator_id, event_id_9, 'C', NOW());

    -- 10. Campus Talk: встреча с героем/ветераном/добровольцем
    event_id_10 := '690b11b5-e230-4006-a038-20470db4b80f';
    INSERT INTO events (
        id, title, body, photo, tags, place, start_date, end_date,
        max_participants, registration_start_date, registration_end_date,
        creator, status, created_at
    ) VALUES (
        event_id_10,
        'Campus Talk: встреча с героем/ветераном/добровольцем',
        'Тёплая встреча с человеком, который сделал вклад для страны: участником волонтёрских программ, ветераном, добровольцем, общественным деятелем. Живой рассказ + Q&A, можно делать прямой эфир в VK. Формат: ламповая лекция/интервью на 60–90 минут. Темы: патриотизм, личные истории, ценности.',
        NULL,
        ARRAY['Лекция', 'Музей']::text[],
        'Актовый зал университета',
        '2026-02-15'::date,
        '2026-02-15'::date,
        100,
        '2025-11-16 10:00:00'::timestamp,
        '2026-02-10 23:59:59'::timestamp,
        creator_id,
        'A',
        NOW()
    );
    INSERT INTO event_participations (id, user_id, event_id, participation_type, created_at)
    VALUES (gen_random_uuid()::TEXT, creator_id, event_id_10, 'C', NOW());

    RAISE NOTICE 'Все 10 событий и записи о участии создателей успешно добавлены в базу данных!';
END $$;

-- Проверка вставленных данных
SELECT
    id,
    title,
    start_date,
    end_date,
    place,
    max_participants,
    status,
    tags,
    creator
FROM events
ORDER BY start_date
LIMIT 10;
