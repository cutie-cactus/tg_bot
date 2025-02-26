CREATE DATABASE tg_bot;
\c tg_bot;

CREATE TABLE "User" (
    TgID TEXT PRIMARY KEY,
    ChatID TEXT NOT NULL,
    Event_count INT DEFAULT 10,
    Time_zone INT DEFAULT 3
);

CREATE TABLE "Event" (
    ReminderID TEXT PRIMARY KEY,
    UserID TEXT NOT NULL,
    Notice_count INT DEFAULT 0,
    Date DATE NOT NULL,
    Time TIME NOT NULL,
    Name TEXT NOT NULL,
    Description TEXT,
    FOREIGN KEY (UserID) REFERENCES "User"(TgID) ON DELETE CASCADE
);

CREATE TABLE "Notice" (
    ReminderID TEXT PRIMARY KEY,
    Date DATE NOT NULL,
    Time TIME NOT NULL,
    FOREIGN KEY (ReminderID) REFERENCES "Event"(ReminderID) ON DELETE CASCADE
);