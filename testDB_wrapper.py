#!/usr/bin/env python
import wpm_db
import db_wrapper
import time

mydb = wpm_db.db("dbFile", "dbLog")

# Test Operations on Application Table
print("\nTest Operations on Application Table")
print("Unique App Insert Test", db_wrapper.add_app(mydb, "App", "1.0", "http://test_app.com", "http://test_app.com/dl", True))
print("Unique App Insert Test", db_wrapper.add_app(mydb, "latestApp", "1.2.3", "http://test.com", "http://test.com/dl"))
print(db_wrapper.get_applications(mydb))
print("Non-Unique App Insert Test", db_wrapper.add_app(mydb, "latestApp", "1.2.3", "http://test.com", "http://test.com/dl"))
print("Get Version Test", db_wrapper.get_app_version(mydb, "latestApp"))
print("Get URLs Test", db_wrapper.get_app_urls(mydb, "latestApp"))
print("Get UninstallFirst Flag - True", db_wrapper.get_app_uninstallFirst(mydb, "App"))
print("Get UninstallFirst Flag - False", db_wrapper.get_app_uninstallFirst(mydb, "latestApp"))
print("Get URLs Original", db_wrapper.get_app_urls(mydb, "latestApp"))
db_wrapper.update_main_url(mydb, "latestApp", "http://newTest.com/index.php")
print("After Change main URL", db_wrapper.get_app_urls(mydb, "latestApp"))
db_wrapper.update_download_url(mydb, "latestApp", "http://newTest.com/dl")
print("After Change dl URL", db_wrapper.get_app_urls(mydb, "latestApp"))
print("Update Version", db_wrapper.add_update_file(mydb, "latestApp", "1.5"))
print("Get Version", db_wrapper.get_app_version(mydb, "latestApp"))

# Test Operations on Dependency Table
print("\nTest Operations on Dependency Table")
print("Add Dependencies", db_wrapper.add_dependencies(mydb, "App", ["latestApp", "latestApp"]))
print("Get Dependency Name", db_wrapper.get_app_dependencies(mydb, "App"))
print("Add Dependencies - Error", db_wrapper.add_dependencies(mydb, "App", ["DNE"]))

# Test Regex Tables
print("\nTest Regex Tables")
print("Add Version Regex", db_wrapper.add_version_regex(mydb, "App", ["[a,b]", "[c-f]"]))
print("Get Version Regex", db_wrapper.get_app_version_regex(mydb, "App"))
print("Delete Version Regex", db_wrapper.del_app_version_regex(mydb, "App", ["[a,b]"]))
print("Get Version Regex - After Deletions", db_wrapper.get_app_version_regex(mydb, "App"))
print("Add EXE Regex", db_wrapper.add_exe_regex(mydb, "App", ["[4,2]", "[1-3]"]))
print("Get EXE Regex", db_wrapper.get_app_exe_regex(mydb, "App"))
print("Delete EXE Regex", db_wrapper.del_app_exe_regex(mydb, "App"))
print("Get EXE Regex - After Deletions", db_wrapper.get_app_exe_regex(mydb, "App"))
print("Add Scripts", db_wrapper.add_scripts(mydb, "latestApp", ["scr1", "scr2", "scr1"]))
print("Get Scripts", db_wrapper.get_app_scripts(mydb, "latestApp"))
print("Get Scripts - Empty", db_wrapper.get_app_scripts(mydb, "App"))
print("Delete Scripts", db_wrapper.del_app_scripts(mydb, "latestApp", ["scr2"]))
print("Get Scripts - After Deletion", db_wrapper.get_app_scripts(mydb, "latestApp"))

# Test Operations on File Tables
print("\nTest Operations on File Tables")
print("Get Current File - Before Insertions", db_wrapper.get_app_currFile(mydb, "latestApp"))
print("Get Old Files - Before Insertions", db_wrapper.get_app_oldFiles(mydb, "latestApp"))
print("Add File - Empty Table", db_wrapper.add_update_file(mydb, "latestApp", "1.5", "install1-5.exe", "installers/", "exe")) 
print("Get Current File - After 1st Insertion", db_wrapper.get_app_currFile(mydb, "latestApp"))
print("Get Old Files - After 1st Insertion", db_wrapper.get_app_oldFiles(mydb, "latestApp"))
print("Add File - Non-Empty Table", db_wrapper.add_update_file(mydb, "latestApp", "1.6", "install1-6.exe", "installers/", "exe")) 
print("Get Current File - After 2nd Insertion", db_wrapper.get_app_currFile(mydb, "latestApp"))
print("Get Old Files - After 2nd Insertion", db_wrapper.get_app_oldFiles(mydb, "latestApp"))
print("Add File - Non-Empty Table", db_wrapper.add_update_file(mydb, "latestApp", "1.7", "install1-7.exe", "installers/", "exe")) 
print("Get Current File - After 3rd Insertion", db_wrapper.get_app_currFile(mydb, "latestApp"))
print("Get Old Files - After 3rd Insertion", db_wrapper.get_app_oldFiles(mydb, "latestApp"))
print("Get Version Test - Before Revert", db_wrapper.get_app_version(mydb, "latestApp"))
print("Revert", db_wrapper.revert_app(mydb, "latestApp", 2, "installers/", "zip"))
print("Get Current File - After Revert", db_wrapper.get_app_currFile(mydb, "latestApp"))
print("Get Old Files - After After Revert", db_wrapper.get_app_oldFiles(mydb, "latestApp"))
print("Get Version Test - After Revert", db_wrapper.get_app_version(mydb, "latestApp"))

# Test Operations on Stats Table
print("\nTest Operations on Stats Table")
print("Add Statistics - 1", db_wrapper.add_stats(mydb, 36, 20))
print("Add Statistics - 2", db_wrapper.add_stats(mydb, 100, 90))
print("Sleeping for 10 seconds...")
time.sleep(10)
print("Add Statistics - 3", db_wrapper.add_stats(mydb, 45, 44))
print("Add Statistics - 4", db_wrapper.add_stats(mydb, 32, 2))
print("Add Statistics - 5", db_wrapper.add_stats(mydb, 9, 5))
print("Get Statistics - All", db_wrapper.get_stats(mydb))
print("Get Statistics - Range", db_wrapper.get_stats(mydb, [int(time.time()) - 5, int(time.time()) + 5]))
