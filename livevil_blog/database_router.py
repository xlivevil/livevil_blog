class MongoDBRouter:

    def db_for_read(self, model, **hints) -> str:
        """
        Reads
        """
        if hasattr(model, 'db_connection'):
            return model.db_connection

        return 'default'

    def db_for_write(self, model, **hints) -> str:
        """
        Writes
        """
        if hasattr(model, 'db_connection'):
            return model.db_connection

        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Relations between objects are allowed if both objects are
        in the pool.
        """
        db_set = {'default', 'mongodb'}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        set postbody use MongoDB
        """
        if db == 'mongodb' and model_name == 'postbody':
            return True
        elif db == 'default' and model_name != 'postbody':
            return True
        return False
