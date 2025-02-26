-- Удаление всех таблиц с учетом зависимостей
DROP TABLE IF EXISTS "Notice" CASCADE;
DROP TABLE IF EXISTS "Event" CASCADE;
DROP TABLE IF EXISTS "User" CASCADE;

-- Отключение от базы перед удалением (в psql используется \c)
\c postgres

-- Удаление самой базы данных
DROP DATABASE IF EXISTS tg_bot;