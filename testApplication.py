#!/usr/bin/env python2.7
import wpm_db, db_wrapper
from wpm_app import app

mydb = wpm_db.db("dbFile", "dbLog")

# Add vim to the db.
vim_name = unicode('vim')
vim_url = "http://www.vim.org"
vim_dl_url = "http://www.vim.org/download.php"
vim_version = "1.2.3"
vim_regex = '".*vim.*\.exe"'
vim_version_regex = '\d+.*\d'


appLogFileName = "appLog"

validQuery, applications = db_wrapper.get_applications(mydb)

print applications
if validQuery and not vim_name in applications:
    db_wrapper.add_app(mydb, vim_name, vim_version, vim_dl_url, vim_url)
    db_wrapper.add_exe_regex(mydb, vim_name, [vim_regex])
    db_wrapper.add_version_regex(mydb, vim_name, [vim_version_regex])

vim = app("vim", mydb, appLogFileName)
print vim.getExeURLs()

vim.checkUpdates()
vim.dlUpdates()

foo = app("vim", mydb, appLogFileName)
foo.dlUpdates()
foo.checkUpdates()

#vBox = Application("virtual box", "https://www.virtualbox.org/wiki/Downloads", 'href=".*Win.*\.exe"')
#
#vBox.checkUpdates()
#vBox.dlUpdates()
