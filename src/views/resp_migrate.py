from src.services.migrations_service import MigrationsService


def resp_migrate(response):
    if response is not None:
        status = '200 OK'
        headers = [('Content-Type', 'text/plain')]
        response(status, headers)
        migration_service = MigrationsService()
        if migration_service.delete_all_db_tables():
            if migration_service.create_all_db_tables():
                if migration_service.migrate_data():
                    print('**************************************')
                    print('THE MIGRATIONS HAS BEEN FINISHED SUCCESSFULLY!')
                    print('**************************************')
                    migration_service.print_db_data()  # to see data and refresh the DB
        resp_body = b'This migration has been finished!'
        return [resp_body]
    else:
        return None

