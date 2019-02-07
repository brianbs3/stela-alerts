import boto3,os,datetime,time

db_user = os.environ["DB_USER"]
db_pass = os.environ["DB_PASS"]

dateStr = time.strftime("%d-%b-%Y_%H%M")
dataFileNameKey = "stela_" + dateStr
dataFileName = "/tmp/" + dataFileNameKey + ".sql"

backupCMD = "mysqldump -u " + db_user + " -p" + db_pass + " -d stela > " + dataFileName
zipCMD = "gzip " + dataFileName
finalName = dataFileName + ".gz"
os.system(backupCMD)
os.system(zipCMD)

print "Final: " + finalName



print "uploading..."

# Create an S3 client
s3 = boto3.resource('s3')
#
# filename = '/Users/bs/stela.sql.gz'
bucket = 'stela-backups'
#
s3.Object(bucket, dataFileNameKey).put(Body=open(finalName, 'rb'))

os.system("rm " + finalName)

print "done."