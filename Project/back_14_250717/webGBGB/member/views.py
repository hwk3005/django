from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.db import IntegrityError
from member.models import Member
import random
import string
import time
import requests



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
                    'message': '가입되지 않은 이메일입니다.'
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
                    return redirect(next_url)  # :흰색_확인_표시: 원래 가려던 페이지로 이동
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
    # join1 페이지에 진입할 때 카카오 회원가입 세션을 명시적으로 지웁니다.
    # 이렇게 하면 join1에서 일반 회원가입을 시작할 때, 이전의 카카오 세션 정보가 남아있지 않게 됩니다.
    if 'kakao_signup_data' in request.session:
        del request.session['kakao_signup_data']
        print("DEBUG: join1 - Kakao signup data cleared on page entry.")
    return render(request, 'member/join1.html')


# Kakao Login
def kakao_login(request):
    """
    카카오 로그인 시작: 카카오 인가 코드 요청
    """
    KAKAO_REST_API_KEY = settings.KAKAO_REST_API_KEY
    KAKAO_REDIRECT_URI = settings.KAKAO_REDIRECT_URI
    
    # scope에 nickname과 email 추가
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={KAKAO_REST_API_KEY}&redirect_uri={KAKAO_REDIRECT_URI}&response_type=code&scope=profile_nickname,account_email"
    )

@csrf_exempt
def kakao_callback(request):
    """
    카카오 인가 코드 수신 후 토큰 발급 및 사용자 정보 가져오기
    이메일로 사용자를 찾아서 로그인 처리
    """
    KAKAO_REST_API_KEY = settings.KAKAO_REST_API_KEY
    KAKAO_REDIRECT_URI = settings.KAKAO_REDIRECT_URI

    code = request.GET.get("code")

    if not code:
        messages.error(request, "카카오 로그인에 실패했습니다. (코드 없음)")
        return redirect('/member/login/') # 로그인 실패 시 로그인 페이지로 리다이렉트

    # 1. 인가 코드로 토큰 요청
    token_request = requests.post(
        "https://kauth.kakao.com/oauth/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "authorization_code",
            "client_id": KAKAO_REST_API_KEY,
            "redirect_uri": KAKAO_REDIRECT_URI,
            "code": code,
        },
    )

    token_json = token_request.json()

    if "access_token" not in token_json:
        messages.error(request, f"카카오 토큰 발급에 실패했습니다: {token_json.get('error_description', '알 수 없는 오류')}")
        return redirect('/member/login/')

    access_token = token_json.get("access_token")

    # 2. 토큰으로 사용자 정보 요청 (닉네임, 이메일, 고유 ID)
    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        },
    )
    profile_json = profile_request.json()

    if "id" not in profile_json:
        messages.error(request, f"카카오 사용자 정보 가져오기에 실패했습니다: {profile_json.get('msg', '알 수 없는 오류')}")
        return redirect('/member/login/')

    kakao_id = str(profile_json.get("id")) # 카카오 고유 ID (숫자형일 수 있으므로 문자열로 변환)
    kakao_account = profile_json.get("kakao_account")

    nickname = kakao_account.get("profile", {}).get("nickname")
    email = kakao_account.get("email") # 카카오 이메일 (예: example@kakao.com)

    # 카카오 이메일은 필수! 없으면 로그인/가입 진행 불가
    if not email:
        messages.error(request, "카카오 계정의 이메일 정보가 없어 로그인/회원가입을 진행할 수 없습니다. 카카오 계정 설정에서 이메일 제공 동의를 확인해주세요.")
        return redirect('/member/login/')

    # 이메일이 있다면 @ 기준으로 분리 (join2.html에서 미리 채울 때 사용)
    kakao_email1 = ''
    kakao_email2 = ''
    if email:
        if '@' in email:
            email_parts = email.split('@')
            kakao_email1 = email_parts[0]
            kakao_email2 = email_parts[1]
        else:
            kakao_email1 = email # @가 없는 경우 (예외 처리)


    # 세션에 카카오 정보 저장 (join2로 넘겨줄 정보)
    # email 정보는 로그인/가입 모두에서 중요하게 사용
    request.session['kakao_signup_data'] = {
        'kakao_id': kakao_id, # DB에 id 필드를 저장하지 않아도 kakao_id는 세션에 유지하여 필요 시 활용 가능
        'nickname': nickname,
        'email': email, # 전체 이메일
        'email1': kakao_email1, # 분리된 이메일 앞부분
        'email2': kakao_email2, # 분리된 이메일 뒷부분
    }

    # ======== 핵심: 이메일로 기존 사용자 찾기 ========
    print(f"--- Kakao Callback Debug Info ---")
    print(f"Kakao Email received: {email}") # 카카오 API에서 받은 이메일
    print(f"---------------------------------")

    try:
        # Member 모델에서 email 필드가 정확히 일치하는 사용자를 찾습니다.
        member = Member.objects.get(email=email)

        # 이미 가입된 사용자가 맞다면 로그인 처리
        request.session['user_id'] = member.id # Member 모델의 고유 ID 필드 (member_id)를 user_id로 사용 가능
        request.session['user_name'] = member.name
        request.session['member_id'] = member.member_id # 이 줄을 추가합니다.
        messages.success(request, f"{member.name}님, 카카오 계정으로 로그인 되었습니다.")
        return redirect('/') # 로그인 완료 후 메인 페이지로 이동

    except Member.DoesNotExist:
        # Member 모델에 해당 이메일을 가진 사용자가 없는 경우 (즉, 카카오로 첫 로그인)
        print(f"DEBUG: Member with Email '{email}' not found in DB. Redirecting to signup.")
        messages.info(request, "카카오 계정으로 가입을 진행합니다. 추가 정보를 입력해주세요.")
        return redirect('/member/join2/') # 추가 정보 입력 페이지로 리다이렉트


def join2(request):
    
    if request.method == 'GET':
        if 'kakao_signup_data' not in request.session: # 카카오 회원가입이 아닌데 직접 접근
            
            messages.warning(request, '정상적인 회원가입 경로로 접근해주세요.')
            return redirect('member:join1')

    # POST 요청 처리
    if request.method == 'POST':
       
        if 'kakao_signup_data' in request.session:
            del request.session['kakao_signup_data']
            print("DEBUG: join2 POST - Kakao signup data cleared for normal signup flow.")

        
        return render(request, 'member/join2.html', {'is_kakao_signup': False}) # 명시적으로 일반 회원가입임을 알림

    
    is_kakao_signup = 'kakao_signup_data' in request.session
    kakao_data = request.session.get('kakao_signup_data', {})

    return render(request, 'member/join2.html', {
        'is_kakao_signup': is_kakao_signup,
        'kakao_signup_data': kakao_data,
        'error': request.GET.get('error')
    })

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

# 카카오 세션 초기화
def clear_kakao_session(request):
    if 'kakao_signup_data' in request.session:
        del request.session['kakao_signup_data']
        
        return JsonResponse
    else:
        return JsonResponse
# 회원가입 처리
def signup_process(request):
    """
    회원가입 처리
    """
    if request.method == 'POST':
        is_kakao_signup = request.POST.get('is_kakao_signup') == 'true'

        name = request.POST.get('name')
        # 이메일은 카카오 가입이든 일반 가입이든 항상 조합
        email_part1 = request.POST.get('email1')
        email_part2 = request.POST.get('email2')
        email = f"{email_part1}@{email_part2}" if email_part1 and email_part2 else ''

        birth = request.POST.get('birth')
        gender = request.POST.get('gender')
        genres = request.POST.get('group_keywords_hidden')

        user_id_for_db = request.POST.get('id') # join2.html에서 넘어온 id 값
        password = request.POST.get('pw')

        if is_kakao_signup:
            # 카카오 가입자의 경우, ID 필드는 'kakao_고유ID' 형태로 저장 (필요하다면)
            # 또는 그냥 비워두고 이메일을 기본 식별자로 사용
            kakao_id = request.session.get('kakao_signup_data', {}).get('kakao_id')
            if kakao_id:
                user_id_for_db = f"kakao_{kakao_id}"
            else:
                user_id_for_db = '' # kakao_id가 없다면 id 필드를 비워둡니다.

            # 카카오 가입자는 비밀번호가 필요 없으므로, 의미 없는 값 저장
            password = "KAKAO_OAUTH_PASSWORD_PLACEHOLDER"
            print(f"DEBUG: Kakao Signup - user_id_for_db: {user_id_for_db}, Email: {email}")

        else: # 일반 회원가입
            pw2 = request.POST.get('pw2')

            if not user_id_for_db or not password or not pw2:
                messages.error(request, '일반 회원가입: 아이디, 비밀번호를 모두 입력해주세요.')
                return render(request, 'member/join2.html', {'error': '필수 정보 누락'})

            if password != pw2:
                messages.error(request, '비밀번호가 일치하지 않습니다.')
                return render(request, 'member/join2.html', {'error': '비밀번호 불일치'})

            # 아이디 중복 확인 (일반 회원가입 시에만)
            if Member.objects.filter(id=user_id_for_db).exists():
                messages.error(request, '이미 사용 중인 아이디입니다.')
                return render(request, 'member/join2.html', {'error': '아이디 중복'})
            print(f"DEBUG: Regular Signup - user_id_for_db: {user_id_for_db}, Email: {email}")


        # 공통 유효성 검사 (이름, 이메일 등)
        if not name or not email:
            messages.error(request, '이름과 이메일은 필수 입력 항목입니다.')
            return render(request, 'member/join2.html', {'error': '필수 정보 누락'})

        # 이메일 중복 확인 (모든 가입 유형에 대해)
        # 단, 카카오 이메일이 이미 존재하는 일반 회원과 충돌할 수 있으므로 주의 필요
        # 실제 서비스에서는 이메일 중복 시 다른 처리 (예: 해당 이메일로 로그인 유도) 필요
        if Member.objects.filter(email=email).exists():
            messages.error(request, '이미 가입된 이메일 주소입니다. 로그인하거나 다른 이메일을 사용해주세요.')
            return render(request, 'member/join2.html', {'error': '이메일 중복'})


        try:
            member = Member(
                name=name,
                id=user_id_for_db, # 카카오 가입자는 'kakao_고유ID' 또는 빈 문자열
                pw=password, # 카카오 가입자는 'KAKAO_OAUTH_PASSWORD_PLACEHOLDER'
                email=email, # 이메일은 항상 올바르게 저장
                birth=birth if birth else None,
                gender=gender if gender else None,
                genres=genres if genres else None
            )
            member.save()
            print(f"DEBUG: Member saved to DB with ID: {member.id}, Email: {member.email}")

            request.session['signup_name'] = name
            messages.success(request, '회원가입이 완료되었습니다.')
            return redirect('/member/join-complete/')

        except IntegrityError as e:
            # unique=True 제약 조건 위반 시 발생 (예: id 또는 email이 unique인 경우)
            print(f"회원가입 데이터베이스 무결성 오류: {e}")
            messages.error(request, '데이터 저장 중 오류가 발생했습니다. (중복된 정보가 있을 수 있습니다)')
            return render(request, 'member/join2.html', {'error': '데이터베이스 오류'})
        except Exception as e:
            print(f"회원가입 오류: {e}")
            messages.error(request, '회원가입 중 알 수 없는 오류가 발생했습니다.')
            return render(request, 'member/join2.html', {
                'error': '회원가입 중 오류가 발생했습니다.'
            })

    # GET 요청 시 처리
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




@csrf_exempt
def send_join2_verification_code(request):
    if request.method == 'POST':
        email1 = request.POST.get('email1', '').strip()
        email2 = request.POST.get('email2', '').strip()
        
        email = f"{email1}@{email2}" if email1 and email2 else ""

        if not email:
            return JsonResponse({
                'success': False, 
                'message': '이메일을 입력해주세요.'
            })
        
        # 이미 가입된 이메일인지 확인
        if Member.objects.filter(email=email).exists():
            return JsonResponse({
                'success': False,
                'message': '이미 가입된 이메일 주소입니다. 다른 이메일을 사용해주세요.'
            })

        # 인증번호 생성 (6자리 숫자)
        verification_code = ''.join(random.choices(string.digits, k=6))
        
        # 세션에 인증번호와 생성시간, 이메일 저장
        request.session['join2_verification_code'] = verification_code
        request.session['join2_verification_time'] = time.time()
        request.session['join2_verification_email'] = email
        request.session['email_verified'] = False

        try:
            send_mail(
                subject='[회원가입] 이메일 인증번호',
                message=f'안녕하세요.\n\n회원가입을 위한 이메일 인증번호는 다음과 같습니다.\n\n인증번호: {verification_code}\n\n※ 인증번호는 5분간 유효합니다.',
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

    return JsonResponse({'success': False, 'message': '잘못된 요청입니다.'})



@csrf_exempt
def verify_join2_code(request):
    if request.method == 'POST':
        input_code = request.POST.get('verification_code', '').strip()

        if not input_code:
            return JsonResponse({
                'success': False,
                'message': '인증번호를 입력해주세요.'
            })

        session_code = request.session.get('join2_verification_code')
        verification_time = request.session.get('join2_verification_time')
        session_email = request.session.get('join2_verification_email')

        if not all([session_code, verification_time, session_email]):
            return JsonResponse({
                'success': False,
                'message': '인증번호를 먼저 요청해주세요.'
            })

        current_time = time.time()
        if current_time - verification_time > 300:
            # 세션 정보 삭제
            for key in ['join2_verification_code', 'join2_verification_time', 'join2_verification_email', 'email_verified']:
                if key in request.session:
                    del request.session[key]
            return JsonResponse({
                'success': False,
                'message': '인증번호가 만료되었습니다. 다시 요청해주세요.'
            })

        if input_code == session_code:
            request.session['email_verified'] = True
            return JsonResponse({
                'success': True,
                'message': '인증이 완료되었습니다.'
            })
        else:
            request.session['email_verified'] = False
            return JsonResponse({
                'success': False,
                'message': '인증번호가 일치하지 않습니다.'
            })

    return JsonResponse({'success': False, 'message': '잘못된 요청입니다.'})
