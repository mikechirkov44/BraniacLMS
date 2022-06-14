from django.core.management import BaseCommand, call_command

class Command(BaseCommand):

    help = (
            'This command using for call makemessages with using flags' 
             '--locale, --ignore, and --no-location'
        )

    def handle(self, *args, **options):
       
       call_command('makemessages', '--locale=ru', '--ignore=env', '--no-location')
