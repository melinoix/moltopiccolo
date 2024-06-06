from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
import os
import json
import time

def load_words(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    words = {}
    for line in lines:
        english, italian = line.strip().split(': ')
        words[english] = italian
    return words

def get_random_word(words):
    english = random.choice(list(words.keys()))
    italian = words[english]
    return english, italian


#--------------------------------------------------#
#--------------------------------------------------#
#--------------------------------------------------#

def hello(request):
    if request.method == "GET":
        if 'logged_in' in request.COOKIES and 'username' in request.COOKIES and 'score' in request.COOKIES and 'best_score' in request.COOKIES:
            context = {
                'username':request.COOKIES['username'],
                'logged_in':request.COOKIES.get('logged_in'),
                'score':request.COOKIES['score'],
                'best_score':request.COOKIES['best_score']
            }
            return render(request,'hello.html',context)
        else:
            return render(request,'hello.html')
    if request.method == "POST":
        return render(request, 'quiz.html')

def login(request):
    if request.method=="GET":
        if 'logged_in' in request.COOKIES and 'username' in request.COOKIES and 'score' in request.COOKIES and 'best_score' in request.COOKIES:
            
            context = {
                'username':request.COOKIES['username'],
                'logged_in':request.COOKIES.get('logged_in'),
                'score':request.COOKIES['score'],
                'best_score':request.COOKIES['best_score']
            }
            response = render(request, 'hello.html', context)
            response.set_cookie('score',0)
            return response
        else:
            return render(request, 'login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        score = 0
        best_score=0
        context ={
            'username':username,
            'logged_in':'TRUE',
            'score':score,
            'best_score':best_score
        }
        response = render(request, 'hello.html',context)

        response.set_cookie('username',username)
        response.set_cookie('logged_in',True)
        response.set_cookie('score',score)
        response.set_cookie('best_score',best_score)
        return response

def logout(request):
    response = HttpResponseRedirect(reverse('login'))

    response.delete_cookie('username')
    response.delete_cookie('logged_in')
    response.delete_cookie('score')
    response.delete_cookie('best_score')
    return response

def quiz(request):
    score = request.COOKIES['score']
    score = int(score)
    file_path = os.getcwd() + '/molto/italian_words.txt' 
    words = load_words(file_path)
    english, italian = get_random_word(words)

        
    
    if request.method == 'POST':
        eng = request.POST.get('eng')
        realeng = request.POST.get('realeng')
        
        if eng==realeng and realeng !=None:
            score += 1
            context = {
                'italian': italian,
                'score':score,
                'english':english
            }  
            response = render(request, 'quiz.html', context)
            response.set_cookie('score',score)
            return response
        if eng!=realeng:
            context = {
                'italian': italian,
                'score':score,
                'english':english,
                'username':request.COOKIES['username'],
            }  
            response = render(request, 'loser.html', context)
            if score>int(request.COOKIES['best_score']):
                response.set_cookie('best_score',score)
            return response
        context = {
                'italian': italian,
                'score':score,
                'english':english
            }  
        response = render(request, 'quiz.html', context)
        response.set_cookie('score',score)
        return response
        
    
def time_up(request):
    ini = 0
    context = {
                'username':request.COOKIES['username'],
                'logged_in':request.COOKIES.get('logged_in'),
                'score':request.COOKIES['score'],
                'best_score':request.COOKIES['best_score']
            }
    response = render(request,'loser.html',context)
    actual = request.COOKIES['score']
    actual = int(actual)
    if actual > int(request.COOKIES['best_score']):
        response.set_cookie('best_score',actual)
    response.set_cookie('score',ini)
    
    return response


