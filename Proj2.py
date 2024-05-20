import argparse
import csv
import os
import pymongo
import sys
import pandas as pd  # type: ignore

#muda
#mongodb://localhost:27017/
client = pymongo.MongoClient("mongodb+srv://alazmine594:muda@cluster0.0scj8gc.mongodb.net/")
mydb = client["mydatabase"]
print(client.list_database_names())
mycollection = mydb["WeeklyQA"]
collection2 = mydb["DBDUMP"]

print(mydb.list_collection_names())


def read_csv(filename):
        global header
        print(f"weekly QAFiles: {filename}")
        
        csv_data = []
        with open (filename, mode = 'r',newline='')as file: 
            csvFile = csv.reader(file)
            found_start = False
            for row in csvFile:
                if not found_start:
                    found_start = True
                    continue
                data = {
                "Test #": row[0],
                "Build #": row[1],
                "Category": row[2],
                "Test Case": row[3],
                "Expected Result": row[4],
                "Actual Result": row[5],
                "Repeatable?": row[6],
                "Blocker?": row[7],
                "Test Owner": row[8]
                }
                mycollection.insert_one(data)
                print(f"Inserted row into MongoDB: {data}")
                #print(row)
                    
def read_xlsx(filename):
    print(f"Reading Excel file: {filename}")
    
    # Remove any trailing backslashes from the filename,skiprows=1
    filename = filename.strip("\\")
    
    df = pd.read_excel(filename)
    for index, row in df.iterrows():
        data = {
            "Test #": row["Test #"],
            "Build #": row["Build #"],
            "Category": row["Category"],
            "Test Case": row["Test Case"],
            "Expected Result": row["Expected Result"],
            "Actual result": row["Actual Result"],
            "Repeatable?" : row["Repeatable?"],
            "Blocker?" : row["Blocker?"],
            "Test Owner" : row["Test Owner"]
        }
        collection2.insert_one(data)
        #print(f"Inserted row into MongoDB: {data}")
    #print(df.col)


def list_all_by_user():
    print("List all by x User: ")
    name = input("Enter the user you want to search ")
    print(f"searching for user:{name}")
    query = {"Test Owner": name}
    results = mycollection.find(query)

    if results.count() > 0:
        print(f"Found Documents of Test Owner: {name}")
        for result in results: 
            print(result)
        else:
            print(f"No Documents from Test Owner: {name}")

def list_all_repeatable_bugs():
    print("Listing all repeatable bugs")
    possibleyes = ["Yes", "yes", "Y", "y"]
    yesquery = {"Repeatable?" : {"$in": possibleyes}}
    results = mycollection.find(yesquery)
    if results.count() > 0:
        print("Repeatable Bugs")
        for result in results:
            print(result)


def list_all_blocker_bugs():
    print("Listing all blocker bugs")
   
def list_all_build_3_19_2024():
    print("Listing all for build 3/19/2024") 

def first_middle_last_test_case():
    print("Listing first, middle, and last test case")

def write_kevin_chaja(output):
    print(f"Writing to output file: {output}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Importing Weekly QA or DB Dump')
    parser.add_argument("-f1","--file",  help = "name to WeeklyQA files that will be processed.")
    parser.add_argument("-f2","--file2", help ="name to DBDUMP" )
    parser.add_argument("-dba","--dbans", action="store_true", help = "Database Answers")
    parser.add_argument("-o","--output",type = str, help = "Name of the output file")
    args = parser.parse_args()

    #if args.qafiles is None:
    # or args.output is None:  
     #   sys.exit("Please provide names of QAFiles and DBDUMP See --help")
    currentdirectory = os.getcwd()
   
    
    if args.file:
       
        input_file_path = os.path.join(currentdirectory, args.file) 
        read_csv(args.file)
    if args.file2: 
        input_file2_path = os.path.join(currentdirectory, args.file2)
        read_xlsx(args.file2)
    if args.dbans:
        list_all_by_user()
        list_all_repeatable_bugs()
        list_all_blocker_bugs()
        list_all_build_3_19_2024()
        first_middle_last_test_case()
    if args.output:
        write_kevin_chaja(args.output)
