'''
This program created a Graphical User Interface use Tkinter and search artist and that artist's familiarity score just like the first part of our homework 6.

Input:
     Ask user for the name of a song.

Output:
    lines information about the song in listbox.(each line listing the name of an artist and that artist's familiarity score.)


Modules :
    Tkinter
    EchoProject_part1
    sys


Author:Yuan Tu

'''





import Tkinter
import sys
import EchoProject_part1



class MyApplication(Tkinter.Frame):
    def __init__(self,master):
        '''
        Constructor of class 'MyApplication'
        Creates a window.
        Then creates a Frame.
        Run bulidMyWidgets(self) method.
        
        
        Input:
           master -- object a Tkinter, which creates a GUI window.
           
    
        '''
        
        Tkinter.Frame.__init__(self,master)
        self.pack()
        self.bulidMyWidgets()
        
    def bulidMyWidgets(self):
        '''
        Creates Widgets of Graphical User Interface for this program.
        
        Creates a label Widget, an Entry Widget, a scrollbar Widget, a listbox Widget, two button Widgets
        
        '''
        self.Song=Tkinter.StringVar(self)
        
        #label Widget
        Label1=Tkinter.Label(self,text='Search Results for Familiarity Score and Artist.')
        Label1.grid(row=0,column=0)   
               
        #Entry Widget
        Song_name=Tkinter.Entry(self,width=60,textvariable=self.Song,background='lightblue')
        Song_name.grid(row=1,column=0)


        #scrollbar Widget
        scrollbar= Tkinter.Scrollbar(self)
        scrollbar.grid(row=2,column=1,sticky='NS')
        
        
        #listbox Widget
        Song_list=Tkinter.Listbox(self,width=60,yscrollcommand=scrollbar.set)
        Song_list.grid(row=2,column=0)
        scrollbar.config(command=Song_list.yview)        
        self.s=Song_list
        
        #search button Widget
        search_button=Tkinter.Button(self,text='Search',command=self.Song_list_generate)
        search_button.grid(row=1,column=1)
        
        #button Widget for quiting
        quit_button=Tkinter.Button(self,text=' Quit ',command=self.Quit)
        quit_button.grid(row=3,column=0)        
        
    def Quit(self):
        '''
        Exit the whole program.
        '''
        print 'See you later ^^.'
        self.master.destroy()
        sys.exit(0)
        
    def generateList(self):
        '''
        Input: self
        
        Return: None
        
        Import HW6_part1 module and search and generate for results.
        
        '''
        Songname=self.Song.get()
        song_list1=HW6_part1.search(start=0,results=10,title=Songname)
        
        sort_list2=HW6_part1.search(song_list1,start=10,results=20,title=Songname)
        print sort_list2
        return sort_list2
    
    def Song_list_generate(self):
        '''
        Input: self
        
        Return: None
        
        Call generateList() generate a list that contains information of the song.
        
        This function help us prints out the results into our listbox.
        
        '''
        j=1
        self.s.insert(0,'Searching results for your song, please be patient.')
        L=self.generateList() # Call generateList() method.
        self.s.delete(0,'end')
        for i in L:
            
            result=str(int(i[0]*100)/100.0)+'  '+i[1]
            self.s.insert(j,str(j)+'.   '+result)
            j+=1


def main():
    '''
    The main logic for the program: 
    
    Creates root as an object of Tkinter.
    Creates Tobject as an object of MyApplication.
    Run the Graphical User Interface.

    '''
    
    root=Tkinter.Tk()
    root.title(' Homework 6')
    Tobject=MyApplication(root)
    Tobject.mainloop()

if __name__=='__main__':  # allow program to be imported without running
    main()





       