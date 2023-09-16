from django.shortcuts import render
from .functionality import functionality as func
from .functionality.functionality import toList,toString
from .models import Keyword   # can also do from webcreatorApp.models import Keyword  but "." can handle it so no need to mentione the App Name explicitly
from .models import Imgpath

# Create your views here.
c = func.videoFunctions()


def appindex(request):
  return render(request,'index.html')

def create(request):                                                                                           

  if request.method=='POST':
    top5= request.POST.get('top5')
    display = request.POST.get('display')
    reverse =request.POST.get('reverse')
    titlebar = request.POST.get('titlebar')

    top5 = toList(top5)
    display = toList(display)

    if (len(top5)>=3 and len(top5)<=10)  and (len(display)>=3 and len(display)<=10) and (len(top5)==len(display)):
      # save keywords to database
      key = Keyword()
      key.pic_keywords = toString(top5)
      key.display_keywords= toString(display)
      key.save() 
      
    #_________________________________ video creation starts______________________________________
    # Step1:  ImageDownloader
      c.imgdownloader(key.id,top5)

    # step2:  Pick the Best fitting images for each keyword
      best_image_paths =c.bestChoice(key.id,reverse)
      string_paths = toString(best_image_paths,sep="|")
      paths = Imgpath(fk=key,paths=string_paths)
      paths.save()

    # step3: start making video  
      c.makeVideo(id=key.id,fk=key)

      c.textOnVideo(key.id,titlebar,reverse,duration=2)
  


      user_id= f"user_{key.id}"
      title = display[0].replace(" ","")
      
      params = {'user_id':user_id,'title':title}
      print(params)
      return render(request,'received.html',params)
    else:
      return render(request,'error.html')
    







