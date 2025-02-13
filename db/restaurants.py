from db_connection import execute, query


def get_last_restaurants(amount: int = 5):
    sql = "SELECT id, name,address FROM restaurants WHERE active = 1 ORDER BY last_modified LIMIT :limit"
    return query(sql, {"limit": amount}).fetchall()


def get_restaurants_by_account_id(account_id: int):
    sql = """SELECT r.* FROM restaurants r WHERE active=1 AND account_id=:account_id"""
    return query(sql, {"account_id": account_id}).fetchall()


def get_single_restaurant(restaurant_id: int):
    sql = """SELECT
            r.*,
            json_group_array(
                json_object(
                    'weekday_number', oh.weekday_number,
                    'restaurant_open', oh.restaurant_open,
                    'restaurant_close', oh.restaurant_close
                )
            ) AS opening_hours
            FROM restaurants r
            LEFT JOIN restaurant_opening_hours oh ON r.id = oh.restaurant_id
            WHERE r.id = :restaurant_id
            GROUP BY r.id;"""
    return query(sql, {"restaurant_id": restaurant_id}).fetchone()


def get_restaurant_by_name(name: str):
    sql = """SELECT * FROM restaurants WHERE name=:name"""
    return query(sql, {"name": name}).fetchone()


def get_restaurant_opening_hours(restaurant_id: int):
    sql = """SELECT weekday_number, restaurant_open, restaurant_close FROM restaurant_opening_hours WHERE restaurant_id = :restaurant_id ORDER BY weekday_number"""
    return query(sql, {"restaurant_id": restaurant_id}).fetchall()


def create_new_restaurant(restaurant_data):
    print(f"{restaurant_data=}")
    sql = """INSERT INTO restaurants
            (active, posted_on, last_modified, name, account_id, address, description)
            VALUES (1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, :name, :account_id, :address, :description)"""
    return execute(sql, restaurant_data)


def create_restaurant_opening_hours(opening_hours):
    # validate opening_hours={'mondaystart': '', 'mondayend': '', 'tuesdaystart': '', 'tuesdayend': '', 'wednesdaystart': '', 'wednesdayend': '', 'thursdaystart': '14:01', 'thursdayend': '14:02', 'fridaystart': '', 'fridayend': '', 'saturdaystart': '', 'saturdayend': '', 'sundaystart': '', 'sundayend': ''}
    pass
