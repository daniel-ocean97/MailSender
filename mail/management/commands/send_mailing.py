from django.core.management.base import BaseCommand
from django.utils import timezone

from mail.models import Mailing  # замените your_app на имя вашего приложения
from mail.services import send_mailing  # импорт вашей функции


class Command(BaseCommand):
    help = "Отправляет все активные рассылки немедленно"

    def add_arguments(self, parser):
        # Опциональный аргумент для фильтрации по ID рассылки
        parser.add_argument(
            "--mailing-id",
            type=int,
            default=None,
            help="ID конкретной рассылки для отправки (отправляет все если не указан)",
        )
        # Флаг для принудительной отправки неактивных рассылок
        parser.add_argument(
            "--force",
            action="store_true",
            help="Принудительно отправляет даже неактивные рассылки",
        )

    def handle(self, *args, **options):
        mailing_id = options["mailing_id"]
        force = options["force"]

        # Определяем набор рассылок для отправки
        if mailing_id:
            mailings = Mailing.objects.filter(id=mailing_id)
            if not mailings.exists():
                self.stdout.write(
                    self.style.ERROR(f"Рассылка с ID {mailing_id} не найдена")
                )
                return
        else:
            mailings = Mailing.objects.all()
            if not force:
                mailings = mailings.filter(status="created")

        total = mailings.count()
        if total == 0:
            self.stdout.write(self.style.WARNING("Нет рассылок для отправки"))
            return

        self.stdout.write(f"Найдено рассылок: {total}")
        self.stdout.write("=" * 50)

        # Отправка каждой рассылки
        for i, mailing in enumerate(mailings, 1):
            self.stdout.write(f"[{i}/{total}] Отправка рассылки ID {mailing.id}...")
            try:
                send_mailing(mailing)
                self.stdout.write(
                    self.style.SUCCESS(f"Успешно отправлена рассылка ID {mailing.id}")
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"Ошибка при отправке рассылки ID {mailing.id}: {str(e)}"
                    )
                )
            self.stdout.write("-" * 50)

        self.stdout.write(
            self.style.SUCCESS(f"Обработка завершена! Отправлено: {total} рассылок")
        )
