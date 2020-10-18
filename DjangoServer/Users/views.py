from django.shortcuts import render
from rest_framework.views import APIView as API
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import Users
from .serializer import UserSerializer, UsersVoiceTrySerializer, UsersFaceTrySerializer
from random import randrange
import requests
import json

from .voicerecognition import start as voice_start
from .facerecogniion import start as face_start

from HackBBVA.settings import EMAIL_HOST_USER

from django.core.mail import EmailMultiAlternatives
from .email import message_email

import websockets
import asyncio
import threading

class UsersCRUD(API):
    permission_classes = ()
    def get(self,request):
        data    = request.data
        exist_emial = Users.objects.filter(email = data['email'])

        return Response(exist_emial.values())

    def post(self, request):
        data    = request.data
        exist_emial = Users.objects.filter(email = data['email'])
        # Revisa si ya existe un usuario con ese email   
        if(exist_emial):
            return Response([
                False,
                {
                    "username":[
                        "Ya existe un usuario con ese email"
                    ],
                }
            ])
        user_serializer = UserSerializer( data = data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({
                "ok":True,
                "data":user_serializer.data
            })
            
        else:
            return Response({
                "ok":False,
                "data":user_serializer.errors
            })


class UsersInformation(API):
    permission_classes = ()
    def post(self,request):
        data    = request.data
        exist_emial = Users.objects.filter(email = data['email'])

        return Response(exist_emial.values())

    



class Login(API):
    permission_classes = ()
    def post(self, request,):
        username = request.data.get("username")
        password = request.data.get("password")
        # Login por email 
        try:
            user = Users.objects.get(email=username)
            if user.check_password(password):
                data = self.getToken(user)
                return Response(data)
        except:
            pass
        
        # Login por nombre de usuario
        user = authenticate(username=username, password=password)
        if user:
            data = self.getToken(user)
            return Response(data)
        else:
            return Response({"ok":False, "token":None, "id":None,  "username":None, "email":None})
    
    def getToken(self, user):
        # Si el usuario no tiene un token, asignarle uno 
        #if not(user.auth_token.key):
        #    Token.objects.create(user=user)
        worlds = ["mundo.", "chimpance.","banco.", "robot.", "automovil.", "teclado.","cuaderno.","celular."]

        random_value = randrange(len(worlds)-1)
        extra = "hola, soy "
        user.token = extra + worlds[random_value]
        user.save()
        return {"ok":True, "token": extra + worlds[random_value], "id":user.id, "username":user.username, "email":user.email}

class LoginBBVArchuletas(API):
    permission_classes = ()
    def post(self,request):
        email = request.data['username']
        user = Users.objects.filter(email = email)
        if user:
            
            subject, from_email, to = 'BBVArchu inisiar sesión', EMAIL_HOST_USER, email
            text_content = 'Inisia sesión con tus datos biometricos'
            html_content = message_email()
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return Response( {"name": user[0].username, "ok":True })
        else:
            return Response({"name": None, "ok":False })


class VoiceRecognition(API):
    permission_classes = ()
    def post(self,request):
        data = request.data
        user_id = data['id']
        voice_try   = data['voice']
        face_try   = data['face']

        user  = Users.objects.filter(id = user_id)
        user  = user[0]
        token = user.token.lower()
        voice = user.voice
        
        voice_name = 'media/' + voice.name
        face = user.face_1
        face_name = 'media/' + face.name
        
        ####################### Voice #####################################
        url = 'https://speaker-recognition.herokuapp.com/enrollVoice/{}'.format(user_id)
        files = {
            "audio": open(voice_name, 'rb'),
            }
        values = {
            "name":"EnrollCustomer",
        }
        r = requests.post(url, files=files, data=values)
        
        data = {
            'user': user_id,
            'voice': voice_try
        }
        serializer = UsersVoiceTrySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        #print(serializer.data)
        voice_name = serializer.data['voice']
        voice_name = voice_name[1:]

        url = 'https://speaker-recognition.herokuapp.com/verifyVoice/{}'.format(user_id)
        files = {
            "audio": open(voice_name, 'rb'),
            }
        values = {
            "name":"VerifyCustomer",
        }
         
        r = requests.post(url, files=files, data=values)
        
        word = False
        #try:
        #    
        #    word = voice_start(voice_name,voice_name[16:])
        #    
        #    word = word['results']['transcripts'][0]['transcript']
        #except Exception as e:
        #    print(e)
        #    word = False 
        
        ####################  Face ####################################3
        data = {
            'user': user_id,
            'face': face_try
        }
        serializer = UsersFaceTrySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
       
        
        face_name_try = serializer.data['face']
        face_name_try = face_name_try[1:]
        
        
        #print(serializer.data)
        #voice_name = serializer.data['voice']
        #voice_name = voice_name[1:]
        
        try:
            face_flag = face_start(face_name,face_name_try)
        except Exception as e:
            
            face_flag = False

        
        try:
            voice_ = r.json()
            
            if voice_["Message"] == "Granted":
                voice = True
            else:
                voice = False
            if voice_["Speech"]:
                word = voice_["Speech"].lower()
                print(word,token)
                if word == token:
                    word = True
                else:
                    word = False
                
        except:
            voice = False

        response = {
            "voice": voice,
            "word":word,
            "face":face_flag
        }
        ok = voice and word and face_flag
        self.notification(user.email,ok)

        return Response(response)
    
    async def web_socket_send(self,socket_server,message):
        async with websockets.connect(socket_server) as socket:
            
            await socket.send(message)    
    
    
    
    def notification(self, email, ok):
       
        name = ""
        for i in email:
            if i == "@":
                break
            name += i
        
        if ok:
            command = "ok"
        else:
            command = "dont"
        message = '{"message":"hola","command":"' + command + '"}'
        
        socket_server = "wss://hydra-ws.abstract-lab.com/ws/{}/".format(name)    
        asyncio.new_event_loop().run_until_complete(self.web_socket_send(socket_server,message))
        