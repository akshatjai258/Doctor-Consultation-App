from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth  import authenticate,  login, logout
from django.views.generic import DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import Contact,Doctor,Specialization
from .forms import UserRegisterForm,UserUpdateForm,DoctorUpdateForm
from django.contrib.auth.decorators import login_required
from .filters import search_doctor,search_user
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.mail import send_mail
from django.conf import settings
from django.template import loader


# Create your views here.

import joblib as jb
model = jb.load('trained_model')

def home(request):
	return render(request,'doctor/home.html')
	
def about(request):
	# return HttpResponse('hr')
	return render(request,'doctor/about.html')

# def validateEmail( email ):
#    from django.core.validators import validate_email
#    from django.core.exceptions import ValidationError
#    try:
#       validate_email( email )
#       return True
#    except ValidationError:
#       return False
	
def contact(request):
	# name=request.post['name']
   if(request.method=='POST'):
      name=request.POST['name']
      email=request.POST['email']
      content=request.POST['content']
      contact=Contact(name=name,email=email,content=content)
      contact.save() 
      html_message = loader.render_to_string('doctor/email_contact.html',{'name':name})
      message = 'Hi '+str(name)+'. Greetings from Filox. Thank you for submitting your query/feedback. In case of a query, we will get back to you as soon as possible. Also, this is a auto-generated mail. So please refrain from replying to this mail.'
      send_mail('We heard you!!',message,settings.EMAIL_HOST_USER,[str(email)],fail_silently=True,html_message=html_message)
      messages.success(request,"Your query is sent successfully !!!")

   return render (request,"doctor/contact.html")

def dashboard(request,pk):
	doctor=Doctor.objects.get(id=pk)
	context={'doctor':doctor}
	return render(request,'doctor/dashboard.html',context)
	

def handleSignup(request):
  if request.method == 'POST':
      form = UserRegisterForm(request.POST)
      if form.is_valid():
          form.save()
          username = form.cleaned_data.get('username')
          email = form.cleaned_data.get('email')
          messages.success(request, f'Account created for {username}!')
          html_message = loader.render_to_string('doctor/email_regis.html',{'username':username})

          message = ''
          send_mail('We heard you!!',message,settings.EMAIL_HOST_USER,[str(email)],fail_silently=True,html_message=html_message)
          return redirect('doctorHome')
  else:
        if request.user.is_authenticated:
          messages.error(request,'you are currently logged in')
          return redirect('doctorHome')
        else:
          form = UserRegisterForm()
  return render(request, 'doctor/register.html', {'form': form})
    
  
def handelLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('doctorHome')
    
    
class ShowProfilePageView(DetailView):
	model = Doctor
	template_name = 'doctor/user_profile.html'

	def get_context_data(self, *args, **kwargs):
		#users = Profile.objects.all()
		context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
		
		page_user = get_object_or_404(Doctor, id=self.kwargs['pk'])

		context["page_user"] = page_user
		return context
		
@login_required
def profile(request):
  if request.method == 'POST':
      u_form = UserUpdateForm(request.POST, instance=request.user)
      d_form = DoctorUpdateForm(request.POST,request.FILES,instance=request.user.doctor)
      if u_form.is_valid() and d_form.is_valid():
          u_form.save()
          d_form.save()
          messages.success(request, f'Your account has been updated!')
          return redirect("edit_profile")

  else:
      u_form = UserUpdateForm(instance=request.user)
      d_form = DoctorUpdateForm(instance=request.user.doctor)

  context = {
      'u_form': u_form,
      'd_form': d_form
  }

  return render(request, 'doctor/editprofile.html', context)



def doctor_list(request):
    doctors=Doctor.objects.all()
    users=User.objects.all()
    myFilter1=search_doctor(request.GET,queryset=doctors)
    # myFilter2=search_user(request.GET,queryset=users)
    doctors=myFilter1.qs
    # users=myFilter2.qs
    paginated_list=Paginator(doctors,5)
    page_number=request.GET.get('page')
    doctor_page_obj=paginated_list.get_page(page_number)
    context={'doctors':doctors,'myFilter1':myFilter1,'doctor_page_obj':doctor_page_obj}
    return render(request,'doctor/doctor_list.html',context)

def checkdisease(request):

  diseaselist=['Fungal infection','Allergy','GERD','Chronic cholestasis','Drug Reaction','Peptic ulcer diseae','AIDS','Diabetes ',
  'Gastroenteritis','Bronchial Asthma','Hypertension ','Migraine','Cervical spondylosis','Paralysis (brain hemorrhage)',
  'Jaundice','Malaria','Chicken pox','Dengue','Typhoid','hepatitis A', 'Hepatitis B', 'Hepatitis C', 'Hepatitis D',
  'Hepatitis E', 'Alcoholic hepatitis','Tuberculosis', 'Common Cold', 'Pneumonia', 'Dimorphic hemmorhoids(piles)',
  'Heart attack', 'Varicose veins','Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia', 'Osteoarthristis',
  'Arthritis', '(vertigo) Paroymsal  Positional Vertigo','Acne', 'Urinary tract infection', 'Psoriasis', 'Impetigo']


  symptomslist=['itching','skin_rash','nodal_skin_eruptions','continuous_sneezing','shivering','chills','joint_pain',
  'stomach_pain','acidity','ulcers_on_tongue','muscle_wasting','vomiting','burning_micturition','spotting_ urination',
  'fatigue','weight_gain','anxiety','cold_hands_and_feets','mood_swings','weight_loss','restlessness','lethargy',
  'patches_in_throat','irregular_sugar_level','cough','high_fever','sunken_eyes','breathlessness','sweating',
  'dehydration','indigestion','headache','yellowish_skin','dark_urine','nausea','loss_of_appetite','pain_behind_the_eyes',
  'back_pain','constipation','abdominal_pain','diarrhoea','mild_fever','yellow_urine',
  'yellowing_of_eyes','acute_liver_failure','fluid_overload','swelling_of_stomach',
  'swelled_lymph_nodes','malaise','blurred_and_distorted_vision','phlegm','throat_irritation',
  'redness_of_eyes','sinus_pressure','runny_nose','congestion','chest_pain','weakness_in_limbs',
  'fast_heart_rate','pain_during_bowel_movements','pain_in_anal_region','bloody_stool',
  'irritation_in_anus','neck_pain','dizziness','cramps','bruising','obesity','swollen_legs',
  'swollen_blood_vessels','puffy_face_and_eyes','enlarged_thyroid','brittle_nails',
  'swollen_extremeties','excessive_hunger','extra_marital_contacts','drying_and_tingling_lips',
  'slurred_speech','knee_pain','hip_joint_pain','muscle_weakness','stiff_neck','swelling_joints',
  'movement_stiffness','spinning_movements','loss_of_balance','unsteadiness',
  'weakness_of_one_body_side','loss_of_smell','bladder_discomfort','foul_smell_of urine',
  'continuous_feel_of_urine','passage_of_gases','internal_itching','toxic_look_(typhos)',
  'depression','irritability','muscle_pain','altered_sensorium','red_spots_over_body','belly_pain',
  'abnormal_menstruation','dischromic _patches','watering_from_eyes','increased_appetite','polyuria','family_history','mucoid_sputum',
  'rusty_sputum','lack_of_concentration','visual_disturbances','receiving_blood_transfusion',
  'receiving_unsterile_injections','coma','stomach_bleeding','distention_of_abdomen',
  'history_of_alcohol_consumption','fluid_overload','blood_in_sputum','prominent_veins_on_calf',
  'palpitations','painful_walking','pus_filled_pimples','blackheads','scurring','skin_peeling',
  'silver_like_dusting','small_dents_in_nails','inflammatory_nails','blister','red_sore_around_nose',
  'yellow_crust_ooze']

  alphabaticsymptomslist = sorted(symptomslist)

  if request.method == 'GET':
    
     return render(request,'doctor/checkdisease.html', {"list2":alphabaticsymptomslist})




  elif request.method == 'POST':
       
      ## access you data by playing around with the request.POST object
      
      inputno = int(request.POST["noofsym"])
      print(inputno)
      if (inputno == 0 ) :
          return JsonResponse({'predicteddisease': "none",'confidencescore': 0 })
  
      else :

        psymptoms = []
        psymptoms = request.POST.getlist("symptoms[]")
       
        print(psymptoms)

      
        """      #main code start from here...
        """
      

      
        testingsymptoms = []
        #append zero in all coloumn fields...
        for x in range(0, len(symptomslist)):
          testingsymptoms.append(0)


        #update 1 where symptoms gets matched...
        for k in range(0, len(symptomslist)):

          for z in psymptoms:
              if (z == symptomslist[k]):
                  testingsymptoms[k] = 1


        inputtest = [testingsymptoms]

        print(inputtest)
      

        predicted = model.predict(inputtest)
        print("predicted disease is : ")
        print(predicted)

        y_pred_2 = model.predict_proba(inputtest)
        confidencescore=y_pred_2.max() * 100
        print(" confidence score of : = {0} ".format(confidencescore))

        confidencescore = format(confidencescore, '.0f')
        predicted_disease = predicted[0]

        

        #consult_doctor codes----------

        #   doctor_specialization = ["Rheumatologist","Cardiologist","ENT specialist","Orthopedist","Neurologist",
        #                             "Allergist/Immunologist","Urologist","Dermatologist","Gastroenterologist"]
        

        Rheumatologist = ['Osteoarthristis','Arthritis']
       
        Cardiologist = ['Heart attack','Bronchial Asthma','Hypertension ']
       
        ENT_specialist = ['(vertigo) Paroymsal  Positional Vertigo','Hypothyroidism' ]

        Orthopedist = []

        Neurologist = ['Varicose veins','Paralysis (brain hemorrhage)','Migraine','Cervical spondylosis']

        Allergist_Immunologist = ['Allergy','Pneumonia',
        'AIDS','Common Cold','Tuberculosis','Malaria','Dengue','Typhoid']

        Urologist = [ 'Urinary tract infection',
         'Dimorphic hemmorhoids(piles)']

        Dermatologist = [  'Acne','Chicken pox','Fungal infection','Psoriasis','Impetigo']

        Gastroenterologist = ['Peptic ulcer diseae', 'GERD','Chronic cholestasis','Drug Reaction','Gastroenteritis','Hepatitis E',
        'Alcoholic hepatitis','Jaundice','hepatitis A',
         'Hepatitis B', 'Hepatitis C', 'Hepatitis D','Diabetes ','Hypoglycemia']
         
        if predicted_disease in Rheumatologist :
           consultdoctor = "Rheumatologist"
           
        if predicted_disease in Cardiologist :
           consultdoctor = "Cardiologist"
           

        elif predicted_disease in ENT_specialist :
           consultdoctor = "ENT specialist"
     
        elif predicted_disease in Orthopedist :
           consultdoctor = "Orthopedist"
     
        elif predicted_disease in Neurologist :
           consultdoctor = "Neurologist"
     
        elif predicted_disease in Allergist_Immunologist :
           consultdoctor = "Allergist/Immunologist"
     
        elif predicted_disease in Urologist :
           consultdoctor = "Urologist"
     
        elif predicted_disease in Dermatologist :
           consultdoctor = "Dermatologist"
     
        elif predicted_disease in Gastroenterologist :
           consultdoctor = "Gastroenterologist"
     
        else :
           consultdoctor = "other"

        if consultdoctor != 'other':

            special = Specialization.objects.get(spec_name=consultdoctor)
            special_id = special.id
            print(special)
        else:
            special_id = 0

      #   request.session['doctortype'] = consultdoctor 

      #   patientusername = request.session['patientusername']
      #   puser = User.objects.get(username=patientusername)
     

        # saving to database.....................

        # patient = puser.patient
      #   diseasename = predicted_disease
      #   no_of_symp = inputno
      #   symptomsname = psymptoms
      #   confidence = confidencescore

        # diseaseinfo_new = diseaseinfo(patient=patient,diseasename=diseasename,no_of_symp=no_of_symp,symptomsname=symptomsname,confidence=confidence,consultdoctor=consultdoctor)
        # diseaseinfo_new.save()
        

        # request.session['diseaseinfo_id'] = diseaseinfo_new.id

      #   print("disease record saved sucessfully.............................")

        

        print(special_id)

        return JsonResponse({'predicteddisease': predicted_disease ,'confidencescore':confidencescore , "consultdoctor": consultdoctor, "special_id":special_id})
