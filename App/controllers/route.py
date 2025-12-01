from datetime import datetime
from App.database import db
from App.models import Drive, Resident, Notification, Area, Street
from App.controllers.resident import send_notification_to_resident


def schedule_route(driver, area_id, street_id, date_str, time_str, menu):
    """Driver schedules a route and all residents on that street get notified."""

    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    time = datetime.strptime(time_str, "%H:%M").time()

    new_route = Drive(
        driverId=driver.id,
        areaId=area_id,
        streetId=street_id,
        date=date,
        time=time,
        status="Upcoming",
        menu=menu
    )

    db.session.add(new_route)
    db.session.commit()

    # Notify all residents in that street
    residents = Resident.query.filter_by(areaId=area_id, streetId=street_id).all()
    for r in residents:
        text = (f"Bread Van is coming to your street!\n"
                f"Date: {date_str} | Time: {time_str}\n"
                f"Menu: {menu}\n"
                f"ETA: Approximately when the drive begins.")

        send_notification_to_resident(r.id, text)

    return new_route


def get_resident_notifications(resident):
    """Return notification history for a resident."""
    return [n.to_json() for n in resident.notifications]


def get_route(route_id):
    """Retrieve detailed route info."""
    return Drive.query.get(route_id)


def cancel_route(driver, route_id):
    """Driver cancels a route, residents are notified."""
    route = Drive.query.get(route_id)

    if not route:
        raise ValueError("Route does not exist.")
    if route.driverId != driver.id:
        raise ValueError("This route does not belong to the logged-in driver.")

    db.session.delete(route)
    db.session.commit()

    # Notify residents
    residents = Resident.query.filter_by(areaId=route.areaId, streetId=route.streetId).all()
    for r in residents:
        msg = f"The scheduled bread van route for your street has been cancelled."
        send_notification_to_resident(r.id, msg)

    return True
