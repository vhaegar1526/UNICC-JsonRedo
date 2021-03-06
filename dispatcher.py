# Factory variant creators.
from Models.ConcreteFactory import email_notif_factory, post_notif_factory, sms_notif_factory
#
from Models.User import User
#
import logging


class Dispatcher:

    # Notifier client map
    NOTIFIER_CLIENTS: dict = {
        "sms": sms_notif_factory.SmsNotifierFactory,
        "post": post_notif_factory.PostNotifierFactory,
        "email": email_notif_factory.EmailNotifierFactory,
    }

    def __init__(self, notif_object: dict) -> None:
        self.notif_object = notif_object

    def push_notification(self) -> str:
        creator = None
        try:
            # Fetch respective function object and invoke with User object as arg.
            creator = Dispatcher.NOTIFIER_CLIENTS.get(self.notif_object['type'].lower())(
                User(name=self.notif_object['name'],
                     email=self.notif_object['email'],
                     phone=self.notif_object['phone'],
                     url=self.notif_object['url'],
                     type=self.notif_object['type'])
            )

        except KeyError as e:
            # 'type' of notifier requested by JSON object isn't supported.
            print(f"{e.args[0]} notifier service isn\'t yet supported.")
            logging.error(
                f"Non existing notifier requested, @{self.notif_object}, SKIPPED")

        except TypeError as e:
            # TODO: Log it.
            logging.error(f"Required param is missing @{self.notif_object}")

        return creator.notify_job()
