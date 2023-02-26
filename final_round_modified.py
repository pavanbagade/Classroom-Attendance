import cv2,os,time,csv # for converting video to frames
from datetime import datetime,date    
from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN # to detect faces
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from threading import Thread
from tkinter import messagebox


global terminate
terminate=1
filename = 'video.mp4'
def first_page():  # gui begins here

    base = Tk()
    base.geometry("700x350")
    base.title("COOL - Count of label ")
    lb = Label(base, text="SMART INDIA HACKATHON", font=("Arial Rounded MT Bold",25))
    lb.place(x=100, y=20)
    lb.pack()
    canvas=Canvas(width=700,height=300)
    canvas.pack()
    Bimage=PhotoImage(file="sih.png")
    canvas.create_image(0,0,image=Bimage,anchor=NW)
    global lock
    numer_of_faces = []
    global faces

    
    def add_new_video_file():
        #base.destroy()
        global  filename
        filename = str(filedialog.askopenfilename())
        #print(filename)
        temp = ''
        for i in filename:
            if i == '/':
                temp += '\\'
            else:
                temp += i
        filename = temp

        print(filename)

    def stop():
        global terminate
        terminate=0

    def frame_extraction():  # Read the video from the given path
        try:
            cam = cv2.VideoCapture(filename)
            print('Function: ',filename)
        except:
            messagebox.showerror("Error",
                                 "Couldn't Load a video file. Make Sure Video File is Present in \"same directory\" as the script")
            base.destroy()
        fps = 25
        currentframe = 0

        try:
            print('Creating a folder named images....')
            if not os.path.exists('images'):
                os.makedirs('images')
        except OSError:
            messagebox.showerror("Error", "Failed to create the Directory")

        while (terminate):
            ret, frame = cam.read()
            if not ret:
                break
            if ret:
                name = './images/frame' + str(currentframe) + '.jpg'
                if currentframe % fps == 0:

                    cv2.imwrite(name, frame)
                    face_detection(name)


            currentframe += 1
        cam.release()

    def get_coordinates(select_frame, result_list):
        # load the image
        data = pyplot.imread(select_frame)
        # plot the image
        pyplot.imshow(data)
        # get the context for drawing boxes
        ax = pyplot.gca()
        # plot each box
        total = 0
        cropp = []
        insert_in_crop = []
        list_of_coordinates = []
        insert_in_list = []
        for result in result_list:
            # get coordinates
            x, y, w, h = result['box']
            insert_in_list.append(x)
            insert_in_list.append(y)
            insert_in_list.append(w)
            insert_in_list.append(h)
            list_of_coordinates.append(insert_in_list)
            insert_in_list = []
            # create the shape
            print(x, y, w, h)
            # rect=Rectangle((x,y),w,h,fill=False,color='red')
        # draw the box
        # ax.add_patch(rect)
        total += 1
        # show the plot
        # print("Total {0} faces detected.".format(total))
        # pyplot.show()
        print(list_of_coordinates)
        thread_for_cropped_faces(list_of_coordinates, select_frame)
        #crop_faces(list_of_coordinates, select_frame)

    def crop_faces(list_of_coordinates, select_frame):
        currentframe = 0
        try:
            # creating a folder named data
            if not os.path.exists('cropped_images'):
                os.makedirs('cropped_images')
        except OSError:
            print('Error: Creating directory of data')
        for i in list_of_coordinates:
            x, y, w, h = i[0], i[1], i[2], i[3]
            try:

                img = cv2.imread(select_frame)
                crop_img = img[y:y + h, x:x + w]
                # crop_img contains embeddings of the cropped images
                # cv2.imshow( crop_img)
                # cv2.imshow(img)
                name = './cropped_images/crop' + str(currentframe) + '.jpg'
                cv2.imwrite(name, crop_img)
                print('Creating...' + name)
                currentframe += 1
                cv2.waitKey(0)


            except:
                continue


    # using mtcnn
    global dict1
    dict1={}
    global count_of_recognized
    count_of_recognized=0






    def face_detection(frame):
        '''
        This function will recognise faces from each frames passed into it using mtcnn
        model. Returns the Maximum no. of faces detected.
        '''  # face detection model
        #txt_box1.delete('1.0', END)
        global dict1
        global temp
        pixels = pyplot.imread(frame)
        detector = MTCNN()
        faces = detector.detect_faces(pixels)
        count_of_each_frame(faces)
        temp=len(faces)
        dict1[frame]=temp
        print(dict1)
        max_count(numer_of_faces)
        numer_of_faces.append(len(faces))
        print("Total {0} Faces detected".format(len(faces)))



    def count_of_each_frame(faces):
        txt_box1.config(text = str(len(faces)))

    def Lock():

        lock = max(numer_of_faces)
        # numer_of_faces.clear()
        txt_box3.config(text = str(lock))
        getdate = date.today()
        gettime = datetime.now().time()
        try:
            if os.path.isfile('attendance.csv'):
                with open('attendance.csv','a', newline='') as f:
                    fieldnames = ['Time','Date','Locked Count']
                    writer = csv.DictWriter(f,fieldnames=fieldnames)
                    writer.writerow({'Time':gettime,'Date':getdate,'Locked Count':lock})
            else:
                with open('attendance.csv','a', newline='') as f:
                    fieldnames = ['Time','Date','Locked Count']
                    writer = csv.DictWriter(f,fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerow({'Time':gettime,'Date':getdate,'Locked Count':lock})


        except:
            pass
        max_frame=list(dict1.keys())[list(dict1.values()).index(lock)]
        print("max_frame")
        temp=""
        for i in max_frame:
            if i == '/':
                temp += '\\'
            else:
                temp += i
        max_frame = str(temp)
        print(max_frame)

        global encodings_of_known_faces


        max_img=pyplot.imread(max_frame)
        detector=MTCNN()
        detected_faces=detector.detect_faces(max_img)
        print(len(detected_faces))
        get_coordinates(max_frame,detected_faces)



    def thread_for_cropped_faces(list_of_coordinates, select_frame):
        thread3 = Thread(target=crop_faces(list_of_coordinates, select_frame))  # Creates a thread for first_page function
        thread3.start()

    def display():
        '''This function implements a new interface for locking the count'''
        # base.destroy()
        base2 = Tk()
        base2.grab_set()
        base2.focus_force()
        label50 = Label(base2, text="Press Enter or Click Submit", font=("Verdana Italic", 10))
        label50.pack()

        def submit(event):

            try:
                x = int(ent1.get())  # x will store the value of entry
                
                txt_box3.config(text = str(x))
                numer_of_faces.append(x)
                base2.destroy()

            except ValueError:
                messagebox.showerror("Error", "Enter a Valid Count!")
                base2.destroy()

            except TypeError:
                messagebox.showerror("Error", "Error Occured while Locking")
                base2.destroy()

        def submit2():
            try:
                x = int(ent1.get())  # x will store the value of entry
                
                txt_box3.config(text = str(x))
                numer_of_faces.append(x)
                base2.destroy()

            except ValueError:
                messagebox.showerror("Error", "Enter a Valid Count!")
                base2.destroy()

            except TypeError:
                messagebox.showerror("Error", "Error Occured while Locking")
                base2.destroy()

        base2.bind('<Return>', submit)
        base2.geometry("300x100")
        base2.title("Displaying Value")
        ent1 = Entry(base2)
        # ent1.grab_set()
        # ent1.focus()
        ent1.pack()
        btn2 = Button(base2, text="Submit", command=submit2)
        btn2.pack()

    def webcam():
        global filename
        filename=0

    def run():
        global terminate
        terminate=1
        control_thread = Thread(target=frame_extraction, daemon=True)
        control_thread.start()








    def max_count(number_of_faces):
        if (len(numer_of_faces) != 0):
            txt_box2.config(text = str(max(number_of_faces)))

    '''
    The following lines are used to create buttons and postion them
    '''
    label1 = Label(base, text="Students Detected", font=("Arial Bold", 10))
    label1.place(x=50, y=100)
    txt_box1 = Label(base, text = "--*--",fg = "green",bg= "black", font ="Times 25 bold" ,padx=15, pady=10)
    txt_box1.place(x=60, y=135)
    btn3 = Button(base, text="Start attendance system", font=("Arial Bold", 10), command=run)
    btn3.place(x=210, y=225)
    btn4 = Button(base, text="Lock", font=("Arial Bold", 10), command=Lock)
    btn4.place(x=575, y=170)
    label2 = Label(base, text="Max Count ", font=("Arial Bold", 10))
    label2.place(x=430, y=100)
    txt_box2 = Label(base, text = "--*--",fg = "green",bg= "black", font ="Times 25 bold" ,padx=15, pady=10)
    txt_box2.place(x=420, y=135)
    label3 = Label(base, text="Locked Count", font=("Arial Bold", 10))
    label3.place(x=240, y=100)
    txt_box3 = Label(base, text = "--*--",fg = "green",bg= "black", font ="Times 25 bold",padx=15, pady=10 )
    txt_box3.place(x=240, y=135)
    btn5 = Button(base, text="Edit Lock", font=("Arial Bold", 10), command=display)
    btn5.place(x=575, y=201)
    btn6 = Button(base, text="Add video ", font=("Arial Bold", 10), command=add_new_video_file)
    btn6.place(x=575, y=138)
    btn7=Button(base, text="Stop",font=("Arial Bold", 10), command=stop)
    btn7.place(x=260, y=260)
    btn8=Button(base, text="Use webcam", font=("Arial Bold", 10), command=webcam)
    btn8.place(x=575, y=105)

    base.mainloop()


def start():
    t1 = Thread(target=first_page)  # Creates a thread for first_page function
    t1.start()  # runs the thread


if __name__ == '__main__':
    start()  # runs the thread function
