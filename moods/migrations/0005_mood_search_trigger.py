from django.contrib.postgres.search import SearchVector
from django.db import migrations


def compute_search_vector(apps, schema_editor):
    Mood = apps.get_model("moods", "Mood")
    Mood.objects.update(search_vector=SearchVector("note_title", "note"))


class Migration(migrations.Migration):
    dependencies = [
        ("moods", "0004_mood_search_vector"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE TRIGGER search_vector_trigger
            BEFORE INSERT OR UPDATE OF note_title, note, search_vector
            ON moods_mood
            FOR EACH ROW EXECUTE PROCEDURE
            tsvector_update_trigger(
                search_vector, 'pg_catalog.english', note_title, note
            );
            UPDATE moods_mood SET search_vector = NULL;
            """,
            reverse_sql="""
            DROP TRIGGER IF EXISTS search_vector_trigger
            ON moods_mood;
            """,
        ),
        migrations.RunPython(
            compute_search_vector, reverse_code=migrations.RunPython.noop
        ),
    ]
