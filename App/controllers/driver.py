from App.database import db
from App.models.driver import Driver
from App.models.drive import Drive
from App.models.street import Street
from sqlalchemy.exc import IntegrityError
from datetime import datetime

class DriverController:
    @staticmethod
    def schedule_drive(driver_id: int, area_id: int, street_id: int, date_str: str, time_str: str):
        driver = Driver.query.get(driver_id)
        if not driver:
            return None
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            time = datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            raise ValueError("Invalid date/time format. Use YYYY-MM-DD and HH:MM")

        d = Drive(driver_id=driver_id, area_id=area_id, street_id=street_id, date=date, time=time, status="Upcoming")
        try:
            db.session.add(d)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise

        # notify residents on the street (if exists)
        street = Street.query.get(street_id)
        if street:
            message = f"SCHEDULED>> Drive {d.id} by Driver {driver_id} on {date} at {time}"
            for resident in street.residents:
                resident.receive_notif(message)
        return d

    @staticmethod
    def cancel_drive(driver_id: int, drive_id: int):
        drive = Drive.query.get(drive_id)
        if not drive:
            return False
        if drive.driver_id != driver_id:
            return False
        try:
            drive.status = "Cancelled"
            db.session.commit()
        except Exception:
            db.session.rollback()
            return False

        street = None
        if drive.street_id is not None:
            from App.models.street import Street
            street = Street.query.get(drive.street_id)
        if street:
            message = f"CANCELLED: Drive {drive.id} by {driver_id} on {drive.date} at {drive.time}"
            for resident in street.residents:
                resident.receive_notif(message)
        return True

    @staticmethod
    def view_drives(driver_id: int):
        return Drive.query.filter_by(driver_id=driver_id).all()

    @staticmethod
    def start_drive(driver_id: int, drive_id: int):
        drive = Drive.query.get(drive_id)
        driver = Driver.query.get(driver_id)
        if not drive or not driver or drive.driver_id != driver_id:
            return None
        try:
            driver.status = "Busy"
            driver.area_id = drive.area_id
            driver.street_id = drive.street_id
            drive.status = "In Progress"
            db.session.commit()
            return drive
        except Exception:
            db.session.rollback()
            return None

    @staticmethod
    def end_drive(driver_id: int, drive_id: int):
        drive = Drive.query.get(drive_id)
        driver = Driver.query.get(driver_id)
        if not drive or not driver or drive.driver_id != driver_id:
            return None
        try:
            driver.status = "Available"
            drive.status = "Completed"
            db.session.commit()
            return drive
        except Exception:
            db.session.rollback()
            return None
