from database.database import Database

database = Database()
database.initializeDatabase(':memory:')
database.initializeTables()
database.createProject('project')
print(database.projectExists('project'))
database.closeConnection()