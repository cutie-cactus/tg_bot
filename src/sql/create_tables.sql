CREATE SCHEMA tg_event;

CREATE TABLE tg_event.User (
    TgID TEXT PRIMARY KEY,
    ChatID TEXT NOT NULL,
    Event_count INT DEFAULT 10,
    Time_zone INT DEFAULT 3
);

CREATE TABLE tg_event.Event (
    EventID SERIAL PRIMARY KEY,
    UserID TEXT NOT NULL,
    Notice_count INT DEFAULT 10,
    Date DATE NOT NULL,
    Time TIME NOT NULL,
    Name TEXT NOT NULL,
    Description TEXT,
    FOREIGN KEY (UserID) REFERENCES tg_event.User(TgID) ON DELETE CASCADE
);

CREATE TABLE tg_event.Notice (
    NoticeID SERIAL PRIMARY KEY,
    EventID INT NOT NULL,
    Date DATE NOT NULL,
    Time TIME NOT NULL,
    FOREIGN KEY (EventID) REFERENCES tg_event.Event(EventID) ON DELETE CASCADE
);