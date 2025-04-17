from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalDetails',
            fields=[
                ('User_id', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True)),
                ('First_Name', models.CharField(max_length=255)),
                ('Middle_Name', models.CharField(blank=True, max_length=255, null=True)),
                ('Last_Name', models.CharField(max_length=255)),
                ('Phone_no', models.CharField(max_length=20, unique=True)),
                ('Mail_id', models.EmailField(max_length=254, unique=True)),
                ('Password', models.CharField(max_length=255)),
                ('Profile_Pic', models.ImageField(blank=True, null=True, upload_to='profile_pics/')),
            ],
        ),
        migrations.CreateModel(
            name='ImageUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='uploads/')),
            ],
        ),
    ]
