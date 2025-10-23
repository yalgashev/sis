from django.core.management.base import BaseCommand
from admin_app.models import Student


class Command(BaseCommand):
    help = 'Setup authentication for students using their ID cards'
    
    def handle(self, *args, **options):
        students = Student.objects.all()
        updated_count = 0
        
        for student in students:
            if student.id_card and not student.username:
                student.setup_authentication()
                student.save()
                updated_count += 1
                self.stdout.write(
                    f'Setup authentication for {student.first_name} {student.last_name} - Username: {student.id_card}'
                )
        
        if updated_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully setup authentication for {updated_count} students')
            )
        else:
            self.stdout.write(
                self.style.WARNING('No students needed authentication setup')
            )