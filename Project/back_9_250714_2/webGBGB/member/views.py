from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from member.models import Member
import random
import string
import time



# 회원 정보 수정

def member_update(request, user_id):
    # 세션에서 로그인 정보 확인
    if 'user_id' not in request.session:
        messages.error(request, '로그인하세요')
        return redirect('/member/login/')  # 로그인 페이지로 리다이렉트
    
    # 현재 로그인한 사용자와 수정하려는 사용자가 같은지 확인
    if request.session['user_id'] != user_id:
        messages.error(request, '본인의 정보만 수정할 수 있습니다.')
        return redirect('/')
    
    # 사용자 정보 가져오기
    member = get_object_or_404(Member, id=user_id)
    
    # 이메일 분리 (@ 기준으로)
    email_parts = member.email.split('@') if member.email else ['', '']
    email1 = email_parts[0] if len(email_parts) > 0 else ''
    email2 = email_parts[1] if len(email_parts) > 1 else ''
    
    # 장르 정보 분리 (콤마 기준으로)
    genres_list = member.genres.split(',') if member.genres else []
    
    context = {
        'member': member,
        'email1': email1,
        'email2': email2,
        'genres_list': genres_list,
        'user_id': user_id,
    }
    
    return render(request, 'member/member_update.html', context)

def member_update_process(request):
    if request.method == 'POST':
        # 세션에서 로그인 정보 확인
        if 'user_id' not in request.session:
            messages.error(request, '로그인하세요')
            return redirect('/member/login/')
        
        user_id = request.session['user_id']
        member = get_object_or_404(Member, id=user_id)
        
        # 폼 데이터 받기
        name = request.POST.get('name')
        pw = request.POST.get('pw')
        email1 = request.POST.get('email1')
        email2 = request.POST.get('email2')
        gender = request.POST.get('gender')
        birth = request.POST.get('birth')
        genres = request.POST.get('group_keywords_hidden')
        
        # 이메일 합치기
        email = f"{email1}@{email2}" if email1 and email2 else ""
        
        # 정보 업데이트
        member.name = name
        if pw:  # 비밀번호가 입력된 경우만 변경
            member.pw = pw
        member.email = email
        member.gender = gender
        member.birth = birth
        member.genres = genres
        
        member.save()
        
        messages.success(request, '회원정보가 성공적으로 수정되었습니다.')
        return redirect('/')
    
    return redirect('/member/login/')


# 비밀번호 찾기


def find2(request):
    return render(request,'member/find2.html')



# 임시 비밀번호 생성 함수
def generate_temp_password():
    """8자리 임시 비밀번호 생성 (영문대소문자+숫자)"""
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.choice(characters) for _ in range(8))


@csrf_exempt
def send_password_reset_code(request):
    """비밀번호 찾기 - 인증번호 전송"""
    if request.method == 'POST':
        user_id = request.POST.get('user_id', '').strip()
        email = request.POST.get('email', '').strip()
        name = request.POST.get('name', '').strip()
        
        if not user_id or not email or not name:
            return JsonResponse({
                'success': False, 
                'message': '아이디, 이메일, 이름을 모두 입력해주세요.'
            })
        
        try:
            # 아이디와 이메일이 모두 일치하는 회원 조회
            member = Member.objects.get(id=user_id, email=email,name=name)
            
            print(f"비밀번호 찾기 - 회원 확인: ID={member.id}, Email={member.email}")
            
            # 인증번호 생성
            verification_code = generate_verification_code()
            
            # 세션에 인증번호와 생성시간, 회원정보 저장
            request.session['pwd_verification_code'] = verification_code
            request.session['pwd_verification_time'] = time.time()
            request.session['pwd_reset_member_id'] = member.id  # 비밀번호 재설정할 회원 ID
            
            # 이메일 전송
            try:
                send_mail(
                    subject='[비밀번호 찾기] 인증번호',
                    message=f'안녕하세요.\n\n비밀번호 찾기 인증번호는 다음과 같습니다.\n\n인증번호: {verification_code}\n\n※ 인증번호는 5분간 유효합니다.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )
                
                return JsonResponse({
                    'success': True,
                    'message': '인증번호가 발송되었습니다. 이메일을 확인해주세요.'
                })
                
            except Exception as e:
                print(f"이메일 전송 오류: {e}")
                return JsonResponse({
                    'success': False,
                    'message': '이메일 전송에 실패했습니다.'
                })
                
        except Member.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': '입력하신 아이디와 이메일이 일치하지 않습니다.'
            })
        except Exception as e:
            print(f"전체 오류: {e}")
            return JsonResponse({
                'success': False,
                'message': '오류가 발생했습니다.'
            })
    
    return JsonResponse({'success': False, 'message': '잘못된 요청입니다.'})


@csrf_exempt
def verify_code_and_reset_password(request):
    """비밀번호 찾기 - 인증번호 확인 및 임시 비밀번호 발송"""
    if request.method == 'POST':
        input_code = request.POST.get('verification_code', '').strip()
        
        if not input_code:
            return JsonResponse({
                'success': False,
                'message': '인증번호를 입력해주세요.'
            })
        
        # 세션에서 인증번호 정보 가져오기
        session_code = request.session.get('pwd_verification_code')
        verification_time = request.session.get('pwd_verification_time')
        reset_member_id = request.session.get('pwd_reset_member_id')
        
        if not all([session_code, verification_time, reset_member_id]):
            return JsonResponse({
                'success': False,
                'message': '인증번호를 먼저 요청해주세요.'
            })
        
        # 5분(300초) 시간 확인
        current_time = time.time()
        if current_time - verification_time > 300:  # 5분 = 300초
            # 만료된 세션 정보 삭제
            keys_to_delete = ['pwd_verification_code', 'pwd_verification_time', 'pwd_reset_member_id']
            for key in keys_to_delete:
                if key in request.session:
                    del request.session[key]
            
            return JsonResponse({
                'success': False,
                'message': '인증번호가 만료되었습니다. 다시 요청해주세요.'
            })
        
        # 인증번호 일치 확인
        if input_code == session_code:
            try:
                # 회원 정보 조회
                member = Member.objects.get(id=reset_member_id)
                
                # 임시 비밀번호 생성
                temp_password = generate_temp_password()
                
                # DB에 임시 비밀번호 저장
                member.pw = temp_password
                member.save()
                
                print(f"임시 비밀번호 설정 완료: {member.id} -> {temp_password}")
                
                # 임시 비밀번호 이메일 발송
                try:
                    send_mail(
                        subject='[비밀번호 찾기] 임시 비밀번호 발급',
                        message=f'안녕하세요.\n\n임시 비밀번호가 발급되었습니다.\n\n임시 비밀번호: {temp_password}\n\n※ 로그인 후 반드시 비밀번호를 변경해주세요.',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[member.email],
                        fail_silently=False,
                    )
                    
                    # 인증 성공 후 세션 정보 삭제
                    keys_to_delete = ['pwd_verification_code', 'pwd_verification_time', 'pwd_reset_member_id']
                    for key in keys_to_delete:
                        if key in request.session:
                            del request.session[key]
                    
                    return JsonResponse({
                        'success': True,
                        'message': '임시 비밀번호가 이메일로 발송되었습니다.'
                    })
                    
                except Exception as e:
                    print(f"임시 비밀번호 이메일 전송 오류: {e}")
                    return JsonResponse({
                        'success': False,
                        'message': '임시 비밀번호 이메일 전송에 실패했습니다.'
                    })
                
            except Member.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': '회원 정보를 찾을 수 없습니다.'
                })
        else:
            return JsonResponse({
                'success': False,
                'message': '인증번호가 일치하지 않습니다.'
            })
    
    return JsonResponse({'success': False, 'message': '잘못된 요청입니다.'})




# 아이디 찾기
def find1(request):
    return render(request,'member/find1.html')


# 인증번호 생성 함수
def generate_verification_code():
    """10자리 랜덤 인증번호 생성"""
    characters = 'qwertyuiopasdfghjklzxcvbnm1234567890'
    return ''.join(random.choice(characters) for _ in range(10))


@csrf_exempt
def send_verification_code(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        name = request.POST.get('name', '').strip()
        
        if not email or not name:
            return JsonResponse({
                'success': False, 
                'message': '이름과 이메일을 모두 입력해주세요.'
            })
        
        try:
            # 해당 이메일로 가입된 회원들을 조회 (복수 가능)
            members = Member.objects.filter(email=email, name=name)
            
            if not members.exists():
                return JsonResponse({
                    'success': False,
                    'message': '이름과 이메일을 다시 확인해주세요.'
                })
            
            # 여러 회원이 있는 경우 첫 번째 회원 선택 (또는 가장 최근 가입자)
            if members.count() > 1:
                print(f"경고: {email} 이메일로 {members.count()}명의 회원이 있습니다.")
                # 가장 최근에 가입한 회원 선택
                member = members.order_by('-member_id').first()
                print(f"가장 최근 가입 회원 선택: {member.id}")
            else:
                member = members.first()
            
            print(f"선택된 회원 - ID: {member.id}, Email: {member.email}")
            
            # 인증번호 생성
            verification_code = generate_verification_code()
            
            # 세션에 인증번호와 생성시간, 이메일, 회원정보 저장
            request.session['verification_code'] = verification_code
            request.session['verification_time'] = time.time()
            request.session['verification_email'] = email
            request.session['found_member_id'] = member.id  # 찾은 회원 ID 저장
            
            # 이메일 전송
            try:
                send_mail(
                    subject='[아이디 찾기] 인증번호',
                    message=f'안녕하세요.\n\n아이디 찾기 인증번호는 다음과 같습니다.\n\n인증번호: {verification_code}\n\n※ 인증번호는 5분간 유효합니다.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )
                
                return JsonResponse({
                    'success': True,
                    'message': '인증번호가 발송되었습니다. 이메일을 확인해주세요.'
                })
                
            except Exception as e:
                print(f"이메일 전송 오류: {e}")
                return JsonResponse({
                    'success': False,
                    'message': '이메일 전송에 실패했습니다.'
                })
                
        except Exception as e:
            print(f"전체 오류: {e}")
            return JsonResponse({
                'success': False,
                'message': '오류가 발생했습니다.'
            })
    
    return JsonResponse({'success': False, 'message': '잘못된 요청입니다.'})



@csrf_exempt
def verify_code_and_find_id(request):
    if request.method == 'POST':
        input_code = request.POST.get('verification_code', '').strip()
        
        if not input_code:
            return JsonResponse({
                'success': False,
                'message': '인증번호를 입력해주세요.'
            })
        
        # 세션에서 인증번호 정보 가져오기
        session_code = request.session.get('verification_code')
        verification_time = request.session.get('verification_time')
        verification_email = request.session.get('verification_email')
        found_member_id = request.session.get('found_member_id')
        
        if not all([session_code, verification_time, verification_email, found_member_id]):
            return JsonResponse({
                'success': False,
                'message': '인증번호를 먼저 요청해주세요.'
            })
        
        # 5분(300초) 시간 확인
        current_time = time.time()
        if current_time - verification_time > 300:  # 5분 = 300초
            # 만료된 세션 정보 삭제
            keys_to_delete = ['verification_code', 'verification_time', 'verification_email', 'found_member_id']
            for key in keys_to_delete:
                if key in request.session:
                    del request.session[key]
            
            return JsonResponse({
                'success': False,
                'message': '인증번호가 만료되었습니다. 다시 요청해주세요.'
            })
        
        # 인증번호 일치 확인
        if input_code == session_code:
            try:
                # 세션에 저장된 회원 ID로 회원 정보 조회
                member = Member.objects.get(id=found_member_id)
                
                # 인증 성공 후 세션 정보 삭제
                keys_to_delete = ['verification_code', 'verification_time', 'verification_email', 'found_member_id']
                for key in keys_to_delete:
                    if key in request.session:
                        del request.session[key]
                
                return JsonResponse({
                    'success': True,
                    'message': '인증이 완료되었습니다.',
                    'user_id': member.id
                })
                
            except Member.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': '회원 정보를 찾을 수 없습니다.'
                })
        else:
            return JsonResponse({
                'success': False,
                'message': '인증번호가 일치하지 않습니다.'
            })
    
    return JsonResponse({'success': False, 'message': '잘못된 요청입니다.'})


@csrf_exempt
def login(request):
    if request.method == 'POST':
        user_id = request.POST.get('id', '').strip()
        user_pw = request.POST.get('pw', '').strip()
        next_url = request.GET.get('next') or request.POST.get('next')

        if not user_id or not user_pw:
            return render(request, 'member/login.html', {
                'error': '아이디와 비밀번호를 모두 입력해주세요.'
            })

        try:
            user = Member.objects.get(id=user_id) 
            if user_pw == user.pw:
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                request.session['member_id'] = user.member_id  # 세션에 로그인 정보 저장(shareMain)
                messages.success(request, '로그인 되었습니다.')
                if next_url:
                    return redirect(next_url)  # ✅ 원래 가려던 페이지로 이동
                else:
                    return redirect('/')
            else:
                return render(request, 'member/login.html', {
                    'error': '비밀번호가 틀렸습니다.'
                })

        except Member.DoesNotExist:
            return render(request, 'member/login.html', {
                'error': '존재하지 않는 아이디입니다.'
            })
    
    return render(request, 'member/login.html')


def join1(request):
    return render(request,'member/join1.html')


def join2(request):
    return render(request,'member/join2.html')

# 1. 아이디 중복 체크 (AJAX용)
@csrf_exempt
def check_id(request):
    if request.method == 'POST':
        user_id = request.POST.get('id', '').strip()
        
        if not user_id:
            return JsonResponse({'available': False})
        
        # 아이디 중복 체크
        if Member.objects.filter(id=user_id).exists():
            return JsonResponse({'available': False})
        else:
            return JsonResponse({'available': True})
    
    return JsonResponse({'available': False})

# 회원가입 처리
@csrf_exempt
def signup_process(request):
    if request.method == 'POST':
        try:
            # 폼 데이터 받기
            name = request.POST.get('name', '').strip()
            user_id = request.POST.get('id', '').strip()
            password = request.POST.get('pw', '').strip()
            password2 = request.POST.get('pw2', '').strip()
            email1 = request.POST.get('email1', '').strip()
            email2 = request.POST.get('email2', '').strip()
            birth = request.POST.get('birth', '').strip()
            gender = request.POST.get('gender', '').strip()
            genres = request.POST.get('group_keywords_hidden', '').strip()
            
            # 필수 항목 체크
            if not all([name, user_id, password, password2, email1, email2]):
                messages.error(request, '모든 필수 항목을 입력해주세요.')
                return render(request, 'member/join2.html', {
                    'error': '모든 필수 항목을 입력해주세요.'
                })
            
            # 비밀번호 길이 체크
            if len(password) < 8:
                messages.error(request, '비밀번호는 8자 이상이어야 합니다.')
                return render(request, 'member/join2.html', {
                    'error': '비밀번호는 8자 이상이어야 합니다.'
                })
            
            # 비밀번호 일치 체크
            if password != password2:
                messages.error(request, '비밀번호가 일치하지 않습니다.')
                return render(request, 'member/join2.html', {
                    'error': '비밀번호가 일치하지 않습니다.'
                })
            
            # 아이디 중복 체크
            if Member.objects.filter(id=user_id).exists():
                messages.error(request, '이미 사용중인 아이디입니다.')
                return render(request, 'member/join2.html', {
                    'error': '이미 사용중인 아이디입니다.'
                })
            
            # 이메일 조합
            email = f"{email1}@{email2}"
            
            # 회원 정보 저장
            member = Member(
                name=name,
                id=user_id,
                pw=password,
                email=email,
                birth=birth if birth else None,
                gender=gender if gender else None,
                genres=genres if genres else None
            )
            member.save()
            
            # 세션에 가입자 이름 저장
            request.session['signup_name'] = name
            
            messages.success(request, '회원가입이 완료되었습니다.')
            return redirect('/member/join-complete/')
            
        except Exception as e:
            print(f"회원가입 오류: {e}")
            messages.error(request, '회원가입 중 오류가 발생했습니다.')
            return render(request, 'member/join2.html', {
                'error': '회원가입 중 오류가 발생했습니다.'
            })
    
    return render(request, 'member/join2.html')



def join3(request):
    # 세션에서 가입한 사용자 이름 가져오기
    signup_name = request.session.get('signup_name', '')
    
    # 가입 완료 후 세션에서 이름 삭제 (보안상)
    if 'signup_name' in request.session:
        del request.session['signup_name']
    
    context = {
        'signup_name': signup_name
    }
    
    return render(request, 'member/join3.html', context)


def logout(request):
    request.session.clear()
    messages.success(request, '로그아웃 되었습니다.')
    return redirect('/')



# 기입용
def sample(request):
    return render(request,'member/sample.html')






