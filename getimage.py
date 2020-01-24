import mysql.connector 
from mysql.connector import errorcode

config = {
    'user':'IntanKW',
    'password':'IntanCantik',
    'host':'labseni.com',
    'port':3306,
    'database':'Trumon3'
}



class GetImage:
    gambar = None
    devId = None
    refsn = None
    number = None 
    cnx = None


    def __init__(self, refsn, image):
        # for checking connection in database connection
        print "masuk"
        self.gambar=image
        self.refsn=refsn
        self.writeImage()

    def writeImage(self):
        print "gambar"
        
        path = "image/"+str(self.refsn)+".png"
        print path
        # with naming file to image directory
        fout = open(path, 'wb')
        fout.write(self.gambar)  
        fout.close()

        print "data"



    def __del__(self):
        print "this is a destructor"
        
        del self.gambar
        del self.refsn
     
# this code will iterate all device to get image 


# select query


try:
    index=0
    sql_get_query = """select * from Image """
    cnx = mysql.connector.connect(**config)
    print "Connected succesfully "
    curr = cnx.cursor()
    print "cursor"
    curr.execute(sql_get_query)
    rows = curr.fetchall()
   
    for row in rows:
        print "halo"
        remon = GetImage(row[2], row[3])
        # refsn 2
        #image 3


        


except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print "mengalami error pada username dan password"                    
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print "database tidak ada"
    else:
        print "Error lainnya : " + `err`