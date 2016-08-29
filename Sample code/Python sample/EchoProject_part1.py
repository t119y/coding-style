'''
This is an elementary program for Echo Nest to ask user for the name of a song, then generates 120 lines, 
each line listing the name of an artist and that artist's familiarity score.

Input: Ask user for the name of a song.

Output: 120 lines information about the song.(each line listing the name of an artist and that artist's familiarity score.)

Modules: pyen

Method: 
    First of all, just make sure API key of Echo Nest works, make sure "import pyen" works properly, make sure internet is well connected.
    
    Then, send request to echo Nest and generate information we need by calling search() function.
    
    Since we can only generate up to 99 responses per request, we may want to send request more than once which also means call search() more than once.
    
    After generation, print results (format: 'familiarity score' 'artist')
    


Author:Yuan Tu

'''

import pyen
with open("Key.txt") as F:
  Key = F.read().strip()
en = pyen.Pyen(Key)

def search(af_list=[],start=0,results=99,title='blue'): #return a list (artist and familier socre of their songs)
    '''
    Input parameter:
    
        af_list (default []) -- a list that we are going to add information to it(the name of an artist and that artist's familiarity score.)
        
        start (default 0) -- a number of where we are going to search for this song.
        
        results (default 99) -- a number of how many results we are going to get.
        
        title (default 'blue') -- a string of the title of the song.
        
    Returns:
        
        af_list -- a sorted(in decreasing order of familiarity ) list that generate the information we want about the song. (format: [(familiarity score,artist),(familiarity score,artist),(familiarity score,artist),......]
        
    
    Idea:
       This is a general purpose function to send requests to Echo Nest, and generate up to 99 responses each request from Echo Nest(which is less than 120 so we need to generate more results later.)
       
       Since the responses from Echo Nest is a dictionary, we need to use 'keyword'--['artist'],['familiarity'] and ['artist_name'] to generate the information we want.
       
       Send request to Echo Nest (based on Developer API Documentation of Echo Nest)
       
       Use for loop(accumulation pattern) to get 
       
       Since we neet to generate 120 different artists, use if statement to make sure there is no duplicate artist in our list.
       
       If:
          there are 120 lines in our list, which means we are done with generating all the information, jump out of the loop and return our results.(a sorted list in decreasing order of familiarity.)
       
       Else:
          
          Sorted our list and Return it in decreasing order of familiarity.
    '''
    response = en.get('song/search',title=title,start=start,results=results)#search a song, get its relvent artists, start from 'start', search for 'results''s results.
    for row in response['songs']:
        fam=en.get('artist/familiarity', name=row['artist_name'])
        try: # make sure excluding Errors.
            result ='{0} {1}'.format(fam['artist']['familiarity'],row['artist_name'])
        except UnicodeEncodeError:
            pass
        
        #print '\nSearching results, please be patient.' # debugging line
        
        if (fam['artist']['familiarity'],row['artist_name']) not in af_list:     # make sure there is no duplicate artist in our list.
            af_list.append((fam['artist']['familiarity'],row['artist_name']))
        if len(af_list)==120:          # If we have generated 120 results, it is time to return our results.
          af_list=sorted(af_list,reverse=True) #Sorted our list in decreasing order of familiarity.
          return af_list      
    af_list=sorted(af_list,reverse=True) #Sorted our list in decreasing order of familiarity.
    return af_list    


def main():
  '''
  The main logic fro the program:
  
  1. Ask user for the name of a song.
  2. Call search() function first time to generate 99 results in our list.
  3. Call search() function second time to generate 120 results totall. (make sure update the input parameters.)
  4. Use accumulation pattern(for loop) to output each lines in decreasing order of familiarity.
  

  '''


  title=raw_input('Please enter a song name: ')
  print '\nSearching results, please be patient.' # debugging line
  list1 = search() #Call search() function first time
    
  sorted_list= search(list1,start=99,results=99,title=title) #Call search() function second time
  for i in sorted_list:
    print str(int(i[0]*100)/100.0)+' '+i[1]  # Make sure the familiarity will be printed as a two decimal number.


if __name__=='__main__':  # allow program to be imported withour running
    main()

    
