CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    active INTEGER DEFAULT 1,
    posted_on TEXT,
    last_modified TEXT,
    last_logged_in TEXT,
    username TEXT UNIQUE,
    password TEXT,
    email TEXT UNIQUE,
    billing_info TEXT,
    firstname TEXT,
    lastname TEXT,
    description TEXT
);
    
CREATE TABLE IF NOT EXISTS restaurants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    active INTEGER DEFAULT 1,
    posted_on TEXT,
    last_modified TEXT,
    name TEXT,
    account_id INTEGER,
    address TEXT,
    description TEXT,
    FOREIGN KEY (account_id) REFERENCES accounts(id)
);


CREATE INDEX idx_account_active ON restaurants (account_id, active);


CREATE TABLE IF NOT EXISTS ratings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    active INTEGER DEFAULT 1,
    account_id INTEGER,
    restaurant_id INTEGER,
    posted_on TEXT,
    last_modified TEXT,
    rating INTEGER,
    content TEXT,
    FOREIGN KEY (account_id) REFERENCES accounts(id),
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
);


CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    active INTEGER DEFAULT 1,
    name TEXT,
    restaurant_id INTEGER,
    posted_on TEXT,
    last_modified TEXT,
    account_id INTEGER,
    start_time TEXT,
    end_time TEXT,
    description TEXT,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id),
    FOREIGN KEY (account_id) REFERENCES accounts(id)
);


CREATE TABLE IF NOT EXISTS buffets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    active INTEGER DEFAULT 1,
    restaurant_id INTEGER,
    posted_on TEXT,
    last_modified TEXT,
    name TEXT,
    price INTEGER,
    description TEXT,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
);

CREATE TABLE buffet_opening_hours (
    weekday_number INTEGER,
    buffet_id INTEGER,
    buffet_open TEXT,
    buffet_close TEXT,
    FOREIGN KEY (buffet_id) REFERENCES buffets(id),
    PRIMARY KEY (weekday_number, buffet_id)
);

CREATE TABLE restaurant_opening_hours (
    weekday_number INTEGER,
    restaurant_id INTEGER,
    restaurant_open TEXT,
    restaurant_close TEXT,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id),
    PRIMARY KEY (weekday_number, restaurant_id)
);
