while True:
    import speech_recognition as sr
    import math
    import time as t
    from tkinter import Tk, Canvas, PhotoImage, Text, Scrollbar, RIGHT, Y, END




    def speech(prompt=""):
        if prompt:
            print(prompt)
        recognizer = sr.Recognizer()
        mic = sr.Microphone()

        while True:
            with mic as source:
                t.sleep(5)
                print("Say something...")
                recognizer.adjust_for_ambient_noise(source)
                try:
                    audio = recognizer.listen(source)
                    text = recognizer.recognize_google(audio, language='en-in')
                    print("You said:", text)
                    if text.lower() == "quit" or text.lower() == 'exit':
                        quit()
                    if text.lower() == "restart":
                        main()
                    return text
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio. Please try again.")
                except sr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition service: {e}")
                except Exception as e:
                    print(f"An error occurred: {e}")


    

    def display_concept_with_image(concept_name, image_path, explanation_text):
        # Create the main window
        window = Tk()
        window.title(concept_name)
        window.configure(bg='black')

        # Load the image
        image = PhotoImage(file=image_path)
        image_width = image.width()
        image_height = image.height()

        # Create and pack the canvas with a black background
        canvas = Canvas(window, width=800, height=600, bg='black')  # Adjust size as needed
        canvas.pack(side="top")

        # Display the image on the canvas
        canvas.create_image((800 - image_width) // 2, (600 - image_height) // 2, anchor='nw', image=image)

        # Create and pack the scrollbar
        scrollbar = Scrollbar(window)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Create and pack the text widget with customized colors
        text_widget = Text(window, wrap="word", yscrollcommand=scrollbar.set, bg='black', fg='white')
        text_widget.pack(expand=True, fill="both")

        # Insert the explanation text
        text_widget.insert(END, explanation_text)

        # Configure the scrollbar
        scrollbar.config(command=text_widget.yview)

        # Start the Tkinter event loop
        window.mainloop()

    def srp_calculation():
        SRP_dict = {
            "lithium": -3.04,
            "sodium": -2.71,
            "magnesium": -2.37,
            "aluminum": -1.66,
            "zinc": -0.76,
            "iron": -0.44,
            "nickel": -0.25,
            "copper": 0.34,
            "silver": 0.80,
            "platinum": 1.20,
            "gold": 1.50
        }

        print("Choose the element from the following list:")
        for element in SRP_dict.keys():
            print(element.capitalize())

        m1 = speech("Choose material 1:").lower()
        while m1 not in SRP_dict.keys():
            m1 = speech("The element you have chosen is not present, please choose another one: ").lower()
        
        m2 = speech("Choose material 2:").lower()
        while m2 not in SRP_dict.keys():
            m2 = speech("The element you have chosen is not present, please choose another one: ").lower()

        v1 = SRP_dict[m1]
        v2 = SRP_dict[m2]

        anode = m1 if v1 < v2 else m2
        cathode = m1 if v1 > v2 else m2
        anode_val = v1 if v1 < v2 else v2
        cathode_val = v1 if v1 > v2 else v2

        print("The anode is", anode.capitalize())
        print("The cathode is", cathode.capitalize())
        print("The Potential value of the cell is", cathode_val - anode_val)


    def nernst_equation():
        formula = "E_cell = E_0_cell - ((2.303RT)/F)log([1]/[M^n+])\nFor a general reaction ^Mn+ + ne- --> nM"
        print("Ok, the formula is as follows\n" + formula)
        print("Please enter value as per the standard units.")
        E_0_cell = float(speech("Enter the standard potential value:"))
        C1 = float(speech("Tell me the concentration of reduced species:"))
        C2 = float(speech("Tell me the concentration of oxidized species:"))
        T = float(speech("Enter the temperature in Kelvin:"))
        n = float(speech("Enter the number of shared electrons:"))
        R = 8.314
        F = 96500

        E_cell = E_0_cell - ((2.303 * R * T) /(n*F)) * math.log10(C1 / C2)
        print("The value of E_cell is", E_cell)


    def CPR():
        print(
            "The formula and its abbrievations:\n(KW)/(DAT)\nK:constant\nW:Weight loss\nD:Density of the object going under corrosion\nA:Surface area of the object\nT:Time taken in years")
        D = {'units': ['mpy', 'mmpy'], "K": [534, 87.6], "W": ['mg', 'mg'], "D": ["g/cm^3", "g/cm^3"],
            "A": ['inch^2', "cm^2"], "T": ['hours', 'hours']}
        
        print(
            "Units must be entered as per the following (Becareful with this part as many people commit mistake in unit conversion):")
        keys = list(D.keys())
        values = list(D.values())
        for i in range(len(D)):
            print(f"{keys[i]}:\t{values[i][0]}\t{values[i][1]}")
        t.sleep(10)
        print("Note that T is in hours, but T is only in hours during calculation later it is converted to years.")
        while True:
            K = (speech("Could you tell me the constant value as per the above table as per the unit of your choice!"))
            if K.split()[0] == '534' or K.split()[0] == '87.6':
                K = float(K)
                break
            else:
                print("The value of the constant 'K' can only be either 534 or 87.6")
                
        W = speech("Moving forward, Tell me the weight!").lower().split()
        weight_value = float(W[0])
        weight_unit = W[1]
        if weight_unit in ['milligram', 'mg', 'milligrams', 'mgs']:
            W = weight_value
        elif weight_unit in ['gram', 'g', 'grams']:
            W = weight_value * 1000
        elif weight_unit in ['kg', 'kilograms', 'kgs', 'kilogram']:
            W = weight_value * 1000000
        

        D = float(speech("Density is our next parameter, so tell me the value of density:"))
        A = speech("Surface area of the metal please!").lower().split()
        A_num = A[0]
        
        if A[1] in ['inch','inches'] and K == 87.6:
            # 1 inch^2 = 6.45 cm^2
            A_num= float(A_num)
            A = A_num/6.45
        elif A[1] in ['cm','centimetres','centimetre','centimeter','centimeters'] and K == 87.6:
            # 1 inch^2 = 6.45 cm^2
            A_num= float(A_num)
            A = A_num 
        elif A[1] in ['cm','centimetres','centimetre','centimeter','centimeters'] and K == 534:
            A_num= float(A_num)
            A = A_num*6.45 
                
        elif A[1] in ['m','metres','metre','meter','meters'] and K == 87.6:
            # 1 m^2 = 10000 cm^2
            A_num= float(A_num)
            A = A_num / 10000

        elif A[1] in ['m','metres','metre','meter','meters'] and K == 534:
            # 1 m^2 = 10000 cm^2 = 6.54*10000 inch^2
            A_num= float(A_num)
            A = (A_num / 10000) * 6.54

        else:
            A = float(A_num)
        T = speech("Time taken to corrode (e.g., '6 months', '2 years', '5000 hours'): ").strip().lower()

        time_hours = 0
        if 'month' in T:
            num_months = float(T.split()[0])
            time_hours = num_months * 24 * 30
        elif 'year' in T:
            num_years = float(T.split()[0])
            time_hours = num_years * 24 * 365
        elif 'day' in T:
            num_hours = float(T.split()[0])
            time_hours = num_hours * 24
        else:
            num_hours = float(T.split()[0])
            time_hours = num_hours
        cpr = (K * W) / (D * A * time_hours)
        print("The value of corrosion penetration rate is:", cpr)


    def pH():
        print("This Formula prints the value of pH on the basis of potential of saturated calomel electrode and glass electrode.\nWe know that potential of saturated calomel electode (SCE) is constant i.e 0.2422\n,then by using a setup of SCE as anode and Glass electrode as cathode, we can determine th pH.\t")
        t.sleep(8)
        print("The formula for pH determination is as follows:\npH = (E_cell - 0.2422 - Eg⁰)/0.0591\t")
        t.sleep(4)
        E_cell = float(speech("Could you tell me the value of E_cell!"))
        E_g_0 = float(speech("Moving on, could you please tell me the value of Eg⁰:"))
        pH = (-E_cell - 0.2422 + E_g_0) / (0.0591)
        print("Aight then the value of pH is as follows", pH)


    def concell():
        R=8.314
        F=96500
        a=float(speech("Could you tell me the concentration of ion in the first beaker?")) 
        b=float(speech("Further ahead, the concentration value in second beaker?"))
        if a > b:
            conc1 = a
            conc2 = b
        elif a < b:
            conc1 = b
            conc2 = a
        else:
            conc1 = a
            conc2 = b
        T=float(speech("Now, I would require the temperature at which the reaction is taking place."))
        n = float(speech("Finally I require the number of electrons shared in the reaction:"))
        e=((2.303*R*T)/(n*F))*math.log10(conc1/conc2)
        print("The value of E_cell in this concentration cell set up is:",e)


    def main():
        print("What would you like to know about?\n1.Calculation of SRP\n2.Calculation of E⁰ cell Nernst Equation\n3.Calculation of CPR\n4.Calculation of pH using glass electrode and saturated calomel electode\
            \n5.Calculation of E_cell in concentration cells.\n6.Information about calomel electrode.\n7.Information about glass electode")
        print("Note: You can always quit the process by saying quit when a speech input is asked!")
        choice = speech().lower()

        if 'srp'  in choice:
            srp_calculation()
        elif 'nernst' in choice:
            nernst_equation()
        elif 'cpr' in choice:
            CPR()
        elif 'ph' in choice:
            pH()
        elif 'concentration' in choice:
            concell()
        elif 'information' and ('calamine' or 'calomel') in choice:
            concept = "CALOMEL ELECTRODE"
            image_path = 'C://Users//dinju//Downloads//Study Download//627961_601796_ans.png'
            explanation = """
Construction:  There is a solid elemental mercury at the bottom of the flask and above that is the paste of mercurous chloride and mercury (calomel paste ) and above that is saturated KCl and a Pt wire to maintain electrical contact.

Working: Here the potential of calomel electrode just depends on the Cl- ions as it is being provided by Sat. KCl as during oxidation or reduction when the number of cl- ions are being consumed, they are provided by the sat KCl. 
Calomel electrode being a refrence electrode it can act as both anode and as cathode as well.

The reactions involved when it acts like  cathode:

Hg2^2+(aq) + 2e-→ 2Hg(l)
Hg₂Cl₂ (s) → Hg2 2+ (aq) + 2Cl-  
________________________________
Hg₂Cl₂(s) + 2e- → 2Hg (l) + 2 Cl-(aq)

The reactions involved when it acts like anode:

2Hg (l) → Hg2^2+ (aq) + 2e
Hg2^2+(aq) + 2Cl6-(aq)→Hg₂Cl₂ 
________________________________
2Hg(l) + 2Cl-(aq) → Hg₂Cl₂ (s)+ 2e-

The net reversible electrode reaction is, Hg₂Cl₂(s) + 2e− 2 Hg(l) + 2 Cl-(aq)


    """
            display_concept_with_image(concept, image_path, explanation)
        elif 'information' and "glass electrode" in choice:
            concept = "Glass Electrode"
            image_path = 'C://Users//dinju//Downloads//Study Download//bgglass.png'
            explanation = '''
Construction: The glass electrode contains a  conducting glass membrane in the bottom, above that there is 0.1 M HCl solution and above that we have Ag/AgCl  is reference electrode which provides external contact as well the Ag/AgCl electrode is dipped in the 0.1 M HCl solution.

Working: when the glass electrode is dipped in the analyte solution there is an ion exchange reaction taking place between the glass membrane and the analyte solution, the H+ ions from the analyte are attracted by the glass membrane and the cations present on the glass membrane are released into the analyte solution,  hence now there is a difference in concentration of hydrogen outside the membrane and inside the membrane, the concentration of inside HCl remains same hence the potential only varies on the concentration of the analyte solution, hence the formula for boundry potential  is given by : Eb = E1 – E2 = 0.0592 log Cl / C2 and the total glass electrode potential  is given by 
                                            Eg⁰ = Eg⁰ – 0.0592 pH

(Here the total boundry potential is constituted by the 3 factors i.e: 1) The boundary potential  2)Assymetric potential 3) Potential of reference  electrode Ag/AgCl )

Extra information: Glass electrode is also called as ions selective electrode, the following name is because the electrode which is sensitive to a specific ion present in an electrolyte whose potential depends upon the activity of a specific ion in the electrolyte. The glass electrode consist of a conducting glass membrane, which is made of metal oxides such as  Na20, CaO,SiO2  these elements have generally low melting point and they have high conductance.it works on the principle of concentration cell that is there is a concentration difference between the 0.1M HCl  and the analyte solution.

            '''
            display_concept_with_image(concept, image_path, explanation)
        else:
            print("Invalid choice. Please make sure you have chosen out of the given options only.")
            main()


    if __name__ == "__main__":
        main()
        t.sleep(3)