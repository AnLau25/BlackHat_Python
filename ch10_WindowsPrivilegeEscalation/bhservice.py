# Techiniche based on taking advantage of high-privilege processes currently running
# Ussing windows manament instrumentation to monitor the creation of new processes
# With this, we can figure out from what files in the process being created
# Then we interject the file-creation processes and inject the sripting code
# This way, the script will be included in the process and executed