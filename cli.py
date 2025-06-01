from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.carpenter import Carpenter
from models.customer import Customer
from models.furniture import Furniture
from models.carpenter_customer import CarpenterCustomer
from datetime import datetime

DATABASE_URL = "sqlite:///furniture.db"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def register_carpenter():
    name = input("Carpenter Name: ")
    location = input("Location: ")
    carpenter = Carpenter(name=name, location=location)
    session.add(carpenter)
    session.commit()
    print(f"✅ Registered Carpenter: {name}")

def view_carpenters():
    carpenters = session.query(Carpenter).all()
    for c in carpenters:
        print(f"🪵 ID: {c.carpenter_id} | {c.name} - {c.location}")

def update_carpenter():
    cid = int(input("Enter Carpenter ID to update: "))
    carpenter = session.query(Carpenter).get(cid)
    if not carpenter:
        print("❌ Carpenter not found.")
        return
    carpenter.name = input("New name: ") or carpenter.name
    carpenter.location = input("New location: ") or carpenter.location
    session.commit()
    print("✅ Carpenter updated.")

def delete_carpenter():
    cid = int(input("Enter Carpenter ID to delete: "))
    carpenter = session.query(Carpenter).get(cid)
    if carpenter:
        session.delete(carpenter)
        session.commit()
        print("🗑️ Carpenter deleted.")
    else:
        print("❌ Not found.")

def add_customer():
    name = input("Customer Name: ")
    customer = Customer(customer_name=name)
    session.add(customer)
    session.commit()
    print(f"✅ Added Customer: {name}")

def view_customers():
    for cust in session.query(Customer).all():
        print(f"🧍 ID: {cust.customer_id} | Name: {cust.customer_name}")

def update_customer():
    cid = int(input("Customer ID: "))
    cust = session.query(Customer).get(cid)
    if not cust:
        print("❌ Not found.")
        return
    cust.customer_name = input("New name: ") or cust.customer_name
    session.commit()
    print("✅ Customer updated.")

def delete_customer():
    cid = int(input("Customer ID: "))
    cust = session.query(Customer).get(cid)
    if cust:
        session.delete(cust)
        session.commit()
        print("🗑️ Deleted.")
    else:
        print("❌ Not found.")

def add_furniture():
    carpenter_id = int(input("Carpenter ID: "))
    name = input("Furniture Name: ")
    cost = float(input("Cost: "))
    color = input("Color: ")
    dim = input("Dimensions: ")

    furniture = Furniture(
        carpenter_id=carpenter_id,
        furniture_name=name,
        furniture_cost=cost,
        color=color,
        dimensions=dim
    )
    session.add(furniture)
    session.commit()
    print(f"🪑 Added: {name}")

def view_furniture():
    choice = input("View (all / available / sold): ").lower()
    query = session.query(Furniture)

    if choice == "available":
        items = query.filter_by(is_sold=False).all()
    elif choice == "sold":
        items = query.filter_by(is_sold=True).all()
    else:
        items = query.all()

    for item in items:
        print(f"🪑 ID: {item.furniture_id} | {item.furniture_name} | Sold: {item.is_sold}")

def delete_furniture():
    fid = int(input("Furniture ID: "))
    item = session.query(Furniture).get(fid)
    if item:
        session.delete(item)
        session.commit()
        print("🗑️ Furniture deleted.")
    else:
        print("❌ Not found.")

def buy_furniture():
    cust_id = int(input("Customer ID: "))
    furn_id = int(input("Furniture ID: "))

    furniture = session.query(Furniture).get(furn_id)
    if not furniture or furniture.is_sold:
        print("❌ Not available.")
        return

    order = CarpenterCustomer(
        customer_id=cust_id,
        carpenter_id=furniture.carpenter_id,
        furniture_id=furn_id
    )
    furniture.is_sold = True
    session.add(order)
    session.commit()
    print("🛒 Furniture purchased.")

def return_furniture():
    order_id = int(input("Order ID to return: "))
    order = session.query(CarpenterCustomer).get(order_id)
    if not order:
        print("❌ Order not found.")
        return
    order.returned = True
    session.commit()
    print("↩️ Furniture marked as returned.")

def remake_furniture():
    order_id = int(input("Order ID: "))
    order = session.query(CarpenterCustomer).get(order_id)
    if not order or not order.returned:
        print("❌ Furniture must be returned first.")
        return

    furn = order.furniture
    furn.color = input("New color: ") or furn.color
    furn.dimensions = input("New dimensions: ") or furn.dimensions
    order.remake_done = True
    session.commit()
    print("🎨 Furniture remade.")

def quit_app():
    print("👋 Exiting...")
    exit()

def menu():
    options = {
        "1": register_carpenter,
        "2": view_carpenters,
        "3": update_carpenter,
        "4": delete_carpenter,
        "5": add_customer,
        "6": view_customers,
        "7": update_customer,
        "8": delete_customer,
        "9": add_furniture,
        "10": view_furniture,
        "11": delete_furniture,
        "12": buy_furniture,
        "13": return_furniture,
        "14": remake_furniture,
        "0": quit_app,
    }

    while True:
        print("\n🎯 MENU")
        for key, func in options.items():
            if hasattr(func, "__name__"):
                print(f"{key}. {func.__name__.replace('_', ' ').title()}")
            else:
                print(f"{key}. Exit")

        choice = input("Choose option: ").strip()
        action = options.get(choice)
        if action:
            action()
        else:
            print("❌ Invalid choice.")


if __name__ == "__main__":
    menu()
